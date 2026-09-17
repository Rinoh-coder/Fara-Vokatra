"""Produire un rapport qualité détaillé pour un manifeste annuel CHIRPS."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    from src.manifest_validator import validate_manifest, write_report
except ModuleNotFoundError:
    from manifest_validator import validate_manifest, write_report


def build_quality_report(manifest_path: Path) -> dict:
    base = validate_manifest(manifest_path, check_files=True)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = [record for record in payload.get("records", []) if "error" not in record]
    dates = sorted({record.get("date") for record in records})
    zone_counts = Counter(record.get("zone_id") for record in records)
    coverages = []
    for record in records:
        stats = record.get("stats", {})
        total_pixels = stats.get("valid_pixels", 0) + stats.get("nodata_pixels", 0)
        if total_pixels:
            coverages.append(stats.get("valid_pixels", 0) / total_pixels)
    min_coverage = min(coverages) if coverages else None
    max_coverage = max(coverages) if coverages else None
    configured_zones = list(payload.get("configuration", {}).get("zones", []))
    expected_days = (base["expected_records"] // len(configured_zones)) if configured_zones else 0
    base.update({
        "quality_version": "0.1",
        "expected_days": expected_days,
        "observed_days": len(dates),
        "zone_record_counts": dict(sorted(zone_counts.items())),
        "coverage": {"minimum": min_coverage, "maximum": max_coverage, "threshold": 0.95, "below_threshold_records": sum(1 for value in coverages if value < 0.95)},
        "complete_year": base["valid"] and len(dates) == expected_days and all(zone_counts[zone] == expected_days for zone in configured_zones),
    })
    base["valid"] = bool(base["valid"] and base["complete_year"])
    return base


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = build_quality_report(args.manifest)
        write_report(report, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Rapport qualité interrompu : {exc}")
        return 1
    print(f"Rapport écrit : {args.output} (valid={report['valid']})")
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
