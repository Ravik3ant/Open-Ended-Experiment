# Radioactive Decay Poisson Analyzer

Menu-driven Python project to test whether radioactive decay counts follow a Poisson distribution.

## Quick Start

```bash
python -m pip install -r requirements.txt
python main.py
```

Then use:

- `1. START` to run all analyses and report generation
- `2. CONFIG` to set data file path or open `config.json` in `nano`

## Project Structure

- `main.py`: interactive CLI (`START`, `CONFIG`, `EXIT`)
- `config.json`: controls colors, mode, shown metrics, paths, seeds
- `poisson_utils.py`: shared math/config utilities
- `experiment1_poisson_runs.py`: Experiment 1 pipeline
- `experiment2_poisson_runs.py`: Experiment 2 pipeline
- `generate_pdf_report.py`: creates final PDF report
- `wiki.md`: detailed explanation of code snippets, formulas, and significance

## Experiments

- **Experiment 1** (fixed `t=10s`, varying subset size)
  - first 50, first 100, random 50, random 100, all rows

- **Experiment 2** (fixed `N=50`, varying time)
  - `t=10s`, `t=20s`, `t=30s`

All plots are frequency vs count, with Poisson expected frequency overlay.

## Data Format

Input workbook should have:

- `Sheet1`: `Sr. Num`, `Count`
- `Sheet2`: `Sr. No.`, `t=20s`, `t=30s`

Default input file is `data.xlsx` (editable in `config.json` or CLI config menu).

## Reproducibility

Running twice with same data and same config gives the same outputs.

Reason: random subsets use fixed seeds from `config.json`.

If you change seeds, random-subset outputs will change.
