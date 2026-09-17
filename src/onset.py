"""Baselines explicables pour détecter l'onset de la saison des pluies.

Les fonctions travaillent sur une série quotidienne déjà agrégée pour une zone.
Elles ne remplacent pas une validation agronomique locale.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ThresholdOnsetConfig:
    """Paramètres de la règle agronomique à seuils."""

    wet_day_mm: float = 1.0
    window_days: int = 3
    min_cumulative_mm: float = 20.0
    lookahead_days: int = 30
    max_dry_days: int = 10
    dry_day_mm: float = 1.0
    search_start_day: int = 1
    search_end_day: int = 365


def _validate_rainfall(rainfall: Sequence[float]) -> np.ndarray:
    values = np.asarray(rainfall, dtype="float64")
    if values.ndim != 1 or values.size == 0:
        raise ValueError("rainfall doit être une série 1D non vide")
    if np.any(~np.isfinite(values)) or np.any(values < 0):
        raise ValueError("rainfall doit contenir des valeurs finies et positives ou nulles")
    return values


def _has_long_dry_spell(values: np.ndarray, start: int, config: ThresholdOnsetConfig) -> bool:
    end = min(values.size, start + config.lookahead_days)
    dry = values[start:end] < config.dry_day_mm
    run = 0
    for is_dry in dry:
        run = run + 1 if is_dry else 0
        if run >= config.max_dry_days:
            return True
    return False


def threshold_onset(rainfall: Sequence[float], config: ThresholdOnsetConfig | None = None) -> int | None:
    """Retourne le jour 1-indexé du premier onset sans faux onset proche.

    La règle cherche une fenêtre de pluie cumulée suffisante contenant au moins
    un jour humide, puis rejette la fenêtre si une séquence sèche trop longue
    suit dans l'horizon prospectif configuré.
    """
    config = config or ThresholdOnsetConfig()
    values = _validate_rainfall(rainfall)
    effective_end = min(config.search_end_day, values.size)
    if not (1 <= config.search_start_day <= effective_end):
        raise ValueError("fenêtre de recherche invalide")
    if config.window_days < 1 or config.lookahead_days < 1 or config.max_dry_days < 1:
        raise ValueError("les fenêtres doivent être positives")
    first = config.search_start_day - 1
    last = min(effective_end, values.size - config.window_days + 1)
    for index in range(first, last):
        window = values[index:index + config.window_days]
        if window.sum() < config.min_cumulative_mm:
            continue
        if not np.any(window >= config.wet_day_mm):
            continue
        if not _has_long_dry_spell(values, index + config.window_days, config):
            return index + 1
    return None


def liebmann_onset(rainfall: Sequence[float], climatology: Sequence[float] | None = None) -> int | None:
    """Retourne le minimum de l'anomalie cumulée, en jour 1-indexé.

    ``climatology`` doit contenir une normale quotidienne de même longueur.
    Si elle est omise, la moyenne de la série est utilisée uniquement comme
    fallback exploratoire ; ce fallback ne doit pas être utilisé pour une
    évaluation historique sans climatologie indépendante.
    """
    values = _validate_rainfall(rainfall)
    if climatology is None:
        normal = np.full(values.size, values.mean(), dtype="float64")
    else:
        normal = np.asarray(climatology, dtype="float64")
        if normal.shape != values.shape or np.any(~np.isfinite(normal)):
            raise ValueError("climatology doit avoir la même forme et des valeurs finies")
    cumulative_anomaly = np.cumsum(values - normal)
    return int(np.argmin(cumulative_anomaly)) + 1


def onset_error_days(observed_day: int | None, predicted_day: int | None) -> int | None:
    """Calcule l'erreur signée prédiction moins observation."""
    if observed_day is None or predicted_day is None:
        return None
    return predicted_day - observed_day
