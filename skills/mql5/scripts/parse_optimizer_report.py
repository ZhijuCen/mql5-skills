#!/usr/bin/env python3
"""
Parse MT5 Strategy Tester Optimization XML report (SpreadsheetML format).

Strategy Tester exports optimization results as an XML-tagged Excel workbook
(also readable by LibreOffice Calc). The first worksheet "Tester Optimizator
Results" contains one row per parameter pass, plus a <DocumentProperties>
block with run metadata (EA, symbol, period, date range, deposit, leverage,
broker, MT5 build).

This script extracts:
  - <DocumentProperties>:  strategy environment (title, deposit, leverage,
                           server, MT5 build, run timestamp)
  - Worksheet:             parameter columns + per-pass result metrics
                           (Pass, Result, Profit, Expected Payoff, Profit
                           Factor, Recovery Factor, Sharpe Ratio, Custom,
                           Equity DD %, Trades)
  - Analysis (--analyze):  parameter orthogonality, parameter effect (does a
                           parameter actually influence output?), best passes
                           by multiple criteria, trade-count distribution,
                           duplicates (passes with identical metric vectors
                           usually mean a parameter is dead), correlation
                           between trade count and result.

Usage:
    python skills/mql5/scripts/parse_optimizer_report.py <report.xml>
    python skills/mql5/scripts/parse_optimizer_report.py <report.xml> --json
    python skills/mql5/scripts/parse_optimizer_report.py <report.xml> --analyze
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import warnings
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

# Silences "It looks like you're using an HTML parser to parse an XML document"
# from the html.parser default. We intentionally use html.parser (no lxml
# dependency).
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# ── Data classes ─────────────────────────────────────────────────────

@dataclass
class Env:
    """Strategy environment extracted from <DocumentProperties>."""
    title: str = ""
    author: str = ""
    revision: str = ""
    created: str = ""
    company: str = ""
    mt5_version: str = ""
    mt5_build: str = ""
    server: str = ""
    deposit: str = ""
    leverage: str = ""
    condition: str = ""
    # Derived (parsed from title)
    ea_name: str = ""
    symbol: str = ""
    period: str = ""
    date_from: str = ""
    date_to: str = ""


# Column groups (stable, from MT5 export)
METRIC_COLS = [
    "Result", "Profit", "Expected Payoff", "Profit Factor",
    "Recovery Factor", "Sharpe Ratio", "Custom", "Equity DD %", "Trades",
]
# Heuristic: every column that is not "Inp*" and not "Pass" is a metric.
# InpUseNewsFilter is a boolean string, all other Inp* are numbers.


# ── Parsing ──────────────────────────────────────────────────────────

def parse_env(soup: BeautifulSoup) -> Env:
    """Pull <DocumentProperties> into an Env dataclass."""
    env = Env()
    dp = soup.find("documentproperties")
    if not dp:
        return env

    # BeautifulSoup lower-cases tag names; keys are already lowercase.
    for child in dp.find_all():
        key = child.name
        val = child.get_text(strip=True)
        if key == "title":
            env.title = val
        elif key == "author":
            env.author = val
        elif key == "revision":
            env.revision = val
        elif key == "created":
            env.created = val
        elif key == "company":
            env.company = val
        elif key == "version":
            env.mt5_version = val
        elif key == "build":
            env.mt5_build = val
        elif key == "server":
            env.server = val
        elif key == "deposit":
            env.deposit = val
        elif key == "leverage":
            env.leverage = val
        elif key == "condition":
            env.condition = val

    # Title pattern (observed): "<EA> <SYMBOL>,<PERIOD> <YYYY.MM.DD>-<YYYY.MM.DD>"
    m = re.match(
        r"(\S+)\s+(\w+),(\w+)\s+(\d{4}\.\d{2}\.\d{2})-(\d{4}\.\d{2}\.\d{2})",
        env.title,
    )
    if m:
        env.ea_name = m.group(1)
        env.symbol = m.group(2)
        env.period = m.group(3)
        env.date_from = m.group(4)
        env.date_to = m.group(5)
    return env


def parse_passes(soup: BeautifulSoup) -> pd.DataFrame:
    """Pull the first worksheet into a typed DataFrame.

    Assumes the well-known MT5 column layout: 1 Pass col + 9 metric cols
    + N Inp* param cols. <Data ss:Type="String"> cells become strings
    (covers InpUseNewsFilter 'true'/'false'); everything else is coerced
    to numeric.
    """
    ws = soup.find("worksheet", attrs={"ss:name": "Tester Optimizator Results"})
    if not ws:
        # Fallback: first worksheet regardless of name
        ws = soup.find("worksheet")
    if not ws:
        return pd.DataFrame()

    table = ws.find("table")
    if not table:
        return pd.DataFrame()

    rows = table.find_all("row")
    if len(rows) < 2:
        return pd.DataFrame()

    headers = [c.get_text(strip=True) for c in rows[0].find_all("cell")]

    data = []
    for r in rows[1:]:
        cells = r.find_all("cell")
        data.append([c.get_text(strip=True) for c in cells])

    df = pd.DataFrame(data, columns=headers)

    # Type inference
    for col in df.columns:
        if col == "Pass":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            continue
        if col == "InpUseNewsFilter":
            # Stay as string "true"/"false" — typed comparison matters
            df[col] = df[col].astype(str)
            continue
        # Numeric metric or numeric parameter
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def parse_report(path: Path) -> tuple[Env, pd.DataFrame]:
    """Convenience wrapper: file → (Env, DataFrame)."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    soup = BeautifulSoup(raw, "html.parser")
    return parse_env(soup), parse_passes(soup)


# ── Analysis ─────────────────────────────────────────────────────────

def _param_cols(df: pd.DataFrame) -> list[str]:
    """Inp* columns that the EA declared for optimization."""
    return [c for c in df.columns if c.startswith("Inp")]


def _backtest_days(env: Env) -> int | None:
    if not (env.date_from and env.date_to):
        return None
    try:
        d0 = datetime.strptime(env.date_from, "%Y.%m.%d")
        d1 = datetime.strptime(env.date_to, "%Y.%m.%d")
        return (d1 - d0).days
    except ValueError:
        return None


def analyze(df: pd.DataFrame, env: Env) -> dict:
    """Run optimization analysis. Returns a dict with sections.

    Sections:
      - orthogonality:           full pass count vs expected cartesian product
      - parameter_cardinality:   how many distinct values each Inp* took
      - parameter_effect:        is the parameter actually doing anything?
                                 (true = metric groups are statistically
                                 distinguishable; false = the param is dead)
      - duplicates:              passes with identical metric vector ⇒ a
                                 parameter is not influencing output
      - best_passes:             top-N by Profit / Profit Factor / Recovery
                                 Factor / Custom
      - trades:                  distribution, daily rate, correlations
      - param_cross:             per-parameter mean Profit / Profit Factor
    """
    out: dict = {"env_card": _env_card(env), "pass_count": int(len(df))}

    if df.empty:
        out["error"] = "No pass rows found"
        return out

    pcols = _param_cols(df)

    # 1. Orthogonality — did the optimizer cover the full cartesian product?
    n = len(df)
    expected = 1
    cardinalities = {}
    for c in pcols:
        u = df[c].nunique(dropna=True)
        cardinalities[c] = int(u)
        expected *= int(u) if u else 1
    out["orthogonality"] = {
        "actual": n,
        "expected_cartesian": expected,
        "complete": n == expected,
        "missing": expected - n if expected > n else 0,
    }
    out["parameter_cardinality"] = cardinalities

    # 2. Parameter effect — for each parameter, does changing its value
    # produce statistically distinguishable Profit groups?
    effects = {}
    for c in pcols:
        groups = df.groupby(c, observed=True)["Profit"]
        # Two signals: (a) range / std ratio; (b) min==max (suggests dead)
        per_group_stats = groups.agg(["count", "mean", "median", "std", "min", "max"])
        max_mean = per_group_stats["mean"].max()
        min_mean = per_group_stats["mean"].min()
        max_min = per_group_stats["max"].max()
        min_min = per_group_stats["min"].min()

        # Aggregate std across all passes (baseline noise)
        global_std = df["Profit"].std() or 0.0
        spread = max_mean - min_mean

        # Effect = spread / global std. >1 = meaningful, <0.3 = negligible.
        effect_ratio = round(spread / global_std, 2) if global_std > 0 else 0.0

        # If max group min == min group max ⇒ groups don't overlap ⇒ strong
        # effect. If they fully overlap ⇒ no separation.
        no_overlap = max_min <= min_mean  # best group's worst is worse than worst group's best

        # Also check: the per-group means are within 1% of each other (truly dead)
        if max_mean > 0:
            relative_spread = spread / abs(max_mean)
        else:
            relative_spread = 0.0

        effects[c] = {
            "n_unique": int(df[c].nunique()),
            "values": sorted(df[c].unique().tolist(), key=str),
            "global_mean_profit": round(float(df["Profit"].mean()), 2),
            "per_group_mean": {
                str(k): round(float(v), 2)
                for k, v in per_group_stats["mean"].items()
            },
            "spread_max_minus_min": round(float(spread), 2),
            "effect_ratio_spread_over_std": effect_ratio,
            "relative_spread_pct": round(relative_spread * 100, 1),
            "groups_separated": bool(no_overlap),
            "dead_param": bool(relative_spread < 0.01),  # <1% spread = dead
        }
    out["parameter_effect"] = effects

    # 3. Duplicates — passes with identical metric vector ⇒ that parameter
    # combination is not actually influencing output.
    metric_cols_present = [c for c in METRIC_COLS if c in df.columns]
    dupes = (
        df.groupby(metric_cols_present, dropna=False)
        .size()
        .reset_index(name="count")
    )
    dupes = dupes[dupes["count"] > 1].sort_values("count", ascending=False)
    out["duplicates"] = {
        "groups_with_dupes": int(len(dupes)),
        "total_dup_rows": int(dupes["count"].sum() - len(dupes)) if len(dupes) else 0,
        "examples": dupes.head(5).to_dict("records"),
    }

    # 4. Best passes by multiple criteria
    out["best_passes"] = {
        "by_profit": _top(df, "Profit", 5),
        "by_profit_factor": _top(df, "Profit Factor", 5),
        "by_recovery_factor": _top(df, "Recovery Factor", 5),
        "by_custom": _top(df, "Custom", 5),
    }

    # 5. Trade-count distribution
    if "Trades" in df.columns:
        tr = df["Trades"]
        out["trades"] = {
            "min": int(tr.min()),
            "max": int(tr.max()),
            "mean": round(float(tr.mean()), 1),
            "median": float(tr.median()),
            "stdev": round(float(tr.std()), 2),
            "deciles": [int(tr.quantile(q / 10)) for q in range(0, 11)],
        }
        # Trades/day: helps detect overtrading relative to backtest length
        days = _backtest_days(env)
        if days and days > 0:
            median_trades = float(tr.median())
            out["trades"]["backtest_days"] = days
            out["trades"]["trades_per_day_median"] = round(median_trades / days, 3)
            out["trades"]["trades_per_day_max"] = round(float(tr.max()) / days, 3)
        # Correlations: overtrading usually correlates negatively with PF
        if "Profit Factor" in df.columns:
            out["trades"]["corr_trades_vs_profit_factor"] = round(
                float(tr.corr(df["Profit Factor"])), 3
            )
        if "Profit" in df.columns:
            out["trades"]["corr_trades_vs_profit"] = round(
                float(tr.corr(df["Profit"])), 3
            )
        if "Equity DD %" in df.columns:
            out["trades"]["corr_trades_vs_equity_dd"] = round(
                float(tr.corr(df["Equity DD %"])), 3
            )

    # 6. Cross-analysis: each parameter's effect on key metrics
    cross = {}
    metric_targets = [c for c in ["Profit", "Profit Factor", "Trades"] if c in df.columns]
    for p in pcols:
        agg_dict = {m: ["mean", "median", "min", "max"] for m in metric_targets}
        agg_dict["Pass"] = "count"
        grp = df.groupby(p, observed=True).agg(agg_dict)
        grp.columns = [f"{m}_{stat}" for m, stat in grp.columns]
        cross[p] = (
            grp.reset_index()
            .rename(columns={"Pass_count": "n_passes"})
            .to_dict("records")
        )
    out["param_cross"] = cross

    # 7. Boolean parameter symmetry check
    #    For boolean Inp* (e.g. InpUseNewsFilter), a 1:1 identical outcome
    #    between true/false groups is the cleanest "dead parameter" signal.
    bool_params = {}
    for p in pcols:
        if df[p].nunique() == 2 and set(df[p].unique()) <= {"true", "false"}:
            for m in ["Profit", "Profit Factor", "Trades", "Recovery Factor"]:
                if m not in df.columns:
                    continue
                t = df.loc[df[p] == "true", m].mean()
                f = df.loc[df[p] == "false", m].mean()
                if abs(t - f) < 1e-6:
                    bool_params.setdefault(p, []).append(m)
    if bool_params:
        out["dead_boolean_params"] = {
            p: sorted(set(metrics))
            for p, metrics in bool_params.items()
        }

    return out


def _env_card(env: Env) -> dict:
    """Compact strategy-environment summary for JSON / text output."""
    days = _backtest_days(env)
    return {
        "ea_name": env.ea_name,
        "symbol": env.symbol,
        "period": env.period,
        "date_from": env.date_from,
        "date_to": env.date_to,
        "backtest_days": days,
        "deposit": env.deposit,
        "leverage": env.leverage,
        "server": env.server,
        "mt5_version": env.mt5_version,
        "mt5_build": env.mt5_build,
        "run_created": env.created,
    }


def _top(df: pd.DataFrame, col: str, n: int) -> list[dict]:
    """Top-N rows by `col`, with the criterion col + parameters preserved."""
    if col not in df.columns or df.empty:
        return []
    pcols = _param_cols(df)
    # Criterion col is the first metric; avoid duplicating it in the tail list
    tail = ["Pass", "Profit", "Profit Factor", "Recovery Factor", "Trades"]
    show = [c for c in [col] + tail if c in df.columns and c not in (col,)]
    # Ensure col itself is first
    show = [col] + [c for c in show if c != col]
    # Pass is always useful
    if "Pass" in df.columns and "Pass" not in show:
        show = ["Pass"] + show
    show = show + [c for c in pcols if c in df.columns and c not in show]
    return df.nlargest(n, col)[show].to_dict("records")


# ── Text output ──────────────────────────────────────────────────────

def _fmt_param_row(row: dict, pcols: list[str]) -> str:
    """Format one best-pass row for the text report."""
    bits = [f"Pass {row.get('Pass', '?'):>3}"]
    for k in ("Profit", "Profit Factor", "Recovery Factor", "Trades"):
        if k in row:
            v = row[k]
            if isinstance(v, float):
                if k == "Trades":
                    bits.append(f"{k}={int(v)}")
                else:
                    bits.append(f"{k}={v:.3f}")
            else:
                bits.append(f"{k}={v}")
    for p in pcols:
        if p in row:
            bits.append(f"{p}={row[p]}")
    return "  ".join(bits)


def print_report(env: Env, df: pd.DataFrame) -> None:
    print("=" * 70)
    print("STRATEGY TESTER OPTIMIZATION REPORT")
    print("=" * 70)
    print(f"  EA:            {env.ea_name or '(unknown)'}")
    print(f"  Symbol:        {env.symbol or '(unknown)'}")
    print(f"  Period:        {env.period or '(unknown)'}")
    print(f"  Date range:    {env.date_from} → {env.date_to}")
    days = _backtest_days(env)
    if days:
        print(f"  Backtest days: {days}")
    print(f"  Deposit:       {env.deposit}")
    print(f"  Leverage:      {env.leverage}")
    print(f"  Server:        {env.server}")
    print(f"  MT5:           {env.mt5_version} (build {env.mt5_build})")
    print(f"  Run created:   {env.created}")
    print()
    if df.empty:
        print("  (no pass rows found)")
        return

    pcols = _param_cols(df)
    print(f"  Passes:        {len(df)}")
    print(f"  Parameters:    {', '.join(pcols) or '(none)'}")
    print()
    print("  Parameter cardinalities:")
    for p in pcols:
        u = df[p].nunique()
        print(f"    {p}: {u} unique value(s)")
    print()
    print("  Use --analyze for full parameter-effect / duplicate / best-pass analysis.")
    print("  Use --json for raw parsed data.")


def print_analyze(env: Env, df: pd.DataFrame, an: dict) -> None:
    print_report(env, df)
    if "error" in an:
        print(f"\nERROR: {an['error']}")
        return
    pcols = _param_cols(df)

    print()
    print("=" * 70)
    print("ORTHOGONALITY")
    print("=" * 70)
    ortho = an["orthogonality"]
    print(f"  Passes:           {ortho['actual']}")
    print(f"  Expected (cart.): {ortho['expected_cartesian']}")
    print(f"  Complete:         {ortho['complete']}")
    if not ortho["complete"]:
        print(f"  Missing:          {ortho['missing']}")

    print()
    print("=" * 70)
    print("PARAMETER EFFECT (does the parameter change the result?)")
    print("=" * 70)
    for p, info in an["parameter_effect"].items():
        flag = "DEAD" if info["dead_param"] else ("weak" if info["effect_ratio_spread_over_std"] < 0.5 else "active")
        print(f"\n  {p}  [{flag}]  "
              f"spread={info['spread_max_minus_min']:.1f}  "
              f"rel_spread={info['relative_spread_pct']:.1f}%  "
              f"effect_ratio={info['effect_ratio_spread_over_std']}")
        for val, mean in info["per_group_mean"].items():
            print(f"    {p}={val!s:>8}  mean Profit = {mean}")

    if an.get("dead_boolean_params"):
        print()
        print("  ⚠️  Boolean parameters with identical metric means on true/false:")
        for p, metrics in an["dead_boolean_params"].items():
            print(f"    {p}: identical on {', '.join(metrics)} — this parameter did not influence the backtest")

    print()
    print("=" * 70)
    print("DUPLICATES (passes with identical metric vectors → dead parameter)")
    print("=" * 70)
    dup = an["duplicates"]
    print(f"  Groups with duplicates:  {dup['groups_with_dupes']}")
    print(f"  Total extra duplicate rows: {dup['total_dup_rows']}")
    if dup["examples"]:
        print("  Examples (top 5 by count):")
        for ex in dup["examples"][:5]:
            print(f"    count={ex['count']}  "
                  f"Profit={ex.get('Profit')}  PF={ex.get('Profit Factor')}  "
                  f"RF={ex.get('Recovery Factor')}  Trades={ex.get('Trades')}")

    print()
    print("=" * 70)
    print("BEST PASSES")
    print("=" * 70)
    for criterion, rows in an["best_passes"].items():
        print(f"\n  Top 5 by {criterion}:")
        for r in rows:
            print(f"    {_fmt_param_row(r, pcols)}")

    if "trades" in an:
        tr = an["trades"]
        print()
        print("=" * 70)
        print("TRADE COUNT DISTRIBUTION")
        print("=" * 70)
        print(f"  Range:    {tr['min']} – {tr['max']}")
        print(f"  Mean:     {tr['mean']}")
        print(f"  Median:   {tr['median']}")
        print(f"  Stdev:    {tr['stdev']}")
        print(f"  Deciles:  {tr['deciles']}")
        if "backtest_days" in tr:
            print(f"  Trades/day (median over {tr['backtest_days']} days): {tr['trades_per_day_median']}")
            print(f"  Trades/day (max):    {tr['trades_per_day_max']}")
        for k in (
            "corr_trades_vs_profit_factor",
            "corr_trades_vs_profit",
            "corr_trades_vs_equity_dd",
        ):
            if k in tr:
                hint = ""
                v = tr[k]
                if k == "corr_trades_vs_profit_factor" and v < -0.3:
                    hint = "  ← more trades → worse PF (overtrading signal)"
                elif k == "corr_trades_vs_equity_dd" and v > 0.3:
                    hint = "  ← more trades → higher drawdown"
                print(f"  {k}: {v}{hint}")


# ── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse MT5 Strategy Tester Optimization XML report"
    )
    parser.add_argument("report", help="Path to ReportOptimizer-*.xml file")
    parser.add_argument("--json", action="store_true", help="Output raw parsed data as JSON")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run optimization analysis (parameter effect, duplicates, best passes, trade distribution)",
    )
    args = parser.parse_args()

    path = Path(args.report)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    env, df = parse_report(path)
    analyze_data = analyze(df, env) if (args.analyze or args.json) else None

    if args.json or args.analyze:
        payload = {
            "env": asdict(env),
            "pass_count": int(len(df)),
            "columns": list(df.columns),
            "passes": df.where(pd.notnull(df), None).to_dict("records"),
        }
        if analyze_data is not None:
            payload["analyze"] = analyze_data
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    else:
        print_report(env, df)


if __name__ == "__main__":
    main()
