import json
from datetime import date
from pathlib import Path

import numpy as np
import rasterio

from src.annual_collection import dates_for_year, run_year


def test_dates_for_year_handles_leap_year():
    assert len(dates_for_year(1991)) == 365
    assert len(dates_for_year(1992)) == 366


def test_run_year_writes_manifest_and_deletes_raw_after_crop(tmp_path: Path, monkeypatch):
    zones = tmp_path / "zones.json"
    zones.write_text(json.dumps({"zones": [{"id": "zone", "bbox": [0, 0, 1, 1]}]}), encoding="utf-8")
    source = tmp_path / "source.tif"
    with rasterio.open(source, "w", driver="GTiff", height=2, width=2, count=1, dtype="float32", crs="EPSG:4326", transform=rasterio.transform.from_origin(0, 2, 1, 1), nodata=-9999) as raster:
        raster.write(np.ones((2, 2), dtype="float32"), 1)
    monkeypatch.setattr("src.annual_collection.dates_for_year", lambda year: [date(year, 1, 1), date(year, 1, 2)])

    def fake_download(url, destination, timeout):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        return True

    monkeypatch.setattr("src.annual_collection.download", fake_download)
    manifest = run_year(zones, 1991, tmp_path / "data")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert len(payload["records"]) == 2
    assert all(record["raw_deleted_after_validation"] for record in payload["records"])
    assert not (tmp_path / "data/raw/chirps/final/rnl/19910101.tif").exists()
    assert not (tmp_path / "data/raw/chirps/final/rnl/19910102.tif").exists()
