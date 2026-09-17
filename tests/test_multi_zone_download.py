import json
from datetime import date
from pathlib import Path

import numpy as np
import rasterio

from src.multi_zone_download import load_zones, run


def write_config(path: Path) -> None:
    path.write_text(json.dumps({"zones": [
        {"id": "west", "bbox": [0, 0, 1, 1]},
        {"id": "east", "bbox": [1, 0, 2, 1]},
    ]}), encoding="utf-8")


def write_raster(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        path, "w", driver="GTiff", height=2, width=2, count=1, dtype="float32",
        crs="EPSG:4326", transform=rasterio.transform.from_origin(0, 2, 1, 1), nodata=-9999,
    ) as raster:
        raster.write(np.array([[1, 2], [3, 4]], dtype="float32"), 1)


def test_load_zones_rejects_duplicate_ids(tmp_path: Path):
    path = tmp_path / "zones.json"
    path.write_text(json.dumps({"zones": [
        {"id": "same", "bbox": [0, 0, 1, 1]},
        {"id": "same", "bbox": [1, 0, 2, 1]},
    ]}), encoding="utf-8")
    try:
        load_zones(path)
    except ValueError as exc:
        assert "dupliqués" in str(exc)
    else:
        raise AssertionError("Une configuration dupliquée aurait dû échouer")


def test_run_keeps_one_raw_and_one_output_per_zone(tmp_path: Path, monkeypatch):
    zones = tmp_path / "zones.json"
    write_config(zones)
    raw = tmp_path / "raw.tif"
    write_raster(raw)

    def fake_download(url, destination, timeout):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw.read_bytes())
        return True

    monkeypatch.setattr("src.multi_zone_download.download", fake_download)
    monkeypatch.setattr("src.multi_zone_download.url_for", lambda day, product, stage: "https://example.test/data.tif")
    manifest = run(zones, date(2024, 1, 1), date(2024, 1, 1), tmp_path / "data")

    assert (tmp_path / "data/raw/chirps/final/rnl/20240101.tif").exists()
    assert (tmp_path / "data/processed/chirps/final/rnl/west/20240101.tif").exists()
    assert (tmp_path / "data/processed/chirps/final/rnl/east/20240101.tif").exists()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert len(payload["records"]) == 2
