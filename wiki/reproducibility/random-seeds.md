# Random Seeds

## What a seed does

A seed initializes the pseudo-random generator. Same seed + same data + same code gives identical sampled subsets.

## Why this project uses fixed seeds

- Reproducible figures and CSVs
- Easier peer review and debugging
- Consistent report regeneration

## Why seeds like `11` and `23`

No physics meaning. They are deterministic IDs used to create repeatable random subsets.
