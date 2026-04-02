from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from poisson_utils import basic_stats, chi2_hist, observed_expected, plot_freq_vs_count


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


def run_experiment1(excel_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_excel(excel_path, sheet_name="Sheet1")[["Sr. Num", "Count"]].dropna().copy()
    data["Count"] = data["Count"].astype(int)

    n_total = len(data)
    first50 = data.iloc[: min(50, n_total)]
    first100 = data.iloc[: min(100, n_total)]
    full = data

    seeds = [11, 23, 37, 53, 71, 89, 101, 131]
    random50 = data.sample(n=min(50, n_total), replace=False, random_state=seeds[0])
    random100 = data.sample(n=min(100, n_total), replace=False, random_state=seeds[1])

    datasets = {
        "First 50": first50,
        "First 100": first100,
        "Random 50 (no replacement)": random50,
        "Random 100 (no replacement)": random100,
        f"All {n_total}": full,
    }

    summary_rows = []
    for name, df in datasets.items():
        fig, ax = plt.subplots(figsize=(10.8, 4.8), constrained_layout=True)
        stats = plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Experiment 1: {name}", "#9ecae1", "#3182bd", "#08519c")
        summary_rows.append({"Dataset": name, **stats})
        safe = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        fig.savefig(output_dir / f"exp1_freq_{safe}.png", dpi=300)
        plt.close(fig)

    fig1, axs1 = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, df) in zip(axs1, [("First 50", first50), ("First 100", first100), (f"All {n_total}", full)]):
        plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Exp1 combined (first subsets): {name}", "#9ecae1", "#3182bd", "#08519c")
    fig1.savefig(output_dir / "exp1_combined_first_subsets_freq.png", dpi=300)
    plt.close(fig1)

    fig2, axs2 = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, df) in zip(axs2, [("Random 50", random50), ("Random 100", random100), (f"All {n_total}", full)]):
        plot_freq_vs_count(ax, df["Count"].to_numpy(), f"Exp1 combined (random subsets): {name}", "#9ecae1", "#3182bd", "#08519c")
    fig2.savefig(output_dir / "exp1_combined_random_subsets_freq.png", dpi=300)
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

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(output_dir / "exp1_summary.csv", index=False)
    print("Experiment 1 outputs saved to:", output_dir)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    run_experiment1(Path("data.xlsx"), Path("outputs"))
