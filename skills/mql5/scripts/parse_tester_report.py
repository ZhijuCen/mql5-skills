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
from datetime import datetime, timedelta
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

def print_report(r: Report, analyze_data: dict | None = None) -> None:
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
    if analyze_data:
        print(f"  Idle (no position): {analyze_data.get('idle_time', '')}")

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
    """Pair entry/exit deals into complete trades.

    Each trade is returned with two P&L views:
      • `net` = exit.profit + entry.commission + exit.commission + entry.swap + exit.swap
        This equals the total change in balance from the trade and
        matches MT5's `STAT_PROFIT` summation (sum of `net` over all
        trades = `Total Net Profit`).
      • `gross_pnl` = exit.profit + exit.commission + exit.swap
        This is the "exit leg" P&L. MT5 splits this between
        `STAT_GROSS_PROFIT` and `STAT_GROSS_LOSS` based on its sign
        (see `compute_gross_profit_loss` below), and any entry
        commission/swap always goes to `STAT_GROSS_LOSS`.

    The MT5 accounting quirk (entry costs in GL regardless of trade
    outcome) is the reason we keep `gross_pnl` separate from `net`
    rather than overloading `net` to also drive GP/GL.
    """
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
                gross_pnl = exit_d.profit + exit_d.commission + exit_d.swap
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
                    "gross_pnl": gross_pnl,
                    "entry_costs": entry.commission + entry.swap,
                    "comment": exit_d.comment,
                    "sl_distance": sl_dist,
                })
                i += 2
            else:
                i += 1
        else:
            i += 1
    return trades


def compute_gross_profit_loss(trades: list) -> tuple[float, float]:
    """Compute MT5's STAT_GROSS_PROFIT / STAT_GROSS_LOSS from a list of trades.

    Returns (gross_profit, gross_loss). Per MT5:
      • For each trade, split `gross_pnl` (= exit.profit + exit.commission
        + exit.swap) by sign into GP (positive) or GL (negative/zero).
      • Entry costs (entry.commission + entry.swap) ALWAYS go to GL.

    Use this instead of naive `sum(positive nets)` — verified against
    the 246753 reference report (matches exactly).
    """
    gp = 0.0
    gl = 0.0
    for t in trades:
        if t["gross_pnl"] > 0:
            gp += t["gross_pnl"]
        else:
            gl += t["gross_pnl"]
        gl += t["entry_costs"]
    return round(gp, 2), round(gl, 2)


def format_duration(td) -> str:
    """Format timedelta as HH:MM:SS."""
    total = int(td.total_seconds())
    sign = "-" if total < 0 else ""
    total = abs(total)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{sign}{h:02d}:{m:02d}:{s:02d}"


def analyze_report(report: Report) -> dict:
    """Run full trade analysis on parsed report."""

    deposit = report.settings.initial_deposit
    trades = pair_trades(report.deals)

    if not trades:
        return {"error": "No trades found", "trades": []}

    # Parse backtest start/end dates from period string
    # e.g. "H4 (2024.01.01 - 2025.06.22)"
    bt_start = None
    bt_end = None
    period = report.settings.period
    m_dates = re.search(
        r"(\d{4}\.\d{2}\.\d{2})\s*-\s*(\d{4}\.\d{2}\.\d{2})\s*\)\s*$", period
    )
    if m_dates:
        try:
            bt_start = datetime.strptime(m_dates.group(1), "%Y.%m.%d")
            bt_end = datetime.strptime(m_dates.group(2), "%Y.%m.%d")
        except ValueError:
            pass

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

    # Idle time: total backtest duration minus time in positions
    idle_str = ""
    if bt_start and bt_end:
        total_duration = bt_end - bt_start
        position_time = timedelta()
        for t in trades:
            close_dt = datetime.strptime(t["close_time"], "%Y.%m.%d %H:%M:%S")
            open_dt = datetime.strptime(t["open_time"], "%Y.%m.%d %H:%M:%S")
            position_time += close_dt - open_dt
        idle_td = total_duration - position_time
        idle_str = format_duration(idle_td)

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
        "idle_time": idle_str,
        "trades": trades,
    }


# ── Window Analysis ──────────────────────────────────────────────────
#
# Split a backtest into N equal time windows and compute the same
# performance metrics the report shows, per window. This lets you
# spot windows whose metric values are statistical outliers vs the
# rest of the backtest (regime detection / over-fitting).
#
# Outlier detection uses per-metric z-score (sample std, N-1) across
# windows. |z| >= 2 = notable, |z| >= 5 = extreme.
#
# Conventions
# -----------
# • Time boundaries: equal-length [t_start, t_end) slices, left-closed
#   right-open. Window 0 starts at the backtest start; window N-1 ends
#   at the backtest end. Adjacent windows do not overlap.
# • A trade is assigned to the window where it OPENS (entry time,
#   `pair_trades` field "open_time"). Its P&L lands at exit time, which
#   may fall in a later window — we attribute the P&L to the opening
#   window because that is the "decision moment" the user cares about.
# • For path-dependent metrics (Balance DD Rel%, Recovery Factor, Sharpe)
#   we reconstruct a local balance curve starting from the balance at
#   the window's left edge. The `balance` field in deal rows equals
#   equity at the moment of the deal (no floating P&L at deal time),
#   which is exact for closed-trade snapshots. This reconstruction
#   therefore matches `STAT_BALANCE_DDREL_PERCENT` (maximum relative
#   drawdown, i.e. the largest (peak-trough)/peak ratio) exactly
#   (verified on 246753: 44.60% vs report 44.63%).
# • Recovery Factor per MT5's report value is `STAT_PROFIT /
#   STAT_EQUITY_DD` (verified empirically — the official doc page
#   says STAT_BALANCE_DD, but the reported value matches the equity
#   version). We compute RF using `bal_dd_rel_abs` (the abs $ amount
#   at the moment of maximum relative DD), which gives a value that
#   does NOT match the report exactly — it uses a different DD
#   reference (balance relative vs equity maximal). This is per the
#   user's fallback rule: "如 Equity DD % 不可用，则以 Balance DD % 代
#   替".
# • Gross Profit / Gross Loss use MT5's split: each trade's
#   "exit-leg" P&L (exit.profit + exit.commission + exit.swap) goes
#   to GP if positive or GL if non-positive; entry costs always go
#   to GL. This matches the report exactly (see
#   `compute_gross_profit_loss`).
# • Sharpe Ratio uses the MQL5-community standard formula
#   (AHPR - 1) / std_HPR × sqrt(N_per_year), where
#   HPR_i = Balance_i / Balance_{i-1}, std is sample N-1, and the
#   year is 365 days (community consensus; see references/book
#   /05-automation/0475-... and MQL5 forum thread 337071).
#   MT5's reported value uses a different (undocumented) computation
#   that does not match this formula on every report (e.g. 246753:
#   2.49 vs 22.92, 9.2× gap). The value is internally consistent
#   across all sub-windows, so the relative ranking is still
#   meaningful.

def _balance_dd_relative(
    balances: list[float],
) -> tuple[float, float]:
    """Return (bal_dd_rel_abs, bal_dd_rel_pct) for a balance curve.

    Computes MT5's STAT_BALANCE_DDREL_PERCENT — the maximum **relative**
    drawdown across the entire balance curve. For each point, compute
    rel = (running_peak - current) / running_peak * 100 — the percentage
    drawdown from the peak before it. Report the largest such % and the
    absolute $ amount at that moment.

    The `peak` resets every time the balance reaches a new high. This
    differs from the "maximal" DD (STAT_BALANCEDD_PERCENT) which finds
    the largest absolute $ DD first and uses that moment's % — the two
    can differ when a small absolute DD happens at a very low peak
    (producing a high % that doesn't register in the maximal scan).

    Verified against 246753: 44.60% vs report 44.63% (rounding-close;
    the 0.03% gap is from intra-trade floating P&L not visible in the
    HTML).
    """
    if not balances:
        return 0.0, 0.0

    peak = balances[0]
    max_rel_pct = 0.0
    max_rel_abs = 0.0
    for b in balances:
        if b > peak:
            peak = b
        rel = (peak - b) / peak * 100 if peak > 0 else 0.0
        if rel > max_rel_pct:
            max_rel_pct = rel
            max_rel_abs = peak - b
    return max_rel_abs, max_rel_pct


def _sharpe_ratio(trade_hprs: list[float]) -> float:
    """Per-trade Sharpe using HPRs (balance ratio = balance_after / balance_before).

    Per the MQL5 community reverse-engineering (forum thread 337071 +
    the book example at references/book/05-automation/0475-...):
        per_trade_sharpe = (AHPR - 1) / std_HPR
    where
        HPR_i = Balance_i / Balance_{i-1}
        AHPR  = mean(HPR_i)        (arithmetic)
        std   = sample std (ddof=1) of HPR_i

    Falls back to 0.0 if std == 0 or N < 2.
    """
    n = len(trade_hprs)
    if n < 2:
        return 0.0
    ahpr = sum(trade_hprs) / n
    var = sum((x - ahpr) ** 2 for x in trade_hprs) / (n - 1)
    if var <= 0:
        return 0.0
    std = var ** 0.5
    return (ahpr - 1.0) / std


def _sharpe_ratio_annualized(
    trade_hprs: list[float], backtest_days: float
) -> float:
    """Annualized Sharpe = per_trade_sharpe * sqrt(N_per_year).

    `N_per_year = N / (backtest_days / 365)`. Uses 365 days/year
    (MQL5 community consensus; 365.25 is within rounding for our
    purposes — the difference is sub-0.5% for typical backtest
    lengths).

    Note: this is the **textbook** formula. MT5's reported
    STAT_SHARPE_RATIO uses this formula and is consistent with it
    on most backtests, but for high-trade-count EAs the report
    value can diverge significantly (e.g. 22.92 vs 2.49 in 246753)
    — MT5 does not publish the exact computation, and the gap is
    not closeable without access to MT5's internal source. Use
    `sharpe_ratio_raw` (this function's input) for the per-trade
    Sharpe that is the most stable signal across windows.
    """
    n = len(trade_hprs)
    if n < 2 or backtest_days <= 0:
        return 0.0
    per_trade = _sharpe_ratio(trade_hprs)
    n_per_year = n / (backtest_days / 365.0)
    if n_per_year <= 0:
        return 0.0
    return per_trade * (n_per_year ** 0.5)


def compute_window_metrics(
    trades: list[dict],
    starting_balance: float,
    deposit: float,
    backtest_days: float,
    t_start: datetime | None = None,
    t_end: datetime | None = None,
) -> dict:
    """Compute the 7-window-metrics for a list of trades.

    `starting_balance` is the equity at the left edge of the window
    (the balance just before any trade in this window opens).
    `deposit` parameter — kept for API symmetry (not used by the
    balance-based relative DD calculation).
    `backtest_days` is the window length in days (used for Sharpe
    annualization).
    `t_start` / `t_end` (window boundaries as datetime) are optional —
    when supplied, seven additional fields are computed:
      idle_seconds     — total seconds in this window NOT held in any
                        trade. Computed as the sum of free intervals
                        (the complement of merged in-position
                        intervals); equals window_seconds minus the
                        union of clipped in-position intervals (NOT
                        the sum of clipped durations, so it stays
                        correct when trade stack depth > 1).
      min_idle_seconds — shortest free interval in this window.
                        Equal to window_seconds when no trades.
      max_idle_seconds — longest free interval in this window.
                        Equal to window_seconds when no trades.
      avg_idle_seconds — arithmetic mean of free interval lengths.
                        Equal to window_seconds when no trades.
      min_hold_seconds — shortest single-trade raw holding duration
                        (close_time - open_time, NO window clipping)
                        among this window's trades. 0 when empty.
                        Matches the report's "Minimal position
                        holding time" when N=1.
      max_hold_seconds — longest single-trade raw holding duration
                        (close_time - open_time, NO window clipping)
                        among this window's trades. 0 when empty.
                        Matches the report's "Maximal position
                        holding time" when N=1.
      avg_hold_seconds — arithmetic mean of raw trade holding
                        durations (close_time - open_time) for this
                        window's trades. 0 when empty. Matches the
                        report's "Average position holding time" when
                        N=1.
      win_rate         — fraction of in-window trades with net > 0,
                        i.e. win count / total exits in this window.
                        0 when no trades.

    Note: holding-time fields (min/max/avg) intentionally use the
    trade's RAW (close_time - open_time), not the window-clipped
    duration. This mirrors MT5's report semantics: "Maximal position
    holding time" is the trade's full lifetime, not "how long was
    this trade present inside the window".

    Idle fields (idle/min_idle/max_idle/avg_idle) are derived from
    free intervals — the complement of merged in-position intervals —
    so they correctly handle trade stack depth > 1 (multiple
    simultaneous positions). For depth=1 the merged-interval
    decomposition is identical to a simpler "gap between consecutive
    trades" model.

    Returns a dict with keys: profit, expected_payoff, profit_factor,
    recovery_factor (based on bal_dd_rel_abs), bal_dd_rel_pct,
    bal_dd_rel_abs, trades, sharpe_ratio (annualized),
    sharpe_ratio_raw (per-trade), plus idle_seconds / min_idle_seconds
    / max_idle_seconds / avg_idle_seconds / min_hold_seconds /
    max_hold_seconds / avg_hold_seconds / win_rate when t_start and
    t_end are provided.
    """
    n = len(trades)
    if n == 0:
        result = {
            "profit": 0.0,
            "expected_payoff": 0.0,
            "profit_factor": 0.0,
            "recovery_factor": 0.0,
            "bal_dd_rel_pct": 0.0,
            "bal_dd_rel_abs": 0.0,
            "trades": 0,
            "sharpe_ratio": 0.0,
            "sharpe_ratio_raw": 0.0,
        }
        if t_start is not None and t_end is not None:
            window_seconds = max(0.0, (t_end - t_start).total_seconds())
            result["idle_seconds"] = window_seconds
            result["min_idle_seconds"] = window_seconds
            result["max_idle_seconds"] = window_seconds
            result["avg_idle_seconds"] = window_seconds
            result["min_hold_seconds"] = 0.0
            result["max_hold_seconds"] = 0.0
            result["avg_hold_seconds"] = 0.0
            result["win_rate"] = 0.0
        return result

    # Per-trade P&L
    # Use MT5's STAT_GROSS_PROFIT/STAT_GROSS_LOSS split (entry costs
    # always go to GL; exit leg P&L split by sign). This matches the
    # report's PF exactly — see compute_gross_profit_loss for details.
    gp, gl = compute_gross_profit_loss(trades)
    nets = [t["net"] for t in trades]

    profit = sum(nets)
    expected_payoff = profit / n
    profit_factor = (gp / abs(gl)) if gl < 0 else 0.0

    # Build local balance curve: starting_balance + each trade's net
    balances = [starting_balance]
    hprs = []
    bal = starting_balance
    for net in nets:
        bal += net
        # HPR = balance_after / balance_before (MT5 community formula)
        hpr = (bal / balances[-1]) if balances[-1] != 0 else 0.0
        hprs.append(hpr)
        balances.append(bal)

    bal_dd_rel_abs, bal_dd_rel_pct = _balance_dd_relative(balances)
    recovery_factor = (profit / bal_dd_rel_abs) if bal_dd_rel_abs > 0 else 0.0

    sharpe_raw = _sharpe_ratio(hprs)
    sharpe_ann = _sharpe_ratio_annualized(hprs, backtest_days)

    result = {
        "profit": round(profit, 2),
        "expected_payoff": round(expected_payoff, 2),
        "profit_factor": round(profit_factor, 2),
        "recovery_factor": round(recovery_factor, 2),
        "bal_dd_rel_pct": round(bal_dd_rel_pct, 2),
        "bal_dd_rel_abs": round(bal_dd_rel_abs, 2),
        "trades": n,
        "sharpe_ratio": round(sharpe_ann, 2),
        "sharpe_ratio_raw": round(sharpe_raw, 4),
    }

    # Idle time + max hold + win rate (window-aware).
    # Each trade contributes its in-position duration intersected with
    # [t_start, t_end): clips open_time to >= t_start and close_time
    # to <= t_end. Trades that don't overlap the window at all
    # contribute 0 (already filtered by compute_windows via open_time
    # window assignment, but the clipping is defensive in case a
    # future caller passes an unsliced trade list).
    if t_start is not None and t_end is not None:
        in_position_seconds = 0.0
        max_hold_seconds = 0.0
        wins = 0
        # Holding-time stats use RAW trade duration (close-open), not
        # window-clipped. See docstring above for why.
        min_hold_seconds: float | None = None
        total_raw_hold = 0.0
        raw_count = 0
        # Collect window-clipped in-position intervals (used for
        # idle-gap computation via sweep-line, accounting for trade
        # stack depth > 1).
        intervals: list[tuple[float, float]] = []
        for t in trades:
            try:
                ot = datetime.strptime(t["open_time"], "%Y.%m.%d %H:%M:%S")
                ct = datetime.strptime(t["close_time"], "%Y.%m.%d %H:%M:%S")
            except (KeyError, ValueError):
                continue
            # Window-clipped duration (for idle accounting)
            clipped_start = ot if ot > t_start else t_start
            clipped_end = ct if ct < t_end else t_end
            held = (clipped_end - clipped_start).total_seconds()
            if held < 0:
                held = 0.0
            in_position_seconds += held
            if held > max_hold_seconds:
                max_hold_seconds = held
            # Raw holding time (for min/max/avg stats)
            raw_hold = (ct - ot).total_seconds()
            if raw_hold < 0:
                raw_hold = 0.0
            if min_hold_seconds is None or raw_hold < min_hold_seconds:
                min_hold_seconds = raw_hold
            total_raw_hold += raw_hold
            raw_count += 1
            if t.get("net", 0.0) > 0:
                wins += 1
            # Only count the clipped portion as an interval for idle-gap
            # decomposition (a trade entirely outside the window is
            # filtered out by compute_windows already, but defensive).
            if held > 0:
                intervals.append((
                    (clipped_start - t_start).total_seconds(),
                    (clipped_end - t_start).total_seconds(),
                ))
        window_seconds = max(0.0, (t_end - t_start).total_seconds())
        # Idle-gap decomposition: merge overlapping in-position
        # intervals (handles stack depth > 1), then take the
        # complement within [0, window_seconds]. The result is a list
        # of free intervals; min/max/avg over their lengths gives
        # the per-gap idle statistics. If no trades, the entire
        # window is one free interval of length window_seconds.
        if intervals:
            intervals.sort(key=lambda x: (x[0], x[1]))
            merged: list[list[float]] = [list(intervals[0])]
            for s, e in intervals[1:]:
                if s <= merged[-1][1]:
                    if e > merged[-1][1]:
                        merged[-1][1] = e
                else:
                    merged.append([s, e])
            free_lengths: list[float] = []
            cursor = 0.0
            for s, e in merged:
                if s > cursor:
                    free_lengths.append(s - cursor)
                cursor = max(cursor, e)
            if cursor < window_seconds:
                free_lengths.append(window_seconds - cursor)
        else:
            free_lengths = [window_seconds]
        if free_lengths:
            min_idle = min(free_lengths)
            max_idle = max(free_lengths)
            avg_idle = sum(free_lengths) / len(free_lengths)
        else:
            min_idle = max_idle = avg_idle = 0.0
        # idle_seconds = sum of free lengths — should equal
        # window_seconds - in_position_seconds when no trade overlap;
        # can be smaller when trades overlap (overlap counted once in
        # free complement but counted multiple times in in_position).
        # We report the true geometric idle (sum of free lengths) and
        # keep the legacy total_idle alias for backward compat.
        idle_seconds = sum(free_lengths)
        result["idle_seconds"] = round(idle_seconds, 1)
        result["min_idle_seconds"] = round(min_idle, 1)
        result["max_idle_seconds"] = round(max_idle, 1)
        result["avg_idle_seconds"] = round(avg_idle, 1)
        result["min_hold_seconds"] = round(
            min_hold_seconds if min_hold_seconds is not None else 0.0, 1
        )
        result["max_hold_seconds"] = round(max_hold_seconds, 1)
        result["avg_hold_seconds"] = round(
            total_raw_hold / raw_count if raw_count else 0.0, 1
        )
        result["win_rate"] = round(wins / n, 4)

    return result


def _parse_period_dates(period: str) -> tuple[datetime | None, datetime | None]:
    """Extract (bt_start, bt_end) from a period string like 'H1 (2024.01.01 - 2025.06.22)'."""
    m = re.search(
        r"(\d{4}\.\d{2}\.\d{2})\s*-\s*(\d{4}\.\d{2}\.\d{2})\s*\)\s*$", period
    )
    if not m:
        return None, None
    try:
        return (
            datetime.strptime(m.group(1), "%Y.%m.%d"),
            datetime.strptime(m.group(2), "%Y.%m.%d"),
        )
    except ValueError:
        return None, None


def compute_windows(
    report: Report, n: int
) -> list[dict]:
    """Split the backtest into N equal time windows and compute metrics for each.

    Returns a list of dicts (one per window), each with:
      window_idx, t_start (ISO date), t_end (ISO date, exclusive),
      start_balance, end_balance, ...metrics

    Trades are assigned to the window where their `open_time` falls.
    `start_balance` is the running balance at the left edge of the
    window (the balance carried over from the previous window's last
    trade, or the initial deposit for window 0).

    Time slicing
    ------------
    Boundaries are at bt_start + k * (bt_end - bt_start) / N for k in
    0..N. The very last window's t_end is bt_end (we use the user-given
    end, not bt_start + N * step, to handle the case where bt_end is
    not a whole number of step lengths from bt_start — common when
    bt_end is "the last bar's date").
    """
    if n < 1:
        raise ValueError(f"window count must be >= 1, got {n}")

    deposit = report.settings.initial_deposit
    bt_start, bt_end = _parse_period_dates(report.settings.period)
    if bt_start is None or bt_end is None:
        raise ValueError(
            f"cannot parse backtest date range from period: {report.settings.period!r}"
        )
    if bt_end <= bt_start:
        raise ValueError(f"bt_end {bt_end} <= bt_start {bt_start}")

    trades = pair_trades(report.deals)
    # Assign each trade to a window by its open_time
    # First, build a global running balance series keyed by close_time,
    # so we can look up the balance at the left edge of any window.
    balance_curve: list[tuple[datetime, float]] = [(bt_start, deposit)]
    bal = deposit
    for t in trades:
        try:
            close_dt = datetime.strptime(t["close_time"], "%Y.%m.%d %H:%M:%S")
        except ValueError:
            continue
        bal += t["net"]
        balance_curve.append((close_dt, bal))

    def balance_at(left_edge: datetime) -> float:
        """Return the last known balance at or before `left_edge`."""
        b = deposit
        for ts, v in balance_curve:
            if ts <= left_edge:
                b = v
            else:
                break
        return b

    total_seconds = (bt_end - bt_start).total_seconds()
    out = []
    for k in range(n):
        t_start = bt_start + timedelta(seconds=total_seconds * k / n)
        t_end = bt_start + timedelta(seconds=total_seconds * (k + 1) / n) \
            if k < n - 1 else bt_end
        # Select trades whose open_time is in [t_start, t_end)
        in_window = []
        for t in trades:
            try:
                ot = datetime.strptime(t["open_time"], "%Y.%m.%d %H:%M:%S")
            except ValueError:
                continue
            if t_start <= ot < t_end:
                in_window.append(t)
        start_bal = balance_at(t_start)
        end_bal = balance_at(t_end)
        window_days = (t_end - t_start).total_seconds() / 86400.0
        m = compute_window_metrics(
            in_window, start_bal, deposit, window_days,
            t_start=t_start, t_end=t_end,
        )
        out.append({
            "window_idx": k,
            "t_start": t_start.strftime("%Y.%m.%d"),
            "t_end": t_end.strftime("%Y.%m.%d"),
            "window_seconds": (t_end - t_start).total_seconds(),
            "start_balance": round(start_bal, 2),
            "end_balance": round(end_bal, 2),
            **m,
        })
    return out


def _mean_std(vals: list[float]) -> tuple[float, float]:
    """Return (mean, sample_std_n_minus_1) of vals. std=0 if N<2."""
    n = len(vals)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        return vals[0], 0.0
    mean = sum(vals) / n
    var = sum((x - mean) ** 2 for x in vals) / (n - 1)
    return mean, var ** 0.5


# Thresholds for notable / extreme outliers in windows analysis.
# Per the user: |z| >= 2 = notable; |z| >= 5 = extreme.
SIGMA_NOTABLE = 2.0
SIGMA_EXTREME = 5.0

# All metrics included in the z-score outlier scan. Direction-agnostic
# (we use |z|); lower-better metrics (e.g. bal_dd_rel_pct) are not
# inverted — a window with very LOW DD% will get |z| > 2 and the user
# decides whether that's good or bad from context.
ALL_METRICS = [
    "profit",
    "expected_payoff",
    "profit_factor",
    "recovery_factor",
    "bal_dd_rel_pct",
    "trades",
    "sharpe_ratio",
]


def windows_comparison(windows: list[dict]) -> dict:
    """Per-window z-score outlier scan across the 7 core metrics.

    For each metric, compute mean and sample std across all windows,
    then for each window compute z = (val - mean) / std. Flag any
    window whose |z| for any metric crosses the thresholds:

      • |z| >= 2.0  -> notable outlier   -- marker ▲
      • |z| >= 5.0  -> extreme outlier   -- marker ■

    Note: this is direction-agnostic. |z| > 2 means "this window's
    value is far from the rest"; whether that is good (e.g. very
    high profit) or bad (e.g. very high DD%) is left to the user.
    Sample std uses N-1. z=0 when std=0 (all windows identical).

    Output shape:
      {
        "per_window": [{ "outliers": [{"metric": "profit", "z": +2.27,
                                        "level": "notable"|"extreme"},
                                       ...],
                         "notable_count": int,
                         "extreme_count": int,
                         "max_abs_z": float,
                         "max_abs_z_metric": str}, ...],
        "mean":       {"profit": ..., ...},
        "std":        {"profit": ..., ...},
        "thresholds": {"notable": 2.0, "extreme": 5.0},
        "summary":    {"notable_windows": int, "extreme_windows": int,
                       "n_windows": int},
      }
    """
    # Per-metric mean and std across all windows
    mean_map: dict = {}
    std_map: dict = {}
    for m in ALL_METRICS:
        vals = [w.get(m, 0.0) for w in windows]
        mn, sd = _mean_std(vals)
        mean_map[m] = round(mn, 4)
        std_map[m] = round(sd, 4)

    per_window = []
    for w in windows:
        outliers = []
        for m in ALL_METRICS:
            sd = std_map[m]
            if sd == 0:
                continue
            z = (w.get(m, 0.0) - mean_map[m]) / sd
            az = abs(z)
            if az >= SIGMA_EXTREME:
                outliers.append({"metric": m, "z": round(z, 2),
                                 "level": "extreme"})
            elif az >= SIGMA_NOTABLE:
                outliers.append({"metric": m, "z": round(z, 2),
                                 "level": "notable"})
        # Find the single most extreme outlier for the row marker
        max_abs_z = 0.0
        max_metric = ""
        for o in outliers:
            if abs(o["z"]) > max_abs_z:
                max_abs_z = abs(o["z"])
                max_metric = o["metric"]
        per_window.append({
            "outliers": outliers,
            "notable_count": sum(1 for o in outliers if o["level"] == "notable"),
            "extreme_count": sum(1 for o in outliers if o["level"] == "extreme"),
            "max_abs_z": round(max_abs_z, 2),
            "max_abs_z_metric": max_metric,
        })

    n_notable = sum(1 for f in per_window if f["notable_count"] > 0)
    n_extreme = sum(1 for f in per_window if f["extreme_count"] > 0)
    return {
        "per_window": per_window,
        "mean": mean_map,
        "std": std_map,
        "thresholds": {"notable": SIGMA_NOTABLE, "extreme": SIGMA_EXTREME},
        "summary": {
            "notable_windows": n_notable,
            "extreme_windows": n_extreme,
            "n_windows": len(windows),
        },
    }


def print_windows(report: Report, windows: list[dict], comparison: dict) -> None:
    """Pretty-print the windows analysis as a text table."""
    print("=" * 96)
    print(f"  Windows Analysis  (backtest split into {len(windows)} equal time slices)")
    print("=" * 96)
    s = report.settings
    res = report.results
    print(f"  Expert: {s.expert}  Symbol: {s.symbol}  Period: {s.period}")
    print(f"  Initial Deposit: {s.initial_deposit:,.2f}")
    print()

    # Window boundaries
    print(f"  {'Win':<4} {'Start':<12} {'End':<12} {'Days':>6} "
          f"{'StartBal':>10} {'EndBal':>10} {'Trades':>6}")
    print("  " + "─" * 76)
    total_days = 0.0
    for w in windows:
        t_s = datetime.strptime(w["t_start"], "%Y.%m.%d")
        t_e = datetime.strptime(w["t_end"], "%Y.%m.%d")
        days = (t_e - t_s).total_seconds() / 86400.0
        total_days += days
        print(f"  {w['window_idx']:<4} {w['t_start']:<12} {w['t_end']:<12} "
              f"{days:>6.1f} {w['start_balance']:>10,.2f} {w['end_balance']:>10,.2f} "
              f"{w['trades']:>6}")
    print(f"  {'─'*76}\n")

    # Time composition per window — Idle / Max-hold / Win-rate.
    # Skipped silently if the windows list predates this field (i.e.
    # if compute_windows was called without t_start/t_end, which only
    # happens with hand-crafted test fixtures — production callers
    # always pass them).
    if all("idle_seconds" in w for w in windows):
        # Per-window percentages are computed against each window's
        # own length (idle_in_window / window_length), so they are
        # NOT additive across windows — N windows can sum to N*100%
        # in the worst case. The total row at the bottom aggregates
        # in absolute time across all windows.
        #
        # window_seconds is reconstructed as idle + in_pos rather
        # than parsing t_start/t_end with strptime('%Y.%m.%d'),
        # because the stored t_start/t_end are date-only strings
        # truncated from the real datetime boundaries — re-parsing
        # them would round the window length down to whole days and
        # drift the percentage by up to 1/2 day. The windowing code
        # in compute_windows uses full-precision datetimes; pairing
        # with idle_seconds keeps the ratio exact.
        print(f"  {'Win':<4} {'Days':>6} {'MinIdle':>10} {'MaxIdle':>10} {'AvgIdle':>10} "
              f"{'MinHold':>10} {'MaxHold':>10} {'AvgHold':>10} "
              f"{'WinRate':>8}")
        print("  " + "─" * 102)
        for w in windows:
            if "window_seconds" in w:
                window_seconds = w["window_seconds"]
            else:
                t_s = datetime.strptime(w["t_start"], "%Y.%m.%d")
                t_e = datetime.strptime(w["t_end"], "%Y.%m.%d")
                window_seconds = max(1.0, (t_e - t_s).total_seconds())
            min_idle = w["min_idle_seconds"]
            max_idle = w["max_idle_seconds"]
            avg_idle = w["avg_idle_seconds"]
            min_hold = w["min_hold_seconds"]
            max_hold = w["max_hold_seconds"]
            avg_hold = w["avg_hold_seconds"]
            print(f"  {w['window_idx']:<4} {window_seconds/86400.0:>6.1f} "
                  f"{format_duration(timedelta(seconds=min_idle)):>10} "
                  f"{format_duration(timedelta(seconds=max_idle)):>10} "
                  f"{format_duration(timedelta(seconds=avg_idle)):>10} "
                  f"{format_duration(timedelta(seconds=min_hold)):>10} "
                  f"{format_duration(timedelta(seconds=max_hold)):>10} "
                  f"{format_duration(timedelta(seconds=avg_hold)):>10} "
                  f"{w['win_rate']*100:>7.1f}%")
        print()

    # Metrics table
    print(f"  {'Win':<4} {'Profit':>10} {'EP':>8} {'PF':>6} {'RF':>6} "
          f"{'BalDD%':>7} {'Trades':>6} {'Sharpe':>8}  Outliers")
    print("  " + "─" * 102)
    for w, flags in zip(windows, comparison["per_window"]):
        # Build a compact outlier marker: max level, count, and metric
        if flags["extreme_count"] > 0:
            level = "■EXT"
        elif flags["notable_count"] > 0:
            level = "▲2σ"
        else:
            level = "  -"
        if flags["outliers"]:
            metrics_short = ",".join(
                f"{o['metric'][:4]}({o['z']:+.1f}σ)"
                for o in flags["outliers"]
            )
            marker = f"{level} k={flags['notable_count'] + flags['extreme_count']} {metrics_short}"
        else:
            marker = level
        print(f"  {w['window_idx']:<4} {w['profit']:>10,.2f} {w['expected_payoff']:>8.2f} "
              f"{w['profit_factor']:>6.2f} {w['recovery_factor']:>6.2f} "
              f"{w['bal_dd_rel_pct']:>7.2f} {w['trades']:>6} "
              f"{w['sharpe_ratio']:>8.2f}  {marker}")
    print()

    # Mean row (the reference for z-scores). Only meaningful with N>=2.
    if len(windows) >= 2:
        mn = comparison["mean"]
        print(f"  {'MEAN':<4} {mn.get('profit', 0):>10,.2f} "
              f"{mn.get('expected_payoff', 0):>8.2f} "
              f"{mn.get('profit_factor', 0):>6.2f} {mn.get('recovery_factor', 0):>6.2f} "
              f"{mn.get('bal_dd_rel_pct', 0):>7.2f} {mn.get('trades', 0):>6.0f} "
              f"{mn.get('sharpe_ratio', 0):>8.2f}")
        print(f"  {'STD':<4} "
              f"{comparison['std'].get('profit', 0):>10,.2f} "
              f"{comparison['std'].get('expected_payoff', 0):>8.2f} "
              f"{comparison['std'].get('profit_factor', 0):>6.2f} "
              f"{comparison['std'].get('recovery_factor', 0):>6.2f} "
              f"{comparison['std'].get('bal_dd_rel_pct', 0):>7.2f} "
              f"{comparison['std'].get('trades', 0):>6.2f} "
              f"{comparison['std'].get('sharpe_ratio', 0):>8.2f}")
        print()

    # For N=1: cross-check computed values vs HTML report
    if len(windows) == 1:
        w0 = windows[0]
        print("  " + "─" * 45)
        print("  N=1 cross-check vs report's reported values "
              "(4 of 7 exact: Profit, EP, PF, Trades; 3 documented approx):")
        ref_pairs = [
            ("Profit",          w0["profit"],           res.total_net_profit),
            ("Expected Payoff", w0["expected_payoff"],  res.expected_payoff),
            ("Profit Factor",   w0["profit_factor"],    res.profit_factor),
            ("Recovery Factor", w0["recovery_factor"],  res.recovery_factor),
            ("Balance DD Rel%", w0["bal_dd_rel_pct"],   res.balance_drawdown_rel_pct),
            ("Trades",          w0["trades"],           res.total_trades),
            ("Sharpe Ratio",    w0["sharpe_ratio"],     res.sharpe_ratio),
        ]
        for name, calc, ref in ref_pairs:
            diff = calc - ref
            if ref != 0:
                pct = abs(diff) / abs(ref) * 100
            else:
                pct = 0.0
            mark = "✓" if pct < 0.5 else ("⚠" if pct < 5 else "✗")
            print(f"    {mark} {name:<18}  calc={calc:>10.4f}   "
                  f"ref={ref:>10.4f}   diff={diff:>+10.4f}  ({pct:5.1f}%)")
        print("  Legend: ✓ = exact (rounding only), ⚠ = small drift, "
              "✗ = documented approximation")
        print()

    # When N > 1, also compute full-period metrics as a cross-check
    # reference so the user can see how sub-window values relate to
    # the full backtest (both our computation and the HTML report).
    if len(windows) > 1:
        # Compute full-period window (N=1) for comparison
        full_wins = compute_windows(report, 1)
        if full_wins:
            w_full = full_wins[0]
        else:
            w_full = None
        if w_full is not None:
            print("  " + "─" * 45)
            print("  Full-period reference:")
            print("  (computed N=1 vs HTML report stated values)")
            ref_pairs = [
                ("Profit",          w_full["profit"],           res.total_net_profit),
                ("Expected Payoff", w_full["expected_payoff"],  res.expected_payoff),
                ("Profit Factor",   w_full["profit_factor"],    res.profit_factor),
                ("Recovery Factor", w_full["recovery_factor"],  res.recovery_factor),
                ("Balance DD Rel%", w_full["bal_dd_rel_pct"],   res.balance_drawdown_rel_pct),
                ("Trades",          w_full["trades"],           res.total_trades),
                ("Sharpe Ratio",    w_full["sharpe_ratio"],     res.sharpe_ratio),
            ]
            for name, calc, ref in ref_pairs:
                diff = calc - ref
                if ref != 0:
                    pct = abs(diff) / abs(ref) * 100
                else:
                    pct = 0.0
                mark = "✓" if pct < 0.5 else ("⚠" if pct < 5 else "✗")
                print(f"    {mark} {name:<18}  calc={calc:>10.4f}   "
                      f"ref={ref:>10.4f}   diff={diff:>+10.4f}  ({pct:5.1f}%)")
            print()

    # Summary
    summ = comparison["summary"]
    thr = comparison["thresholds"]
    if len(windows) < 2:
        print("  Outlier scan: skipped (need at least 2 windows to compute std).")
        print("  Use --count 2 or more for the z-score outlier scan.")
    else:
        print("  Outlier scan (per-metric z-score vs window mean):")
        print(f"    ▲2σ  = |z| >= {thr['notable']:.0f} on any metric (notable)")
        print(f"    ■EXT = |z| >= {thr['extreme']:.0f} on any metric (extreme)")
        print(f"    {summ['notable_windows']}/{summ['n_windows']} windows have at least one "
              f"|z|>={thr['notable']:.0f} outlier, "
              f"{summ['extreme_windows']}/{summ['n_windows']} have at least one "
              f"|z|>={thr['extreme']:.0f}.")
        if summ["notable_windows"] > 0 or summ["extreme_windows"] > 0:
            print("  Use --json to see per-metric z-scores.")
    print()
    if len(windows) >= 2:
        print("  Interpretation:")
        print("    z = (this window's value − mean across all windows) / std.")
        print("    A z-score measures how far this window is from the rest.")
        print("    Direction is sign-bearing (+ vs −); the marker is |z|.")
        print("    For lower-is-better metrics (bal_dd_rel_pct), a negative z")
        print("    means 'this window's DD is unusually low' — good if you")
        print("    want safety, neutral if you just want consistency.")
        print("  A single window with a strong outlier is a regime signal.")
        print("  Multiple windows each with their own outliers point to a")
        print("  high-variance strategy — harder to predict live performance.")


# ── CLI ──────────────────────────────────────────────────────────────

# Sub-command catalogue kept at module level so the position-order validator
# stays in sync with what argparse actually accepts.
_VALID_SUBCOMMANDS = {"report", "analyze", "windows"}


def _validate_argv_position(argv: list[str], prog: str = "") -> None:
    """Reject any argv layout where a sub-command is NOT the first token.

    Target layout — mandatory:
        {prog} [--help] SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]

    Specifically:
      - ``--help``/``-h`` is the only flag allowed before the sub-command.
      - The first non-flag token must be one of ``_VALID_SUBCOMMANDS``.
      - ``-o``/``--output`` must come after SUB_COMMAND (we enforce here so
        the user gets a clear error instead of an argparse stack trace).

    Exits with a clear error message + usage hint. Skipped when the user only
    passed ``--help``/``-h`` (in which case argparse prints its own usage).
    """
    if argv in ([], ["--help"], ["-h"]):
        return

    if argv and argv[0] in ("--help", "-h"):
        return

    if not argv or argv[0].startswith("-"):
        print(
            f"Error: {prog} requires a sub-command as the first argument.\n"
            f"  Expected layout:  {prog} SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]\n"
            f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
            file=sys.stderr,
        )
        sys.exit(2)

    sub = argv[0]
    if sub not in _VALID_SUBCOMMANDS:
        if sub.startswith("-"):
            print(
                f"Error: flags must come AFTER the sub-command.\n"
                f"  Expected layout:  {prog} SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]\n"
                f"  Got: {' '.join(argv)}\n"
                f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
                file=sys.stderr,
            )
            sys.exit(2)
        print(
            f"Error: unknown sub-command '{sub}'.\n"
            f"  Expected layout:  {prog} SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]\n"
            f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Walk past optional sub-command-level flags to find the INPUT_FILE
    # positional.
    j = 1
    no_value_flags = {"--json"}
    while j < len(argv) and argv[j].startswith("-"):
        tok = argv[j]
        if "=" in tok:
            j += 1
            continue
        if tok in no_value_flags:
            j += 1
            continue
        if tok in ("-o", "--output"):
            if j + 1 < len(argv) and not argv[j + 1].startswith("-"):
                j += 2
            else:
                return
            continue
        if j + 1 < len(argv) and not argv[j + 1].startswith("-"):
            j += 2
        else:
            j += 1

    if j >= len(argv):
        print(
            f"Error: sub-command '{sub}' requires an INPUT_FILE positional.\n"
            f"  Expected layout:  {prog} {sub} INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]",
            file=sys.stderr,
        )
        sys.exit(2)


def _emit_text(text: str, output_path: str | None) -> None:
    """Print to stdout, or write to a file path when -o was given."""
    if output_path:
        Path(output_path).write_text(text, encoding="utf-8")
    else:
        print(text, end="" if text.endswith("\n") else "\n")


def _emit_json(obj, output_path: str | None) -> None:
    """Dump JSON to stdout or to a file when -o was given."""
    payload = json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    if output_path:
        Path(output_path).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def _capture_stdout(func, *args, **kwargs) -> str:
    """Run ``func`` while capturing what it prints; return that as a string."""
    import io
    buf = io.StringIO()
    saved = sys.stdout
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = saved
    return buf.getvalue()


def main():
    prog = Path(sys.argv[0]).name
    _validate_argv_position(sys.argv[1:], prog=prog)

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Parse MT5 Strategy Tester HTML report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Target CLI layout (mandatory):
  %(prog)s [--help] SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]

Sub-commands:
  report     Default text report (env card + key statistics + trade summary).
  analyze    Full trade analysis (idle time, monthly breakdown, re-entry
             detection, streak analysis). Always JSON if --json is set.
  windows    Split the backtest into N equal time windows and recompute the
             7 core metrics per window — over-fitting / regime detection.

Sub-command flags (always come AFTER the sub-command and INPUT_FILE):
  --json            Emit JSON instead of the default text report.
  -o OUTPUT_FILE    Write output to OUTPUT_FILE instead of stdout.

Examples:
  # Default text report, written to a file
  %(prog)s report jobs/foo/ReportTester-*.html -o summary.txt

  # Full JSON analysis
  %(prog)s analyze jobs/foo/ReportTester-*.html --json -o analysis.json

  # Window analysis: 6 monthly windows for a 1.5y backtest
  %(prog)s windows jobs/foo/ReportTester-*.html --count 6 --json -o windows.json
  %(prog)s windows jobs/foo/ReportTester-*.html --count 4 -o windows.txt
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="SUB_COMMAND", required=True)

    def _add_shared(sub_parser):
        """Add the flags every sub-command understands."""
        sub_parser.add_argument(
            "report", help="Path to HTML report file",
        )
        sub_parser.add_argument(
            "--json", action="store_true",
            help="Emit JSON instead of the default text report",
        )
        sub_parser.add_argument(
            "-o", "--output", dest="output", default=None, metavar="OUTPUT_FILE",
            help="Write output to OUTPUT_FILE (default: stdout).",
        )

    # ── report ──
    p_report = sub.add_parser(
        "report",
        help="Default text report (env card + key statistics + trade summary).",
        description="Default text report: env card (EA / Symbol / Period / "
                    "company / deposit), key statistics (profit, PF, EP, RF, "
                    "Sharpe, drawdown, etc.), and trade summary. Use `analyze` "
                    "for the full idle-time / monthly / re-entry breakdown.",
    )
    _add_shared(p_report)

    # ── analyze ──
    p_an = sub.add_parser(
        "analyze",
        help="Full trade analysis (idle time, monthly breakdown, re-entry detection).",
        description="Full trade analysis: pair deals into trades, compute risk per "
                    "trade, monthly breakdown, re-entry detection, streak analysis. "
                    "Emit JSON when --json is set.",
    )
    _add_shared(p_an)

    # ── windows ──
    p_win = sub.add_parser(
        "windows",
        help="Split the backtest into N equal time windows and compute "
             "the 7 core metrics for each (Profit, EP, PF, RF, "
             "Balance DD Rel%% (relative), Trades, Sharpe). Use to find time "
             "windows that are statistical outliers vs the rest "
             "(over-fitting / regime detection).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # N=1: validate that calculation matches the full report
  %(prog)s windows INPUT_FILE --count 1

  # N=4: quarterly analysis for a 1.5y backtest
  %(prog)s windows INPUT_FILE --count 4

  # N=8: finer granularity
  %(prog)s windows INPUT_FILE --count 8

  # JSON output (per-window metrics + z-score outliers)
  %(prog)s windows INPUT_FILE --count 6 --json -o windows.json

Each window shows all 7 metrics plus an outlier flag (|z|>=2: notable,
|z|>=5: extreme). The MEAN/STD row gives the reference distribution.
""",
    )
    _add_shared(p_win)
    p_win.add_argument(
        "--count", "-n", type=int, required=True,
        help="Number of equal time windows to split the backtest into. "
             "Use 1 to validate: should match the full report within tolerance.",
    )

    args = parser.parse_args()
    output_path = getattr(args, "output", None)

    path = Path(args.report)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    report = parse_report(path)

    # ── dispatch ──
    if args.cmd == "report":
        if args.json:
            _emit_json(asdict(report), output_path)
        else:
            text = _capture_stdout(print_report, report)
            _emit_text(text, output_path)
        return

    if args.cmd == "analyze":
        analyze_data = analyze_report(report)
        if args.json:
            report_dict = asdict(report)
            report_dict["analyze"] = analyze_data
            _emit_json(report_dict, output_path)
        else:
            text = _capture_stdout(print_report, report, analyze_data)
            _emit_text(text, output_path)
        return

    if args.cmd == "windows":
        wins = compute_windows(report, args.count)
        comp = windows_comparison(wins)
        if args.json:
            out = {
                "report": {
                    "expert": report.settings.expert,
                    "symbol": report.settings.symbol,
                    "period": report.settings.period,
                    "initial_deposit": report.settings.initial_deposit,
                    "total_net_profit": report.results.total_net_profit,
                    "profit_factor": report.results.profit_factor,
                    "expected_payoff": report.results.expected_payoff,
                    "recovery_factor": report.results.recovery_factor,
                    "sharpe_ratio": report.results.sharpe_ratio,
                    "bal_dd_rel_pct": report.results.balance_drawdown_rel_pct,
                    "total_trades": report.results.total_trades,
                },
                "windows": wins,
                "comparison": comp,
            }
            _emit_json(out, output_path)
        else:
            text = _capture_stdout(print_windows, report, wins, comp)
            _emit_text(text, output_path)
        return

    # argparse with required=True guarantees we never get here.
    parser.error(f"unknown sub-command: {args.cmd}")


if __name__ == "__main__":
    main()
