# Quick Ref — Strategy Performance Metrics

Companion to `SKILL.md` §6 "Report Analysis". Covers the nine metrics
introduced in the MQL5 blog *Evaluating Trading Strategy Performance
Metrics* ([post 755078](https://www.mql5.com/en/blogs/post/755078)),
each one anchored to MetaQuotes' own wording in the Strategy Tester
report ([Testing Report help](https://www.metatrader5.com/en/terminal/help/algotrading/testing_report))
rather than to the blog's summary — the blog is a reading aid, not a
specification, and half of its nine explanations are wrong or
misleading (§3).

Five of the nine have **no `TesterStatistics()` ID**: they exist only in
the report HTML, so an optimization cannot rank passes by them unless
you recompute them yourself (§6).

## 1. Metric map

| Metric | MT5 report label | `TesterStatistics()` | `parse_tester_report.py` | Unit |
|---|---|---|---|---|
| Profit Factor | `Profit Factor` | `STAT_PROFIT_FACTOR` | `profit_factor` | ratio |
| Expected Payoff | `Expected Payoff` | `STAT_EXPECTED_PAYOFF` | `expected_payoff` | money / trade |
| Recovery Factor | `Recovery Factor` | `STAT_RECOVERY_FACTOR` | `recovery_factor` | ratio |
| Sharpe Ratio | `Sharpe Ratio` | `STAT_SHARPE_RATIO` | `sharpe_ratio` | ratio (annualized) |
| AHPR | `AHPR` | — report only | `ahpr`, `ahpr_pct` | factor (+ % in brackets) |
| GHPR | `GHPR` | — report only | `ghpr`, `ghpr_pct` | factor (+ % in brackets) |
| LR Correlation | `LR Correlation` | — report only | `lr_correlation` | −1 … 1 |
| LR Standard Error | `LR Standard Error` | — report only | `lr_standard_error` | deposit currency |
| Z-Score | `Z-Score` | — report only | `z_score`, `z_score_pct` | sigma |

The parser reads all nine, but the `report` text output prints only the
first four; the rest are in `--json`. `windows` recomputes only seven
core metrics — Profit, EP, PF, RF, Balance DD Rel %, Trades, SR (plus
`growth` = net profit / starting balance) — see `AGENTS.md` for the
documented N=1 tolerances.

ENUM reference: `references/docs/01-constants/0159-constants-environment-state-statistics.md`.

## 2. Definitions, formulas, how to read

`B_i` = balance after trade `i`; `N` = number of trades;
`HPR_i = B_i / B_{i-1}` (holding-period return factor).

### 2.1 Profit Factor

```
PF = Σ(winning trades) / |Σ(losing trades)|
```

MT5: "ratio of the gross profit to the gross loss. A value of one means
that these parameters are equal." `STAT_GROSS_LOSS = 0` ⇒ PF is
`DBL_MAX` — that means *no losing trade in the sample*, not "infinite
edge". Small `N` produces exactly this.

Reading: `< 1.0` rework the strategy, not the parameters; `1.0–1.5`
fragile (one bad regime erases the edge); `> 1.5` usable;
`> 2.5` go hunting for overfitting before believing it. PF ignores
*where* the gross profit came from — a single outsized win can carry a
losing system.

### 2.2 Expected Payoff

```
EP = net profit / number of trades
```

Money per trade, costs included (commission + swap are already inside
each trade's P&L). Backtest EP is an **upper bound**: live spread
widening, slippage and requotes only subtract. Compare EP against the
per-trade cost of live execution before scaling. `analyze` also emits
`eppl` (EP per lot) so lot-size differences do not masquerade as edge.

### 2.3 Recovery Factor

```
RF = net profit / STAT_BALANCE_DD        (absolute balance DD, money)
```

MT5: "the amount of money risked by the Expert Advisor to make the
profit it obtained… ratio of gained profit to the maximum drawdown".
Both terms are money, so RF is **lot-invariant** — a lot sweep leaves it
bit-identical (used as an invariant in `quick-ref-complex-criterion.md`
§2.2).

Reading: `< 1` the system has not yet earned back its worst peak-to-trough;
`1–3` typical for an acceptable system; `> 5` usually means the drawdown
sample is too benign (short period, no stress regime), not that the
strategy is superb. Note the denominator is *balance* DD — floating
(equity) pain is excluded, so a grid/martingale EA can post a flattering
RF. Check `equity_drawdown_rel_pct` next to it.

### 2.4 Sharpe Ratio

```
per-trade  SR_raw = (AHPR − 1) / std(HPR)          (risk-free = 0)
reported   SR     = SR_raw · sqrt(N / years)
```

MT5 uses a zero risk-free rate and annualizes the per-trade figure by
trade frequency, so the reported number **scales with how often the EA
trades**. The exact internal formula is unpublished and the textbook
reconstruction does not reproduce it on high-frequency systems (repo
measurement: 246753 report 22.92 vs textbook 2.49 — see `AGENTS.md`,
`parse_tester_report.py` `_sharpe_ratio_annualized`).

Reading: do **not** transplant the textbook "SR ≥ 1 is good" threshold —
it is meaningless on MT5's annualized-per-trade number. Compare SR only
between runs with similar trade counts and durations. MT5's own Complex
Criterion model saturates `G_sr` at `SR ≈ 3`
(`quick-ref-complex-criterion.md` §2.1), i.e. the platform's own quality
scoring treats ~3 as the top of the useful band; SR 48 adds nothing.
For shape over time use `windows` `sharpe_ratio_raw` (per-trade), which
is comparable across windows.

### 2.5 AHPR

```
AHPR = mean(HPR_i) = (1/N) · Σ B_i / B_{i-1}
```

MT5: "arithmetic mean of a trade (change in percents)… The arithmetic
mean usually overestimates the profitability of a trading system as
compared to the geometric mean." Reported as a factor with the percent
in brackets; `> 1` = profitable.

### 2.6 GHPR

```
GHPR = (Π HPR_i)^(1/N) = (B_N / B_0)^(1/N)
```

MT5: "geometric mean shows by how many times the capital changed after
each trade in average."

Both AHPR and GHPR are **per closed trade**, never per bar / day /
"holding period" in the time sense. `GHPR ≈ 1.0xx` is normal — `1.5`
would mean *+50 % per trade*, not "+50 % overall" (blog §3 error).

Useful invariants and uses:

- `GHPR > 1` ⟺ net profit > 0 (same information, rescaled per trade) —
  its value is that it normalizes growth by **trade count**, so a 50-trade
  and a 500-trade run become comparable.
- `AHPR − GHPR` is the **variance drag**: a wide gap means high per-trade
  volatility, i.e. the compounding-inefficient case that also inflates
  the Sharpe denominator.
- Both are ratios of consecutive balances, so **withdrawals corrupt
  them** (`STAT_WITHDRAWAL > 0` ⇒ an HPR < 1 that is not a loss).

### 2.7 LR Correlation

Pearson correlation between the balance curve and its least-squares
straight line (over the trade sequence).

MT5: "Correlation between the balance graph and the linear regression
allows to estimate the degree of the capital variability. The less sharp
peaks and troughs on the balance curve, the closer the parameter value
is to 1. Values close to zero mean the random nature of trading."

Reading: `≈ 1` smooth monotone ramp; `≈ 0` noise-dominated; negative
net-declining balance curve. It says **nothing** about trend-following
vs mean-reversion (blog §3 error). Heuristic caution: `> 0.99` on a long
backtest is a *red flag* — real markets do not deliver straight lines,
so a perfectly smooth equity curve usually means curve-fit entries, no
adverse regime in the sample, or a fill model that never hits the hard
cases.

### 2.8 LR Standard Error

```
LR_SE = sqrt( (1/N) · Σ (B_i − B̂_i)² )      in deposit currency
```

MT5: "standard error of balance deviation from the linear regression…
It only makes sense to compare systems with similar initial conditions
(the same values of the initial equity). The higher the value, the more
balance deviates from a straight line."

It is a **dispersion in money**, not a model-accuracy score (blog §3
error). Normalize by initial deposit (`LR_SE / deposit`) before comparing
across tests, and never compare it between different deposits or
different lot sizes.

### 2.9 Z-Score

A **runs/series test on the win-loss sequence**, not a performance score:

```
P = 2 · W · L                       W, L = count of wins, losses
R = number of runs (consecutive win or loss blocks)
Z = (N · (R − 0.5) − P) / sqrt( P · (P − N) / (N − 1) )
```

MT5: "series testing (the probability of correlation between trades)…
The Z score indicates deviation from normal distribution in the sigma. A
value above 3 indicates that a win will be followed by a loss with the
probability of 3 sigma (99.67%). A value below -3 indicates that a win
will be followed by a win with the probability of 3 sigma (99.67%)."

Sign convention (matches the runs test): **negative = clustering**
(wins follow wins, losses follow losses), **positive = alternation**
(wins and losses flip more than chance). `|Z| > 3` ≈ 99.7 % significant.

Reading: strongly negative Z on a grid/martingale EA is the expected
signature of correlated trades — one regime can wipe the account, so
fixed-fractional sizing is mandatory and consecutive-loss limits must be
sized for the streak, not the average. Strongly positive Z means the
sequence alternates more than chance, which is what a fixed
win/loss-taking system looks like. Needs `N ≳ 30` to mean anything.
`z_score_pct` is only the bracketed value MT5 renders next to the sigma
figure (`parse_pct` of the same cell) — not an independent statistic.

## 3. Corrections to blog 755078

| Blog claim | What MT5 actually reports |
|---|---|
| Z-Score "assesses performance relative to historical data… a Z-Score of 2 means performance is two standard deviations above the mean" | Z-Score is a **runs test on the win/loss order** (§2.9). It is not a return statistic and never describes "performance above the mean". |
| LR Correlation "positive correlation suggests a trend-following strategy" | It measures **balance-curve smoothness** (§2.7). A trend-following EA and a mean-reversion EA can both score 0.9. |
| GHPR "1.5 implies 50 % growth over successive holding periods" | GHPR is a **per-trade multiplier**: 1.5 = +50 % *per trade*, which is not a realistic value. Real reports sit at 1.00–1.05. |
| AHPR "average rate of return for each holding period" | Correct only if "holding period" = **one closed trade** (§2.5). It is not per bar, per day, or per time-held. |
| Sharpe "1 or higher suggests a favorable risk-return tradeoff" | MT5's SR is **annualized by trade frequency** and can reach tens on intraday EAs (§2.4). The textbook threshold does not transfer; compare like-for-like runs only. |
| LR Standard Error "assesses the accuracy of the linear regression line in predicting returns" | It is the **money** dispersion of balance around the line, comparable only at equal initial deposit (§2.8). Not a predictive-accuracy metric. |
| Profit Factor, Expected Payoff, Recovery Factor definitions | Consistent with MT5, but the blog omits that RF divides by **absolute balance** DD (money) and that `GrossLoss = 0` makes PF `DBL_MAX`. |

## 4. Reading order

Follow the same order as `SKILL.md` §6 — each step can invalidate the
next one:

| # | Check | Metric | Exposed by |
|---|---|---|---|
| 1 | Data quality | History Quality, modelling mode | `report` |
| 2 | Edge exists | Profit Factor, Expected Payoff | `report`, `windows` |
| 3 | Edge is affordable | Max DD % (balance **and** equity) | `report`, `windows` |
| 4 | Edge repays the pain | Recovery Factor | `report`, `windows` |
| 5 | Edge is consistent | Sharpe, `AHPR − GHPR` drag | `report --json` |
| 6 | Edge is smooth, not fitted | LR Correlation, LR Standard Error | `report --json` |
| 7 | Edge is not one lucky streak | Z-Score, max consecutive wins/losses | `report --json` |
| 8 | Edge survives time slices | per-window PF / RF / SR / DD | `windows --count N` |

A single metric proves nothing: PF 3.0 with RF 0.4, LR corr 0.995 and
Z −5 is a curve-fit system with clustered losses, not a good one.

## 5. Traps

- **Report-only ≠ optimizable.** Z-Score, AHPR, GHPR, LR Correlation and
  LR Standard Error have no `TesterStatistics()` ID, so they cannot be
  an optimization criterion as-is; returning one from `OnTester()`
  collapses the ranking into the single `Custom` / `Result` column and
  the other eight metrics stop driving the search (§6).
- **SR, GHPR, LR_SE are scale- and frequency-sensitive.** A lot sweep
  moves profit, EP and DD (and therefore AHPR/GHPR, which are ratios of
  consecutive balances); measured invariant across a lot sweep: Trades,
  PF, RF, SR, win rate. Longer tests move SR and per-trade GHPR. Never
  compare these across different lot sizes, deposits or trade counts
  without normalizing.
- **Withdrawals poison HPR-based metrics.** `STAT_WITHDRAWAL > 0` makes
  AHPR/GHPR/SR/LR read a withdrawal as a losing trade.
- **Equity vs balance.** RF, LR Correlation, LR Standard Error and the
  balance-curve metrics are computed on the **balance** curve, so floating
  drawdown is invisible to them. Grid/martingale EAs look far better than
  they are; always pair with `equity_drawdown_rel_pct`.
- **`windows` does not recompute these five.** Per-window Z-Score / LR /
  AHPR / GHPR require the trade list; use `report --json` or `analyze`
  and compute them per window if a stability answer is needed.

## 6. Recomputing the report-only five

`TesterStatistics()` cannot supply them, but they are all closed-form on
the trade list — the same formulas in §2.5–2.9. Two paths:

1. **Python (preferred for analysis)** — `report --json` carries the
   full `deals` array with per-deal `profit` and running `balance`;
   compute `HPR_i = balance_i / balance_{i-1}` for AHPR/GHPR/SR, a
   least-squares fit over the balance series for LR Correlation/SE, and
   the runs-test formula for Z-Score. This is the same arithmetic
   `parse_tester_report.py` uses for the window metrics.
2. **`OnTester()` (needed to rank an optimization)** — build the trade
   list from `HistoryDeal*` in the tester, compute the metric, return it.
   That value becomes `STAT_CUSTOM_ONTESTER` / the `Custom` column, so
   only **one** composite is possible per run; if several metrics must
   drive the ranking, combine them inside the EA and document the
   weighting (that is exactly what MT5's own Complex Criterion does —
   see `quick-ref-complex-criterion.md`).

## Sources

- Blog (requested source): *Evaluating Trading Strategy Performance
  Metrics: A Comprehensive Overview* —
  <https://www.mql5.com/en/blogs/post/755078> (2023-11-25).
- Authoritative definitions: MT5 terminal help, *Testing Report* —
  <https://www.metatrader5.com/en/terminal/help/algotrading/testing_report>.
- `ENUM_STATISTICS`: `references/docs/01-constants/0159-constants-environment-state-statistics.md`.
- Repo measurements of the Sharpe divergence and the CC saturation
  points: `AGENTS.md`, `quick-ref-complex-criterion.md` §2.1–2.2,
  `parse_tester_report.py` (`_sharpe_ratio`, `_sharpe_ratio_annualized`).
