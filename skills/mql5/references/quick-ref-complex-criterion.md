# Quick Ref — MT5 "Complex Criterion" (`OptimizationCriterion=7`)

Companion to `SKILL.md` §6. Covers the Strategy Tester criterion
**"Complex Criterion max"**, its reverse-engineered formula, the
`complex_criterion.py` script, and the accuracy limits.

## 1. What it is

`[Tester] OptimizationCriterion=7` in the tester INI selects
**Complex Criterion max** (build 2615+, 2020-09). It is a single
**0…100** quality score per pass that MetaQuotes exposes as:

| Where | How |
|---|---|
| Optimization results table | `Result` column (`<Cell><Data>…`) |
| `ReportOptimizer-*.xml` | the `Result` column of the pass row |
| MQL5 code | `TesterStatistics(STAT_COMPLEX_CRITERION)` (build 3800+) |
| Genetic optimizer | the ranking criterion when `=7` is selected |

Cell colouring in the results table always follows this score, even when
another criterion is selected for display: **< 20 red**, **> 80 dark
green**. Range is `0…100`; the observed maximum over 9 970 real passes is
`99.97`.

MetaQuotes publishes only the *input list* (news 2160 / 5242 / 5245):

> Number of Deals, Drawdown, Recovery Factor, Expected Payoff, Sharpe Ratio
> … the complex criterion gradually selects the best passes: firstly, by the
> number of deals, then by the Expected Payoff, Recovery Factor, and so on.

The formula itself is **not documented**. Everything below was recovered
experimentally (see §5) and must be treated as a *model*, not as
MetaQuotes source.

## 2. Formula

With `σ(x) = 1 / (1 + e^-x)` (logistic), `T` = `STAT_TRADES`,
`DD` = `STAT_EQUITY_DDREL_PERCENT` (Equity Drawdown Relative, %):

```
cc = 100 · σ((T − 40) / 5) · Q

Q  = 0.2 · σ((20 − DD) / 2.5) + Qo

Qo = 0.0335
   + G_rf(RF)            # RF = STAT_RECOVERY_FACTOR
   + G_sr(SR)            # SR = STAT_SHARPE_RATIO
   + G_pf(PF)            # PF = STAT_PROFIT_FACTOR
   + G_wr(WR)            # WR = profit trades / (profit + loss trades)
```

`G_*` are **monotone saturating tables** (piecewise linear, flat outside
their knot range) calibrated against MT5. They are listed verbatim in
`scripts/complex_criterion.py` (`TABLES`). Their shapes:

| Component | Saturates at | Span (min → max) | Reading |
|---|---|---|---|
| `G_rf` | RF ≈ 4 | 0 → 0.219 | return per unit of *balance* drawdown |
| `G_sr` | SR ≈ 3 | 0 → 0.141 | per-trade consistency |
| `G_pf` | PF ≈ 2.5 | 0 → 0.381 | edge per unit of risk |
| `G_wr` | WR ≈ 0.60 | 0 → 0.170 | hit rate |

`Qo` therefore lives in ≈ `0.03…0.94` and `Q` in ≈ `0.03…1.14`; the
practical ceiling is `Q ≈ 1.00` → `cc = 99.97`. The script clamps the
result at `100.0` (a perfect pass can push the four quality tables
marginally above 1.0).

### 2.1 The trades factor is exact

`σ((T − 40) / 5)` reproduces MT5 to the last displayed digit. Proof
pattern used: take, for every trade count `T`, the **best** pass (the
passes whose quality components are all saturated) — those all collapse
onto one 2-decimal value that is `100 · σ((T−40)/5)`:

| T | 8 | 10 | 12 | 15 | 20 | 25 | 30 | 40 | 50 | 60 | 80 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| observed max | 0.17 | 0.25 | 0.37 | 0.67 | 1.80 | 4.74 | 11.92 | 49.99 | 88.06 | 98.18 | 99.94 |
| `100σ((T−40)/5)` | 0.165 | 0.247 | 0.371 | 0.669 | 1.799 | 4.743 | 11.920 | 50.000 | 88.080 | 98.201 | 99.967 |

Consequences: fewer than ~30 trades ⇒ score < 12 whatever the quality;
more than ~80 trades ⇒ the factor is saturated (no reward for more
trades, no penalty either). This is the "firstly, by the number of
deals" half of the MetaQuotes sentence.

#### Trade-count ↔ score ceiling (saturated quality)

| T | 10 | 20 | 25 | 30 | **33** | 35 | 40 | 45 | **47** | 50 | 60 | 70 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cc` ceiling | 0.25 | 1.80 | 4.74 | 11.92 | **19.78** | 26.89 | 50.00 | 73.11 | **80.22** | 88.08 | 98.20 | 99.75 |

Reading: **20 points (the red/green boundary) is crossed at `T ≈ 33`**,
**80 points (dark green) at `T ≈ 47`**, 50 points exactly at `T = 40`.
Verified against real data — `optim-0001` holds 745 passes with
`Trades < 50` whose `Result` peaks at **85.78** (T = 49), and a controlled
probe run produced `STAT_COMPLEX_CRITERION = 71.88101` at `T = 45`
(PF 2.09, RF 2.54, SR 48.0, equity DD 0.15 %).

**Common misreading to avoid:** "Trades < 50 ⇒ score ≤ 20" is *false* —
the `T = 50` row already reaches 88. What *is* true is that below
`T ≈ 33` the trades factor alone caps the score under 20, so such passes
are effectively disqualified regardless of quality.

### 2.2 The drawdown factor is exact

`0.2 · σ((20 − DD) / 2.5)` with **equity** relative drawdown. Isolated by
a *lot-sweep* experiment: running one parameter set at several lots
scales `profit`, `EP` and `DD%` while leaving `T`, `PF`, `RF`, `SR` and
the win rate **bit-identical**. Along such a sweep

```
cc / (100 · σ_T) − Qo  =  0.2 · σ((20 − DD) / 2.5)
```

holds to ~1e-5, and the DD-dependent increment at low drawdown is
`0.2000` in every sweep. A grid search over the three constants returns
`A = 0.200`, `ref = 20.00`, `scale = 2.50` — round numbers, on the
**equity** curve (balance drawdown fits worse: RMSE 0.0129 vs 0.0124).
Half-way point at 20 % equity DD; ±2.5 % moves the factor between 0.12
and 0.88, so DD is the sharpest single lever in the formula.

### 2.3 The composite part is calibrated

`Qo` is the sum of four saturating quality components. Established facts:

* **Additive, not multiplicative.** `Qo` is bounded (`≈0.03…0.94`) and a
  bad pass still scores ≈ 0.04, not 0 — a product of per-metric factors
  would go to zero.
* **Lot-invariant inputs only.** Inside a lot sweep `Qo` is constant to
  1e-5 while `EP` moves 50×; therefore *expected payoff*, *net profit*
  and *absolute drawdown* are **not** components (the news text is
  imprecise here).
* **Four components.** `Qo` reaches 0.80 for a pass with
  `RF > 6, SR > 20, PF > 3.5` and no further increase beyond — i.e.
  4 × 0.2.
* **Which four.** A greedy additive search over every available
  `ENUM_STATISTICS` value (and derived ratios) selects exactly
  `RF, SR, PF, WR`; adding any other statistic raises R² by < 0.002.
* **Not recoverable exactly.** The four tables are fitted; their exact
  closed form is still unknown (§4).

## 3. Using the script

```sh
# single-test HTML report → one number (uses the win/loss trade split)
uv run python scripts/complex_criterion.py report ReportTester-1234567.html

# optimizer XML → per-pass table (only the 8 statistics the XML carries)
uv run python scripts/complex_criterion.py xml ReportOptimizer-50083774.xml --limit 20

# optimizer XML → accuracy report of the model vs MT5's own Result column
uv run python scripts/complex_criterion.py validate ReportOptimizer-50083774.xml

# any sub-command: --json / -o FILE
uv run python scripts/complex_criterion.py validate ReportOptimizer-50083774.xml --json -o acc.json
```

`report` imports `parse_tester_report.py` from the same directory for the
HTML parsing. Values are printed with **2 decimals, rounded** (MT5's own
display precision).

## 4. Accuracy (measured, not claimed)

| Validation set | n | median \|Δ\| | p90 | p99 | max |
|---|---|---|---|---|---|
| Single-test / full statistics (controlled probe grid, §5) | 8 640 | **0.21** | 0.76 | 2.56 | 3.63 |
| `optim-0001/ReportOptimizer-50083774.xml` (no win rate) | 9 970 | **0.77** | 4.61 | 9.67 | 13.3 |

Reproduce with `complex_criterion.py validate`.

Cumulative distribution (full statistics, 8 640 passes):

| \|Δ\| ≤ | 0.05 | 0.10 | 0.50 | 1.00 | 2.00 |
|---|---|---|---|---|---|
| share of passes | 8.2 % | 16.4 % | 85.5 % | 92.4 % | 97.5 % |

**So 2-decimal agreement is NOT achieved** for the composite part: only
~1 % of passes round to the same 2-decimal value as MT5. The trades
factor and the drawdown factor *are* exact, so the residual error is
entirely in the four calibrated quality tables (§2.3) — the part whose
closed form is still unknown.

If a 2-decimal-exact value is required, do not model it: read
`STAT_COMPLEX_CRITERION` from MT5 itself with the probe EA (§5.3).

Why the optimizer-XML number is worse: an optimizer export carries only
`Profit, EP, PF, RF, SR, Equity DD %, Trades` — **no win/loss trade
counts** — so the `G_wr` component cannot be evaluated and the script falls
back to its calibrated average (`WR_SATURATED`). A single-test HTML report
*does* carry `Profit Trades` / `Loss Trades`, and is ~4× closer.

Parsing adds its own error: the HTML report rounds `PF`/`RF`/`SR` and
`DD%` to 2 dp, worth ≈ 0.01–0.05 points on the result.

Known blind spot: the calibrated tables sum slightly above the true
ceiling for a *fully* saturated pass, so the model clamps at `100.00`
while MT5 stops at `99.97` (≈ 14 % of the 9 970 passes land in that
region) and loses drawdown sensitivity there. Lowering the intercept to
remove the overshoot costs far more accuracy elsewhere (median error
0.77 → 1.2 points), so the clamp is kept.

## 5. How this was established (repeatable)

### 5.1 Probe EA — exact per-pass values

`assets/tester/complex-criterion-probe.mq5` trades a parameterised
schedule (entry period, lot, TP, SL, hold bars, direction) and writes one
CSV line per pass from `OnTester()` with **all** `ENUM_STATISTICS` values
plus `STAT_COMPLEX_CRITERION` at full precision:

```
MQL5/Experts/CCProbe.ex5  ->  <data dir>/Tester/Agent-*/MQL5/Files/ccprobe.csv
```

Notes learned the hard way:

* `Print()` from `OnTester()` is **suppressed during optimization** — write
  a file instead (`FILE_COMMON` also failed silently here; the plain
  agent-local path works, one CSV per `Tester/Agent-*/MQL5/Files`).
* `STAT_COMPLEX_CRITERION` **is** available in a single test (build 6230),
  at full double precision — this is the ground truth for any calibration.
* Orders need an explicit `request.type_filling` from
  `SymbolInfoInteger(SYMBOL_FILLING_MODE)`, otherwise every trade fails
  with `[Unsupported filling mode]` and the pass has `T == 0`.
* MetaEditor `/compile:` fails when the path contains a space — compile in
  a space-free directory and copy the `.ex5` into `MQL5/Experts`.
* A 3 000-pass Grid over a 2.3-month M15 range completes in ~40 s, so the
  whole calibration set costs a few minutes.

### 5.2 Lot-sweep design (the key trick)

Hold every parameter fixed and vary **only** `InpLot`. Because MT5
computes statistics per trade, this scales `profit`, `EP`, `DD` and `DD%`
by the lot while `T`, `PF`, `RF`, `SR`, win rate and the win/loss sequence
stay identical. Each sweep therefore yields a clean one-dimensional cut
through `cc` — enough to isolate the drawdown factor exactly and to prove
which statistics do **not** enter.

### 5.3 Getting the exact value from MT5

1. Copy `assets/tester/complex-criterion-probe.mq5` into
   `MQL5/Experts/`, compile, deploy.
2. Run any single test (`mql5_helper.py tester INI`).
3. Read `STAT_COMPLEX_CRITERION` from
   `<instance>/Tester/Agent-*/MQL5/Files/ccprobe.csv` (column `cc`, 10 dp).
   The probe only writes the file — `Print()` is dropped because it is
   suppressed during optimization.

To re-calibrate after a MetaQuotes change, regenerate a Grid with the
probe and refit the four tables (§2.3) — the fitting procedure is a ridge
solve over piecewise-linear hat bases plus a monotonicity projection.

## 6. Practical notes

* The criterion is **lot-invariant** except through `DD%`: doubling the
  lot leaves `RF`, `SR`, `PF`, `WR`, `T` untouched and only pushes `DD`
  right, i.e. it *punishes* leverage — that is the intended behaviour.
* `T < 40` dominates everything (σ is ≈ 0.02 at T = 20). Do not compare
  passes with wildly different trade counts on this criterion.
* Colour thresholds (< 20 / > 80) line up with `T ≈ 33` / `T ≈ 47` for a
  saturated-quality pass.
* Because `EP` and `profit` are ignored, a high-profit / low-win-rate pass
  and a low-profit / high-win-rate pass with the same `PF`, `RF`, `SR`,
  `DD` and `T` score the same. Use `parse_optimizer_report.py` alongside
  this criterion, never instead of it.
