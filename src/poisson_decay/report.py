from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from .poisson_utils import load_config, select_mode


def add_text_page(pdf: PdfPages, title: str, lines: list[str]):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("white")
    fig.text(0.06, 0.965, title, fontsize=16, fontweight="bold")
    y = 0.93
    for line in lines:
        if line == "":
            y -= 0.012
        else:
            fig.text(0.06, y, line, fontsize=10)
            y -= 0.018
        if y < 0.05:
            pdf.savefig(fig)
            plt.close(fig)
            fig = plt.figure(figsize=(8.27, 11.69))
            fig.patch.set_facecolor("white")
            y = 0.95
    pdf.savefig(fig)
    plt.close(fig)


def add_image_page(pdf: PdfPages, title: str, image_path: Path, caption: str):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("white")
    fig.text(0.06, 0.965, title, fontsize=14, fontweight="bold")
    img = plt.imread(image_path)
    ax = fig.add_axes([0.08, 0.16, 0.84, 0.74])
    ax.imshow(img)
    ax.axis("off")
    fig.text(0.08, 0.11, caption, fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)


def summary_lines(df: pd.DataFrame, cols: list[str], label_col: str = "Dataset") -> list[str]:
    lines = []
    for _, row in df.iterrows():
        parts = [f"{c}={row[c]:.4f}" if isinstance(row[c], float) else f"{c}={row[c]}" for c in cols if c in df.columns]
        lines.append(f"- {row[label_col]}: " + ", ".join(parts))
    return lines


def _metric_explanations(level: str) -> list[str]:
    common = [
        "- Mean (mu): average count; estimates Poisson lambda.",
        "- SD: measured spread of counts.",
        "- Poisson SD sqrt(mu): ideal Poisson spread.",
        "- Fano = variance/mean: near 1 indicates Poisson-like behavior.",
        "- chi2/dof: agreement between observed and expected Poisson frequencies.",
    ]
    if level == "summary":
        return common
    return common + [
        "- Variance s^2 = (1/(N-1)) * sum((x_i-mu)^2).",
        "- SEM = SD/sqrt(N): uncertainty in mean estimate.",
        "- Relative error scale 1/sqrt(mu): fractional counting uncertainty.",
        "- chi2 = sum((O_k-E_k)^2/E_k), reduced chi2 = chi2/dof.",
    ]


def build_report(config_path: Path = Path("config.json"), mode: str | None = None):
    cfg = load_config(config_path)
    mode_cfg = select_mode(cfg, mode)
    out = Path(cfg["defaults"]["output_dir"])

    exp1 = pd.read_csv(out / "exp1_summary.csv")
    exp2 = pd.read_csv(out / "exp2_summary.csv")
    exp1_avg = pd.read_csv(out / "exp1_random_multiseed_avg.csv")

    if mode_cfg["report_level"] == "summary":
        exp1_cols = ["N", "Mean", "Sample_SD", "Chi2_per_DOF_hist"]
        exp2_cols = ["N", "Mean", "Sample_SD", "Chi2_per_DOF_hist"]
    else:
        exp1_cols = ["N", "Mean", "Sample_SD", "Poisson_SD_sqrt_mean", "Fano_var_over_mean", "Chi2_per_DOF_hist"]
        exp2_cols = [
            "N",
            "Mean",
            "Sample_SD",
            "Poisson_SD_sqrt_mean",
            "Relative_error_1_over_sqrt_mean",
            "Fano_var_over_mean",
            "Chi2_per_DOF_hist",
        ]

    pdf_path = out / "poisson_report.pdf"
    with PdfPages(pdf_path) as pdf:
        add_text_page(
            pdf,
            f"Poisson Analysis Report ({cfg['defaults']['mode'] if mode is None else mode})",
            [
                "Objective: verify radioactive decay counts follow Poisson statistics.",
                "Approach: frequency-vs-count histograms with Poisson expected curve and sqrt(n) error bars.",
                "",
                "Experiment 1: first 50/100, random 50/100, and full set.",
                "Experiment 2: t=10s, t=20s, t=30s at fixed N=50.",
                "",
                "Meaning of metrics:",
                *_metric_explanations(mode_cfg["report_level"]),
            ],
        )

        add_image_page(pdf, "Experiment 1 (First subsets)", out / "exp1_combined_first_subsets_freq.png", "Observed bars vs Poisson expected line.")
        add_image_page(pdf, "Experiment 1 (Random subsets)", out / "exp1_combined_random_subsets_freq.png", "Random subsets are sampled without replacement.")
        add_text_page(
            pdf,
            "Experiment 1 Summary",
            [
                "Main dataset summaries:",
                *summary_lines(exp1, exp1_cols),
                "",
                "Random-subset multi-seed averages:",
                *summary_lines(exp1_avg.rename(columns={"N_random_avg": "SubsetSize"}), ["SubsetSize", "Mean", "Sample_SD", "Chi2_per_DOF_hist"], label_col="SubsetSize"),
            ],
        )

        add_image_page(pdf, "Experiment 2 (Time windows)", out / "exp2_combined_times_freq.png", "Fixed N=50, increasing time window raises mean counts.")
        add_text_page(
            pdf,
            "Experiment 2 Summary",
            [
                *summary_lines(exp2, exp2_cols),
                "",
                "Interpretation:",
                "- Mean count rises from 10s to 20s to 30s.",
                "- Relative error scale decreases with larger counting time.",
                "- This matches expected Poisson counting-statistics behavior.",
            ],
        )

    print(pdf_path)
