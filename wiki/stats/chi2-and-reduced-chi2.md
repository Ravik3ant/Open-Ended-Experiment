# Chi-square and Reduced Chi-square

## Definitions

- Observed bin count: `O_k`
- Expected Poisson bin count: `E_k`

Chi-square statistic:

`chi2 = sum((O_k - E_k)^2 / E_k)`

Reduced chi-square:

`chi2_reduced = chi2 / dof`

where `dof` is approximate degrees of freedom.

## Why filter low expected bins

When `E_k` is too small, `((O_k-E_k)^2/E_k)` becomes unstable and can dominate unfairly. The implementation filters bins with `E_k < 1`.

## Interpretation

- Around `1`: model and data are broadly consistent
- Much larger than `1`: poor fit or underestimated uncertainties
- Much smaller than `1`: overestimated uncertainties or over-smoothed data

## Caveat

Reduced chi-square is a diagnostic, not an absolute proof by itself. Use together with SD vs `sqrt(mu)`, Fano, and visual histogram agreement.
