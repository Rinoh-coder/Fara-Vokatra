"""Analyser les dates d'onset par année à partir d'une série CHIRPS quotidienne."""
from __future__ import annotations

import argparse
import csv
import logging
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

import numpy as np

from src.onset import ThresholdOnsetConfig, liebmann_onset, threshold_onset

LOG = logging.getLogger("season_analysis")
DAYS_PER_YEAR = 365


@dataclass(frozen=True)
class DailyObservation:
    day: date
    rainfall_mm: float
    coverage_fraction: float


@dataclass(frozen=True)
class SeasonResult:
    year: int
    status: str
    n_days: int
    onset_threshold_day: int | None
    onset_liebmann_day: int | None
    climatology_years: int


def load_daily_csv(path: Path) -> list[DailyObservation]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"date", "mean_mm", "coverage_fraction"}
        if not required.issubset(reader.fieldnames or set()):
            raise ValueError(f"Colonnes requises absentes: {sorted(required)}")
        observations = []
        for row in reader:
            if not row["mean_mm"]:
                continue
            rainfall = float(row["mean_mm"])
            coverage = float(row["coverage_fraction"])
            if not np.isfinite(rainfall) or rainfall < 0:
                raise ValueError(f"Pluie invalide pour {row['date']}")
            observations.append(DailyObservation(date.fromisoformat(row["date"]), rainfall, coverage))
    if not observations:
        raise ValueError("Aucune observation quotidienne exploitable")
    if len({item.day for item in observations}) != len(observations):
        raise ValueError("Dates dupliquées dans la série quotidienne")
    return sorted(observations, key=lambda item: item.day)


def _day_index(day: date) -> int | None:
    if day.month == 2 and day.day == 29:
        return None
    start = date(day.year, 1, 1)
    index = (day - start).days
    if day.month > 2 and day.year % 4 == 0 and (day.year % 100 != 0 or day.year % 400 == 0):
        index -= 1
    return index


def _year_vectors(observations: list[DailyObservation]) -> dict[int, np.ndarray]:
    grouped: dict[int, dict[int, float]] = defaultdict(dict)
    for item in observations:
        index = _day_index(item.day)
        if index is not None:
            grouped[item.day.year][index] = item.rainfall_mm
    vectors = {}
    for year, values in grouped.items():
        if len(values) == DAYS_PER_YEAR:
            vectors[year] = np.array([values[index] for index in range(DAYS_PER_YEAR)], dtype="float64")
    return vectors


def analyze_onsets(
    observations: list[DailyObservation],
    threshold_config: ThresholdOnsetConfig | None = None,
) -> list[SeasonResult]:
    vectors = _year_vectors(observations)
    results = []
    for year in sorted({item.day.year for item in observations}):
        rainfall = vectors.get(year)
        if rainfall is None:
            results.append(SeasonResult(year, "incomplete", 0, None, None, 0))
            continue
        previous = [vector for other_year, vector in vectors.items() if other_year != year]
        if not previous:
            results.append(SeasonResult(year, "no_independent_climatology", DAYS_PER_YEAR, threshold_onset(rainfall, threshold_config), None, 0))
            continue
        climatology = np.mean(np.vstack(previous), axis=0)
        results.append(SeasonResult(
            year, "ok", DAYS_PER_YEAR,
            threshold_onset(rainfall, threshold_config),
            liebmann_onset(rainfall, climatology), len(previous),
        ))
    return results


def write_results(results: list[SeasonResult], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0]).keys()) if results else ["year"])
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        results = analyze_onsets(load_daily_csv(args.input))
        write_results(results, args.output)
    except (OSError, ValueError) as exc:
        LOG.error("Analyse interrompue : %s", exc)
        return 1
    LOG.info("%d années analysées dans %s", len(results), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
