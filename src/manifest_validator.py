"""Valider la complétude et la provenance d'un manifeste CHIRPS multi-zone."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable


def _dates(start: date, end: date) -> set[str]:
    values = set()
    current = start
    while current <= end:
        values.add(current.isoformat())
        current += timedelta(days=1)
    return values


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(path: Path, check_files: bool = True) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    configuration = payload.get("configuration", {})
    try:
        start = date.fromisoformat(configuration["start"])
        end = date.fromisoformat(configuration["end"])
        zones = list(configuration["zones"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Configuration de manifeste invalide") from exc
    if not zones or len(set(zones)) != len(zones):
        raise ValueError("La configuration doit contenir des zones uniques")

    records = payload.get("records", [])
    keys = [(record.get("date"), record.get("zone_id")) for record in records]
    duplicate_keys = sorted(f"{day}/{zone}" for (day, zone), count in Counter(keys).items() if count > 1)
    expected = {(day, zone) for day in _dates(start, end) for zone in zones}
    observed = set(keys)
    missing = sorted(f"{day}/{zone}" for day, zone in expected - observed)
    unexpected = sorted(f"{day}/{zone}" for day, zone in observed - expected)
    errors = [
        {"date": record.get("date"), "zone_id": record.get("zone_id"), "error": record.get("error")}
        for record in records if "error" in record
    ]
    missing_files = []
    checksum_mismatches = []
    if check_files:
        for record in records:
            for field, checksum_field in (("raw_path", "raw_sha256"), ("cleaned_path", "cleaned_sha256")):
                raw_path = record.get(field)
                if not raw_path:
                    missing_files.append({"key": [record.get("date"), record.get("zone_id")], "path": raw_path})
                    continue
                if field == "raw_path" and record.get("raw_deleted_after_validation") is True:
                    continue
                target = Path(raw_path)
                if not target.exists():
                    missing_files.append({"key": [record.get("date"), record.get("zone_id")], "path": raw_path})
                elif record.get(checksum_field) and _sha256(target) != record[checksum_field]:
                    checksum_mismatches.append({"key": [record.get("date"), record.get("zone_id")], "path": raw_path})

    valid = not any((duplicate_keys, missing, unexpected, errors, missing_files, checksum_mismatches))
    return {
        "manifest": str(path), "valid": valid, "expected_records": len(expected),
        "observed_records": len(records), "zones": zones,
        "date_range": {"start": start.isoformat(), "end": end.isoformat()},
        "duplicate_records": duplicate_keys, "missing_records": missing,
        "unexpected_records": unexpected, "errors": errors,
        "missing_files": missing_files, "checksum_mismatches": checksum_mismatches,
    }


def write_report(report: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-file-check", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = validate_manifest(args.manifest, check_files=not args.skip_file_check)
        write_report(report, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Validation interrompue : {exc}")
        return 1
    print(f"Rapport écrit : {args.output} (valid={report['valid']})")
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
