# Pipeline Overview

## End-to-end flow

1. Read `config.json`.
2. Validate input workbook format.
3. Run Experiment 1 (subset-size study).
4. Run Experiment 2 (time-window study).
5. Build consolidated PDF report.

## Experiment 1 outputs

- Individual frequency-vs-count plots
- Combined subset figures
- `exp1_summary.csv`
- `exp1_random_multiseed_raw.csv`
- `exp1_random_multiseed_avg.csv`
- `exp1_seed_stability_summary.csv`
- `exp1_seed_stability_report.md`

## Experiment 2 outputs

- Individual frequency-vs-count plots
- Combined time-window figure
- `exp2_summary.csv`

## Report outputs

- `poisson_report.pdf`
