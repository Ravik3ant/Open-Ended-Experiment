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


def _plot_freq_vs_count(ax, counts, title: str, mode_cfg: dict, colors: dict, include_relative_error: bool):
    stats = basic_stats(counts, include_relative_error=include_relative_error)
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


def build_multiseed_random_summary(data: pd.DataFrame, seeds: list[int]) -> pd.DataFrame:
    rows = []
    for size in [50, 100]:
        n = min(size, len(data))
        for seed in seeds:
            sample = data.sample(n=n, replace=False, random_state=seed)
            stats = basic_stats(sample["Count"].to_numpy())
            _, obs, exp = observed_expected(sample["Count"].to_numpy())
            _, _, red = chi2_hist(obs, exp)
            rows.append({"Subset_size": n, "Seed": seed, **stats, "Chi2_per_DOF_hist": red})
    return pd.DataFrame(rows)


def build_seed_stability_summary(multiseed: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for subset_size, grp in multiseed.groupby("Subset_size"):
        fano_ok = ((grp["Fano_var_over_mean"] >= 0.8) & (grp["Fano_var_over_mean"] <= 1.2)).mean()
        chi2_ok = ((grp["Chi2_per_DOF_hist"] >= 0.5) & (grp["Chi2_per_DOF_hist"] <= 1.5)).mean()
        mean_cv_pct = (grp["Mean"].std(ddof=1) / grp["Mean"].mean() * 100.0) if grp["Mean"].mean() != 0 else float("nan")
        stable = (fano_ok >= 0.7) and (chi2_ok >= 0.7) and (mean_cv_pct <= 5.0)

        summary_rows.append(
            {
                "Subset_size": int(subset_size),
                "Seeds_tested": int(len(grp)),
                "Mean_of_mean": float(grp["Mean"].mean()),
                "Std_of_mean": float(grp["Mean"].std(ddof=1)),
                "Mean_CV_percent": float(mean_cv_pct),
                "Mean_Fano": float(grp["Fano_var_over_mean"].mean()),
                "Std_Fano": float(grp["Fano_var_over_mean"].std(ddof=1)),
                "Fano_pass_fraction": float(fano_ok),
                "Mean_chi2_per_dof": float(grp["Chi2_per_DOF_hist"].mean()),
                "Std_chi2_per_dof": float(grp["Chi2_per_DOF_hist"].std(ddof=1)),
                "Chi2_pass_fraction": float(chi2_ok),
                "Stable_conclusion": bool(stable),
            }
        )
    return pd.DataFrame(summary_rows)


def write_seed_stability_markdown(stability_df: pd.DataFrame, output_path: Path):
    lines = [
        "# Seed Stability Report",
        "",
        "This report checks whether conclusions from random subsets are stable across multiple seeds.",
        "",
        "Pass rules used:",
        "- Fano in [0.8, 1.2] for at least 70% of seeds",
        "- chi2/dof in [0.5, 1.5] for at least 70% of seeds",
        "- mean CV <= 5% across seeds",
        "",
    ]
    for _, r in stability_df.iterrows():
        lines.extend(
            [
                f"## Subset size {int(r['Subset_size'])}",
                f"- Seeds tested: {int(r['Seeds_tested'])}",
                f"- Mean of subset means: {r['Mean_of_mean']:.4f}",
                f"- Std of subset means: {r['Std_of_mean']:.4f}",
                f"- Mean CV (%): {r['Mean_CV_percent']:.3f}",
                f"- Mean Fano: {r['Mean_Fano']:.4f} (pass fraction: {r['Fano_pass_fraction']:.2f})",
                f"- Mean chi2/dof: {r['Mean_chi2_per_dof']:.4f} (pass fraction: {r['Chi2_pass_fraction']:.2f})",
                f"- Stable conclusion: {'YES' if r['Stable_conclusion'] else 'NO'}",
                "",
            ]
        )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def run_experiment1(excel_path: Path, output_dir: Path, config_path: Path = Path("config.json"), mode: str | None = None):
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = load_config(config_path)
    mode_cfg = select_mode(cfg, mode)
    mode_cfg["show_grid"] = cfg["plot"]["show_grid"]
    dpi = cfg["plot"]["figure_dpi"]

    data = pd.read_excel(excel_path, sheet_name="Sheet1")[["Sr. Num", "Count"]].dropna().copy()
    data["Count"] = data["Count"].astype(int)

    n_total = len(data)
    first50 = data.iloc[: min(50, n_total)]
    first100 = data.iloc[: min(100, n_total)]
    full = data

    seeds = cfg["random"]["seeds"]
    random50 = data.sample(n=min(50, n_total), replace=False, random_state=seeds[0])
    random100 = data.sample(n=min(100, n_total), replace=False, random_state=seeds[1])

    datasets = {
        "First 50": first50,
        "First 100": first100,
        "Random 50 (no replacement)": random50,
        "Random 100 (no replacement)": random100,
        f"All {n_total}": full,
    }

    colors = mode_cfg["colors"]["exp1"]
    summary_rows = []
    for name, df in datasets.items():
        fig, ax = plt.subplots(figsize=(10.8, 4.8), constrained_layout=True)
        stats = _plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Experiment 1: {name}", mode_cfg, colors, include_relative_error=False)
        summary_rows.append({"Dataset": name, **stats})
        safe = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        fig.savefig(output_dir / f"exp1_freq_{safe}.png", dpi=dpi)
        plt.close(fig)

    fig1, axs1 = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, df) in zip(axs1, [("First 50", first50), ("First 100", first100), (f"All {n_total}", full)]):
        _plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Exp1 combined (first subsets): {name}", mode_cfg, colors, include_relative_error=False)
    fig1.savefig(output_dir / "exp1_combined_first_subsets_freq.png", dpi=dpi)
    plt.close(fig1)

    fig2, axs2 = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, df) in zip(axs2, [("Random 50", random50), ("Random 100", random100), (f"All {n_total}", full)]):
        _plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Exp1 combined (random subsets): {name}", mode_cfg, colors, include_relative_error=False)
    fig2.savefig(output_dir / "exp1_combined_random_subsets_freq.png", dpi=dpi)
    plt.close(fig2)

    multiseed = build_multiseed_random_summary(data, seeds)
    multiseed.to_csv(output_dir / "exp1_random_multiseed_raw.csv", index=False)
    multiseed_avg = (
        multiseed.groupby("Subset_size", as_index=False)[
            ["Mean", "Sample_SD", "Poisson_SD_sqrt_mean", "SEM", "Fano_var_over_mean", "Chi2_per_DOF_hist"]
        ]
        .mean()
        .rename(columns={"Subset_size": "N_random_avg"})
    )
    multiseed_avg.to_csv(output_dir / "exp1_random_multiseed_avg.csv", index=False)

    stability = build_seed_stability_summary(multiseed)
    stability.to_csv(output_dir / "exp1_seed_stability_summary.csv", index=False)
    write_seed_stability_markdown(stability, output_dir / "exp1_seed_stability_report.md")

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(output_dir / "exp1_summary.csv", index=False)
    print("Experiment 1 outputs saved to:", output_dir)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nSeed stability summary:")
    print(stability.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    cfg = load_config("config.json")
    run_experiment1(Path(cfg["defaults"]["data_path"]), Path(cfg["defaults"]["output_dir"]), Path("config.json"), cfg["defaults"]["mode"])
