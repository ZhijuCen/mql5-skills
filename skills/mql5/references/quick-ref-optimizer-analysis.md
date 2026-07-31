# Quick Ref — Optimization Report Analysis (Details)

Companion to `SKILL.md` §6 "Optimization Report Analysis". This file
contains the deeper details (full sort table, `failures` example
output, `outliers` sigma guidance, parameter effect ranges) that did
not fit in the 500-line SKILL.md budget.

## Scripts entry points

```
python scripts/parse_optimizer_report.py SUB_COMMAND REPORT.xml [OPTS] [-o OUT]

SUB_COMMANDS:
  report     env card + parameter cardinalities + orthogonality
  analyze    parameter effect, duplicates, best passes, trade distribution
  outliers   per-pass z-score scan (8 perf metrics)
  failures   per-parameter value distribution over deployable failures
```

`--json` switches to JSON. `-o FILE` writes the report to a file.
Always confirm the environment card from the first lines of `report`
before drawing any conclusion about a specific pass.

## 1. Strategy environment card

`<DocumentProperties>` encodes the strategy environment on one line
in `Title`: `<EA> <SYMBOL>,<PERIOD> <YYYY.MM.DD>-<YYYY.MM.DD>`,
plus `Deposit`, `Leverage`, `Server`, MT5 `Version`/`Build`, and run
timestamp. Confirm before evaluating any pass:

- EA / Symbol / Period / Date range match the spec
- Deposit × Leverage match the broker account class
- Server is the intended broker (demo vs live, broker name)
- MT5 build is current (5.00 / build 5000+ as of 2025)
- Date range covers the regime you want to test (≥ 1 year for swing,
  ≥ 3 years for trend)

A date range shorter than the strategy's intended holding period
structurally biases the optimization.

## 2. Orthogonality check

Compare `orthogonality.actual` vs `orthogonality.expected_cartesian`
(product of parameter cardinalities). Mismatch means the Strategy
Tester skipped passes (e.g. due to errors) — the table is incomplete
and per-parameter means will be biased. Re-run with longer timeout
or fix the EA so every pass completes.

## 3. Dead parameter detection

Two patterns, in order of signal strength:

- `parameter_effect[X].dead_param == true` — per-group mean Profit
  range is < 1% of the maximum group mean. Parameter is not doing
  anything; remove it from optimization to halve the search space.
- `dead_boolean_params[X]` — all metrics (Profit, PF, RF, Trades)
  are bit-for-bit identical between `true` and `false` groups. The
  cleanest dead-parameter signal: the parameter is either never read
  in the EA, or it toggles a code path that never triggers on this
  backtest (common when `if(InpUseNewsFilter)` cannot load news —
  wrong calendar URL, demo server, off-hours).

## 4. Duplicate metric vectors

`duplicates.groups_with_dupes` counts rows with identical metric
vectors (Profit, PF, RF, Trades, ...). A high count (>30% of total)
almost always points to a dead parameter — duplicated rows differ
only in the dead parameter's value. Example: 432 passes with a
binary dead parameter collapse to 216 unique metric vectors,
producing 216 duplicate pairs.

## 5. Best-pass selection — multiple criteria

The script reports top-5 by four criteria. They usually agree on
the top few but diverge on the tail. Read them together:

| Criterion         | Favors                          | Watch out                                  |
|-------------------|---------------------------------|--------------------------------------------|
| **Profit**        | Total return                    | Can hide low win rate with lucky runs     |
| **Profit Factor** | Edge per unit of risk           | Trade-count blind (low n)                  |
| **Recovery Factor** | Return per unit of max DD     | Inflated by small DD, not big wins         |
| **Custom**        | Whatever `OnTester()` returns   | If OnTester only counts profit, equivalent to Profit |

For a robust pick, find the pass that appears in **multiple top-5
lists AND has Trades count near the median** (statistical
significance). A pass with 161 trades near the min is barely
significant; 175 is the most reliable signal on the example run.

## 6. Parameter effect ranking

`parameter_effect` orders parameters by `effect_ratio_spread_over_std`
(= spread between best and worst group means, divided by the global
Profit std):

- `> 1.0` — dominant driver; focus tuning here
- `0.3 ≤ ratio ≤ 1.0` — meaningful but secondary
- `< 0.3` — weak; many values perform similarly

Combined with the per-group means, the gradient direction tells
you where to widen or narrow the search range. Beware
counterintuitive results (e.g. tighter SL winning on mean Profit) —
they often mean SL is rarely hit and the "edge" is just trade-count
noise.

## 7. Trade-count distribution (overtrading detection)

Watch `trades.deciles` and `trades.corr_trades_vs_*`:

- `corr_trades_vs_profit < -0.3` — more trades → less profit.
  Strategy degrades as it scales; common with mean-reversion or
  re-entry on loss.
- `corr_trades_vs_equity_dd > 0.3` — more trades → more drawdown.
  Overtuning costs both ways.
- `trades_per_day_median` — convert the trade count to a rate
  against the backtest days. < 0.1/day for H4 = fine, > 1/day on
  H4 = scalper regime (spread-sensitive).

The trade-count RANGE itself is diagnostic. Range of 14 (161-175)
on 432 passes means parameters only changed entry/exit timing
slightly, not the core signal. Range of 50+ means a parameter is
blocking trades entirely.

## 8. Optimization reporting template

When reporting optimization results, include:

1. Environment card (EA, symbol, period, date range, deposit, server)
2. Pass count vs expected cartesian (orthogonality status)
3. Dead parameters (if any) — these are bugs to fix, not "remove from
   optimization" wins
4. Top-3 passes by Profit, with their full parameter vector
5. Top-3 by Recovery Factor (more important than raw profit for live
   trading)
6. Trade count distribution (median, range, correlation with profit)
7. Per-parameter gradient (which direction to push next iteration)
8. Recommended next pass (extend ranges if any edge is the optimum)

Skip the "best PF" and "best recovery factor" sections only when they
identify the same pass as "best profit" — otherwise the disagreement
is the most interesting finding (regime-specific trade-off).

## 9. Per-pass outlier scan

The `outliers` subcommand does a per-metric z-score scan over the 8
performance metrics (Result, Profit, Expected Payoff, Profit Factor,
Recovery Factor, Sharpe Ratio, Custom, Equity DD %). Trades is
explicitly excluded from the metric scan and used only as an
exclusion filter.

### Direction conventions

- **Higher-is-better** (Result, Profit, Expected Payoff, Profit
  Factor, Recovery Factor, Sharpe Ratio, Custom): outlier = `z >= +σ`
- **Lower-is-better** (Equity DD %): outlier = `z <= -σ`

### Sort priority (`--sort`)

Default (abbreviation form):

```
R↓, EP↓, PF↓, RF↓, SR↓, P↓, DD↑, C↓, T↓
```

| Code | Full metric     | Direction |
|------|-----------------|-----------|
| R    | Result          | ↓ (desc)  |
| P    | Profit          | ↓ (desc)  |
| EP   | Expected Payoff | ↓ (desc)  |
| PF   | Profit Factor   | ↓ (desc)  |
| RF   | Recovery Factor | ↓ (desc)  |
| SR   | Sharpe Ratio    | ↓ (desc)  |
| C    | Custom          | ↓ (desc)  |
| DD   | Equity DD %     | ↑ (asc)   |
| T    | Trades          | ↓ (desc)  |

`DD↑` sorts ascending (lower drawdown first). Supply a
comma-separated list of abbreviations to reorder — e.g. `--sort
EP,RF,R,P` puts Expected Payoff first, with the remaining metrics
appended in default positional order.

### Two disjoint sets

- **Set A** — passes with at least one perf-metric outlier (top N by
  Result). Candidates for closer inspection: a pass posting `z > +2`
  on Profit *and* `z > +2` on Sharpe together is genuinely
  exceptional; `z > +2` on Profit alone with everything else flat is
  more likely small-sample variance.
- **Set B** — passes with no perf-metric outlier (top M by Result).
  Next-tier passes — strong but unremarkable relative to the rest
  of the run.

Low-Trades passes (`Trades z <= -σ`) are dropped before either set
is built and shown separately.

### Sigma choice

σ=2.0 is the default. For runs with hundreds of passes that's
strict enough to be useful (~5% of values expected to clear it under
a normal distribution, concentrated at the extremes). Drop to σ=1.5
for runs with <100 passes if Set A is empty; σ=3.0 only for runs with
>1000 passes.

## 10. Failure-set analysis

`outliers` answers *"which individual passes are statistical
extremes?"*; `failures` answers *"which parameter values concentrate
in the deployable failures?"* — passes satisfying at least one of 6
absolute (run-independent) criteria:

```
Profit           < 0      (the EA bled money on the run)
Profit Factor    < 1.0    (gross loss ≥ gross profit)
Expected Payoff  < 0.1    (avg trade outcome is negligible)
Equity DD %      > 60.0   (drawdown exceeded 60% of equity)
Recovery Factor  < 1      (net profit does not cover max DD — fragile)
Sharpe Ratio     < 1.0    (per-trade returns aren't distinguishable from noise)
```

Thresholds are intentionally NOT z-scored: a pass satisfying every
criterion is deployment-grade on absolute terms, not only relative
to this run.

### Reading the output

```
Passes total:     432
Passes failing:   420  (97.22% of total)
Passes passing:    12

Criteria table (any one fires ⇒ failing):
  Profit < 0.0                            14   3.24%
  Profit Factor < 1.0                     14   3.24%
  Expected Payoff < 0.1                   16   3.70%
  Equity DD % > 60.0                       0   0.00%   ← not triggered
  Recovery Factor < 1                     420  97.22%   ← DOMINANT driver
  Sharpe Ratio < 1.0                      18   4.17%
```

The criterion that fires most often is the run's **release blocker**.
In the example above, RF<1 fires on 97% of passes — the optimization
grid is dominated by an RF<1 ground, and tuning within it won't
produce a deployable EA. Either widen the parameter search range
(tighter SLs, asymmetric risk) or change the underlying EA logic.

### Per-parameter value distribution

For each input parameter column the script tabulates the **count and
percentage of failing passes** holding each value (share of the
failure set) plus `pct_of_global` (share of all passes with that
value that ended up failing):

```
Parameter: InpRiskPercent (5 distinct values in failure set)
  value  count  pct_of_failures  global_count  pct_of_global
   1       10         2.4%            18        55.6%
   2       18         4.3%            50        36.0%
   3       80        19.0%            80       100.0%   ← smoking gun
```

`pct_of_global` concentration signals:

- > 50% on a single value → almost every pass with that setting
  fails. Smoking gun — drop the value from the optimization grid
  (it never works) or treat it as a fundamental EA bug.
- 0–30% → value is roughly as good/bad as average; sampling noise.
- All values clustered at similar % → parameter is not the
  differentiator; look elsewhere.

### When to use `failures` vs `outliers`

- `outliers` ranks **extreme passes** — useful for hundreds-of-passes
  runs when you want to know which ~10 deserve hand inspection.
- `failures` ranks **parameter values** — useful for pruning the
  optimization grid (drop values with high `pct_of_global`) or for
  structural diagnosis (one criterion dominating).

Both views are complementary: check `failures` first for systematic
issues (RiskPercent axis, dominant criterion), then `outliers` to
inspect specific passes inside the surviving parameter region.

## 11. Generic column typing (EA-agnostic by design)

`parse_optimizer_report.py` does not hardcode input-parameter names:

- **Type inference** comes from the SpreadsheetML header: a body
  cell with `<Data ss:Type="String">` stays as a string column
  (boolean Inp* rendered as `"true"`/`"false"`); numeric cells
  become `float64` (or `Int64` when every value is whole).
- **Input-parameter detection** uses column position, not name
  prefix: `Trades` is the last fixed column; every column after it
  is an optimization input regardless of whether its name starts
  with `Inp`. So an EA naming parameters `StopLoss`, `TakeProfit`,
  `UseNewsFilter` parses correctly without script changes.
