from datetime import date
from pathlib import Path

import numpy as np
import rasterio

from src.chirps_series import aggregate_directory, aggregate_raster


def write_raster(path: Path, values: np.ndarray) -> None:
    with rasterio.open(
        path, "w", driver="GTiff", height=values.shape[0], width=values.shape[1],
        count=1, dtype="float32", crs="EPSG:4326", transform=rasterio.transform.from_origin(0, 2, 1, 1),
        nodata=-9999,
    ) as raster:
        raster.write(values.astype("float32"), 1)


def test_aggregate_raster_reports_mean_and_coverage(tmp_path: Path):
    path = tmp_path / "20240101.tif"
    write_raster(path, np.array([[1, 3], [5, -9999]], dtype=float))
    record = aggregate_raster(path, min_coverage=0.75)
    assert record.date == date(2024, 1, 1)
    assert record.mean_mm == 3.0
    assert record.valid_pixels == 3
    assert record.coverage_fraction == 0.75


def test_low_coverage_is_explicitly_missing(tmp_path: Path):
    path = tmp_path / "20240102.tif"
    write_raster(path, np.array([[1, -9999], [-9999, -9999]], dtype=float))
    record = aggregate_raster(path, min_coverage=0.75)
    assert record.mean_mm is None
    assert record.valid_pixels == 1


def test_aggregate_directory_writes_csv_and_checks_dates(tmp_path: Path):
    input_dir = tmp_path / "rasters"
    input_dir.mkdir()
    write_raster(input_dir / "20240101.tif", np.ones((2, 2)))
    write_raster(input_dir / "20240102.tif", np.full((2, 2), 2))
    output = tmp_path / "daily.csv"
    records = aggregate_directory(input_dir, output, start=date(2024, 1, 1), end=date(2024, 1, 2))
    assert len(records) == 2
    lines = output.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("date,mean_mm")
    assert "2024-01-02,2.000000" in lines[2]
