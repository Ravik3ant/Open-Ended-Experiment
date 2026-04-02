# Code: `experiment2.py`

## Scientific goal

At fixed sample count (`N=50`), test how statistics change with counting time.

## Data paths through code

1. Read `Sheet1` and `Sheet2`.
2. Build datasets for:
   - `t=10s`
   - `t=20s`
   - `t=30s`
3. For each dataset:
   - compute stats (including relative error scale)
   - compute histogram vs Poisson expectation
   - render plot and save CSV

## Expected outcome

- Mean counts increase with time window.
- Relative error scale `1/sqrt(mean)` decreases.
