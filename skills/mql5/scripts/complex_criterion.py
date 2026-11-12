#!/usr/bin/env python3
"""Compute MetaTrader 5's Strategy Tester "Complex Criterion" from a backtest report.

MT5's ``OptimizationCriterion=7`` ("Complex Criterion max") is a 0-100 quality
score that MetaQuotes does not document.  This script implements the
reverse-engineered model described in
``skills/mql5/references/quick-ref-complex-criterion.md``:

    cc = 100 * sigma((trades - 40) / 5) * (0.2 * sigma((20 - eq_dd_pct) / 2.5)
                                           + Qo)

    Qo = B0 + G_rf(rf) + G_sr(sr) + G_pf(pf) + G_wr(win_rate)

``sigma`` is the logistic function, ``G_*`` are monotone piecewise-linear
tables (calibrated; see the reference), ``eq_dd_pct`` is
``STAT_EQUITY_DDREL_PERCENT`` (Equity Drawdown Relative, %).

Sub-commands::

    # single-test HTML report -> one number
    complex_criterion.py report ReportTester-*.html

    # optimizer XML -> per-pass table (uses only the 8 statistics the XML has)
    complex_criterion.py xml ReportOptimizer-*.xml [--limit N]

    # optimizer XML -> accuracy of the model against MT5's own Result column
    complex_criterion.py validate ReportOptimizer-*.xml

All sub-commands accept ``--json`` and ``-o FILE``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --------------------------------------------------------------------------- #
# Model constants (calibrated 2026-11-12, see quick-ref-complex-criterion.md) #
# --------------------------------------------------------------------------- #

#: Reference number of trades and its logistic scale.
TRADES_REF = 40.0
TRADES_SCALE = 5.0
#: Reference equity drawdown (%) and its logistic scale.
DD_REF = 20.0
DD_SCALE = 2.5
#: Weight of the drawdown term inside the quality sum.
DD_WEIGHT = 0.2
#: Constant of the quality sum (floor of the composite part).
QO_INTERCEPT = 0.033549
#: Win-rate term used when the report does not expose win/loss trade counts.
WR_SATURATED = 0.034419

#: Monotone piecewise-linear tables: knots (ascending) -> cumulative value.
TABLES: dict[str, tuple[list[float], list[float]]] = {
    "rf": (
        [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 12, 20],
        [0.0, 0.001134, 0.001134, 0.005878, 0.057284, 0.139133, 0.191628,
         0.204263, 0.2113, 0.214347, 0.216254, 0.217402, 0.217823, 0.218346,
         0.218699],
    ),
    "sr": (
        [-5, 0, 1, 2, 3, 4, 5, 6, 8, 10, 14, 20, 30, 50],
        [0.0, 0.006065, 0.033579, 0.133485, 0.140756, 0.140756, 0.140756,
         0.140756, 0.140756, 0.140756, 0.140756, 0.140756, 0.140756,
         0.140756],
    ),
    "pf": (
        [0.4, 0.8, 0.95, 1.0, 1.03, 1.06, 1.09, 1.12, 1.16, 1.2, 1.3, 1.45,
         1.6, 1.8, 2.1, 2.5, 3, 4, 6, 10, 50],
        [0.0, 0.002586, 0.002586, 0.002586, 0.023639, 0.050151, 0.068429,
         0.084547, 0.098994, 0.120444, 0.164252, 0.228346, 0.298865,
         0.348491, 0.368401, 0.371943, 0.374888, 0.375676, 0.376388,
         0.377683, 0.380914],
    ),
    "wr": (
        [0.1, 0.3, 0.38, 0.42, 0.45, 0.47, 0.49, 0.51, 0.53, 0.56, 0.6],
        [0.0, 0.002316, 0.003991, 0.007871, 0.020929, 0.039201, 0.066796,
         0.095948, 0.12452, 0.148727, 0.170006],
    ),
}

#: Statistics the optimizer XML exposes (everything else is unavailable there).
XML_STATS = (
    "Pass", "Result", "Profit", "Expected Payoff", "Profit Factor",
    "Recovery Factor", "Sharpe Ratio", "Custom", "Equity DD %", "Trades",
)


# --------------------------------------------------------------------------- #
# Core model                                                                  #
# --------------------------------------------------------------------------- #

def _sigma(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def _table(name: str, value: float) -> float:
    """Linear interpolation on a calibrated table (flat outside the knots)."""
    knots, vals = TABLES[name]
    if value <= knots[0]:
        return vals[0]
    if value >= knots[-1]:
        return vals[-1]
    for i in range(len(knots) - 1):
        if value <= knots[i + 1]:
            span = knots[i + 1] - knots[i]
            frac = 0.0 if span == 0 else (value - knots[i]) / span
            return vals[i] + frac * (vals[i + 1] - vals[i])
    return vals[-1]


def quality_sum(
    *,
    recovery_factor: float,
    sharpe: float,
    profit_factor: float,
    win_rate: float | None = None,
) -> float:
    """Qo = B0 + G_rf + G_sr + G_pf + G_wr  (bounded ~0.03 .. ~0.94)."""
    qo = QO_INTERCEPT
    qo += _table("rf", recovery_factor)
    qo += _table("sr", sharpe)
    qo += _table("pf", profit_factor)
    qo += WR_SATURATED if win_rate is None else _table("wr", win_rate)
    return qo


def complex_criterion(
    *,
    trades: int,
    equity_dd_pct: float,
    recovery_factor: float,
    sharpe: float,
    profit_factor: float,
    win_rate: float | None = None,
) -> float:
    """Return the Complex Criterion on MT5's 0..100 scale (unrounded).

    ``win_rate`` is ``profit_trades / (profit_trades + loss_trades)``.  Pass
    ``None`` when the source report does not expose the win/loss trade split
    (an optimizer XML does not); the calibrated average is used instead, which
    costs accuracy (see the reference document).
    """
    s_trades = _sigma((trades - TRADES_REF) / TRADES_SCALE)
    s_dd = _sigma((DD_REF - equity_dd_pct) / DD_SCALE)
    qo = quality_sum(
        recovery_factor=recovery_factor,
        sharpe=sharpe,
        profit_factor=profit_factor,
        win_rate=win_rate,
    )
    # The four quality tables can sum marginally above 1.0 on a perfect pass;
    # MT5's scale is capped at 100 (observed maximum 99.97).
    return min(100.0, 100.0 * s_trades * (DD_WEIGHT * s_dd + qo))


# --------------------------------------------------------------------------- #
# Optimizer XML (SpreadsheetML) reader                                        #
# --------------------------------------------------------------------------- #

_SS = "{urn:schemas-microsoft-com:office:spreadsheet}"


def read_optimizer_xml(path: Path) -> tuple[list[str], list[dict]]:
    """Return (header, rows) from a ReportOptimizer-*.xml SpreadsheetML file."""
    root = ET.parse(path).getroot()
    rows = list(root.iter(_SS + "Row"))
    if not rows:
        raise SystemExit(f"{path}: no rows found")
    header: list[str] = []
    for cell in rows[0]:
        data = cell.find(_SS + "Data")
        header.append((data.text if data is not None else "") or "")
    out: list[dict] = []
    for row in rows[1:]:
        rec: dict = {}
        for name, cell in zip(header, row):
            data = cell.find(_SS + "Data")
            rec[name] = None if data is None else data.text
        out.append(rec)
    return header, out


def _num(value, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(value)
    except ValueError:
        return default


def xml_row_criterion(rec: dict) -> float:
    """Compute the criterion from an optimizer-XML pass row."""
    return complex_criterion(
        trades=int(_num(rec.get("Trades"))),
        equity_dd_pct=_num(rec.get("Equity DD %")),
        recovery_factor=_num(rec.get("Recovery Factor")),
        sharpe=_num(rec.get("Sharpe Ratio")),
        profit_factor=_num(rec.get("Profit Factor")),
        win_rate=None,  # the optimizer XML has no win/loss trade counts
    )


# --------------------------------------------------------------------------- #
# Single-test HTML report reader                                              #
# --------------------------------------------------------------------------- #

def html_report_criterion(path: Path) -> dict:
    """Compute the criterion from a single-test ReportTester-*.html file."""
    from parse_tester_report import parse_report  # local module, needs bs4

    rep = parse_report(path)
    res = rep.results
    trades = res.total_trades
    wins, losses = res.profit_trades, res.loss_trades
    win_rate = wins / (wins + losses) if (wins + losses) else None
    value = complex_criterion(
        trades=trades,
        equity_dd_pct=res.equity_drawdown_rel_pct,
        recovery_factor=res.recovery_factor,
        sharpe=res.sharpe_ratio,
        profit_factor=res.profit_factor,
        win_rate=win_rate,
    )
    return {
        "expert": getattr(rep.settings, "expert", None),
        "symbol": getattr(rep.settings, "symbol", None),
        "period": getattr(rep.settings, "period", None),
        "trades": trades,
        "equity_dd_pct": res.equity_drawdown_rel_pct,
        "recovery_factor": res.recovery_factor,
        "sharpe_ratio": res.sharpe_ratio,
        "profit_factor": res.profit_factor,
        "profit_trades": wins,
        "loss_trades": losses,
        "win_rate": win_rate,
        "complex_criterion": round(value, 2),
    }


# --------------------------------------------------------------------------- #
# Output helpers                                                              #
# --------------------------------------------------------------------------- #

def _emit(text: str, path: str | None) -> None:
    if path:
        Path(path).write_text(text, encoding="utf-8")
        print(f"written: {path}")
    else:
        print(text)


def _emit_json(obj, path: str | None) -> None:
    _emit(json.dumps(obj, indent=2, ensure_ascii=False), path)


def _fmt_report(d: dict) -> str:
    wr = f"{d['win_rate'] * 100:.2f}%" if d["win_rate"] is not None else "n/a"
    return "\n".join(
        [
            "Complex Criterion",
            "-" * 58,
            f"  Expert / symbol   : {d['expert']} {d['symbol']} {d['period']}",
            f"  Trades            : {d['trades']}",
            f"  Equity DD rel. %  : {d['equity_dd_pct']:.4f}",
            f"  Recovery Factor   : {d['recovery_factor']:.4f}",
            f"  Sharpe Ratio      : {d['sharpe_ratio']:.4f}",
            f"  Profit Factor     : {d['profit_factor']:.4f}",
            f"  Win rate          : {wr}  ({d['profit_trades']}/{d['loss_trades']})",
            "-" * 58,
            f"  Complex Criterion : {d['complex_criterion']:.2f}",
        ]
    )


def _stats(errors: list[float]) -> dict:
    if not errors:
        return {}
    errors = sorted(errors)
    n = len(errors)

    def q(p: float) -> float:
        return errors[min(n - 1, int(round(p * (n - 1))))]

    return {
        "n": n,
        "median_abs": round(q(0.5), 4),
        "p75_abs": round(q(0.75), 4),
        "p90_abs": round(q(0.90), 4),
        "p99_abs": round(q(0.99), 4),
        "max_abs": round(errors[-1], 4),
        "within_0.005": round(sum(1 for e in errors if e <= 0.005) / n * 100, 2),
        "within_0.05": round(sum(1 for e in errors if e <= 0.05) / n * 100, 2),
        "within_1.0": round(sum(1 for e in errors if e <= 1.0) / n * 100, 2),
    }


# --------------------------------------------------------------------------- #
# Sub-commands                                                                #
# --------------------------------------------------------------------------- #

def cmd_report(args) -> int:
    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    if path.suffix.lower() not in (".html", ".htm"):
        raise SystemExit("report expects a single-test ReportTester-*.html file")
    data = html_report_criterion(path)
    if args.json:
        _emit_json(data, args.output)
    else:
        _emit(_fmt_report(data), args.output)
    return 0


def cmd_xml(args) -> int:
    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    header, rows = read_optimizer_xml(path)
    missing = [k for k in XML_STATS if k not in header]
    if missing:
        raise SystemExit(f"{path}: not an optimization report (missing {missing})")
    out = []
    for rec in rows[: args.limit or len(rows)]:
        computed = round(xml_row_criterion(rec), 2)
        reported = _num(rec.get("Result"), float("nan"))
        out.append(
            {
                "pass": rec.get("Pass"),
                "reported": reported,
                "computed": computed,
                "delta": round(computed - reported, 2),
                "trades": int(_num(rec.get("Trades"))),
                "equity_dd_pct": _num(rec.get("Equity DD %")),
                "recovery_factor": _num(rec.get("Recovery Factor")),
                "sharpe_ratio": _num(rec.get("Sharpe Ratio")),
                "profit_factor": _num(rec.get("Profit Factor")),
            }
        )
    if args.json:
        _emit_json(out, args.output)
        return 0
    lines = [
        f"Complex Criterion — {path.name} ({len(out)} passes)",
        f"{'Pass':>10} {'MT5':>8} {'model':>8} {'delta':>8} {'Trades':>7}"
        f" {'EqDD%':>8} {'RF':>7} {'SR':>7} {'PF':>6}",
        "-" * 78,
    ]
    for r in out:
        lines.append(
            f"{str(r['pass']):>10} {r['reported']:>8.2f} {r['computed']:>8.2f}"
            f" {r['delta']:>+8.2f} {r['trades']:>7} {r['equity_dd_pct']:>8.2f}"
            f" {r['recovery_factor']:>7.2f} {r['sharpe_ratio']:>7.2f}"
            f" {r['profit_factor']:>6.2f}"
        )
    _emit("\n".join(lines), args.output)
    return 0


def cmd_validate(args) -> int:
    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    header, rows = read_optimizer_xml(path)
    missing = [k for k in XML_STATS if k not in header]
    if missing:
        raise SystemExit(f"{path}: not an optimization report (missing {missing})")
    errors = []
    worst = []
    for rec in rows:
        reported = _num(rec.get("Result"), float("nan"))
        if reported != reported:  # NaN
            continue
        computed = xml_row_criterion(rec)
        delta = computed - reported
        errors.append(abs(delta))
        worst.append((abs(delta), rec.get("Pass"), reported, round(computed, 2)))
    worst.sort(reverse=True)
    summary = _stats(errors)
    payload = {"file": str(path), "passes": len(errors), "error": summary,
               "worst": [{"pass": p, "reported": r, "computed": c}
                         for _, p, r, c in worst[:10]]}
    if args.json:
        _emit_json(payload, args.output)
        return 0
    lines = [
        f"Complex Criterion model — validation against {path.name}",
        "-" * 62,
        f"  passes compared      : {summary['n']}",
        f"  median |error|       : {summary['median_abs']:.3f} points",
        f"  p75 / p90 / p99      : {summary['p75_abs']:.3f} / "
        f"{summary['p90_abs']:.3f} / {summary['p99_abs']:.3f}",
        f"  max |error|          : {summary['max_abs']:.3f}",
        f"  |error| <= 0.005     : {summary['within_0.005']:.1f}%",
        f"  |error| <= 0.05      : {summary['within_0.05']:.1f}%",
        f"  |error| <= 1.00      : {summary['within_1.0']:.1f}%",
        "",
        "  NOTE: an optimizer XML carries no win/loss trade counts, so the",
        "  win-rate component cannot be evaluated and the model runs with its",
        "  calibrated average.  Single-test HTML reports do carry them and are",
        "  reproduced much more closely.",
        "-" * 62,
        f"  {'worst pass':>12} {'MT5':>8} {'model':>8} {'delta':>8}",
    ]
    for err, p, r, c in worst[:10]:
        lines.append(f"  {str(p):>12} {r:>8.2f} {c:>8.2f} {c - r:>+8.2f}")
    _emit("\n".join(lines), args.output)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compute MT5's Strategy Tester Complex Criterion from a report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("path", help="report file")
        p.add_argument("--json", action="store_true", help="JSON output")
        p.add_argument("-o", "--output", help="write output to FILE")

    p = sub.add_parser("report", help="single-test HTML report -> one number")
    common(p)
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("xml", help="optimizer XML -> per-pass table")
    common(p)
    p.add_argument("--limit", type=int, default=0, help="only the first N passes")
    p.set_defaults(func=cmd_xml)

    p = sub.add_parser("validate", help="optimizer XML -> model accuracy")
    common(p)
    p.set_defaults(func=cmd_validate)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
