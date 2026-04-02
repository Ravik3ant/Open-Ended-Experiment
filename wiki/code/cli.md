# Code: `cli.py`

## Responsibilities

- Menu rendering with `rich`
- Running full analysis pipeline
- Config editing actions
- Data validation command

## Key functions

- `main()`: main menu loop (`START`, `CONFIG`, `VALIDATE DATA`, `EXIT`).
- `start_pipeline()`: validates input, runs both experiments, builds report.
- `config_menu()`: edit data path, output path, mode, or open `nano`.
- `show_current_config()`: table view of active config values.

## Why it matters

- Ensures operator-friendly workflow.
- Reduces errors by validating before expensive runs.
