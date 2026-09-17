import json
from pathlib import Path

import numpy as np
import rasterio

from src.annual_collection import run_year
from src.annual_quality import build_quality_report


def test_quality_report_marks_complete_year(tmp_path: Path, monkeypatch):
    zones = tmp_path / "zones.json"
    zones.write_text(json.dumps({"zones": [{"id": "zone", "bbox": [0, 0, 1, 1]}]}), encoding="utf-8")
    source = tmp_path / "source.tif"
    with rasterio.open(source, "w", driver="GTiff", height=2, width=2, count=1, dtype="float32", crs="EPSG:4326", transform=rasterio.transform.from_origin(0, 2, 1, 1), nodata=-9999) as raster:
        raster.write(np.ones((2, 2), dtype="float32"), 1)
    monkeypatch.setattr("src.annual_collection.dates_for_year", lambda year: [__import__('datetime').date(year, 1, 1)])
    monkeypatch.setattr("src.annual_collection.download", lambda url, destination, timeout: (destination.parent.mkdir(parents=True, exist_ok=True), destination.write_bytes(source.read_bytes())))
    manifest = run_year(zones, 1991, tmp_path / "data")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["configuration"]["end"] = "1991-01-01"
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    report = build_quality_report(manifest)
    assert report["valid"] is True
    assert report["expected_days"] == 1
    assert report["observed_days"] == 1
    assert report["zone_record_counts"] == {"zone": 1}
