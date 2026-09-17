import numpy as np
import pytest

from src.onset import (
    ThresholdOnsetConfig,
    liebmann_onset,
    onset_error_days,
    threshold_onset,
)


def test_threshold_onset_rejects_false_onset():
    rainfall = np.array([0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 15, 10, 5], dtype=float)
    config = ThresholdOnsetConfig(
        wet_day_mm=5, window_days=3, min_cumulative_mm=20,
        lookahead_days=7, max_dry_days=5, search_end_day=15,
    )
    assert threshold_onset(rainfall, config) == 12


def test_threshold_onset_returns_none_when_no_valid_window():
    rainfall = np.zeros(20)
    assert threshold_onset(rainfall) is None


def test_liebmann_onset_uses_cumulative_anomaly_minimum():
    climatology = np.full(10, 5.0)
    rainfall = np.array([0, 0, 1, 2, 3, 8, 9, 10, 10, 10], dtype=float)
    assert liebmann_onset(rainfall, climatology) == 5


def test_input_validation_and_error():
    with pytest.raises(ValueError):
        threshold_onset([1, -1, 2])
    assert onset_error_days(10, 13) == 3
    assert onset_error_days(None, 13) is None
