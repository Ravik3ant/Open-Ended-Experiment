# Project Structure

The project follows a `src` layout to separate application code from root-level scripts and data.

## Top-level

- `main.py`: CLI entry wrapper.
- `experiment1_poisson_runs.py`: wrapper to run experiment 1 directly.
- `experiment2_poisson_runs.py`: wrapper to run experiment 2 directly.
- `generate_pdf_report.py`: wrapper to generate report directly.
- `config.json`: runtime configuration.
- `requirements.txt`: dependency list.
- `wiki/`: detailed docs.
- `src/`: core package code.

## Package (`src/poisson_decay`)

- `cli.py`: rich terminal interface.
- `poisson_utils.py`: statistics and Poisson math utilities.
- `data_validation.py`: Excel workbook checks.
- `experiment1.py`: subset-size experiment pipeline.
- `experiment2.py`: time-window experiment pipeline.
- `report.py`: PDF generation.

## Why `src` layout

- Prevents accidental import of wrong local files.
- Improves long-term maintainability for large research codebases.
- Makes package boundaries explicit.
