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
    python skills/mql5/scripts/parse_optimizer_report.py <report.xml> outliers [--top-outliers N] [--top-normal M] [--sigma K] [--json]
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

    Column layout is determined from the SpreadsheetML header row: any
    <Data ss:Type="String"> cell in the header marks a string column
    (typically a boolean Inp* parameter rendered as "true"/"false");
    everything else is coerced to numeric. This is EA-agnostic — no
    hardcoded Inp* parameter names.

    The Pass column is always forced to nullable Int64 (it's a row id
    even when declared as Number in the SpreadsheetML). All other
    Number columns become float64 (or Int64 when every value is a whole
    number — useful for InpSLPips-style integer parameters).
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

    # Header row: just extract column names. Header cells are always
    # ss:Type="String" (they hold text labels), so we can't use them
    # to decide which body columns are strings.
    header_cells = rows[0].find_all("cell")
    headers: list[str] = [c.get_text(strip=True) for c in header_cells]

    # First body row: inspect each cell's <Data ss:Type="..."> to learn
    # which columns hold strings (e.g. boolean Inp* as "true"/"false").
    # Number-typed cells declare ss:Type="Number" (sometimes absent).
    first_body_cells = rows[1].find_all("cell")
    string_cols: set[int] = set()
    for i, c in enumerate(first_body_cells):
        data_tag = c.find("data")
        if data_tag is None:
            continue
        ss_type = (data_tag.get("ss:type") or "").lower()
        if ss_type == "string":
            string_cols.add(i)

    # Body rows: pull text. We don't trust per-row ss:Type for numeric
    # columns because MT5 sometimes leaves it off; pandas' to_numeric
    # is the authoritative check.
    body: list[list[str]] = []
    for r in rows[1:]:
        cells = r.find_all("cell")
        body.append([c.get_text(strip=True) for c in cells])

    df = pd.DataFrame(body, columns=headers)

    # Type inference driven by the first body row's ss:Type.
    for i, col in enumerate(df.columns):
        if col == "Pass":
            # Pass is always an integer row id
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            continue
        if i in string_cols:
            # ss:Type="String" — keep as raw text (e.g. "true"/"false").
            df[col] = df[col].astype(str)
            continue
        # Numeric: try Int64 if every value is a whole number, else float64
        coerced = pd.to_numeric(df[col], errors="coerce")
        if pd.notna(coerced).all() and (coerced.dropna() % 1 == 0).all():
            df[col] = coerced.astype("Int64")
        else:
            df[col] = coerced.astype("float64")

    return df


def parse_report(path: Path) -> tuple[Env, pd.DataFrame]:
    """Convenience wrapper: file → (Env, DataFrame)."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    soup = BeautifulSoup(raw, "html.parser")
    return parse_env(soup), parse_passes(soup)


# ── Analysis ─────────────────────────────────────────────────────────

def _param_cols(df: pd.DataFrame) -> list[str]:
    """Input parameter columns the EA declared for optimization.

    The MT5 export puts Pass + the 9 standard metrics first, then
    every optimization parameter afterwards. We rely on column
    position (everything after ``Trades``), NOT on a name prefix —
    parameter names don't always start with ``Inp*`` in real exports.
    """
    cols = list(df.columns)
    if "Trades" in cols:
        idx = cols.index("Trades")
        return cols[idx + 1:]
    # Fallback: no Trades column — assume nothing is a parameter
    return []


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


# ── Outlier analysis (per-pass z-score over optimization passes) ─────

# Per-metric direction: True = higher-is-better (we look at z >= +sigma),
# False = lower-is-better (we look at z <= -sigma). Equity DD % is the
# only lower-is-better metric — low DD means the strategy is safer.
_PERF_METRICS_HIGHER_IS_BETTER = {
    "Result": True,
    "Profit": True,
    "Expected Payoff": True,
    "Profit Factor": True,
    "Recovery Factor": True,
    "Sharpe Ratio": True,
    "Custom": True,
    "Equity DD %": False,
}


def _mean_std(values: list[float]) -> tuple[float, float]:
    """Return (mean, sample std N-1) of `values`. std=0 if N<2."""
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        return values[0], 0.0
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1)
    return mean, var ** 0.5


def _z_scores(values: list[float]) -> list[float]:
    """Sample-std z-scores for `values`. z=0 when std=0."""
    mean, std = _mean_std(values)
    if std == 0:
        return [0.0] * len(values)
    return [(v - mean) / std for v in values]


def _outlier_metrics_for_row(
    z_by_metric: dict[str, float],
    sigma: float,
) -> list[dict]:
    """Per-row outlier flags, in the "performance-strongly-strong" sense.

    For each metric, the row is "strong" when its z is on the GOOD side
    of the mean by at least `sigma` standard deviations:

      - higher-is-better metric  -> z >=  sigma
      - lower-is-better  metric  -> z <= -sigma  (e.g. low DD is good)

    Returns a list of {"metric": ..., "z": ...} entries, one per metric
    that qualifies. Empty list means no performance metric is a
    "strongly-strong" outlier.
    """
    flags = []
    for m, z in z_by_metric.items():
        higher = _PERF_METRICS_HIGHER_IS_BETTER.get(m, True)
        if higher and z >= sigma:
            flags.append({"metric": m, "z": round(z, 2)})
        elif (not higher) and z <= -sigma:
            flags.append({"metric": m, "z": round(z, 2)})
    return flags


def find_outliers(
    df: pd.DataFrame,
    sigma: float = 2.0,
    top_outliers: int = 10,
    top_normal: int = 5,
) -> dict:
    """Per-pass z-score outlier scan across the 8 performance metrics.

    Two disjoint pass sets are returned:

      set_outliers — passes with AT LEAST ONE performance metric whose
        z-score crosses ±sigma in the "strongly-strong" direction
        (higher-is-better: z >= +sigma; lower-is-better Equity DD %:
        z <= -sigma). Sorted by Result desc; top `top_outliers` shown.

      set_normal — passes with NO performance-metric outlier. Sorted by
        Result desc; top `top_normal` shown.

    Both sets EXCLUDE passes whose Trades count is itself a low-side
    outlier (z <= -sigma). Such passes have too few trades to trust
    their performance numbers — including them would inflate the
    outlier set with cheap-pass artifacts.

    Also returns the per-metric mean / std / sigma threshold table so
    the user can judge whether the outlier counts are meaningful.

    Output shape:
      {
        "per_metric":  {"profit": {"mean":..., "std":..., "threshold_+sigma":...,
                                    "threshold_-sigma":..., "direction": "higher"|"lower"},
                         ...},
        "trades":      {"mean":..., "std":..., "low_outlier_z": ...},
        "sigma":       float,
        "n_passes":    int,
        "excluded":    [{"Pass":..., "Trades":..., "z": ...}, ...],  # low-Trades outliers
        "set_outliers":[{Pass, Result, profit, ..., outliers: [{metric, z}, ...],
                         params: {InpSLPips: ..., ...}}, ...],
        "set_normal":  [...],
        "counts":      {"outliers": int, "normal": int, "excluded": int},
      }
    """
    out: dict = {"sigma": sigma, "n_passes": int(len(df))}

    if df.empty:
        out["error"] = "No pass rows"
        return out

    # The 8 performance metrics (everything in METRIC_COLS except Trades)
    perf_metrics = [c for c in METRIC_COLS if c in df.columns and c != "Trades"]
    out["per_metric"] = {}
    z_perf_by_row: list[dict[str, float]] = []
    for m in perf_metrics:
        vals = [float(v) for v in df[m].tolist()]
        mean, std = _mean_std(vals)
        zs = _z_scores(vals)
        higher = _PERF_METRICS_HIGHER_IS_BETTER.get(m, True)
        out["per_metric"][m] = {
            "mean": round(mean, 4),
            "std": round(std, 4),
            "threshold_+sigma": round(mean + sigma * std, 4),
            "threshold_-sigma": round(mean - sigma * std, 4),
            "direction": "higher" if higher else "lower",
        }
        # Pad / align z rows with column index (defensive: pad if cols differ)
        for i, z in enumerate(zs):
            if i >= len(z_perf_by_row):
                z_perf_by_row.append({})
            z_perf_by_row[i][m] = z

    # Trades: only used for the low-Trades exclusion filter
    if "Trades" in df.columns:
        trades_vals = [float(v) for v in df["Trades"].tolist()]
        mean, std = _mean_std(trades_vals)
        out["trades"] = {
            "mean": round(mean, 2),
            "std": round(std, 2),
            "low_outlier_threshold": round(mean - sigma * std, 2),
        }
        trades_z = _z_scores(trades_vals)
    else:
        trades_z = [0.0] * len(df)
        out["trades"] = None

    pcols = _param_cols(df)

    # Build per-row records; carry Pass / Result / metric values / z / params
    rows = []
    for idx, row in df.iterrows():
        z_map = z_perf_by_row[idx] if idx < len(z_perf_by_row) else {}
        rec = {
            "Pass": int(row["Pass"]) if "Pass" in df.columns and pd.notna(row["Pass"]) else None,
            "Result": float(row["Result"]) if "Result" in df.columns and pd.notna(row["Result"]) else None,
            "perf_metrics": {m: float(row[m]) for m in perf_metrics if pd.notna(row[m])},
            "z_metrics": {m: round(z_map.get(m, 0.0), 2) for m in perf_metrics},
            "Trades": int(row["Trades"]) if "Trades" in df.columns and pd.notna(row["Trades"]) else None,
            "Trades_z": round(trades_z[idx], 2) if idx < len(trades_z) else 0.0,
            "params": {p: (row[p] if pd.notna(row[p]) else None) for p in pcols},
        }
        rec["outliers"] = _outlier_metrics_for_row(z_map, sigma)
        rows.append(rec)

    # Exclusion: passes with Trades z <= -sigma — too few trades to trust.
    excluded = [r for r in rows if r["Trades_z"] <= -sigma]
    eligible = [r for r in rows if r["Trades_z"] > -sigma]
    out["excluded"] = [
        {"Pass": r["Pass"], "Trades": r["Trades"], "Trades_z": r["Trades_z"]}
        for r in excluded
    ]

    # Sort eligible passes by Result desc
    eligible.sort(key=lambda r: (r["Result"] is None, -(r["Result"] or 0.0)))

    # Set A: at least one performance-metric outlier
    set_a = [r for r in eligible if r["outliers"]]
    # Set B: no performance-metric outlier
    set_b = [r for r in eligible if not r["outliers"]]

    out["set_outliers"] = set_a[:top_outliers]
    out["set_normal"] = set_b[:top_normal]
    out["counts"] = {
        "outliers": len(set_a),
        "normal": len(set_b),
        "excluded_low_trades": len(excluded),
    }
    return out


def _fmt_outlier_row(rec: dict, pcols: list[str]) -> str:
    """One-pass outlier record as two compact lines (metrics, params).

    Layout:
      Pass 42 | Result=2.31 | Profit=800.10 EP=4.55 PF=1.61 RF=4.55 ... | z: Profit(+2.4σ), Sharpe(+2.1σ)
        params: InpSLPips=30, InpTPPips=180, InpUseNewsFilter=true
    """
    out_bits = []
    pass_str = f"Pass {rec['Pass']}" if rec["Pass"] is not None else "Pass ?"
    res_str = f"Result={rec['Result']:.2f}" if rec["Result"] is not None else "Result=?"
    out_bits.append(f"  {pass_str:<10} {res_str}")

    # Metric values (in canonical METRIC_COLS order minus Trades)
    metric_bits = []
    for m in METRIC_COLS:
        if m == "Trades":
            continue
        if m not in rec["perf_metrics"]:
            continue
        v = rec["perf_metrics"][m]
        # Short labels for readability
        short = {
            "Result": "Res",
            "Profit": "Prof",
            "Expected Payoff": "EP",
            "Profit Factor": "PF",
            "Recovery Factor": "RF",
            "Sharpe Ratio": "Sharpe",
            "Custom": "Cust",
            "Equity DD %": "EqDD%",
        }.get(m, m)
        metric_bits.append(f"{short}={v:.2f}")
    trades_part = f" Trades={rec['Trades']}" if rec["Trades"] is not None else ""
    out_bits.append("  Metrics: " + "  ".join(metric_bits) + trades_part)

    # Outlier annotations: only the metrics that crossed the threshold
    if rec["outliers"]:
        annot = ", ".join(
            f"{o['metric']}({o['z']:+.2f}σ)" for o in rec["outliers"]
        )
        out_bits.append(f"  Outliers: {annot}")
    else:
        out_bits.append("  Outliers: (none)")

    # Input parameters — keep all of them, one per line if many
    if pcols:
        param_parts = []
        for p in pcols:
            val = rec["params"].get(p)
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            param_parts.append(f"{p}={val}")
        # Wrap to <=4 params per line for readability
        lines = []
        cur = []
        cur_len = 0
        for part in param_parts:
            if cur and cur_len + len(part) + 2 > 70:
                lines.append(", ".join(cur))
                cur = [part]
                cur_len = len(part)
            else:
                cur.append(part)
                cur_len += len(part) + 2
        if cur:
            lines.append(", ".join(cur))
        out_bits.append("  Params: " + lines[0])
        for extra in lines[1:]:
            out_bits.append("          " + extra)

    return "\n".join(out_bits)


def print_outliers(env: Env, df: pd.DataFrame, out: dict) -> None:
    """Pretty-print the outlier scan as a text report.

    Layout follows the windows subcommand style: header card, then
    a per-metric reference table (mean / std / sigma threshold),
    then the two pass sets grouped by [Metrics] and [Params].
    """
    print("=" * 78)
    print(f"  Optimization Outlier Scan  (per-pass z-score across {out.get('n_passes', '?')} passes)")
    print("=" * 78)
    print(f"  EA: {env.ea_name or '(unknown)'}  Symbol: {env.symbol or '(unknown)'}  "
          f"Period: {env.period or '(unknown)'}")
    print(f"  Date range: {env.date_from} → {env.date_to}")
    print(f"  Sigma threshold: {out['sigma']:.1f}  "
          f"(direction: higher-is-better uses z>=+σ; Equity DD % uses z<=-σ)")
    print()

    if "error" in out:
        print(f"  ERROR: {out['error']}")
        return

    # Per-metric reference table
    print(f"  {'Metric':<22} {'Dir':>5} {'Mean':>12} {'Std':>10} "
          f"{'+σ threshold':>14} {'-σ threshold':>14}")
    print("  " + "─" * 80)
    for m in METRIC_COLS:
        if m == "Trades" or m not in out["per_metric"]:
            continue
        info = out["per_metric"][m]
        print(f"  {m:<22} {info['direction']:>5} "
              f"{info['mean']:>12.4f} {info['std']:>10.4f} "
              f"{info['threshold_+sigma']:>14.4f} {info['threshold_-sigma']:>14.4f}")
    if out.get("trades"):
        t = out["trades"]
        print(f"  {'Trades (excluded)':<22} {'low':>5} "
              f"{t['mean']:>12.2f} {t['std']:>10.2f} "
              f"{'--':>14} {t['low_outlier_threshold']:>14.2f}")
    print()

    # Counts
    c = out["counts"]
    print(f"  Set A (>=1 perf outlier, sorted by Result desc): {c['outliers']} passes")
    print(f"  Set B (no perf outlier,   sorted by Result desc): {c['normal']} passes")
    if c["excluded_low_trades"]:
        print(f"  Excluded (Trades z<=-σ, too few trades to trust): {c['excluded_low_trades']} passes")
    print()

    pcols = _param_cols(df)

    # Set A
    if out["set_outliers"]:
        print("=" * 78)
        print(f"  SET A — Passes with at least one performance-metric outlier")
        print(f"          (top {len(out['set_outliers'])} by Result; "
              f"{c['outliers']} total eligible)")
        print("=" * 78)
        for rec in out["set_outliers"]:
            print(_fmt_outlier_row(rec, pcols))
            print()
    else:
        print("  SET A: empty (no eligible passes have a performance-metric outlier)")
        print()

    # Set B
    if out["set_normal"]:
        print("=" * 78)
        print(f"  SET B — Passes with no performance-metric outlier (top {len(out['set_normal'])} by Result)")
        print("=" * 78)
        for rec in out["set_normal"]:
            print(_fmt_outlier_row(rec, pcols))
            print()
    else:
        print("  SET B: empty (every eligible pass has at least one performance-metric outlier)")
        print()

    # Excluded (low-Trades)
    if out["excluded"]:
        print("=" * 78)
        print(f"  EXCLUDED — Passes with Trades z <= -{out['sigma']:.0f}σ (too few trades to trust)")
        print("=" * 78)
        for e in out["excluded"]:
            print(f"  Pass {e['Pass']:<6} Trades={e['Trades']:<5} Trades_z={e['Trades_z']:+.2f}σ")
        print()

    # Interpretation
    print("  Interpretation:")
    print(f"    z = (this pass's value − mean across all passes) / std.")
    print(f"    For higher-is-better metrics, the outlier criterion is z >= +{out['sigma']:.0f}.")
    print(f"    For lower-is-better (Equity DD %), the criterion is z <= -{out['sigma']:.0f}.")
    print(f"    The Trades exclusion guards against over-fitting: a pass with")
    print(f"    very few trades can post an extreme metric value purely by")
    print(f"    luck, so we drop those before ranking the rest.")


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
        description="Parse MT5 Strategy Tester Optimization XML report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text report (default)
  python %(prog)s ReportOptimizer-*.xml

  # JSON dump (raw parsed data)
  python %(prog)s ReportOptimizer-*.xml --json

  # Full optimization analysis (parameter effect, duplicates, best passes)
  python %(prog)s ReportOptimizer-*.xml --analyze

  # Outlier scan: per-pass z-score on the 8 perf metrics,
  # split into "has at least one strong outlier" vs "no outlier"
  python %(prog)s ReportOptimizer-*.xml outliers
  python %(prog)s ReportOptimizer-*.xml outliers --top-outliers 5 --top-normal 5 --sigma 2
  python %(prog)s ReportOptimizer-*.xml outliers --json
""",
    )
    parser.add_argument("report", help="Path to ReportOptimizer-*.xml file")
    parser.add_argument("--json", action="store_true", help="Output raw parsed data as JSON")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run optimization analysis (parameter effect, duplicates, best passes, trade distribution)",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_out = sub.add_parser(
        "outliers",
        help="Per-pass z-score outlier scan on the 8 performance metrics. "
             "Splits passes into a 'strongly-strong' set (at least one metric with |z|>=σ "
             "in the favourable direction) and a 'no-outlier' set, both sorted by Result "
             "desc and printed with the metrics group + the input-parameter group.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: sigma=2, top 10 outlier passes, top 5 normal passes
  python parse_optimizer_report.py ReportOptimizer-*.xml outliers

  # Tighter sigma threshold and custom top-N
  python parse_optimizer_report.py ReportOptimizer-*.xml outliers --sigma 3 --top-outliers 5

  # JSON output for further processing
  python parse_optimizer_report.py ReportOptimizer-*.xml outliers --json

For higher-is-better metrics (Profit, Profit Factor, Recovery Factor,
Sharpe Ratio, Expected Payoff, Custom, Result), an outlier is z >= +σ.
For lower-is-better (Equity DD %), an outlier is z <= -σ. Passes whose
Trades count is itself a low-side outlier (z <= -σ) are excluded
first — they have too few trades to trust.
""",
    )
    p_out.add_argument(
        "--sigma", "-s", type=float, default=2.0,
        help="z-score threshold for the outlier scan (default: 2.0)",
    )
    p_out.add_argument(
        "--top-outliers", type=int, default=10,
        help="Number of passes to show from the 'has at least one outlier' set (default: 10)",
    )
    p_out.add_argument(
        "--top-normal", type=int, default=5,
        help="Number of passes to show from the 'no outlier' set (default: 5)",
    )
    p_out.add_argument(
        "--json", action="store_true", help="Output outliers data as JSON",
    )

    args = parser.parse_args()

    path = Path(args.report)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    env, df = parse_report(path)
    analyze_data = analyze(df, env) if (args.analyze or args.json) else None

    if args.cmd == "outliers":
        out_data = find_outliers(
            df,
            sigma=args.sigma,
            top_outliers=args.top_outliers,
            top_normal=args.top_normal,
        )
        if getattr(args, "json", False):
            payload = {
                "env": asdict(env),
                "pass_count": int(len(df)),
                "columns": list(df.columns),
                "outliers": out_data,
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
        else:
            print_outliers(env, df, out_data)
        return

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
