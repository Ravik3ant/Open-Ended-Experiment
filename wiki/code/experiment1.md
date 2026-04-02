# Code: `experiment1.py`

## Scientific goal

At fixed counting time (`t=10s`), test how estimates behave with changing sample size.

## Data paths through code

1. Read `Sheet1` columns `Sr. Num`, `Count`.
2. Build subsets:
   - first 50
   - first 100
   - random 50 (without replacement)
   - random 100 (without replacement)
   - full set
3. For each subset:
   - compute stats
   - compute observed vs expected frequencies
   - plot with `sqrt(n)` error bars
4. Export summary CSV and images.

## Robustness extensions

- Multi-seed random summary across many seeds.
- Seed-stability report with pass-fraction logic for Fano and chi2/dof.
