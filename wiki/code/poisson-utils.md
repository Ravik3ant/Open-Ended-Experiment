# Code: `poisson_utils.py`

## Purpose

Shared statistical and configuration primitives used across all modules.

## Functions

- `load_config(path)`
  - Loads JSON config.
- `select_mode(config, mode)`
  - Chooses `scientific` or `clean` settings.
- `poisson_pmf(k, lam)`
  - Computes Poisson PMF with log-gamma numerical stabilization.
- `basic_stats(counts, include_relative_error=False)`
  - Mean, variance, SD, SEM, Fano, optional relative error.
- `observed_expected(counts)`
  - Returns histogram support `k`, observed frequencies, expected Poisson frequencies.
- `chi2_hist(observed, expected)`
  - Histogram chi-square and reduced chi-square with low-expected-bin filtering.

## Numerical notes

- PMF uses `lgamma(k+1)` instead of factorial to avoid overflow.
- Chi-square ignores bins with expected `< 1` to avoid unstable weighting.
