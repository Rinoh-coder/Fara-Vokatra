"""Produire un rapport qualité annuel CHIRPS avec empreinte terrestre stable."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio

try:
    from src.manifest_validator import validate_manifest, write_report
except ModuleNotFoundError:
    from manifest_validator import validate_manifest, write_report


def _land_adjusted_coverages(records: list[dict], threshold: float = 0.95) -> tuple[list[float], dict]:
    by_zone: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_zone[record["zone_id"]].append(record)
    coverages = []
    footprints = {}
    record_coverages = {}
    for zone, zone_records in by_zone.items():
        validity = []
        for record in zone_records:
            with rasterio.open(record["cleaned_path"]) as raster:
                data = raster.read(1)
            validity.append(np.isfinite(data) & (data >= 0))
        stack = np.stack(validity)
        stable_count = max(1, math.ceil(threshold * stack.shape[0]))
        land_mask = stack.sum(axis=0) >= stable_count
        land_pixels = int(land_mask.sum())
        for record, valid in zip(zone_records, validity):
            coverage = float((valid & land_mask).sum() / land_pixels) if land_pixels else 0.0
            record_coverages[(record["date"], zone)] = coverage
            coverages.append(coverage)
        footprints[zone] = {"days": len(zone_records), "stable_land_pixels": land_pixels, "raster_pixels": int(land_mask.size), "bbox_fraction": land_pixels / int(land_mask.size) if land_mask.size else 0.0}
    return coverages, footprints, record_coverages


def build_quality_report(manifest_path: Path) -> dict:
    base = validate_manifest(manifest_path, check_files=True)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = [record for record in payload.get("records", []) if "error" not in record]
    dates = sorted({record.get("date") for record in records})
    zone_counts = Counter(record.get("zone_id") for record in records)
    configured_zones = list(payload.get("configuration", {}).get("zones", []))
    expected_days = (base["expected_records"] // len(configured_zones)) if configured_zones else 0
    coverages, footprints, record_coverages = _land_adjusted_coverages(records)
    below = sum(1 for value in coverages if value < 0.95)
    base.update({
        "quality_version": "0.2",
        "expected_days": expected_days,
        "observed_days": len(dates),
        "zone_record_counts": dict(sorted(zone_counts.items())),
        "coverage": {"definition": "valid pixels relative to stable land footprint, not all BBOX pixels", "minimum": min(coverages) if coverages else None, "maximum": max(coverages) if coverages else None, "threshold": 0.95, "below_threshold_records": below},
        "stable_land_footprint": footprints,
        "complete_year": base["valid"] and len(dates) == expected_days and all(zone_counts[zone] == expected_days for zone in configured_zones),
    })
    base["valid"] = bool(base["valid"] and base["complete_year"] and below == 0)
    return base


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = build_quality_report(args.manifest)
        write_report(report, args.output)
    except (OSError, ValueError, json.JSONDecodeError, rasterio.errors.RasterioIOError) as exc:
        print(f"Rapport qualité interrompu : {exc}")
        return 1
    print(f"Rapport écrit : {args.output} (valid={report['valid']})")
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
