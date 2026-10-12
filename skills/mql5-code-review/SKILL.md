---
name: mql5-code-review
description: >
  Static code review skill for MQL5 Expert Advisors (and Indicators,
  Scripts, Services). Reviews source WITHOUT running it: trading-logic
  correctness, risk formulas, indicator / multi-timeframe semantics,
  tick-level performance, tester-vs-live parity, state-persistence
  failure modes, numeric precision, diagnosability, chart-GUI/UX, and
  readability. Ships a regex red-flag scanner (mql5_redflags.py) plus
  report / checklist templates. Use when: reviewing MQL5 EA source,
  pre-deploy audits, finding failure modes and inefficiencies before
  spending time on backtests, reviewing third-party or article code,
  mentoring, establishing review standards for MQL5 code.
license: MIT
compatibility: >
  Target: MQL5 source (*.mq5, *.mqh). Analysis is static only — no
  execution, no compilation required (optional compile cross-check via
  ../mql5 skill's mql5_helper.py). Scanner is Python 3 stdlib-only.
metadata:
  version: "0.1"
  focus-areas:
    - trading-logic
    - risk-formulas
    - failure-modes
    - performance
    - gui-ux
    - readability
---

# MQL5 Code Review Skill

Find what a backtest will NOT tell you — by reading the source. This skill
reviews MQL5 EA code **statically**: failure modes that are rare or
account-state-dependent, inefficiencies that only hurt after weeks of
live run, silent numeric errors, and diagnosability gaps that make the
real incident untraceable. Runtime validation (backtests, optimization,
deal-level debugging) is the domain of the `mql5` skill — use this
skill first to shrink the search space before you burn tester time.

## 1. Purpose and Scope

**In scope** (static analysis of source):
- Correctness of trading logic, risk formulas, indicator/MTF semantics
- Failure modes: restart, weekend gaps, broker differences, event races
- Inefficiency: per-tick hot path, object churn, string/array growth
- Diagnosability: silent failures, log context, input validation
- GUI/UX: panel overflow, anchoring, update throttling, cleanup
- Readability: naming (vs `../mql5/references/quick-ref-code-style.md`),
  dead code, magic numbers, structure

**Out of scope** (hand off, do not do here):
- Running backtests / optimizations / report analysis → `mql5` skill
  (`mql5_helper.py tester`, `parse_tester_report.py`)
- Compiling as the primary verification → optional cross-check only
  (`mql5` skill's `mql5_helper.py check`)
- Live trading, signal monitoring → `mql-signals` skill

## 2. Review Mindset

**Goals**: catch failure modes before they cost money; share the "why"
behind each finding; leave the code more understandable.

**Not the goals**: showing off, blocking on style alone (label style as
🟢), rewriting to personal preference, reviewing what linters/compile
warnings already catch (report only the aggregate).

**Feedback rules**:
- Specific and actionable: name the file:line, the failure scenario, the fix
- Focused on the code, not the author — third-party/article code gets the
  same treatment as own code, but state assumptions explicitly
- Balanced: list strengths too (see report template)
- Prioritized: 🔴 blocking findings first, always with a concrete failure
  scenario ("what happens when…")

## 3. Severity Labels

| Label | Meaning | Action |
|-------|---------|--------|
| 🔴 `[blocking]` | Will fail, loses money, or is untraceable in a realistic scenario | Must fix before live |
| 🟡 `[important]` | Degraded behaviour / portability / diagnosability gap | Should fix, discuss if disagree |
| 🟢 `[nit]` | Readability, style, minor cleanup | Non-blocking |
| 💡 `[suggestion]` | Alternative approach worth considering | Optional |
| 📚 `[learning]` | Educational note, no action needed | — |
| 🎉 `[praise]` | Genuinely good pattern — say so | — |

A backtest that already passes does NOT downgrade a 🔴: the failure may
be exactly the state the backtest did not reach (restart, gap, stop-out,
broker change). See `references/failure-modes.md`.

## 4. Review Process (4 Phases)

### Phase 1 — Context (2–3 min)

Answer before reading code:

1. **Program type** — EA (`OnTick`)? This skill assumes EA; adapt for
   Indicator/Script/Service.
2. **Origin** — own EA / third-party / mql5.com article / signal vendor?
   For third-party code, assume no documentation: document your
   assumptions in the report.
3. **Account & symbols** — hedging or netting? single- or multi-symbol?
   Account currency vs symbol profit currency?
4. **State model** — what must survive an EA restart (position tracking,
   counters, pending-order state machine)?
5. **GUI** — does it draw panels/objects? Which notifications (Alert /
   push / e-mail) does it emit?
6. **Size triage** — >400 changed lines: review in slices (per file or
   per subsystem); do not skim.

### Phase 2 — High-Level (5–10 min)

1. **Architecture**: class split consistent with the project convention
   (`C`+PascalCase classes, `m_` members — baseline:
   `../mql5/references/quick-ref-code-style.md`)? Signal generation /
   risk sizing / execution / reporting separated, or a 2000-line OnTick?
2. **Risk model**: which of the three formulas (A: points→SL, B: risk%+lots→SL,
   C: risk%+SL→lots) — and is it applied consistently?
   `../mql5/SKILL.md` §5.
3. **Event model**: new-bar gate in OnTick? Timer? Reentrancy guard for
   trade functions shared by OnTick/OnTimer/OnTradeTransaction?
4. **Restart model**: is there a re-adoption path
   (`PositionsTotal()` + magic scan) or does state start from zero?
5. **GUI update model**: change-driven vs per-tick, timer-driven display?
   → `references/gui-ux-review.md`.

### Phase 3 — Line-by-Line (10–30 min)

Work through the dimension table in §6, one dimension at a time. Run
the scanner (§5) first and fold its findings in — but never copy them
blindly: the scanner is regex-level, it produces both false positives
(needs human dismissal) and false negatives (needs human eyes).

### Phase 4 — Summary and Verdict (2–3 min)

1. Group findings by severity; every 🔴 gets a concrete failure scenario.
2. List strengths.
3. Verdict: ✅ Approve / 💬 Comment / 🔄 Request Changes (any 🔴 ⇒ 🔄).
4. Copy into `assets/review-report-template.md` and deliver.

## 5. Automated Pre-Scan — mql5_redflags.py

Stdlib-only static scanner. Run it first, then review each finding
humanly:

```
python skills/mql5-code-review/scripts/mql5_redflags.py scan FILE.mq5 [MORE.mq5 ...]
python skills/mql5-code-review/scripts/mql5_redflags.py scan DIR/ --json -o findings.json
python skills/mql5-code-review/scripts/mql5_redflags.py --list-rules
```

Scanning a single `.mq5` automatically follows its **quoted**
`#include "..."` directives recursively — the whole project-local
module tree is covered without enumerating files. Built-in/stdlib
includes (`#include <...>`) are never followed; `--no-includes`
restricts the scan to exactly the paths given. Unresolved quoted
includes are noted on stderr so coverage gaps stay visible.

Exit code: 0 = no 🔴 findings, 1 = at least one 🔴, 2 = usage/IO error.

| Rule | Sev | Detects |
|------|-----|---------|
| no-retcode-check | 🔴/🟡 | `CTrade` order call: return discarded → 🔴; bool-conditioned/assigned but no `ResultRetcode` within 24 lines → 🟡 (CTrade bool true = communicated, not accepted) |
| object-cleanup-missing | 🔴 | Object create/set present but no `OnDeinit` cleanup |
| objects-delete-all-noprefix | 🔴 | `ObjectsDeleteAll()` full-chart wipe (no prefix / empty prefix) |
| notify-no-throttle | 🔴 | `Alert`/`SendNotification`/`SendMail` in OnTick with no bar/signal guard |
| trade-in-oninit | 🔴 | Order/position call inside `OnInit` |
| sleep-in-event | 🟡 | `Sleep()` inside OnTick/OnTimer (blocks the terminal event thread) |
| print-flood | 🟡 | `Print`/`PrintFormat` in OnTick (journal flood → real incidents drown) |
| object-create-in-ontick | 🟡 | create/delete objects per tick (should be create-once, update) |
| chartredraw-in-ontick | 🟡 | `ChartRedraw()` per tick (batch + single redraw instead) |
| discarded-copy-return | 🟡 | `Copy*` called as a statement — return value (count/-1) dropped |
| handle-release-missing | 🟡 | Indicator handles created, no `IndicatorRelease` anywhere |
| ontick-no-newbar-guard | 🟡 | Trade calls in OnTick but no new-bar gate — full logic every tick |
| fileopen-no-check | 🟡 | `FileOpen` without `INVALID_HANDLE` check |
| webrequest-usage | 🟢 | `WebRequest` — whitelist + 4014 handling reminder |
| dll-import | 🟢 | `#import "….dll"` — permission/security review reminder |
| hardcoded-symbol | 🟢 | Symbol-name literal (XAUUSD/EURUSD/…) instead of `_Symbol`/param |
| double-equality | 🟢 | `==` on price-like variables (float comparison; sentinel-zero and enum-constant comparisons exempted) |
| todo-fixme | 🟢 | TODO/FIXME/XXX/HACK left in source |
| commented-code | 🟢 | ≥3 consecutive commented-out code lines (dead code) |

Scanner output is **evidence, not conclusions**: dismiss false positives
in the report with one line of reasoning; every kept finding still needs
the human failure-scenario write-up. Rules are calibrated against real
EA reviews (an 11-finding run adjudicated to 5 true positives);
re-calibrate thresholds when a run yields systematic false positives
rather than weakening the human review.

## 6. Review Dimensions

| # | Dimension | Key checks | Reference |
|---|-----------|------------|-----------|
| 1 | Trading logic & order flow | retcode checks, magic isolation, hedging/netting branches, filling mode, partial close, SL/TP modify, pending-order lifecycle | `references/trading-logic-review.md` |
| 2 | Risk & money management | 3 formulas, profit-currency conversion, lot quantization, stops level, `OrderCalcProfit` verification | `references/trading-logic-review.md` §5 |
| 3 | Indicators & multi-TF | handle lifecycle, `CopyBuffer` checks, series order, `prev_calculated`, MTF bar alignment, repaint | `references/indicator-review.md` |
| 4 | Time & bars | new-bar detection, timezone/DST mixing, weekend gaps, session boundaries | `references/failure-modes.md` §B |
| 5 | State & failure modes | restart survival, reentrancy, order/position races, long-run resource growth | `references/failure-modes.md` |
| 6 | Numeric precision | `==` on doubles, NaN/Inf, division by zero, first-tick zero prices, `NormalizeDouble` placement | `references/diagnostics-and-numeric.md` §G |
| 7 | Diagnosability | silent failure paths, log context, OnInit fail-fast validation, swallowed returns | `references/diagnostics-and-numeric.md` §F |
| 8 | Performance | OnTick hot path, repeated series copies, per-tick loops, string/array churn, object churn | `references/performance-review.md` |
| 9 | Tester↔live parity | `MQL_TESTER` branches, no-internet assumption, randomness, spread/slippage modelling, look-ahead | `references/tester-live-parity.md` |
| 10 | GUI/UX | panel overflow, anchoring, theme portability, update throttling, notification throttling, cleanup | `references/gui-ux-review.md` |
| 11 | Security & permissions | DLL imports, WebRequest whitelist, file-path boundaries, config parsing robustness | `references/diagnostics-and-numeric.md` §H |
| 12 | Readability & style | naming per code-style baseline, dead code, magic numbers, function size, copy-paste, comment quality | `references/common-bugs-checklist.md` |

## 7. Tooling Integration

The `mql5` skill (same repo) provides verification tooling — invoke it,
do not reimplement:

| Need | Tool |
|------|------|
| Style baseline (naming, class structure) | `../mql5/references/quick-ref-code-style.md` |
| Correct patterns (CTrade setup, risk helpers) | `../mql5/assets/templates/ea-skeleton.mq5`, `risk-helpers.mqh` |
| Syntax-only compile cross-check | `../mql5/scripts/mql5_helper.py check FILE.mq5` |
| SL/TP formula verification vs real symbol spec | `../mql5/scripts/verify_sl_tp_formulas.py verify [SYMBOL …]` |
| Pitfall catalog (the "why" behind many rules) | `../mql5/SKILL.md` §8 |

When a finding's fix touches risk formulas, hand the fixed formula to
`verify_sl_tp_formulas.py` before calling it done.

## 8. Assets

- `assets/review-checklist.md` — quick per-dimension checklist
  (lightweight pass; the full 4-phase process is §4)
- `assets/review-report-template.md` — copy-fill report with severity
  sections, dimension summary, scanner summary, copy-paste finding blocks

## 9. References

- `references/common-bugs-checklist.md` — high-frequency MQL5 bug
  patterns + readability/style checklist (dimension 12)
- `references/trading-logic-review.md` — order flow, risk formulas,
  money management (dimensions 1–2)
- `references/indicator-review.md` — handles, buffers, MTF, repaint
  (dimension 3)
- `references/failure-modes.md` — restart, time/session, broker
  portability, event races, long-run leaks (dimensions 4–5)
- `references/diagnostics-and-numeric.md` — diagnosability, numeric
  precision, security boundaries (dimensions 6–7, 11)
- `references/performance-review.md` — tick-level hot path (dimension 8)
- `references/tester-live-parity.md` — what backtests silently lie
  about (dimension 9)
- `references/gui-ux-review.md` — panels, objects, notifications,
  throttling (dimension 10)
