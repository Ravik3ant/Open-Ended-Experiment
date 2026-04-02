from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from poisson_utils import basic_stats, chi2_hist, load_config, observed_expected, select_mode


def _stats_text(stats: dict, mode_cfg: dict) -> str:
    labels = {
        "N": lambda s: f"N={s['N']}",
        "Mean": lambda s: f"mean={s['Mean']:.2f}",
        "Sample_SD": lambda s: f"SD={s['Sample_SD']:.2f}",
        "Poisson_SD_sqrt_mean": lambda s: f"sqrt(mean)={s['Poisson_SD_sqrt_mean']:.2f}",
        "Relative_error_1_over_sqrt_mean": lambda s: f"1/sqrt(mean)={s['Relative_error_1_over_sqrt_mean']:.4f}",
        "Fano_var_over_mean": lambda s: f"Fano={s['Fano_var_over_mean']:.3f}",
        "Chi2_per_DOF_hist": lambda s: f"chi2/dof={s['Chi2_per_DOF_hist']:.3f}",
    }
    return "\n".join(labels[k](stats) for k in mode_cfg["stats_to_show"] if k in labels and k in stats)


def _plot_freq_vs_count(ax, counts, title: str, mode_cfg: dict, colors: dict):
    stats = basic_stats(counts, include_relative_error=True)
    k, observed, expected = observed_expected(counts)
    _, _, red = chi2_hist(observed, expected)
    stats["Chi2_per_DOF_hist"] = red

    ax.bar(k, observed, width=0.86, color=colors["bar"], edgecolor=colors["edge"], alpha=0.9, label="Observed frequency")
    ax.errorbar(k, observed, yerr=(observed.clip(min=1.0) ** 0.5), fmt="none", ecolor=colors["error"], elinewidth=1.1, capsize=2, label="Observed error = sqrt(n)")
    ax.plot(k, expected, color=mode_cfg["colors"]["expected"], linewidth=2.0, marker="o", markersize=3.5, label="Expected Poisson frequency")

    if mode_cfg["show_stats_box"]:
        ax.text(
            0.02,
            0.98,
            _stats_text(stats, mode_cfg),
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8.7,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666666", alpha=0.92),
        )

    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("Count")
    ax.set_ylabel("Frequency")
    if mode_cfg.get("show_grid", True):
        ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)
    return stats


def run_experiment2(excel_path: Path, output_dir: Path, config_path: Path = Path("config.json"), mode: str | None = None):
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = load_config(config_path)
    mode_cfg = select_mode(cfg, mode)
    mode_cfg["show_grid"] = cfg["plot"]["show_grid"]
    dpi = cfg["plot"]["figure_dpi"]

    s1 = pd.read_excel(excel_path, sheet_name="Sheet1")
    s2 = pd.read_excel(excel_path, sheet_name="Sheet2")

    base = s1[["Sr. Num", "Count"]].dropna().copy()
    base["Count"] = base["Count"].astype(int)

    n = min(50, len(base), len(s2))
    datasets = {
        "t=10s, N=50": base.iloc[:n]["Count"].to_numpy(),
        "t=20s, N=50": s2.iloc[:n]["t=20s"].dropna().astype(int).to_numpy(),
        "t=30s, N=50": s2.iloc[:n]["t=30s"].dropna().astype(int).to_numpy(),
    }

    colors = mode_cfg["colors"]["exp2"]
    rows = []
    for name, counts in datasets.items():
        fig, ax = plt.subplots(figsize=(10.8, 4.8), constrained_layout=True)
        stats = _plot_freq_vs_count(ax, counts, f"Experiment 2: {name}", mode_cfg, colors)
        rows.append({"Dataset": name, **stats})
        safe = name.lower().replace(" ", "_").replace("=", "").replace(",", "")
        fig.savefig(output_dir / f"exp2_freq_{safe}.png", dpi=dpi)
        plt.close(fig)

    fig, axs = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, counts) in zip(axs, datasets.items()):
        _plot_freq_vs_count(ax, counts, f"Exp2 combined: {name}", mode_cfg, colors)
    fig.savefig(output_dir / "exp2_combined_times_freq.png", dpi=dpi)
    plt.close(fig)

    summary = pd.DataFrame(rows)
    summary.to_csv(output_dir / "exp2_summary.csv", index=False)
    print("Experiment 2 outputs saved to:", output_dir)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    cfg = load_config("config.json")
    run_experiment2(Path(cfg["defaults"]["data_path"]), Path(cfg["defaults"]["output_dir"]), Path("config.json"), cfg["defaults"]["mode"])
