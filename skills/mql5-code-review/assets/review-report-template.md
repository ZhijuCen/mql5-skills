# MQL5 Code Review Report

Copy-fill template. English by convention. One report per review
session; attach the scanner JSON/text output as an appendix.

---

## Summary

[1–2 sentences: what was reviewed and the overall assessment.]

| Field | Value |
|-------|-------|
| Files reviewed | [file list + line counts] |
| Program type | [EA / Indicator / Script / Service] |
| Origin | [own / third-party / article / signal vendor] |
| Account mode | [hedging / netting] |
| Scanner run | [`mql5_redflags.py scan …` — N findings (X 🔴, Y 🟡, Z 🟢)] |
| Verdict | [ ] ✅ Approve  [ ] 💬 Comment  [ ] 🔄 Request Changes |

## Strengths

- [Genuinely good patterns — name them specifically]

## Blocking Findings (🔴)

### 🔴 B1 — [Title]

**Location:** `file.mq5:123`
**Dimension:** [trading-logic / risk / indicators / failure-modes /
numeric / performance / gui-ux / security / readability]

[The failure scenario: when does it fail, what happens, what does it
cost. One concrete scenario per finding — "position opens twice after
a terminal restart because …"]

**Suggested fix:**
```mql5
// minimal patch sketch or the pattern to follow
```

### 🔴 B2 — [Title]

…

## Important Findings (🟡)

### 🟡 I1 — [Title]

**Location:** `file.mqh:45`
**Dimension:** […]
[Degraded behaviour and why it matters]

**Consider:**
- Option A: [description]
- Option B: [description]

## Nits (🟢)

- 🟢 [file:line] [Suggestion] — not blocking.

## Suggestions (💡)

- 💡 [Alternative approach worth considering]

## Learning Notes (📚)

- 📚 [Educational context shared for the author, no action needed]

## Praise (🎉)

- 🎉 [Specific good work]

## Dimension Summary

| Dimension | Status | Key note |
|-----------|--------|----------|
| Trading logic & order flow | [✅/⚠️/❌] | […] |
| Risk & money management | [✅/⚠️/❌] | […] |
| Indicators & multi-TF | [✅/⚠️/❌] | […] |
| Time & bars | [✅/⚠️/❌] | […] |
| State & failure modes | [✅/⚠️/❌] | […] |
| Numeric precision | [✅/⚠️/❌] | […] |
| Diagnosability | [✅/⚠️/❌] | […] |
| Performance | [✅/⚠️/❌] | […] |
| Tester↔live parity | [✅/⚠️/❌] | […] |
| GUI/UX | [✅/⚠️/❌] | […] |
| Security & permissions | [✅/⚠️/❌] | […] |
| Readability & style | [✅/⚠️/❌] | […] |

Legend: ✅ clean / ⚠️ 🟡-level findings only / ❌ 🔴 present.

## Scanner Dismissals

Findings the scanner raised and the reviewer dismissed (false
positives). One line each — keeps the audit trail honest.

- [rule-id file:line] dismissed: [reason]

## Tester↔Live Expectations

[Where live behaviour will be worse than any backtest, and roughly by
how much: spread, slippage, latency, gap risk, restart windows. Zero
sentences are only allowed after the parity guide's checklist was
actually walked.]

## Next Steps

1. [Fix order: which 🔴 first, which 🟡 batched]
2. [Verification: `mql5` skill — `verify_sl_tp_formulas.py` for risk
   fixes, `mql5_helper.py check` for compile cross-check, backtest
   for behavioural changes]
3. [Re-review trigger: scope of the re-review]

---

## Appendix — Scanner Output

[Paste `mql5_redflags.py scan` text output or attach the `--json`
file.]

## Quick Copy — Finding Blocks

```
🔴 **[blocking]** [Title]

**Location:** `file.mq5:NNN`
**Scenario:** [concrete failure scenario]

**Suggested fix:**
\`\`\`mql5
// patch sketch
\`\`\`
```

```
🟡 **[important]** [Title]

**Location:** `file.mq5:NNN`
[Why this matters / degraded behaviour]

**Consider:**
- Option A: […]
- Option B: […]
```

```
🟢 **[nit]** [Suggestion]

Not blocking, but consider [improvement].
```

```
🎉 **[praise]** Great work on [specific thing]!
[Why this is good]
```

```
📚 **[learning]** [Educational note]

For context, [X] works this way because [Y]. No action needed.
```
