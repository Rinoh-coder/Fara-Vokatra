"""Construire une série quotidienne régionale à partir de GeoTIFF CHIRPS nettoyés."""
from __future__ import annotations

import argparse
import csv
import logging
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio

LOG = logging.getLogger("chirps_series")
DATE_PATTERN = re.compile(r"^(?P<day>\d{8})\.tif$")


@dataclass(frozen=True)
class DailyRecord:
    date: date
    mean_mm: float | None
    valid_pixels: int
    total_pixels: int
    coverage_fraction: float
    min_mm: float | None
    max_mm: float | None


def _parse_date(path: Path) -> date:
    match = DATE_PATTERN.match(path.name)
    if not match:
        raise ValueError(f"Nom de fichier inattendu : {path.name}; attendu YYYYMMDD.tif")
    return date.fromisoformat(match.group("day")[:4] + "-" + match.group("day")[4:6] + "-" + match.group("day")[6:])


def _files(input_dir: Path) -> list[Path]:
    paths = sorted(input_dir.glob("*.tif"))
    if not paths:
        raise FileNotFoundError(f"Aucun GeoTIFF trouvé dans {input_dir}")
    dates = [_parse_date(path) for path in paths]
    if len(set(dates)) != len(dates):
        raise ValueError("Plusieurs fichiers correspondent à la même date")
    return paths


def aggregate_raster(path: Path, min_coverage: float = 0.95) -> DailyRecord:
    if not 0 < min_coverage <= 1:
        raise ValueError("min_coverage doit être dans ]0, 1]")
    day = _parse_date(path)
    with rasterio.open(path) as raster:
        values = raster.read(1, masked=True).astype("float64")
        data = np.asarray(values.filled(np.nan), dtype="float64")
    total_pixels = int(data.size)
    valid = data[np.isfinite(data) & (data >= 0)]
    valid_pixels = int(valid.size)
    coverage = valid_pixels / total_pixels if total_pixels else 0.0
    if coverage < min_coverage:
        LOG.warning("Couverture insuffisante pour %s: %.3f < %.3f", day, coverage, min_coverage)
        mean = minimum = maximum = None
    else:
        mean = float(valid.mean()) if valid.size else None
        minimum = float(valid.min()) if valid.size else None
        maximum = float(valid.max()) if valid.size else None
    return DailyRecord(day, mean, valid_pixels, total_pixels, coverage, minimum, maximum)


def _expected_dates(start: date, end: date) -> set[date]:
    dates = set()
    current = start
    while current <= end:
        dates.add(current)
        current += timedelta(days=1)
    return dates


def aggregate_directory(
    input_dir: Path,
    output_csv: Path,
    min_coverage: float = 0.95,
    start: date | None = None,
    end: date | None = None,
) -> list[DailyRecord]:
    paths = _files(input_dir)
    records = [aggregate_raster(path, min_coverage) for path in paths]
    if start is not None and end is not None:
        if start > end:
            raise ValueError("start doit être antérieur ou égal à end")
        found = {record.date for record in records}
        missing = sorted(_expected_dates(start, end) - found)
        if missing:
            raise ValueError("Dates manquantes: " + ", ".join(day.isoformat() for day in missing))
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "mean_mm", "valid_pixels", "total_pixels", "coverage_fraction", "min_mm", "max_mm"])
        for record in records:
            writer.writerow([
                record.date.isoformat(), "" if record.mean_mm is None else f"{record.mean_mm:.6f}",
                record.valid_pixels, record.total_pixels, f"{record.coverage_fraction:.6f}",
                "" if record.min_mm is None else f"{record.min_mm:.6f}",
                "" if record.max_mm is None else f"{record.max_mm:.6f}",
            ])
    return records


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-coverage", type=float, default=0.95)
    parser.add_argument("--start", type=date.fromisoformat)
    parser.add_argument("--end", type=date.fromisoformat)
    args = parser.parse_args(argv)
    if (args.start is None) != (args.end is None):
        parser.error("--start et --end doivent être fournis ensemble")
    return args


def main(argv: Iterable[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    try:
        records = aggregate_directory(args.input_dir, args.output, args.min_coverage, args.start, args.end)
    except (FileNotFoundError, ValueError, rasterio.errors.RasterioIOError) as exc:
        LOG.error("Agrégation interrompue : %s", exc)
        return 1
    LOG.info("%d jours agrégés dans %s", len(records), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
