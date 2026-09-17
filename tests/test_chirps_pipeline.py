from datetime import date
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from src.chirps_pipeline import crop_and_clean, date_range, download, url_for


def test_date_range_is_inclusive():
    assert list(date_range(date(2024, 1, 1), date(2024, 1, 3))) == [
        date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)
    ]


def test_url_for_chirps_v3():
    assert url_for(date(2024, 1, 2), "rnl", "final") == (
        "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/rnl/2024/"
        "chirps-v3.0.rnl.2024.01.02.tif"
    )


def test_crop_and_clean_replaces_invalid_values(tmp_path: Path):
    source = tmp_path / "source.tif"
    destination = tmp_path / "cleaned.tif"
    values = np.array([[1, -2], [np.nan, 4]], dtype="float32")
    with rasterio.open(source, "w", driver="GTiff", height=2, width=2, count=1,
                       dtype="float32", crs="EPSG:4326", transform=from_origin(0, 2, 1, 1), nodata=-9999) as raster:
        raster.write(values, 1)

    stats = crop_and_clean(source, destination, (0, 0, 2, 2))
    with rasterio.open(destination) as raster:
        cleaned = raster.read(1)
        assert raster.nodata == -9999
        assert cleaned[0, 0] == 1
        assert cleaned[0, 1] == -9999
        assert cleaned[1, 0] == -9999
        assert cleaned[1, 1] == 4
    assert stats["valid_pixels"] == 2
    assert stats["nodata_pixels"] == 2


def test_download_retries_transient_network_failure(tmp_path: Path, monkeypatch):
    destination = tmp_path / "retry.tif"
    class Response:
        status_code = 200
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): return None
        def iter_content(self, chunk_size): yield b"complete"
    calls = {"count": 0}
    def get(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] < 2:
            raise OSError("transient TLS failure")
        return Response()
    monkeypatch.setattr("src.chirps_pipeline.requests.get", get)
    monkeypatch.setattr("src.chirps_pipeline.sleep", lambda _: None)
    assert download("https://example.test/retry.tif", destination, timeout=10) is True
    assert calls["count"] == 2
    assert destination.read_bytes() == b"complete"
    assert not destination.with_suffix(".tif.part").exists()


def test_download_removes_partial_file_on_failure(tmp_path: Path, monkeypatch):
    destination = tmp_path / "nested" / "file.tif"
    class BrokenResponse:
        status_code = 200
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): return None
        def iter_content(self, chunk_size):
            yield b"partial"
            raise OSError("simulated connection failure")
    monkeypatch.setattr("src.chirps_pipeline.requests.get", lambda *args, **kwargs: BrokenResponse())
    monkeypatch.setattr("src.chirps_pipeline.sleep", lambda _: None)
    try:
        download("https://example.test/file.tif", destination, timeout=1)
    except OSError as exc:
        assert "simulated" in str(exc)
    else:
        raise AssertionError("Le téléchargement aurait dû échouer")
    assert not destination.exists()
    assert not destination.with_suffix(".tif.part").exists()


def test_download_removes_partial_file_on_total_timeout(tmp_path: Path, monkeypatch):
    destination = tmp_path / "nested" / "timeout.tif"
    class SlowResponse:
        status_code = 200
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): return None
        def iter_content(self, chunk_size): yield b"partial"
    monkeypatch.setattr("src.chirps_pipeline.requests.get", lambda *args, **kwargs: SlowResponse())
    ticks = iter([0.0, 2.0, 2.0])
    monkeypatch.setattr("src.chirps_pipeline.time.monotonic", lambda: next(ticks))
    try:
        download("https://example.test/slow.tif", destination, timeout=1)
    except TimeoutError as exc:
        assert "dépassant" in str(exc)
    else:
        raise AssertionError("Le téléchargement aurait dû dépasser le délai total")
    assert not destination.exists()
    assert not destination.with_suffix(".tif.part").exists()
