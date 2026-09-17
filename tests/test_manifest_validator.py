import hashlib
import json
from pathlib import Path

from src.manifest_validator import validate_manifest, write_report


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_manifest(tmp_path: Path, records: list[dict]) -> Path:
    raw = tmp_path / "raw.tif"
    cleaned = tmp_path / "cleaned.tif"
    raw.write_bytes(b"raw")
    cleaned.write_bytes(b"cleaned")
    for record in records:
        record.setdefault("raw_path", str(raw))
        record.setdefault("cleaned_path", str(cleaned))
        record.setdefault("raw_sha256", checksum(raw))
        record.setdefault("cleaned_sha256", checksum(cleaned))
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({
        "configuration": {"start": "2024-01-01", "end": "2024-01-02", "zones": ["west", "east"]},
        "records": records,
    }), encoding="utf-8")
    return path


def record(day: str, zone: str) -> dict:
    return {"date": day, "zone_id": zone}


def test_valid_manifest_checks_files_and_checksums(tmp_path: Path):
    path = make_manifest(tmp_path, [
        record("2024-01-01", "west"), record("2024-01-01", "east"),
        record("2024-01-02", "west"), record("2024-01-02", "east"),
    ])
    report = validate_manifest(path)
    assert report["valid"] is True
    assert report["expected_records"] == 4


def test_manifest_reports_missing_and_duplicate_records(tmp_path: Path):
    path = make_manifest(tmp_path, [record("2024-01-01", "west"), record("2024-01-01", "west")])
    report = validate_manifest(path)
    assert report["valid"] is False
    assert "2024-01-01/west" in report["duplicate_records"]
    assert "2024-01-02/east" in report["missing_records"]


def test_manifest_reports_checksum_mismatch(tmp_path: Path):
    path = make_manifest(tmp_path, [
        {**record("2024-01-01", "west"), "raw_sha256": "bad"},
        record("2024-01-01", "east"), record("2024-01-02", "west"), record("2024-01-02", "east"),
    ])
    report = validate_manifest(path)
    assert report["valid"] is False
    assert len(report["checksum_mismatches"]) == 1


def test_write_report_creates_json(tmp_path: Path):
    path = make_manifest(tmp_path, [record("2024-01-01", "west"), record("2024-01-01", "east"), record("2024-01-02", "west"), record("2024-01-02", "east")])
    report_path = tmp_path / "reports" / "quality.json"
    write_report(validate_manifest(path), report_path)
    assert json.loads(report_path.read_text(encoding="utf-8"))["valid"] is True
