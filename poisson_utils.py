import math

import matplotlib.pyplot as plt
import numpy as np


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


def plot_freq_vs_count(
    ax,
    counts: np.ndarray,
    title: str,
    bar_color: str,
    edge_color: str,
    err_color: str,
    show_relative_error: bool = False,
) -> dict:
    stats = basic_stats(counts, include_relative_error=show_relative_error)
    k, observed, expected = observed_expected(counts)
    obs_err = np.sqrt(np.maximum(observed, 1.0))
    chi2, dof, red = chi2_hist(observed, expected)

    ax.bar(k, observed, width=0.86, color=bar_color, edgecolor=edge_color, alpha=0.9, label="Observed frequency")
    ax.errorbar(k, observed, yerr=obs_err, fmt="none", ecolor=err_color, elinewidth=1.1, capsize=2, label="Observed error = sqrt(n)")
    ax.plot(k, expected, color="#d62728", linewidth=2.0, marker="o", markersize=3.5, label="Expected Poisson frequency")

    lines = [
        f"N={stats['N']}",
        f"mean={stats['Mean']:.2f}",
        f"SD={stats['Sample_SD']:.2f}",
        f"sqrt(mean)={stats['Poisson_SD_sqrt_mean']:.2f}",
    ]
    if show_relative_error:
        lines.append(f"1/sqrt(mean)={stats['Relative_error_1_over_sqrt_mean']:.4f}")
    lines.extend([f"Fano={stats['Fano_var_over_mean']:.3f}", f"chi2/dof={red:.3f}"])
    ax.text(
        0.02,
        0.98,
        "\n".join(lines),
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8.7,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666666", alpha=0.92),
    )

    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("Count")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)

    return {**stats, "Chi2_hist": chi2, "DOF_hist": dof, "Chi2_per_DOF_hist": red}
