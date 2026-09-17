"""Téléchargement et nettoyage reproductibles des rasters quotidiens CHIRPS v3.

Les fichiers bruts et les sorties générées restent hors Git. Le pipeline écrit un
manifeste JSON pour rendre chaque téléchargement et transformation auditable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator

import numpy as np
import rasterio
from rasterio.errors import RasterioIOError
from rasterio.windows import Window, from_bounds
import requests

LOG = logging.getLogger("chirps_pipeline")
BASE_URL = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily"
NODATA = -9999.0


@dataclass(frozen=True)
class Config:
    start: date
    end: date
    west: float
    south: float
    east: float
    north: float
    product: str
    stage: str
    data_root: Path
    timeout: int = 60

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return self.west, self.south, self.east, self.north


def date_range(start: date, end: date) -> Iterator[date]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def url_for(day: date, product: str, stage: str) -> str:
    filename = f"chirps-v3.0.{product}.{day:%Y.%m.%d}.tif"
    return f"{BASE_URL}/{stage}/{product}/{day:%Y}/{filename}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path, timeout: int) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        LOG.info("Déjà présent : %s", destination)
        return False
    temporary = destination.with_suffix(destination.suffix + ".part")
    LOG.info("Téléchargement : %s", url)
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            if response.status_code == 404:
                raise FileNotFoundError(f"Fichier CHIRPS introuvable (404): {url}")
            response.raise_for_status()
            with temporary.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    temporary.replace(destination)
    return True


def crop_and_clean(source: Path, destination: Path, bbox: tuple[float, float, float, float]) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(source) as raster:
        window = from_bounds(*bbox, transform=raster.transform).intersection(
            Window(0, 0, raster.width, raster.height)
        )
        window = window.round_offsets().round_lengths()
        if window.width <= 0 or window.height <= 0:
            raise ValueError(f"Emprise hors raster: {bbox}")
        values = raster.read(1, window=window, masked=True).astype("float32")
        data = np.asarray(values.filled(NODATA), dtype="float32")
        invalid = (~np.isfinite(data)) | (data < 0)
        data[invalid] = NODATA
        transform = raster.window_transform(window)
        profile = raster.profile.copy()
        profile.update(
            driver="GTiff", height=data.shape[0], width=data.shape[1],
            transform=transform, dtype="float32", count=1, nodata=NODATA,
            compress="deflate", predictor=2,
        )
        if data.shape[0] >= 16 and data.shape[1] >= 16:
            profile.update(tiled=True, blockxsize=256, blockysize=256)
        else:
            profile.pop("tiled", None)
            profile.pop("blockxsize", None)
            profile.pop("blockysize", None)
        with rasterio.open(destination, "w", **profile) as output:
            output.write(data, 1)
            output.update_tags(
                source_dataset="CHIRPS v3 daily",
                processing="crop_bbox_and_invalid_to_nodata",
                bbox=",".join(map(str, bbox)),
                units="mm/day",
            )
        valid = data[data != NODATA]
        return {
            "width": int(data.shape[1]), "height": int(data.shape[0]),
            "valid_pixels": int(valid.size),
            "nodata_pixels": int((data == NODATA).sum()),
            "min_mm": float(valid.min()) if valid.size else None,
            "max_mm": float(valid.max()) if valid.size else None,
        }


def run(config: Config) -> Path:
    raw_root = config.data_root / "raw" / "chirps" / config.stage / config.product
    processed_root = config.data_root / "processed" / "chirps" / config.stage / config.product
    manifest_path = config.data_root / "processed" / "chirps" / "manifests" / (
        f"{config.start:%Y%m%d}_{config.end:%Y%m%d}_{config.product}_{config.stage}.json"
    )
    records = []
    for day in date_range(config.start, config.end):
        url = url_for(day, config.product, config.stage)
        raw = raw_root / f"{day:%Y%m%d}.tif"
        cleaned = processed_root / f"{day:%Y%m%d}.tif"
        try:
            downloaded = download(url, raw, config.timeout)
            stats = crop_and_clean(raw, cleaned, config.bbox)
            records.append({
                "date": day.isoformat(), "url": url,
                "raw_path": str(raw), "cleaned_path": str(cleaned),
                "downloaded_this_run": downloaded,
                "raw_sha256": sha256(raw), "cleaned_sha256": sha256(cleaned),
                "stats": stats,
            })
        except (requests.RequestException, FileNotFoundError, RasterioIOError, ValueError) as exc:
            LOG.error("Échec pour %s: %s", day.isoformat(), exc)
            records.append({"date": day.isoformat(), "url": url, "error": str(exc)})
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset": "CHIRPS v3 daily",
        "source": BASE_URL,
        "configuration": {**asdict(config), "start": config.start.isoformat(), "end": config.end.isoformat(), "data_root": str(config.data_root)},
        "records": records,
    }
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    if any("error" in record for record in records):
        raise RuntimeError(f"Le manifeste contient des erreurs : {manifest_path}")
    return manifest_path


def parse_args(argv: list[str] | None = None) -> Config:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, type=date.fromisoformat)
    parser.add_argument("--end", required=True, type=date.fromisoformat)
    parser.add_argument("--bbox", nargs=4, required=True, type=float, metavar=("WEST", "SOUTH", "EAST", "NORTH"))
    parser.add_argument("--product", choices=("rnl", "sat"), default="rnl")
    parser.add_argument("--stage", choices=("final", "prelim"), default="final")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args(argv)
    west, south, east, north = args.bbox
    if args.start > args.end or not (west < east and south < north):
        parser.error("Dates ou emprise invalides")
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        parser.error("BBOX hors limites géographiques")
    return Config(args.start, args.end, west, south, east, north, args.product, args.stage, args.data_root, args.timeout)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        manifest = run(parse_args())
    except (RuntimeError, ValueError, FileNotFoundError, RasterioIOError) as exc:
        LOG.error("Pipeline interrompu : %s", exc)
        return 1
    LOG.info("Manifeste écrit : %s", manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
