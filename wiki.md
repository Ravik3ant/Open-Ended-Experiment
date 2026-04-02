# Project Wiki: Code, Metrics, and Significance

## 1) Code Walkthrough (What Each Snippet Does)

### `poisson_utils.py`

- `load_config(...)`
  - Reads `config.json`.
  - Centralizes defaults like data path, mode, colors, and display options.

- `select_mode(config, mode)`
  - Picks mode-specific behavior (`scientific` or `clean`).
  - Controls which stats appear on plots and report detail level.

- `poisson_pmf(k, lam)`
  - Computes Poisson probability `P(X=k)` for each integer `k`.
  - Uses log form with `lgamma` to stay numerically stable.

- `basic_stats(counts, include_relative_error=False)`
  - Computes core metrics from raw counts.
  - Returns dictionary used for plot annotations and CSV outputs.

- `observed_expected(counts)`
  - Builds observed histogram (frequency per count value).
  - Builds expected frequencies from Poisson model: `N * P(X=k)`.

- `chi2_hist(observed, expected)`
  - Calculates histogram chi-square goodness-of-fit.
  - Filters bins where expected count is too small (`E < 1`) to avoid unstable chi-square terms.

### `experiment1_poisson_runs.py`

- Reads `Sheet1`.
- Creates subsets:
  - first 50
  - first 100
  - random 50 (without replacement)
  - random 100 (without replacement)
  - all rows
- Plots each dataset as frequency vs count and writes:
  - per-plot PNGs
  - combined first-subset figure
  - combined random-subset figure
  - summary CSV
  - multi-seed random robustness CSVs

### `experiment2_poisson_runs.py`

- Reads `Sheet1` and `Sheet2`.
- Builds three `N=50` datasets:
  - `t=10s` from `Sheet1`
  - `t=20s` from `Sheet2`
  - `t=30s` from `Sheet2`
- Plots frequency vs count for each and combined.
- Writes summary CSV.

### `generate_pdf_report.py`

- Reads experiment CSV summaries and generated images.
- Creates `outputs/poisson_report.pdf`.
- In `scientific` mode: detailed metric explanations and richer tables.
- In `clean` mode: concise explanations and fewer shown metrics.

### `config.json`

- Controls:
  - default data path
  - output folder
  - visual mode (`scientific` / `clean`)
  - seeds for random sampling
  - colors
  - which metrics appear in plot stats box
  - report detail level

## 2) Parameter Definitions, Derivations, and Importance

Let observed counts be `x_1, x_2, ..., x_N`.

- **Mean (`mu`)**
  - Derivation: arithmetic average.
  - Formula: `mu = (1/N) * sum(x_i)`.
  - Importance: Poisson parameter estimate (`lambda`).

- **Variance (`s^2`)**
  - Derivation: average squared deviation from mean (sample-corrected).
  - Formula: `s^2 = (1/(N-1)) * sum((x_i - mu)^2)`.
  - Importance: quantifies fluctuation power.

- **Sample Standard Deviation (`s`)**
  - Derivation: square-root of variance.
  - Formula: `s = sqrt(s^2)`.
  - Importance: fluctuation scale in same units as counts.

- **Poisson SD (`sqrt(mu)`)**
  - Derivation (Poisson property): `Var(X)=E[X]=mu`, so `SD=sqrt(mu)`.
  - Importance: benchmark to compare with measured SD.

- **SEM (Standard Error of Mean)**
  - Derivation: spread of sampling distribution of mean.
  - Formula: `SEM = s / sqrt(N)`.
  - Importance: precision of estimated mean; shrinks as `N` increases.

- **Relative error scale (`1/sqrt(mu)`)**
  - Derivation: `SD/mean` for Poisson is `sqrt(mu)/mu = 1/sqrt(mu)`.
  - Importance: fractional counting uncertainty; reduces as counts rise.

- **Fano factor (`F`)**
  - Derivation: normalized variance.
  - Formula: `F = variance / mean`.
  - Importance:
    - `F ~ 1` Poisson-like
    - `F > 1` over-dispersion (extra noise/drift)
    - `F < 1` under-dispersion

- **Chi-square (`chi2`) and reduced chi-square (`chi2/dof`)**
  - Derivation: weighted squared residual between observed and expected histogram bins.
  - Formula:
    - `chi2 = sum((O_k - E_k)^2 / E_k)`
    - `reduced = chi2 / dof`
  - Importance: goodness-of-fit score for Poisson model.
  - Typical interpretation: near 1 indicates reasonable fit.

## 3) Why Running Twice May or May Not Change Results

- With the current setup, random subsets use fixed seeds from `config.json`.
- So, running twice with same data + same config gives identical outputs.
- If you change seeds or use a non-fixed random generator, random subset outputs will differ.

## 4) Scientific vs Clean Mode

- **scientific**
  - more metrics on plots
  - detailed report text and formulas
  - colorful plot palette

- **clean**
  - fewer metrics on plots
  - shorter report text
  - grayscale-like simple palette

Switch mode in `config.json` under `defaults.mode`.

## 5) CLI Behavior

Use `main.py` for menu-driven flow:

- `START`
  - runs Experiment 1 + Experiment 2 + PDF report using current config.

- `CONFIG`
  - set data file path from CLI input.
  - open `config.json` in nano for manual editing.
