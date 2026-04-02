# Radioactive Decay Poisson Analysis

This project checks whether radioactive decay counting data follows a Poisson distribution.

The analysis is split into two experiments:

- **Experiment 1 (fixed time, varying sample size)**
  - Uses `t = 10 s` data from `Sheet1`
  - Compares: first 50, first 100, random 50, random 100, and full set
  - Goal: show statistical estimates become more stable as sample size grows

- **Experiment 2 (fixed sample size, varying counting time)**
  - Uses `N = 50` for each time window: `t = 10 s`, `20 s`, `30 s`
  - Goal: show relative counting uncertainty decreases as counting time increases

All primary plots are **frequency vs count** (histogram style), which is the correct way to test Poisson behavior.

## Data File Format

Put `data.xlsx` in the project root.

Expected sheets/columns:

- `Sheet1`: `Sr. Num`, `Count`
- `Sheet2`: `Sr. No.`, `t=20s`, `t=30s`

## Files and What They Do

- `poisson_utils.py`
  - Shared helper functions used by both experiments
  - Computes Poisson PMF, statistics, expected histogram, chi-square, and plotting function

- `experiment1_poisson_runs.py`
  - Runs Experiment 1
  - Generates individual and combined plots
  - Creates `exp1_summary.csv`
  - Creates multi-seed random subset summaries:
    - `exp1_random_multiseed_raw.csv`
    - `exp1_random_multiseed_avg.csv`

- `experiment2_poisson_runs.py`
  - Runs Experiment 2
  - Generates individual and combined plots
  - Creates `exp2_summary.csv`

- `generate_pdf_report.py`
  - Builds `outputs/poisson_report.pdf` with:
    - experiment objective
    - metric explanations
    - combined plots
    - summary tables and interpretation

- `requirements.txt`
  - Python dependencies

## Installation

```bash
python -m pip install -r requirements.txt
```

## How to Run

```bash
python experiment1_poisson_runs.py
python experiment2_poisson_runs.py
python generate_pdf_report.py
```

Outputs are written to `outputs/`.

## Meaning of Parameters

Let measured counts be `x_1, x_2, ..., x_N`.

- **Mean (`mu`)**
  - Formula: `mu = (1/N) * sum(x_i)`
  - Meaning: best estimate of Poisson parameter `lambda`

- **Variance (`s^2`)**
  - Formula: `s^2 = (1/(N-1)) * sum((x_i - mu)^2)`
  - Meaning: spread of measured counts

- **Sample SD (`s`)**
  - Formula: `s = sqrt(s^2)`
  - Meaning: observed absolute fluctuations

- **Poisson SD (`sqrt(mu)`)**
  - Formula: `sigma_P = sqrt(mu)`
  - Meaning: theoretical Poisson fluctuation scale
  - Check: if `s` is close to `sqrt(mu)`, data is Poisson-like

- **SEM (Standard Error of Mean)**
  - Formula: `SEM = s / sqrt(N)`
  - Meaning: uncertainty in the estimated mean
  - As `N` increases, SEM usually decreases

- **Relative error scale (`1/sqrt(mu)`)**
  - Formula: `1/sqrt(mu)`
  - Meaning: approximate fractional counting uncertainty
  - As count level (or counting time) increases, this decreases

- **Fano Factor (`F`)**
  - Formula: `F = variance / mean`
  - Interpretation:
    - `F ~ 1`: Poisson-like
    - `F > 1`: over-dispersion (extra fluctuations)
    - `F < 1`: under-dispersion

- **Chi-square and reduced chi-square (`chi2/dof`)**
  - Bin-wise formula: `chi2 = sum((O_k - E_k)^2 / E_k)`
    - `O_k` = observed frequency in bin `k`
    - `E_k` = expected Poisson frequency in bin `k`
  - Reduced chi-square: `chi2/dof`
  - Interpretation (rule of thumb): values near `1` indicate reasonable agreement

## Notes

- Random subsets are sampled **without replacement** (no repeats inside one subset).
- If a histogram bar has zero height, it means that count value did not occur in that sample.
- Empty bins are intentionally shown for a complete frequency-vs-count view.
