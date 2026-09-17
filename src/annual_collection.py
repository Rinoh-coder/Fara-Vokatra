"""Collecte CHIRPS d'une année, reprenable jour par jour et compatible avec l'archivage."""
from __future__ import annotations

import argparse
import json
import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

try:
    from src.chirps_pipeline import crop_and_clean, download, sha256, url_for
    from src.multi_zone_download import load_zones
except ModuleNotFoundError:  # Exécution directe : python3 src/annual_collection.py
    from chirps_pipeline import crop_and_clean, download, sha256, url_for
    from multi_zone_download import load_zones

LOG = logging.getLogger("annual_collection")


def dates_for_year(year: int) -> list[date]:
    current = date(year, 1, 1)
    end = date(year, 12, 31)
    dates = []
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def run_year(zones_path: Path, year: int, data_root: Path, product: str = "rnl", stage: str = "final", timeout: int = 60) -> Path:
    zones = load_zones(zones_path)
    raw_root = data_root / "raw" / "chirps" / stage / product
    processed_root = data_root / "processed" / "chirps" / stage / product
    manifest_path = data_root / "processed" / "chirps" / "manifests" / f"year_{year}_{product}_{stage}.json"
    payload = {
        "dataset": "CHIRPS v3 daily",
        "configuration_file": str(zones_path),
        "configuration": {"start": f"{year}-01-01", "end": f"{year}-12-31", "product": product, "stage": stage, "zones": [z["id"] for z in zones], "chunk": "year", "raw_policy": "delete_after_successful_crop_and_checksum"},
        "records": [],
    }
    if manifest_path.exists():
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = {(r.get("date"), r.get("zone_id")): r for r in payload.get("records", []) if "error" not in r}
    for day in dates_for_year(year):
        iso = day.isoformat()
        if all((iso, zone["id"]) in records for zone in zones):
            continue
        url = url_for(day, product, stage)
        raw = raw_root / f"{day:%Y%m%d}.tif"
        try:
            download(url, raw, timeout)
            raw_checksum = sha256(raw)
            day_records = []
            for zone in zones:
                zone_id = zone["id"]
                cleaned = processed_root / zone_id / f"{day:%Y%m%d}.tif"
                stats = crop_and_clean(raw, cleaned, tuple(zone["bbox"]))
                day_records.append({"date": iso, "zone_id": zone_id, "url": url, "raw_path": str(raw), "cleaned_path": str(cleaned), "raw_sha256": raw_checksum, "cleaned_sha256": sha256(cleaned), "stats": stats, "raw_deleted_after_validation": True})
            for record in day_records:
                records[(record["date"], record["zone_id"])] = record
            raw.unlink(missing_ok=True)
            payload["records"] = sorted(records.values(), key=lambda r: (r["date"], r["zone_id"]))
            _write_json(manifest_path, payload)
            LOG.info("%s terminé (%d/%d jours)", iso, len({r["date"] for r in records.values()}), len(dates_for_year(year)))
        except Exception as exc:
            payload["records"] = sorted([*records.values(), {"date": iso, "url": url, "error": str(exc)}], key=lambda r: (r.get("date", ""), r.get("zone_id", "")))
            _write_json(manifest_path, payload)
            raise
    return manifest_path


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zones", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        manifest = run_year(args.zones, args.year, args.data_root, timeout=args.timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        LOG.error("Collecte interrompue : %s", exc)
        return 1
    LOG.info("Manifeste annuel : %s", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
