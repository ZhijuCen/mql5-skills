#!/usr/bin/env python3
"""
Parse MT5 Strategy Tester HTML report.

Extracts: account properties, EA parameters, P&L metrics, orders, deals.

Usage:
    python skills/mql5/scripts/parse_tester_report.py <report.html>
    python skills/mql5/scripts/parse_tester_report.py <report.html> --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

from bs4 import BeautifulSoup, Tag


# ── Data classes ─────────────────────────────────────────────────────

@dataclass
class Settings:
    expert: str = ""
    symbol: str = ""
    period: str = ""
    company: str = ""
    currency: str = ""
    initial_deposit: float = 0.0
    leverage: str = ""
    inputs: dict[str, str] = field(default_factory=dict)


@dataclass
class Results:
    history_quality: str = ""
    bars: int = 0
    ticks: int = 0
    symbols: int = 0
    total_net_profit: float = 0.0
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    balance_drawdown_abs: float = 0.0
    balance_drawdown_max: float = 0.0
    balance_drawdown_max_pct: float = 0.0
    balance_drawdown_rel: float = 0.0
    balance_drawdown_rel_pct: float = 0.0
    equity_drawdown_abs: float = 0.0
    equity_drawdown_max: float = 0.0
    equity_drawdown_max_pct: float = 0.0
    equity_drawdown_rel: float = 0.0
    equity_drawdown_rel_pct: float = 0.0
    profit_factor: float = 0.0
    expected_payoff: float = 0.0
    margin_level: float = 0.0
    recovery_factor: float = 0.0
    sharpe_ratio: float = 0.0
    z_score: float = 0.0
    z_score_pct: float = 0.0
    ahpr: float = 0.0
    ahpr_pct: float = 0.0
    ghpr: float = 0.0
    ghpr_pct: float = 0.0
    lr_correlation: float = 0.0
    lr_standard_error: float = 0.0
    on_tester_result: float = 0.0
    total_trades: int = 0
    total_deals: int = 0
    short_trades: int = 0
    short_won_pct: float = 0.0
    long_trades: int = 0
    long_won_pct: float = 0.0
    profit_trades: int = 0
    profit_trades_pct: float = 0.0
    loss_trades: int = 0
    loss_trades_pct: float = 0.0
    largest_profit_trade: float = 0.0
    largest_loss_trade: float = 0.0
    avg_profit_trade: float = 0.0
    avg_loss_trade: float = 0.0
    max_consec_wins: int = 0
    max_consec_wins_amt: float = 0.0
    max_consec_losses: int = 0
    max_consec_losses_amt: float = 0.0
    max_consec_profit: float = 0.0
    max_consec_profit_count: int = 0
    max_consec_loss: float = 0.0
    max_consec_loss_count: int = 0
    avg_consec_wins: int = 0
    avg_consec_losses: int = 0
    min_hold_time: str = ""
    max_hold_time: str = ""
    avg_hold_time: str = ""
    # MFE/MAE
    corr_profit_mfe: float = 0.0
    corr_profit_mae: float = 0.0
    corr_mfe_mae: float = 0.0


@dataclass
class Order:
    open_time: str = ""
    order: int = 0
    symbol: str = ""
    type: str = ""
    volume: str = ""
    price: float = 0.0
    sl: float = 0.0
    tp: float = 0.0
    close_time: str = ""
    state: str = ""
    comment: str = ""


@dataclass
class Deal:
    time: str = ""
    deal: int = 0
    symbol: str = ""
    type: str = ""
    direction: str = ""
    volume: float = 0.0
    price: float = 0.0
    order: int = 0
    commission: float = 0.0
    swap: float = 0.0
    profit: float = 0.0
    balance: float = 0.0
    comment: str = ""


@dataclass
class Report:
    settings: Settings = field(default_factory=Settings)
    results: Results = field(default_factory=Results)
    orders: list[Order] = field(default_factory=list)
    deals: list[Deal] = field(default_factory=list)


# ── Parsing helpers ──────────────────────────────────────────────────

def decode_html(path: Path) -> str:
    """Read MT5 report (UTF-16LE) and return UTF-8 string."""
    raw = path.read_bytes()
    # Detect BOM
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    if raw[:2] == b"\xfe\xff":
        return raw.decode("utf-16-be")
    # Try utf-16-le without BOM
    try:
        return raw.decode("utf-16-le")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def parse_number(text: str) -> float:
    """Parse number from MT5 report format: '1 305.90' → 1305.90, '-201.39' → -201.39"""
    text = text.strip()
    if not text:
        return 0.0
    # Remove spaces used as thousand separators
    text = text.replace(" ", "")
    # Extract first number-like token (may include %, parentheses)
    m = re.search(r"[-\d][\d,.]*", text)
    if not m:
        return 0.0
    num_str = m.group().replace(",", "")
    try:
        return float(num_str)
    except ValueError:
        return 0.0


def parse_pct(text: str) -> float:
    """Extract percentage value: '100.27% (516.89)' → 100.27"""
    m = re.search(r"([\d.]+)%", text)
    return float(m.group(1)) if m else 0.0


def td_text(td: Tag) -> str:
    """Get text content of a <td>, stripping whitespace."""
    return td.get_text(strip=True)


# ── Main parser ──────────────────────────────────────────────────────

def parse_report(html_path: Path) -> Report:
    html = decode_html(html_path)
    soup = BeautifulSoup(html, "html.parser")
    report = Report()

    tables = soup.find_all("table")
    if not tables:
        print("Error: no tables found in HTML", file=sys.stderr)
        return report

    # ── Table 0: Settings + Results ──────────────────────────────────
    main_table = tables[0]
    rows = main_table.find_all("tr")

    section = "settings"
    stats_map: dict[str, str] = {}

    for row in rows:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        # Detect section headers
        text_all = " ".join(td_text(c) for c in cells)
        if "Settings" in text_all and len(cells) <= 3:
            section = "settings"
            continue
        if "Results" in text_all and len(cells) <= 3:
            section = "results"
            continue

        if section == "settings":
            # Settings rows: label in col 0-2, value in col 3+
            if len(cells) < 2:
                continue
            label = td_text(cells[0])
            # Input parameters: label is empty, value is in the next cell
            if not label and len(cells) >= 2:
                val = td_text(cells[-1])
                if val.startswith("==="):
                    continue  # group header
                if "=" in val:
                    k, v = val.split("=", 1)
                    report.settings.inputs[k.strip()] = v.strip()
                continue
            # Standard settings fields
            if label.endswith(":"):
                label = label[:-1]
            val = td_text(cells[-1]) if len(cells) >= 2 else ""
            if label == "Expert":
                report.settings.expert = val
            elif label == "Symbol":
                report.settings.symbol = val
            elif label == "Period":
                report.settings.period = val
            elif label == "Company":
                report.settings.company = val
            elif label == "Currency":
                report.settings.currency = val
            elif label == "Initial Deposit":
                report.settings.initial_deposit = parse_number(val)
            elif label == "Leverage":
                report.settings.leverage = val

        elif section == "results":
            # Results: find label cells (ending with ":") and pair with next cell
            for i, cell in enumerate(cells):
                lbl = td_text(cell)
                if not lbl.endswith(":") or not lbl:
                    continue
                lbl = lbl.rstrip(":")
                # Value is the next cell
                if i + 1 < len(cells):
                    val = td_text(cells[i + 1])
                else:
                    val = ""
                stats_map[lbl] = val

    # ── Map stats_map to Results fields ──────────────────────────────
    r = report.results
    r.history_quality = stats_map.get("History Quality", "")
    r.bars = int(parse_number(stats_map.get("Bars", "0")))
    r.ticks = int(parse_number(stats_map.get("Ticks", "0")))
    r.symbols = int(parse_number(stats_map.get("Symbols", "0")))
    r.total_net_profit = parse_number(stats_map.get("Total Net Profit", "0"))
    r.gross_profit = parse_number(stats_map.get("Gross Profit", "0"))
    r.gross_loss = parse_number(stats_map.get("Gross Loss", "0"))
    r.balance_drawdown_abs = parse_number(stats_map.get("Balance Drawdown Absolute", "0"))
    r.balance_drawdown_max = parse_number(stats_map.get("Balance Drawdown Maximal", "0"))
    r.balance_drawdown_max_pct = parse_pct(stats_map.get("Balance Drawdown Maximal", "0"))
    r.balance_drawdown_rel = parse_number(stats_map.get("Balance Drawdown Relative", "0"))
    r.balance_drawdown_rel_pct = parse_pct(stats_map.get("Balance Drawdown Relative", "0"))
    r.equity_drawdown_abs = parse_number(stats_map.get("Equity Drawdown Absolute", "0"))
    r.equity_drawdown_max = parse_number(stats_map.get("Equity Drawdown Maximal", "0"))
    r.equity_drawdown_max_pct = parse_pct(stats_map.get("Equity Drawdown Maximal", "0"))
    r.equity_drawdown_rel = parse_number(stats_map.get("Equity Drawdown Relative", "0"))
    r.equity_drawdown_rel_pct = parse_pct(stats_map.get("Equity Drawdown Relative", "0"))
    r.profit_factor = parse_number(stats_map.get("Profit Factor", "0"))
    r.expected_payoff = parse_number(stats_map.get("Expected Payoff", "0"))
    r.margin_level = parse_pct(stats_map.get("Margin Level", "0"))
    r.recovery_factor = parse_number(stats_map.get("Recovery Factor", "0"))
    r.sharpe_ratio = parse_number(stats_map.get("Sharpe Ratio", "0"))
    z = stats_map.get("Z-Score", "0")
    r.z_score = parse_number(z)
    r.z_score_pct = parse_pct(z)
    ahpr = stats_map.get("AHPR", "0")
    r.ahpr = parse_number(ahpr)
    r.ahpr_pct = parse_pct(ahpr)
    ghpr = stats_map.get("GHPR", "0")
    r.ghpr = parse_number(ghpr)
    r.ghpr_pct = parse_pct(ghpr)
    r.lr_correlation = parse_number(stats_map.get("LR Correlation", "0"))
    r.lr_standard_error = parse_number(stats_map.get("LR Standard Error", "0"))
    r.on_tester_result = parse_number(stats_map.get("OnTester result", "0"))
    r.total_trades = int(parse_number(stats_map.get("Total Trades", "0")))
    r.total_deals = int(parse_number(stats_map.get("Total Deals", "0")))

    # Parse Short/Long Trades: "5 (20.00%)"
    short = stats_map.get("Short Trades (won %)", "0")
    r.short_trades = int(parse_number(short))
    r.short_won_pct = parse_pct(short)
    long = stats_map.get("Long Trades (won %)", "0")
    r.long_trades = int(parse_number(long))
    r.long_won_pct = parse_pct(long)

    pt = stats_map.get("Profit Trades (% of total)", "0")
    r.profit_trades = int(parse_number(pt))
    r.profit_trades_pct = parse_pct(pt)
    lt = stats_map.get("Loss Trades (% of total)", "0")
    r.loss_trades = int(parse_number(lt))
    r.loss_trades_pct = parse_pct(lt)

    r.largest_profit_trade = parse_number(stats_map.get("Largest profit trade", "0"))
    r.largest_loss_trade = parse_number(stats_map.get("Largest loss trade", "0"))
    r.avg_profit_trade = parse_number(stats_map.get("Average profit trade", "0"))
    r.avg_loss_trade = parse_number(stats_map.get("Average loss trade", "0"))

    # Consecutive: "3 (85.31)" or "1"
    mcw = stats_map.get("Maximum consecutive wins ($)", "0")
    r.max_consec_wins = int(parse_number(mcw))
    m = re.search(r"\(([-\d.]+)\)", mcw)
    r.max_consec_wins_amt = float(m.group(1)) if m else 0.0

    mcl = stats_map.get("Maximum consecutive losses ($)", "0")
    r.max_consec_losses = int(parse_number(mcl))
    m = re.search(r"\(([-\d.]+)\)", mcl)
    r.max_consec_losses_amt = float(m.group(1)) if m else 0.0

    # "361.91 (2)"
    mcp = stats_map.get("Maximal consecutive profit (count)", "0")
    r.max_consec_profit = parse_number(mcp)
    m = re.search(r"\((\d+)\)", mcp)
    r.max_consec_profit_count = int(m.group(1)) if m else 0

    mcl2 = stats_map.get("Maximal consecutive loss (count)", "0")
    r.max_consec_loss = parse_number(mcl2)
    m = re.search(r"\((\d+)\)", mcl2)
    r.max_consec_loss_count = int(m.group(1)) if m else 0

    r.avg_consec_wins = int(parse_number(stats_map.get("Average consecutive wins", "0")))
    r.avg_consec_losses = int(parse_number(stats_map.get("Average consecutive losses", "0")))

    r.min_hold_time = stats_map.get("Minimal position holding time", "")
    r.max_hold_time = stats_map.get("Maximal position holding time", "")
    r.avg_hold_time = stats_map.get("Average position holding time", "")

    r.corr_profit_mfe = parse_number(stats_map.get("Correlation (Profits,MFE)", "0"))
    r.corr_profit_mae = parse_number(stats_map.get("Correlation (Profits,MAE)", "0"))
    r.corr_mfe_mae = parse_number(stats_map.get("Correlation (MFE,MAE)", "0"))

    # ── Table 1+: Orders and Deals ───────────────────────────────────
    # The second table contains both Orders and Deals sections,
    # each with their own header row (bgcolor=#E5F0FC)
    for tbl in tables[1:]:
        header_rows = tbl.find_all("tr", bgcolor=re.compile(r"#E5F0FC"))
        for header_row in header_rows:
            headers = [td_text(th) for th in header_row.find_all(["td", "th"])]

            # Find data rows that follow this header (until next header or end)
            all_rows = tbl.find_all("tr")
            hdr_idx = all_rows.index(header_row)
            data_rows = []
            for r in all_rows[hdr_idx + 1:]:
                bg = r.get("bgcolor", "")
                if re.match(r"#(FFFFFF|F7F7F7)", str(bg)):
                    data_rows.append(r)
                elif r.find("th") and ("Deals" in td_text(r) or "Orders" in td_text(r)):
                    break  # next section header

            if "Open Time" in headers and "Order" in headers:
                # Orders table — cells are in order, colspan only affects visual layout
                for dr in data_rows:
                    cells = dr.find_all("td")
                    if len(cells) < 10:
                        continue
                    vals = [td_text(c) for c in cells]
                    order = Order(
                        open_time=vals[0],
                        order=int(parse_number(vals[1])),
                        symbol=vals[2],
                        type=vals[3],
                        volume=vals[4],
                        price=parse_number(vals[5]),
                        sl=parse_number(vals[6]),
                        tp=parse_number(vals[7]),
                        close_time=vals[8],
                        state=vals[9],
                        comment=vals[10] if len(vals) > 10 else "",
                    )
                    report.orders.append(order)

            elif "Deal" in headers and "Direction" in headers:
                # Deals table
                for dr in data_rows:
                    cells = dr.find_all("td")
                    if len(cells) < 10:
                        continue
                    vals = [td_text(c) for c in cells]
                    deal = Deal(
                        time=vals[0],
                        deal=int(parse_number(vals[1])),
                        symbol=vals[2],
                        type=vals[3],
                        direction=vals[4],
                        volume=parse_number(vals[5]),
                        price=parse_number(vals[6]),
                        order=int(parse_number(vals[7])),
                        commission=parse_number(vals[8]),
                        swap=parse_number(vals[9]),
                        profit=parse_number(vals[10]),
                        balance=parse_number(vals[11]),
                        comment=vals[12] if len(vals) > 12 else "",
                    )
                    report.deals.append(deal)

    return report


# ── Pretty print ─────────────────────────────────────────────────────

def print_report(r: Report) -> None:
    s = r.settings
    res = r.results

    print("=" * 72)
    print("  MT5 Strategy Tester Report")
    print("=" * 72)

    print(f"\n  Expert:     {s.expert}")
    print(f"  Symbol:     {s.symbol}")
    print(f"  Period:     {s.period}")
    print(f"  Company:    {s.company}")
    print(f"  Currency:   {s.currency}")
    print(f"  Deposit:    {s.initial_deposit:,.2f}")
    print(f"  Leverage:   {s.leverage}")

    if s.inputs:
        print(f"\n  EA Parameters ({len(s.inputs)}):")
        for k, v in s.inputs.items():
            print(f"    {k} = {v}")

    print(f"\n{'─' * 72}")
    print("  Data Quality")
    print(f"{'─' * 72}")
    print(f"  History Quality: {res.history_quality}")
    print(f"  Bars:            {res.bars:,}")
    print(f"  Ticks:           {res.ticks:,}")
    print(f"  Symbols:         {res.symbols}")

    print(f"\n{'─' * 72}")
    print("  P&L Summary")
    print(f"{'─' * 72}")
    print(f"  Net Profit:      {res.total_net_profit:>12,.2f}")
    print(f"  Gross Profit:    {res.gross_profit:>12,.2f}")
    print(f"  Gross Loss:      {res.gross_loss:>12,.2f}")
    print(f"  Profit Factor:   {res.profit_factor:>12.2f}")
    print(f"  Expected Payoff: {res.expected_payoff:>12.2f}")
    print(f"  Recovery Factor: {res.recovery_factor:>12.2f}")
    print(f"  Sharpe Ratio:    {res.sharpe_ratio:>12.2f}")

    print(f"\n{'─' * 72}")
    print("  Drawdown")
    print(f"{'─' * 72}")
    print(f"  Balance Abs:     {res.balance_drawdown_abs:>12,.2f}")
    print(f"  Balance Max:     {res.balance_drawdown_max:>12,.2f} ({res.balance_drawdown_max_pct:.2f}%)")
    print(f"  Balance Rel:     {res.balance_drawdown_rel_pct:.2f}% ({res.balance_drawdown_rel:,.2f})")
    print(f"  Equity Abs:      {res.equity_drawdown_abs:>12,.2f}")
    print(f"  Equity Max:      {res.equity_drawdown_max:>12,.2f} ({res.equity_drawdown_max_pct:.2f}%)")
    print(f"  Equity Rel:      {res.equity_drawdown_rel_pct:.2f}% ({res.equity_drawdown_rel:,.2f})")

    print(f"\n{'─' * 72}")
    print("  Trade Statistics")
    print(f"{'─' * 72}")
    print(f"  Total Trades:    {res.total_trades:>8}    Total Deals:   {res.total_deals}")
    print(f"  Short (won%):    {res.short_trades:>8} ({res.short_won_pct:.2f}%)")
    print(f"  Long  (won%):    {res.long_trades:>8} ({res.long_won_pct:.2f}%)")
    print(f"  Profit Trades:   {res.profit_trades:>8} ({res.profit_trades_pct:.2f}%)")
    print(f"  Loss Trades:     {res.loss_trades:>8} ({res.loss_trades_pct:.2f}%)")
    print(f"  Largest Win:     {res.largest_profit_trade:>12,.2f}")
    print(f"  Largest Loss:    {res.largest_loss_trade:>12,.2f}")
    print(f"  Avg Win:         {res.avg_profit_trade:>12,.2f}")
    print(f"  Avg Loss:        {res.avg_loss_trade:>12,.2f}")
    print(f"  Max Consec Wins: {res.max_consec_wins:>4} (${res.max_consec_wins_amt:,.2f})")
    print(f"  Max Consec Loss: {res.max_consec_losses:>4} (${res.max_consec_losses_amt:,.2f})")

    print(f"\n{'─' * 72}")
    print("  Holding Times")
    print(f"{'─' * 72}")
    print(f"  Min: {res.min_hold_time}  Max: {res.max_hold_time}  Avg: {res.avg_hold_time}")

    print(f"\n{'─' * 72}")
    print(f"  Orders: {len(r.orders)}    Deals: {len(r.deals)}")
    print(f"{'─' * 72}")

    if r.orders:
        print(f"\n  {'Open Time':<20} {'Ord':>5} {'Type':<5} {'Vol':>6} {'Price':>10} {'SL':>10} {'TP':>10} {'State':<8} {'Comment'}")
        for o in r.orders[:10]:
            print(f"  {o.open_time:<20} {o.order:>5} {o.type:<5} {o.volume:>6} {o.price:>10.2f} {o.sl:>10.2f} {o.tp:>10.2f} {o.state:<8} {o.comment}")
        if len(r.orders) > 10:
            print(f"  ... ({len(r.orders) - 10} more)")

    if r.deals:
        print(f"\n  {'Time':<20} {'Deal':>5} {'Type':<5} {'Dir':<4} {'Vol':>6} {'Price':>10} {'Comm':>8} {'Swap':>8} {'Profit':>10} {'Balance':>10}")
        for d in r.deals[:10]:
            print(f"  {d.time:<20} {d.deal:>5} {d.type:<5} {d.direction:<4} {d.volume:>6.2f} {d.price:>10.2f} {d.commission:>8.2f} {d.swap:>8.2f} {d.profit:>10.2f} {d.balance:>10.2f}")
        if len(r.deals) > 10:
            print(f"  ... ({len(r.deals) - 10} more)")



# ── Trade Analysis ───────────────────────────────────────────────────

def pair_trades(deals: list) -> list:
    """Pair entry/exit deals into complete trades."""
    trading = [d for d in deals if d.type != "balance"]

    trades = []
    i = 0
    while i < len(trading):
        if trading[i].direction == "in":
            entry = trading[i]
            if i + 1 < len(trading) and trading[i + 1].direction == "out":
                exit_d = trading[i + 1]
                net = (exit_d.profit + entry.commission + exit_d.commission
                       + entry.swap + exit_d.swap)
                sl_dist = 0.0
                if "sl" in exit_d.comment:
                    sl_dist = abs(entry.price - exit_d.price)
                trades.append({
                    "open_time": entry.time,
                    "close_time": exit_d.time,
                    "type": entry.type,
                    "volume": entry.volume,
                    "entry": entry.price,
                    "exit": exit_d.price,
                    "profit": exit_d.profit,
                    "commission": entry.commission + exit_d.commission,
                    "swap": entry.swap + exit_d.swap,
                    "net": net,
                    "comment": exit_d.comment,
                    "sl_distance": sl_dist,
                })
                i += 2
            else:
                i += 1
        else:
            i += 1
    return trades


def analyze_report(report: Report) -> dict:
    """Run full trade analysis on parsed report."""
    from datetime import datetime

    deposit = report.settings.initial_deposit
    trades = pair_trades(report.deals)

    if not trades:
        return {"error": "No trades found", "trades": []}

    # Per-trade risk check
    for t in trades:
        t["risk_pct"] = abs(t["net"]) / deposit * 100 if deposit > 0 else 0

    # SL hit vs TP hit
    sl_trades = [t for t in trades if "sl " in t["comment"]]
    tp_trades = [t for t in trades if "tp " in t["comment"]]
    other = [t for t in trades if t not in sl_trades and t not in tp_trades]

    avg_win = (sum(t["net"] for t in tp_trades) / len(tp_trades)) if tp_trades else 0
    avg_loss = (sum(t["net"] for t in sl_trades) / len(sl_trades)) if sl_trades else 0
    win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    breakeven_wr = (abs(avg_loss) / (avg_win + abs(avg_loss))
                    if (avg_win + abs(avg_loss)) > 0 else 0)

    # Consecutive loss analysis
    streaks = []
    streak = 0
    for t in trades:
        if t["net"] <= 0:
            streak += 1
        else:
            if streak > 0:
                streaks.append(streak)
            streak = 0
    if streak > 0:
        streaks.append(streak)

    # Re-entry detection: SL hit followed by same direction with larger lot
    reentries = []
    for i in range(len(trades) - 1):
        t1, t2 = trades[i], trades[i + 1]
        if "sl " in t1["comment"] and t1["type"] == t2["type"]:
            if t2["volume"] > t1["volume"]:
                reentries.append({
                    "after_trade": i + 1,
                    "time": t2["open_time"],
                    "type": t2["type"],
                    "prev_lot": t1["volume"],
                    "new_lot": t2["volume"],
                    "multiplier": round(t2["volume"] / t1["volume"], 1),
                })

    # Monthly breakdown
    monthly = {}
    for t in trades:
        month = t["open_time"][:7]
        if month not in monthly:
            monthly[month] = {"count": 0, "net": 0.0, "wins": 0, "losses": 0}
        monthly[month]["count"] += 1
        monthly[month]["net"] += t["net"]
        if t["net"] > 0:
            monthly[month]["wins"] += 1
        else:
            monthly[month]["losses"] += 1

    for m in monthly:
        d = monthly[m]
        d["net"] = round(d["net"], 2)
        d["win_rate"] = round(d["wins"] / d["count"] * 100, 1) if d["count"] else 0

    # Volume pattern
    lots = [t["volume"] for t in trades]
    unique_lots = sorted(set(lots))

    # Last trade gap relative to script execution time
    last_close = trades[-1]["close_time"]
    try:
        last_dt = datetime.strptime(last_close, "%Y.%m.%d %H:%M:%S")
        gap_days = (datetime.now() - last_dt).days
    except Exception:
        gap_days = -1

    return {
        "sl_hits": len(sl_trades),
        "tp_hits": len(tp_trades),
        "other_exits": len(other),
        "win_loss_ratio": round(win_loss_ratio, 2),
        "breakeven_win_rate": round(breakeven_wr * 100, 1),
        "win_rate_gap_pct": round((len(tp_trades) / len(trades) - breakeven_wr) * 100, 1),
        "consec_loss_streaks": streaks,
        "reentries": reentries,
        "monthly": monthly,
        "lot_pattern": {
            "unique_lots": unique_lots,
            "uniform": len(unique_lots) == 1,
        },
        "last_trade_close": last_close,
        "gap_days_to_now": gap_days,
        "trades": trades,
    }


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Parse MT5 Strategy Tester HTML report")
    parser.add_argument("report", help="Path to HTML report file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--analyze", action="store_true",
                        help="Run trade analysis (pair deals, risk check, monthly breakdown)")
    args = parser.parse_args()

    path = Path(args.report)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    report = parse_report(path)

    if args.analyze:
        report_dict = asdict(report)
        report_dict["analyze"] = analyze_report(report)
        print(json.dumps(report_dict, indent=2, ensure_ascii=False))
    elif args.json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
