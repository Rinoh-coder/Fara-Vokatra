"""Pilote multi-zone CHIRPS : brut partagé, sorties séparées et manifeste global."""
from __future__ import annotations

import argparse
import json
import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

try:
    from src.chirps_pipeline import crop_and_clean, download, sha256, url_for
except ModuleNotFoundError:  # Exécution directe : python3 src/multi_zone_download.py
    from chirps_pipeline import crop_and_clean, download, sha256, url_for

LOG = logging.getLogger("multi_zone_download")


def date_range(start: date, end: date) -> Iterable[date]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def load_zones(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    zones = payload.get("zones")
    if not isinstance(zones, list) or not zones:
        raise ValueError("La configuration doit contenir une liste zones non vide")
    seen = set()
    for zone in zones:
        zone_id = zone.get("id")
        bbox = zone.get("bbox")
        if not isinstance(zone_id, str) or zone_id in seen:
            raise ValueError("Identifiants de zones absents ou dupliqués")
        if not isinstance(bbox, list) or len(bbox) != 4:
            raise ValueError(f"BBOX invalide pour {zone_id}")
        west, south, east, north = bbox
        if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
            raise ValueError(f"BBOX hors limites pour {zone_id}")
        seen.add(zone_id)
    return zones


def run(
    zones_path: Path,
    start: date,
    end: date,
    data_root: Path,
    product: str = "rnl",
    stage: str = "final",
    timeout: int = 60,
) -> Path:
    if start > end:
        raise ValueError("start doit être antérieur ou égal à end")
    zones = load_zones(zones_path)
    raw_root = data_root / "raw" / "chirps" / stage / product
    processed_root = data_root / "processed" / "chirps" / stage / product
    manifest_path = data_root / "processed" / "chirps" / "manifests" / (
        f"multi_zone_{start:%Y%m%d}_{end:%Y%m%d}_{product}_{stage}.json"
    )
    records = []
    for day in date_range(start, end):
        url = url_for(day, product, stage)
        raw = raw_root / f"{day:%Y%m%d}.tif"
        try:
            downloaded = download(url, raw, timeout)
            raw_checksum = sha256(raw)
            for zone in zones:
                zone_id = zone["id"]
                cleaned = processed_root / zone_id / f"{day:%Y%m%d}.tif"
                stats = crop_and_clean(raw, cleaned, tuple(zone["bbox"]))
                records.append({
                    "date": day.isoformat(), "zone_id": zone_id, "url": url,
                    "raw_path": str(raw), "cleaned_path": str(cleaned),
                    "downloaded_this_run": downloaded, "raw_sha256": raw_checksum,
                    "cleaned_sha256": sha256(cleaned), "stats": stats,
                })
        except Exception as exc:
            LOG.error("Échec pour %s: %s", day.isoformat(), exc)
            records.append({"date": day.isoformat(), "url": url, "error": str(exc)})
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset": "CHIRPS v3 daily",
        "configuration_file": str(zones_path),
        "configuration": {
            "start": start.isoformat(), "end": end.isoformat(),
            "product": product, "stage": stage, "zones": [zone["id"] for zone in zones],
        },
        "records": records,
    }
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    if any("error" in record for record in records):
        raise RuntimeError(f"Le manifeste contient des erreurs : {manifest_path}")
    return manifest_path


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zones", type=Path, required=True)
    parser.add_argument("--start", type=date.fromisoformat, required=True)
    parser.add_argument("--end", type=date.fromisoformat, required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--product", choices=("rnl", "sat"), default="rnl")
    parser.add_argument("--stage", choices=("final", "prelim"), default="final")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        manifest = run(args.zones, args.start, args.end, args.data_root, args.product, args.stage, args.timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        LOG.error("Pilote interrompu : %s", exc)
        return 1
    LOG.info("Manifeste multi-zone écrit : %s", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
