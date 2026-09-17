from datetime import date, timedelta
from pathlib import Path

import numpy as np

from src.season_analysis import DailyObservation, analyze_onsets, load_daily_csv, write_results


def synthetic_year(year: int, onset_day: int, shift: float = 0.0) -> list[DailyObservation]:
    start = date(year, 1, 1)
    observations = []
    for index in range(365):
        day = start + timedelta(days=index + (1 if index >= 59 and year % 4 == 0 else 0))
        rainfall = 0.2 if index < onset_day - 1 else 8.0
        observations.append(DailyObservation(day, rainfall + shift, 1.0))
    return observations


def test_analysis_uses_independent_climatology():
    observations = synthetic_year(2021, 100) + synthetic_year(2022, 110, 0.2) + synthetic_year(2023, 120, 0.4)
    results = analyze_onsets(observations)
    assert [result.status for result in results] == ["ok", "ok", "ok"]
    assert all(result.climatology_years == 2 for result in results)
    assert all(result.onset_liebmann_day is not None for result in results)


def test_incomplete_year_is_flagged():
    observations = synthetic_year(2021, 100)[:-1]
    results = analyze_onsets(observations)
    assert results[0].status == "incomplete"
    assert results[0].onset_threshold_day is None


def test_write_results_is_readable(tmp_path: Path):
    observations = synthetic_year(2021, 100) + synthetic_year(2022, 100)
    output = tmp_path / "onsets.csv"
    write_results(analyze_onsets(observations), output)
    content = output.read_text(encoding="utf-8")
    assert "onset_threshold_day" in content
