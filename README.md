# Radioactive Decay Poisson Analyzer

Research-oriented toolkit for testing Poisson behavior of radioactive decay counts using frequency-vs-count analysis.

## What Changed (Major)

- Refactored to `src` package layout.
- Added robust ignore rules for generated output folders.
- Upgraded docs into multi-page `wiki/` folder.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

Menu:

- `1) START`: run full pipeline
- `2) CONFIG`: edit path/mode/output/nano config
- `3) VALIDATE DATA`: check workbook format
- `4) EXIT`

## Structure

- `src/poisson_decay/`: core package code
- `main.py`: root wrapper entrypoint
- `experiment1_poisson_runs.py`: wrapper to run experiment 1
- `experiment2_poisson_runs.py`: wrapper to run experiment 2
- `generate_pdf_report.py`: wrapper to generate report
- `wiki/`: detailed research docs

## Data Format

Excel file should contain:

- `Sheet1`: `Sr. Num`, `Count`
- `Sheet2`: `Sr. No.`, `t=20s`, `t=30s`

Default path is `data.xlsx` (editable via config menu).

## Reproducibility

Runs are deterministic with same config and data because seeds are fixed.

See:

- `wiki/reproducibility/random-seeds.md`
- `wiki/reproducibility/seed-stability.md`

## Documentation

Start from:

- `wiki/README.md`
