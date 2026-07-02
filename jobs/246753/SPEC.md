
# One Shot Gold

Job Status: Finished by other person, but this job is worth to be implemented.

Budget: 30+ USD.

## Specification

Platform: MetaTrader 5 (MQL5) Main Symbol: XAUUSD (Gold) – but adaptable to other pairs Strategy: Place Buy Stop / Sell Stop pending orders at or near the top/bottom detected within the last 50 candles (updated default), combined with smart news filter and virtual stops.

1. Detection & Pending Order Placement Logic

    Automatically detect Swing High (top) and Swing Low (bottom) within the last 50 (Customize) candles (using Fractals, ZigZag, or highest/lowest price within the period).
    Sell Stop: Placed below the most recent Swing Low (with an optional offset, e.g., -3 to -10 pips to avoid fake breakouts).
    Buy Stop: Placed above the most recent Swing High (with optional offset, e.g., +3 to +10 pips).
    Support OCO (One Cancels the Other): When one pending order is triggered, the other is automatically deleted.
    Pending Order Expiration: Auto-delete after X hours (default 24 hours or 0 = no expiration).
    Signal Confirmation (to reduce false entries):
        Confirming candle close (bullish candle for Buy Stop, bearish for Sell Stop).
        Optional: Multi-timeframe confirmation (H1 signal must align with H4/D1).
        Optional: Momentum filter (e.g., RSI >50 for Buy Stop, <50 for Sell Stop).

2. Risk & Position Management

    Automatically calculate lot size based on % risk per trade and SL in pips. Formula: Lot = (Account Balance × Risk%) / (SL_pips × PipValue per lot)
    Maximum simultaneous orders/pendings: Default 1–2 per symbol.
    Maximum daily loss (%): Stop all trading if loss exceeds the limit (e.g., 3–5%).
    Maximum weekly loss (optional).

3. Order Management (SL / TP / Trailing)

    SL: 40 pips (calculated from the actual entry price after pending activation).
    TP: 200 pips (from actual entry price).
    Trailing Stop: 30 pips (starts after +30 pips profit, moves in steps).
    Advanced options:
        Trailing based on ATR (e.g., 1.5 × ATR(14)).
        Break-even: Move SL to entry or +X pips after Y pips in profit.
    Automatically adjust for broker digits (2/3/4/5 digits).

4. News Filter (Fully integrated in MQL5 code – no DLL)

    Enable / Disable completely.
    MinutesBeforeNews: Allow placing pending orders X minutes before news.
    MinutesAfterNews: Avoid placing new orders or cancel pending X minutes after news.
    Filter by news impact: Weak / Medium / Strong / Optional (selectable per level).
    Currency filter: Only block news relevant to XAU or USD (for XAUUSD).
    Spread protection during news window: Skip if spread > X pips.
    Option: Completely skip high-impact / strong news.

5. Hide SL/TP/Trailing (Prevent broker stop hunting)

    Virtual mode (EA manages closing internally – no real SL/TP sent to broker).
    Draw colored lines on chart for monitoring:
        Red: Virtual Stop Loss
        Green: Virtual Take Profit
        Yellow/Orange: Virtual Trailing Stop
    Input to enable/disable hiding and drawing lines.

6. Execution Protection

    Max slippage allowed (points): e.g., 3.0–5.0.
    Max spread allowed (points): e.g., 2.5–4.0 for XAUUSD.
    Check spread + slippage right before placing pending order.
    Skip order if limits exceeded.

7. Additional Features

    Unique Magic Number + Comment (e.g., "ReversalStop_XAU").
    Detailed logging: To file and chart comments (reason for pending, upcoming news…).
    Alerts & Notifications: Push notification / Email / Telegram when:
        Pending order placed
        Pending triggered → position opened
        Order closed (profit/loss)
        News approaching
        Daily loss limit reached
    Time filter: Only place pending orders during high-liquidity sessions (London + New York).

8. Main Input Parameters (Updated)

    | Group | Parameter | Description | Default |
    | --- | --- | --- | --- |
    | General | MagicNumber | Magic number | 202509 |
    | | MaxSpread | Maximum spread (points) | 10 |
    | | MaxSlippage | Maximum slippage (points) | 30 |
    | Risk | RiskPercent | Risk % per trade | 1.0 |
    | | MaxDailyLossPct | Max daily loss (%) | 4.0 |
    | | MaxOrders | Max simultaneous orders/pendings | 2 |
    | Entry | SwingCandles | Number of candles to detect top/bottom | 50 |
    | | OffsetPips | Offset distance for pending (pips) | 5.0 |
    | | UseMTFConfirmation | Use multi-timeframe confirmation | true |
    | Pending | PendingExpirationHours | Cancel pending after X hours (0 = no expiration) | 24 |
    | | UseOCO | One Cancels the Other | true |
    | SL/TP/Trailing | SLPips | Stop Loss (pips) | 40 |
    | | TPPips | Take Profit (pips) | 200 |
    | | TrailingPips | Trailing Stop (pips) | 30 |
    | | UseBreakEven | Enable break-even | true |
    | | BreakEvenAfterPips | Move SL after X pips profit | 50 |
    | News | UseNewsFilter | Enable news filter | true |
    | | MinutesBeforeNews | Minutes before news | 15 |
    | | MinutesAfterNews | Minutes after news | 30 |
    | | MaxNewsImportance | Max allowed news impact (1=low, 2=med, 3=high) | 2 |
    | Visual / Hide | UseVirtualStops | Enable virtual SL/TP/Trailing | true |
    | | DrawLines | Draw colored lines on chart | true |

## References

[Break Out EA MT5](https://www.mql5.com/en/job/246753)
