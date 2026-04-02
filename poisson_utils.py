import json
import math
from pathlib import Path

import numpy as np


def load_config(config_path: Path | str = "config.json") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def select_mode(config: dict, mode: str | None = None) -> dict:
    selected = mode or config["defaults"]["mode"]
    if selected not in config["modes"]:
        raise ValueError(f"Unknown mode: {selected}")
    return config["modes"][selected]


def poisson_pmf(k: np.ndarray, lam: float) -> np.ndarray:
    k = np.asarray(k, dtype=float)
    log_p = k * np.log(lam) - lam - np.vectorize(math.lgamma)(k + 1.0)
    return np.exp(log_p)


def basic_stats(counts: np.ndarray, include_relative_error: bool = False) -> dict:
    counts = np.asarray(counts, dtype=float)
    n = counts.size
    mean = float(np.mean(counts))
    var = float(np.var(counts, ddof=1)) if n > 1 else float("nan")
    sd = float(np.sqrt(var)) if n > 1 else float("nan")
    sem = sd / math.sqrt(n) if n > 1 else float("nan")
    poisson_sd = math.sqrt(mean) if mean > 0 else float("nan")
    fano = var / mean if mean > 0 else float("nan")

    out = {
        "N": int(n),
        "Mean": mean,
        "Variance": var,
        "Sample_SD": sd,
        "Poisson_SD_sqrt_mean": poisson_sd,
        "SEM": sem,
        "Fano_var_over_mean": fano,
    }
    if include_relative_error:
        out["Relative_error_1_over_sqrt_mean"] = 1.0 / math.sqrt(mean) if mean > 0 else float("nan")
    return out


def observed_expected(counts: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray(counts, dtype=int)
    k_min, k_max = int(values.min()), int(values.max())
    k = np.arange(k_min, k_max + 1)
    bins = np.arange(k_min - 0.5, k_max + 1.5, 1.0)
    observed, _ = np.histogram(values, bins=bins)
    expected = values.size * poisson_pmf(k, float(values.mean()))
    return k, observed.astype(float), expected.astype(float)


def chi2_hist(observed: np.ndarray, expected: np.ndarray) -> tuple[float, int, float]:
    mask = expected >= 1.0
    if not np.any(mask):
        return float("nan"), 0, float("nan")
    chi2 = float(np.sum(((observed[mask] - expected[mask]) ** 2) / expected[mask]))
    dof = int(mask.sum() - 2)
    return chi2, dof, (chi2 / dof if dof > 0 else float("nan"))
