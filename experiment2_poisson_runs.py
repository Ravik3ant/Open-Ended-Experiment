from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from poisson_utils import plot_freq_vs_count


def run_experiment2(excel_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

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

    rows = []
    for name, counts in datasets.items():
        fig, ax = plt.subplots(figsize=(10.8, 4.8), constrained_layout=True)
        stats = plot_freq_vs_count(
            ax,
            counts,
            f"Experiment 2: {name}",
            bar_color="#c7e9c0",
            edge_color="#238b45",
            err_color="#006d2c",
            show_relative_error=True,
        )
        rows.append({"Dataset": name, **stats})
        safe = name.lower().replace(" ", "_").replace("=", "").replace(",", "")
        fig.savefig(output_dir / f"exp2_freq_{safe}.png", dpi=300)
        plt.close(fig)

    fig, axs = plt.subplots(3, 1, figsize=(11, 13), constrained_layout=True)
    for ax, (name, counts) in zip(axs, datasets.items()):
        plot_freq_vs_count(
            ax,
            counts,
            f"Exp2 combined: {name}",
            bar_color="#c7e9c0",
            edge_color="#238b45",
            err_color="#006d2c",
            show_relative_error=True,
        )
    fig.savefig(output_dir / "exp2_combined_times_freq.png", dpi=300)
    plt.close(fig)

    summary = pd.DataFrame(rows)
    summary.to_csv(output_dir / "exp2_summary.csv", index=False)
    print("Experiment 2 outputs saved to:", output_dir)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    run_experiment2(Path("data.xlsx"), Path("outputs"))
