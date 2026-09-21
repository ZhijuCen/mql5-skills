#!/usr/bin/env python3
"""Analyze an MQL5 signal positions CSV export (trade history).

Source of the file
------------------
mql5.com signal detail page -> "Trading history" tab -> "Export to CSV: History"
downloads  `/en/signals/<signal_id>/export/positions`  (login required,
subscription NOT required — the export is richer than the web view).

File format (verified on signal 2271402, 2026-09)
--------------------------------------------------
* UTF-8 with BOM, semicolon-separated, CRLF-ish lines.
* 11-column header:
      Time;Type;Volume;Symbol;Price;Volume;Time;Price;Commission;Swap;Profit
* Deal rows: Type in {Buy, Sell}; Time(open)..Price(close) describe the round
  trip.  Profit does NOT include Commission/Swap (they are separate columns,
  stored negative).  Net p&l = Profit + Commission + Swap.
* Other rows (Type = Balance / Deposit / Withdrawal / Credit / Adjustment ...)
  carry balance operations; their last field is the balance delta.
* Times are `YYYY.MM.DD HH:MM:SS` (dot-separated date, space-separated time).

What this script computes
-------------------------
* reconciliation vs the detail-page figures (trades, profit) when provided
* per-year profile  -> detects strategy shifts (trade count / lot / duration)
* per-symbol p&l    -> separates profit core from experimental additions
* monthly net p&l   -> finds the loss months
* tail risk         -> worst-k sums, loss concentration
* chronological losing streaks
* holding pattern   -> quantifies the "win small / hold losers" (dead-hang) signature
* recent window     -> current regime check
* funding forensics -> deposits/withdrawals from balance ops (capital injection?)
* auto red flags

Usage
-----
python skills/mql-signals/scripts/analyze_signals_csv.py <positions.csv> [options]

Options:
  --page-trades N     total trades shown on the detail page (reconciliation)
  --page-profit X     total profit shown on the detail page, e.g. 7120.51
  --page-win N        winning trades shown on the detail page
  --min-held-days N   holding-pattern threshold (default 5)
  --recent-days N     recent-window length by close date (default 90)
  --from-month M       first month to print in the monthly table (default 2024.01)
  --json               machine-readable JSON dump (any sub-output)
  -o FILE              write report (text or JSON) to FILE
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime
import json
import statistics
import sys

DEAL_TYPES = {"Buy", "Sell"}
BALANCE_TYPES = {"Balance", "Deposit", "Withdrawal", "Credit", "Adjustment", "Fee", "Tax", "Bonus"}
HDR = ["Time", "Type", "Volume", "Symbol", "Price", "Volume", "Time", "Price", "Commission", "Swap", "Profit"]
# indices into a parsed row
I_TIME_OPEN, I_TYPE, I_VOL, I_SYM, I_PX_OPEN, _, I_TIME_CLOSE, I_PX_CLOSE, I_COMM, I_SWAP, I_PNL = range(11)


def _f(x: str) -> float:
    try:
        return float(str(x).strip())
    except (TypeError, ValueError):
        return 0.0


def _date(s: str) -> datetime.date:
    return datetime.date(*map(int, s[:10].split(".")))


def load_rows(path: str):
    """Return (deals, balance_ops): parsed rows from the export."""
    with open(path, encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    data = rows[1:] if len(rows) > 1 and rows[0] and "Type" in rows[0][0] else rows
    deals, ops = [], []
    for r in data:
        if len(r) < 9:
            continue
        t = r[I_TYPE].strip()
        if t in DEAL_TYPES:
            if len(r) >= 11:
                deals.append(r)
        elif t in BALANCE_TYPES:
            ops.append(r)
    # numeric coercion for deals
    for d in deals:
        d[I_VOL] = float(d[I_VOL])
        d[I_COMM], d[I_SWAP], d[I_PNL] = _f(d[I_COMM]), _f(d[I_SWAP]), _f(d[I_PNL])
        d[I_PX_OPEN], d[I_PX_CLOSE] = _f(d[I_PX_OPEN]), _f(d[I_PX_CLOSE])
        d[I_TIME_OPEN] = d[I_TIME_OPEN].strip()[:19]
        d[I_TIME_CLOSE] = d[I_TIME_CLOSE].strip()[:19]
    return deals, ops


def holding_days(d) -> int:
    return (_date(d[I_TIME_CLOSE]) - _date(d[I_TIME_OPEN])).days


def analyze(deals, ops, min_held=5, recent_days=90, from_month="2024.01",
            page_trades=None, page_profit=None, page_win=None):
    out = {}
    n = len(deals)
    pnl_gross = sum(d[I_PNL] for d in deals)
    comm = sum(d[I_COMM] for d in deals)
    swap = sum(d[I_SWAP] for d in deals)
    net = pnl_gross + comm + swap
    wins = [d for d in deals if d[I_PNL] > 0]
    losses = [d for d in deals if d[I_PNL] <= 0]
    ordered = sorted(deals, key=lambda d: d[I_TIME_CLOSE])
    out["summary"] = {
        "deals": n, "open_span": min(d[I_TIME_OPEN] for d in deals)[:10],
        "close_span": max(d[I_TIME_CLOSE] for d in deals)[:10],
        "pnl_gross_excl_costs": round(pnl_gross, 2),
        "commission": round(comm, 2), "swap": round(swap, 2),
        "net_incl_costs": round(net, 2),
        "win": len(wins), "loss": len(losses),
        "win_pct": round(100 * len(wins) / n, 2),
        "best": round(max(d[I_PNL] for d in deals), 2),
        "worst": round(min(d[I_PNL] for d in deals), 2),
    }
    if page_trades is not None or page_profit is not None or page_win is not None:
        rec = {}
        if page_trades is not None:
            rec["trades_hidden"] = page_trades - n
        if page_profit is not None:
            rec["profit_diff_vs_page"] = round(net - page_profit, 2)
        if page_win is not None:
            rec["win_rows_vs_page"] = len(wins) - page_win
        out["reconciliation"] = rec

    # balance ops / funding forensics
    funding = collections.defaultdict(float)
    for r in ops:
        funding[r[I_TYPE].strip()] += _f(r[-1])
    out["funding"] = {k: round(v, 2) for k, v in sorted(funding.items())}

    # per year
    years = collections.defaultdict(list)
    for d in deals:
        years[d[I_TIME_OPEN][:4]].append(d)
    year_rows = []
    for y in sorted(years):
        yl = years[y]
        durs = [holding_days(d) for d in yl]
        year_rows.append({
            "year": y, "n": len(yl),
            "avg_lot": round(statistics.mean(d[I_VOL] for d in yl), 3),
            "median_dur_days": statistics.median(durs),
            "sum_lot": round(sum(d[I_VOL] for d in yl), 2),
            "net": round(sum(d[I_PNL] for d in yl) + sum(d[I_COMM] for d in yl) + sum(d[I_SWAP] for d in yl), 2),
        })
    out["by_year"] = year_rows

    # per symbol
    syms = collections.defaultdict(list)
    for d in deals:
        syms[d[I_SYM]].append(d)
    out["by_symbol"] = [
        {"symbol": s, "n": len(v),
         "net": round(sum(d[I_PNL] for d in v) + sum(d[I_COMM] for d in v) + sum(d[I_SWAP] for d in v), 2)}
        for s, v in sorted(syms.items(), key=lambda kv: -len(kv[1]))
    ]

    # monthly
    months = collections.defaultdict(list)
    for d in deals:
        months[d[I_TIME_OPEN][:7]].append(d)
    out["by_month"] = [
        {"month": m, "n": len(v),
         "net": round(sum(d[I_PNL] for d in v) + sum(d[I_COMM] for d in v) + sum(d[I_SWAP] for d in v), 2)}
        for m, v in sorted(months.items()) if m >= from_month
    ]

    # tail risk
    pns = sorted(d[I_PNL] for d in deals)
    tails = {}
    for k in (5, 10, 20, 50, 100):
        if k <= n:
            tails[str(k)] = {"sum": round(sum(pns[:k]), 2), "threshold": round(pns[k - 1], 2)}
    losers_total = sum(x for x in pns if x < 0)
    winners_total = sum(x for x in pns if x > 0)
    tail1 = max(1, n // 100)
    tails["worst_1pct"] = {"n": tail1, "sum": round(sum(pns[:tail1]), 2),
                           "share_of_all_losses": round(100 * sum(pns[:tail1]) / losers_total, 1) if losers_total else None}
    out["tail"] = {"worst_k": tails, "losers_total": round(losers_total, 2), "winners_total": round(winners_total, 2)}

    # streaks (chronological by close)
    streak = mx_streak = streak_end = 0
    for d in ordered:
        if d[I_PNL] <= 0:
            streak += 1
            if streak > mx_streak:
                mx_streak, streak_end = streak, d[I_TIME_CLOSE]
        else:
            streak = 0
    out["max_consecutive_losses"] = {"count": mx_streak, "ended": streak_end}

    # holding pattern
    held = [(d, holding_days(d)) for d in deals]
    held_n = [(d, du) for d, du in held if du >= min_held]
    held_wins = [d[I_PNL] for d, _ in held_n if d[I_PNL] > 0]
    held_losses = [d[I_PNL] for d, _ in held_n if d[I_PNL] <= 0]
    out["holding"] = {
        "min_held_days": min_held,
        "n": len(held_n),
        "win": len(held_wins), "loss": len(held_losses),
        "net": round(sum(held_wins) + sum(held_losses), 2),
        "sum_wins": round(sum(held_wins), 2), "sum_losses": round(sum(held_losses), 2),
    }

    # recent window (by close date)
    if deals:
        last = _date(max(d[I_TIME_CLOSE] for d in deals))
        cut = last - datetime.timedelta(days=recent_days)
        recent = [d for d in deals if _date(d[I_TIME_CLOSE]) >= cut]
        out["recent"] = {"days": recent_days, "n": len(recent),
                         "net": round(sum(d[I_PNL] for d in recent) + sum(d[I_COMM] for d in recent) + sum(d[I_SWAP] for d in recent), 2)}
    return out


def flags(a: dict) -> list[str]:
    """Auto-detected red flags; each item is one printable line."""
    fl = []
    y = a["by_year"]
    if len(y) >= 2:
        prev = y[0]
        for r in y[1:]:
            reasons = []
            if r["n"] >= 3 * prev["n"]:
                reasons.append(f"deals {prev['n']}->{r['n']}")
            if r["avg_lot"] >= 3 * max(prev["avg_lot"], 0.001) or prev["avg_lot"] >= 3 * max(r["avg_lot"], 0.001):
                reasons.append(f"avg_lot {prev['avg_lot']}->{r['avg_lot']}")
            dur = r["median_dur_days"]; pd = prev["median_dur_days"]
            if (dur == 0 and pd >= 2) or (pd == 0 and dur >= 2):
                reasons.append(f"holding {pd}d->{dur}d")
            if len(reasons) >= 2:
                fl.append(f"[strategy shift?] {r['year']}: " + ", ".join(reasons))
            prev = r
    s = a["summary"]
    if s["win_pct"] >= 90 and s["worst"] < -50 and s["net"] < 0:
        fl.append("[high-win-rate trap] >90% win rate but net negative — tail risk dominates")
    if a["holding"]["net"] < 0 and a["holding"]["n"] >= 20:
        h = a["holding"]
        fl.append(f"[dead-hang signature] trades held >= {h['min_held_days']}d net {h['net']:+.2f} "
                  f"(wins {h['sum_wins']:+.2f} / losses {h['sum_losses']:+.2f}) — winners cut, losers held")
    t = a["tail"]
    one = t["worst_k"].get("worst_1pct", {})
    if one.get("share_of_all_losses") and one["share_of_all_losses"] >= 25:
        fl.append(f"[tail concentration] worst 1% of trades carry {one['share_of_all_losses']}% of all losses")
    fnd = a["funding"]
    dep = fnd.get("Deposit", 0.0) + fnd.get("Balance", 0.0)
    wd = fnd.get("Withdrawal", 0.0)
    if dep > 0 and wd <= 0:
        fl.append(f"[funding] net deposits +{dep:+.2f}, zero withdrawals — possible capital masking")
    vol = [r["sum_lot"] for r in y]
    if len(vol) >= 2 and max(vol) >= 8 * statistics.median(vol + [0]):
        fl.append(f"[activity spike] yearly volume jumps to {max(vol):.0f} lots (median year {statistics.median(vol):.0f})")
    return fl


def render(a: dict, flags_: list[str], min_held: int) -> str:
    S = a["summary"]
    L = []
    L.append(f"deals            {S['deals']}   span {S['open_span']} .. {S['close_span']}")
    L.append(f"pnl gross        {S['pnl_gross_excl_costs']:+.2f}  (excl. costs)")
    L.append(f"commission/swap  {S['commission']:+.2f} / {S['swap']:+.2f}")
    L.append(f"NET              {S['net_incl_costs']:+.2f}")
    L.append(f"win/loss         {S['win']} / {S['loss']}  ({S['win_pct']}%)   best {S['best']:+.2f} / worst {S['worst']:+.2f}")
    if "reconciliation" in a:
        r = a["reconciliation"]
        L.append("reconciliation: " + " | ".join(f"{k} = {v}" for k, v in r.items()))
    fnd = a.get("funding") or {}
    if fnd:
        L.append("funding ops: " + ", ".join(f"{k} {v:+.2f}" for k, v in fnd.items()))
    L.append("\n-- per year (n, avgLot, medDurDays, sumLot, net) --")
    for r in a["by_year"]:
        L.append(f"  {r['year']}  n={r['n']:5d}  lot={r['avg_lot']:.3f}  medDur={r['median_dur_days']:2.0f}d  "
                 f"sumLot={r['sum_lot']:8.2f}  net={r['net']:+10.2f}")
    L.append("\n-- per symbol --")
    for r in a["by_symbol"]:
        L.append(f"  {r['symbol']:8s} n={r['n']:5d}  net={r['net']:+10.2f}")
    L.append("\n-- monthly net (from %s) --" % (a["by_month"][0]["month"] if a["by_month"] else "-"))
    for r in a["by_month"]:
        L.append(f"  {r['month']}  n={r['n']:4d}  net={r['net']:+9.2f}")
    L.append("\n-- tail risk (worst k) --")
    for k, v in a["tail"]["worst_k"].items():
        L.append(f"  worst {k:>9s}: sum={v['sum']:+10.2f} (threshold {v.get('threshold', ''):>8})".rstrip())
    t = a["tail"]
    L.append(f"  all losers {t['losers_total']:+.2f}  all winners {t['winners_total']:+.2f}")
    mc = a["max_consecutive_losses"]
    L.append(f"max consecutive losing trades (chron., pnl<=0): {mc['count']} (ended {mc['ended']})")
    h = a["holding"]
    L.append(f"\nholding >= {min_held}d: n={h['n']}  win={h['win']} loss={h['loss']}  "
             f"net={h['net']:+.2f} (wins {h['sum_wins']:+.2f} / losses {h['sum_losses']:+.2f})")
    if "recent" in a:
        r = a["recent"]
        L.append(f"recent {r['days']}d: n={r['n']}  net={r['net']:+.2f}")
    if flags_:
        L.append("\n-- flagged --")
        L.extend("  " + x for x in flags_)
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="MQL5 signal positions CSV analyzer")
    ap.add_argument("csv", help="path to the exported positions CSV")
    ap.add_argument("--page-trades", type=int, default=None)
    ap.add_argument("--page-profit", type=float, default=None)
    ap.add_argument("--page-win", type=int, default=None)
    ap.add_argument("--min-held-days", type=int, default=5)
    ap.add_argument("--recent-days", type=int, default=90)
    ap.add_argument("--from-month", default="2024.01")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-o", "--output", default=None)
    args = ap.parse_args()

    deals, ops = load_rows(args.csv)
    if not deals:
        print("no Buy/Sell rows found — is this a positions export?", file=sys.stderr)
        return 2
    a = analyze(deals, ops, min_held=args.min_held_days, recent_days=args.recent_days,
                from_month=args.from_month, page_trades=args.page_trades,
                page_profit=args.page_profit, page_win=args.page_win)
    fl = flags(a)

    if args.json:
        payload = {"analysis": a, "flags": fl}
        text = json.dumps(payload, indent=2, ensure_ascii=False)
    else:
        text = render(a, fl, args.min_held_days)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())