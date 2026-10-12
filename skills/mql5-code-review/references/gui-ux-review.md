# Chart GUI / UX Review Guide

Static review of chart-object UI (panels, labels, buttons, lines) and
notification UX in MQL5 EA source. GUI bugs do not lose trades
directly, but they destroy trust in the EA and, in the notification
case, cause real incidents (push floods get accounts muted). Severity:
🔴 actionable harm (floods, chart destruction), 🟡 degraded
usability/portability, 🟢 polish.

## Table of Contents

- [§1 Layout and Text Overflow](#1-layout-and-text-overflow)
- [§2 Theme, DPI, and Anchoring Portability](#2-theme-dpi-and-anchoring-portability)
- [§3 Update Frequency and Redraw Cost](#3-update-frequency-and-redraw-cost)
- [§4 Lifecycle and Multi-Instance Safety](#4-lifecycle-and-multi-instance-safety)
- [§5 Content Correctness and Notification Throttling](#5-content-correctness-and-notification-throttling)
- [Review Checklist](#review-checklist)

---

## §1 Layout and Text Overflow

MQL5 offers no text-measurement API: `ObjectGetString` width is
unknown until the chart draws it. Overflow is therefore a *design*
question the source must answer.

```mql5
// ❌ Blocking-grade UX bug: fixed 120px panel, value text grows
// without bound — "Balance: $1,234,567.89" spills past the panel
ObjectSetString(0, panelBg, OBJPROP_TEXT, "");
ObjectSetString(0, lblBalance, OBJPROP_TEXT,
                "Balance: " + DoubleToString(balance, 2));

// ✅ Width budgeted for the worst case; text truncated, not spilled
string fmt = "Balance: %.2f";
string txt = StringFormat(fmt, balance);
if(StringLen(txt) > MAX_CHARS)          // MAX_CHARS from panel width
    txt = StringSubstr(txt, 0, MAX_CHARS - 1) + "…";
ObjectSetString(0, lblBalance, OBJPROP_TEXT, txt);
```

Checklist:
- [ ] 🟡 Fixed-width panels: is there a documented worst-case length
  (digits, currency, sign, separators) per field? Values reviewed:
  balance/equity/profit (grow with account size), symbol names
  (broker suffixes), countdown strings.
- [ ] 🟡 Truncation strategy present (`StringLen` guard +
  `StringSubstr`) for any field fed by external data (symbol, comment).
- [ ] 🟡 `OBJ_LABEL` does **not** wrap: multi-line text must be
  split into one label per line — grep for `\\n` in label texts
  (it renders literally or as nothing, depending on build). Wait —
  review finding: `\n` in `OBJ_LABEL` text is not line-breaking;
  verify each intended line is a separate object.
- [ ] 🟡 Long text in `OBJ_BUTTON` / `OBJ_RECTANGLE_LABEL` — button
  captions are not ellipsized either; fixed button widths need the
  same budget.
- [ ] 🟢 Comment in source stating the assumed font metrics
  (e.g. "8px/char at size 9 Consolas") so future edits re-check the
  budget.

## §2 Theme, DPI, and Anchoring Portability

- [ ] 🟡 Hardcoded colors (`C'red'`, `0xRRGGBB`, `clrRed`) on chart
  objects: unreadable when the user runs the opposite theme (white
  background + white text). Review: colors either derived from
  `ChartGetInteger(0, CHART_COLOR_BACKGROUND/TEXT)` contrast, or
  documented as requiring a specific theme.
- [ ] 🟡 Anchor vs chart scroll: objects placed at *price/time*
  coordinates (`OBJPROP_PRICE`/`OBJPROP_TIME`, `OBJ_TREND` panels)
  move with scrolling/zooming and disappear with auto-scale. Panels
  must use corner-anchored pixel placement:

```mql5
// ❌ panel drifts with scroll/zoom
ObjectSetInteger(0, panel, OBJPROP_TIME,  t0);
ObjectSetInteger(0, panel, OBJPROP_PRICE, p0);

// ✅ corner-anchored pixel layout (screen space)
ObjectSetInteger(0, panel, OBJPROP_CORNER, CORNER_LEFT_UPPER);
ObjectSetInteger(0, panel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER);
ObjectSetInteger(0, panel, OBJPROP_XDISTANCE, baseX);
ObjectSetInteger(0, panel, OBJPROP_YDISTANCE, baseY);
```

- [ ] 🟡 Subwindow choice: indicator-window objects (`OBJPROP_WINDOW`
  > 0) — does the EA assume the window number it was authored in?
  Window indices shift when the user adds/removes indicators. Prefer
  main chart or verify index handling.
- [ ] 🟡 DPI: pixel coordinates render smaller on high-DPI displays;
  fixed 12px fonts can become unreadable. Acceptable limitation,
  but should be a documented one-liner in the source header.
- [ ] 🟡 Auto-scale interplay: price-anchored arrows/lines
  (`OBJ_ARROW`, `OBJ_TREND`) distort the visible price range; if the
  EA draws lines for analysis, `OBJPROP_BACK = true` and
  `OBJPROP_RAY_RIGHT = false` prevent chart sabotage.
- [ ] 🟢 One layout table (X/Y constants) in the source instead of
  magic pixel numbers inline — the single most review-friendly GUI
  pattern.

## §3 Update Frequency and Redraw Cost

Each `ObjectSet*` marks the chart dirty; `ChartRedraw()` forces a
full repaint. Per-tick GUI work is the classic EA performance leak.

```mql5
// ❌ Blocking-grade on busy symbols: 4 object writes × 50 ticks/s
void OnTick() {
    ObjectSetDouble(0, lblBid, OBJPROP_PRICE, SymbolInfoDouble(_Symbol, SYMBOL_BID));
    ObjectSetString (0, lblBid, OBJPROP_TEXT,  DoubleToString(bid, 5));
    ObjectSetInteger(0, lblBar, OBJPROP_COLOR, isNewBar ? clrLime : clrGray);
    ChartRedraw();                       // full repaint per tick
}

// ✅ Change-driven update + one redraw per batch (or timer-driven)
void OnTick() {
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    if(bid == m_lastBidShown) return;    // no visual change → no work
    m_lastBidShown = bid;
    ObjectSetString(0, lblBid, OBJPROP_TEXT, DoubleToString(bid, 5));
    ChartRedraw(false);                  // queued, cheap
    // or: EventSetTimer(1) → update all labels once per second
}
```

Checklist:
- [ ] 🟡 Per-tick `ObjectSet*` without change detection — compare to
  the previously shown value first (change-driven).
- [ ] 🟡 `ChartRedraw()` (full) per tick or per object — batch all
  updates, then one redraw at the end of the update pass;
  `ChartRedraw(false)` queues without forcing.
- [ ] 🟡 Create/delete churn: `ObjectCreate` in the tick path (each
  delete+create flickers and allocates) — create all objects once in
  OnInit, then only update properties.
- [ ] 🟡 Object count budget: hundreds of objects slow the entire
  terminal (all charts). Review cumulative `ObjectCreate` sites for
  unique-name discipline and cap (e.g. ≤ ~100 per chart).
- [ ] 🟡 Display cadence: dashboards/countdowns do not need tick
  resolution — a 1s (or bar) timer is sufficient and cheap.
  `CHARTEVENT_CHART_CHANGE` handlers (theme/TF switches) must be
  light; they fire on every resize/scroll.
- [ ] 🟢 Per-frame allocations (string building for every label every
  update) — cache unchanged strings.

## §4 Lifecycle and Multi-Instance Safety

```mql5
// ❌ Blocking: EA removed from chart → panel permanently orphaned
void OnDeinit(const int reason) { /* nothing */ }

// ❌ Blocking: full-chart wipe destroys the user's own objects too
void OnDeinit(const int reason) { ObjectsDeleteAll(0, ""); }

// ✅ prefix-scoped cleanup
void OnDeinit(const int reason) {
    ObjectsDeleteAll(0, PREFIX);            // exact prefix
    // or: loop delete by stored names
    ChartRedraw(0);
}
```

Checklist:
- [ ] 🔴 `OnDeinit` cleanup exists for every object-creating EA;
  absence = permanent chart garbage + name collisions on re-attach.
- [ ] 🔴 Cleanup scope: `ObjectsDeleteAll(0, "")` or argument-less
  variants destroy user-drawn objects and other EAs' UI. Must be
  prefix-scoped. 🔴 regardless of intent.
- [ ] 🟡 Name uniqueness: prefix derived from EA + magic + (if
  multi-chart) symbol — two instances on one chart (hedging basket
  dashboards) must not collide. Review the name-construction function.
- [ ] 🟡 `OBJPROP_SELECTABLE`/`OBJPROP_SELECTED` set `false` on
  decorative/panel objects — otherwise users drag/resize the panel by
  accident and blame the EA.
- [ ] 🟡 Button state round-trip: `CHARTEVENT_OBJECT_CLICK` handler
  must reset the button's visual state on every path, including
  failed actions (`OBJPROP_STATE` toggles on click and *stays*
  toggled if unhandled).
- [ ] 🟡 Re-init paths: parameter change re-runs OnInit — objects
  created again; either delete-first or create-if-absent
  (`ObjectFind(0, name) < 0` guard) to avoid
  "object already exists" errors.
- [ ] 🟢 `reason` in OnDeinit used meaningfully (log why the EA
  stopped; `REASON_REMOVE` vs `REASON_RECOMPILE` vs `REASON_ACCOUNT`
  — an account switch log line aids incident reviews).

## §5 Content Correctness and Notification Throttling

### Display formatting

- [ ] 🟡 Decimal places: `DoubleToString(price, 2)` on a 5-digit
  symbol or JPY pair — digits must come from
  `(int)SymbolInfoInteger(sym, SYMBOL_DIGITS)`. One formatting
  helper for all price labels.
- [ ] 🟡 Stale-value marking: when the market is closed (or a
  symbol's feed is disabled), the dashboard shows the last values
  with no indication — display the last-update time or dim the panel.
- [ ] 🟢 Localized separators: `DoubleToString` always uses `.`
  decimal / no grouping; consistent formatting across the panel beats
  locale correctness here.

### Notification throttling — the flood incident class

`Alert`, `SendNotification`, `SendMail`, `SendAppMessage` all have
external rate and cost consequences: MT5 push gets the terminal or
account muted after a flood; email through the terminal can trip
broker/SMTP limits; Alerts on a desktop VPS pile up unseen. Any
emission path reachable per tick without a guard is a 🔴.

```mql5
// ❌ Blocking: every tick above the level → hundreds of pushes/hour
void OnTick() {
    double rsi = /* current rsi */;
    if(rsi > 70)
        SendNotification(_Symbol + " RSI overbought: " + DoubleToString(rsi, 1));
}

// ✅ once-per-(bar|signal) with state, plus a global cooldown
datetime m_lastNotify = 0;
int      m_notifyCount = 0;
bool AllowNotify() {
    if(TimeCurrent() - m_lastNotify < 300)     // cooldown, seconds
        return false;
    m_lastNotify = TimeCurrent();
    if(++m_notifyCount > MAX_PER_DAY) {        // daily budget
        if(m_notifyCount == MAX_PER_DAY + 1)   // log the cutoff once
            Print("daily notification budget exhausted — suppressing");
        return false;
    }
    return true;
}
void OnTick() {
    if(rsi > 70 && NewBarOrNewSignal() && AllowNotify())
        SendNotification(...);
}
```

Checklist:
- [ ] 🔴 Every `Alert`/`SendNotification`/`SendMail`/
  `SendAppMessage` call site: reachable per tick? has a
  once-per-signal (bar/state-change) guard AND a cooldown/budget?
  Three separate protections, in this order of importance.
- [ ] 🔴 Transition-edge semantics: notify on the *edge* (level
  crossed), not the *state* (level exceeded) — state-based emission
  re-fires every tick while the condition holds.
- [ ] 🟡 Capability pre-check before notifying (fail silently to
  journal, not to a user-visible error dialog stack):
  - push: `TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ALLOWED)`
  - e-mail: `TerminalInfoInteger(TERMINAL_EMAIL_ENABLED)`
  - alerts: visual-mode considerations
- [ ] 🟡 Notification content budget: push messages truncate; put
  symbol + condition + value first, context later.
- [ ] 🟡 Alerts per symbol/condition independently throttled (one
  cooldown variable for 5 conditions = the first condition eats the
  whole budget; per-condition state maps).
- [ ] 🟢 `Alert()` inside `OnDeinit` (cleanup summary) — review for
  spam on parameter re-optimization loops (OnDeinit fires per pass).

## Review Checklist

1. Panel widths budgeted for worst-case text; truncation, not spill
2. No `\\n`-dependent labels; per-line objects
3. Colors theme-aware or documented; corner-anchored pixel layout
4. Change-driven updates; batched single redraw; create-once pattern
5. Object count bounded; display cadence = timer, not tick
6. OnDeinit prefix-scoped cleanup exists
7. Names unique per instance; objects non-selectable; buttons reset
8. Prices formatted with SYMBOL_DIGITS; stale values marked
9. Notifications: edge-triggered + cooldown + daily budget; capability
   pre-checked
