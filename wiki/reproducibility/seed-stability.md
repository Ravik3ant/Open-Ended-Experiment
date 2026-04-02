# Seed Stability Method

## Goal

Check whether conclusions depend too much on one random subset draw.

## Inputs

- Random subsets for multiple seeds
- Metrics per seed: mean, Fano, chi2/dof

## Stability rules used in code

For each subset size:

- Fano pass fraction: proportion with `Fano in [0.8, 1.2]`
- Chi-square pass fraction: proportion with `chi2/dof in [0.5, 1.5]`
- Mean CV percent: `std(mean)/mean * 100`

Stable if all hold:

- Fano pass fraction >= 0.70
- Chi-square pass fraction >= 0.70
- Mean CV percent <= 5

## Outputs

- `exp1_seed_stability_summary.csv`
- `exp1_seed_stability_report.md`
