# Signals Analysis Reference — metric cheat sheet & red-flag taxonomy

Companion to `skills/mql-signals/SKILL.md`. This document explains how to read
every metric on an mql5.com signal detail page, how to mine the reviews, and
how to interpret the CSV forensics output. Built and verified on signal 2271402
("Deux ex machina", Victor Gomez Sanchez, 2021–2026, 1,860 exported deals).

## 1. Metric reading order (detail page)

Populate the table left-to-right; every row has one sentence of interpretation.

| Metric | What to record | What it tells you |
|---|---|---|
| Growth % | + initial deposit | The % is meaningless without the base. 747% on a 50 USD deposit = 374 USD absolute. 6,361% on 477 EUR (with 40K EUR in/out flows) is a different animal. Always restate as absolute profit. |
| Deposits / Withdrawals | sums, net | Provider pools equity: deposits in, profits/principal out. Net deposit >> 0 with no withdrawals = equity-masking risk. |
| Equity vs Balance | both | Balance-DD is insurer-like; Equity-DD (floating) is what really happens. Report both. |
| Profit Trades % | % | Very high (95%+) with losses concentrated is a tail-risk profile, not a good sign. 70–80% is normal for a real system. |
| Trading activity % | % of days traded | >50% = nearly always in the market (scalper); <30% = selective (swing). Not a quality metric by itself, but matches the author's claims. |
| Max deposit load | % | >30% = position size can reach dangerous levels; 98% = all-in bet. |
| Maximum drawdown (gauge) | % | Rough guide; the CSV gives the precise by-balance/by-equity split. |
| Sharpe Ratio | value | <0.2 = weak risk-adjusted return; 0.2–0.4 = mediocre; >0.5 rare on signals. Do not trust a "great growth" signal with Sharpe 0.09. |
| Profit Factor | value | Gross profit / gross loss. 1.8–2.5 is typical and fine. |
| Recovery Factor | value | Net / max drawdown. 4–15 plausible band; >16 with low DD = mostly stable months. |
| Expected Payoff | value | Mean net per trade including costs (the CSV confirms). |
| Average Profit / Average Loss | both | Loss > Win (e.g. −16.7 vs +11.0) requires a high win rate; with the consecutive-loss run from the CSV you can simulate survivability. |
| Monthly growth / Annual Forecast | % | Annual forecast is a mechanical extrapolation. Monthly growth is the honest number; discount it by episodes. |
| Max deposit load / drawdown split | both | Cross-check by-balance vs by-equity for hidden floating stress. |
| Slippage table | median × copies | Prefer brokers whose pool is large AND median slippage low. A 2.9-pip pool with 7,800 copies is the reality of copying; a 0.0-pip pool with 1 copy is noise. |

## 2. MQL5 system warnings ("What's new") — read them literally

The platform runs its own risk engine on every signal account. These warnings
are the most objective evidence on the page:

| Warning | Meaning | Severity |
|---|---|---|
| "80% of growth achieved within N days. This comprises X% of days of the signal's entire lifetime" | Growth burst concentration. Repeated occurrence = the track record misleads (it is a few lucky stretches). | **High** — strongest overclaim signal; saw it 3x on one signal each time a burst happened. |
| "Too much growth in the last month indicates a high risk" | Same engine, monthly view. | **High** |
| "Share of growth for 80% ... too low" / "Share of trading days is too low" | Account inactive most of the time. | Medium |
| "No trading activity detected for the last 6 days" / "Low trading activity - only N trades" | Inactivity episodes — maintenance loans, or a dead signal. Compare to "Latest trade: X ago". | Medium |
| "Too frequent deals may negatively impact copying results" | Timing pressure on subscriber accounts (pending-order races). | Medium (copy quality) |
| "Signal account leverage was changed ... 1:500 - 1:2000" | Leverage hikes to 1:2000+ = account-blender signature. | **High** |
| "No swaps are charged" | Provider account is swap-free; subscriber swap cost is hidden from the stats. | Medium |

## 3. Review mining

Glob the last 30 reviews and file them into buckets:

- **Copy failures** ("not copied", "mapping didn't work", "no trades copied"):
  check `Slippage` table and the author's broker for suitability; these users
  usually mismatched deposit/lot or broker family.
- **Deposit/lot mismatch**: "lead trader on 5,000 USD uses 0.01 min lot, my
  1,000 USD account never copied" — a real mechanism, not a review artifact:
  ask if the user's account is ≥ the lead account size.
- **Strategy drift** ("changed strategy without notice", "pairs changed"):
  verify with the CSV per-year profile (see §4). This one complaint matched a
  documented Feb-2025 pivot on 2271402.
- **Holding/死扛** ("no SL", "draining my account", "死扛会爆仓"):
  verify with the holding-pattern section of the CSV output.
- **Duplicate strategy** ("95% of trades same as signal X"): the same EA
  multiplied across several paid signals — a red flag for honesty, not
  performance.
- **Long-term testimonies**: a subscriber who stayed 1–2+ years writing a
  balanced review ("held through the 2025 Trump-tariff drawdowns without
  blowing up") is the highest-value evidence class on the page.

## 4. CSV forensics — how the output reads

Run: `python skills/mql-signals/scripts/analyze_signals_csv.py <file>.csv`

Output contract (all monetary values EUR/USD/JPY as exported):

1. **summary** — deals, span, gross pnl (excl. costs), commission, swap, net
   (= page profit, verified within 0.2 on the reference signal),
   win/loss, best/worst.
2. **reconciliation** — with `--page-*`: hidden trades (page vs file) and
   profit delta. Expect ±15 trades and <1.00 currency units; larger deltas
   mean the export was truncated/censored.
3. **funding ops** — sum of Deposit / Withdrawal / Balance rows:
   - `Balance -1343.06` = silent debits/credits below deposit granularity —
     combine with the page's deposits/withdrawals for the equity-masking check.
4. **by_year** — n / avg_lot / median_holding / sum_lot / net:
   - Sudden change in any of the first four by >3x = **strategy shift year**.
     The reference signal: 2025 n 128→891, lot 0.21→0.31, holding 2→0 days,
     sum_lot 26→278, net +1847→−561 — a completely different strategy that
     happened to be the only losing year.
5. **by_symbol** — profit core vs experiments: 2271402 makes everything from
   AUDCAD/NZDCAD/AUDNZD; US30/DE40/XAUUSD are net-negative additions.
6. **by_month** — the loss months; on 2271402 exactly 2025-03/04/05.
7. **tail** — worst-k sums, worst-1% share of total losses (>25% = heavy tail),
   losers/winners totals.
8. **max_consecutive_losses** — chronological streak; the reference signal shows 8-9, consistent with "win small, lose in streaks".
9. **holding** — net of trades held ≥ N days. Negative net with losses >> wins
   is the dead-hang signature (on 2271402: 201 deals, +1001 wins vs −2645
   losses held). This is the quantitative form of the 死扛 complaint.
10. **recent** — last N days by close date: current regime check.

## 5. Verdict rules

- Tier **Verified sound** requires: multi-year record, zero "80% growth"
  warnings, stable monthly curve, no dead-hang signature, transparent funding,
  currently active.
- Tier **Conditional** fits systems with a clean core + one documented bad
  episode caused by a strategy experiment. Advice: size copy down, set a
  subscriber-side drawdown stop, re-check the per-symbol table monthly for
  new experiment symbols.
- Tier **Reject** on any of: burst-growth warnings, no-SL/TP grid strategy,
  leverage 1:2000+, net-deposit equity masking, mass copy-failure complaints.

Subscription economics: `fee <= balance * monthly_growth_pct / 100`.
Monthly growth 1.17% + 30 USD fee ⇒ break-even at ≈ 2,600 EUR. Always state
the break-even deposit; it is the single most useful number for the user.

## 6. Worked example (2271402 — Deux ex machina)

Full public numbers for reference and for testing the analyzer:

| Field | Value |
|---|---|
| Price / broker / leverage | 30 EUR/mo, ICMarketsSC-MT5, 1:500, 99% algo |
| History | 280 weeks since 2021, current container since 2024-11-15 |
| Funding | initial 477.65 EUR; deposits 19,565.61 / withdrawals 21,386.32 |
| Page stats | 1,875 trades (73.9% win), net +7,120.51, best +218 / worst −138 |
| CSV (1,860 deals) | gross +8,152.30, comm −636.11, swap −395.52 → net +7,120.67 |
| Per-year net | 2021 +439, 2022 +1,297, 2023 +3,783, 2024 +2,067, **2025 −561**, 2026 +694 |
| Per-symbol net | AUDCAD +4,415 · NZDCAD +2,787 · AUDNZD +1,341 · US30 −895 · DE40 −478 · XAUUSD −93 |
| Tail | worst 5 = −673; worst 1% = 25.4% of all losses |
| Holding ≥5d | 201 deals, +1,001 wins / −2,645 losses = dead-hang signature |
| Flags | 2025 strategy shift (n 128→891, holding 2d→0d), activity spike 26→278 lots |

Lesson: the "2025 survived the crashes" marketing is true but inverted — 2025
was a strategy experiment that produced the only loss year, exclusively from
DE40/US30 index positions; the AUD/NZD/CAD core never lost money in any year.
The dead-hang pattern and the Feb-2025 strategy pivot, both flagged in
reviews, are visible and quantifiable in the CSV alone.