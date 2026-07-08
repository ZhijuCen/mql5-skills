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
    python skills/mql5/scripts/parse_optimizer_report.py <report.xml> outliers [--top-outliers N] [--top-normal M] [--sigma K] [--sort ABBR_LIST] [--json]
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

# ── Sort abbreviations (for the `outliers` --sort / --priority argument) ──

# Abbreviation → full metric name lookup for the --sort argument.
_SORT_ABBR_TO_FULL = {
    "R": "Result",
    "P": "Profit",
    "EP": "Expected Payoff",
    "PF": "Profit Factor",
    "RF": "Recovery Factor",
    "SR": "Sharpe Ratio",
    "C": "Custom",
    "DD": "Equity DD %",
    "T": "Trades",
}

# Sort direction: True = ascending, False = descending.
# Result / Profit / Expected Payoff / Profit Factor / Recovery Factor /
# Sharpe Ratio / Custom / Trades all descend (higher-is-better).
# Equity DD % ascends (lower drawdown is better).
_SORT_ASCENDING: set[str] = {"Equity DD %"}

# Default sort priority (used when --sort is omitted).
_DEFAULT_SORT_PRIORITY: list[str] = [
    "Result", "Expected Payoff", "Profit Factor",
    "Recovery Factor", "Sharpe Ratio", "Profit",
    "Equity DD %", "Custom", "Trades",
]


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


def _parse_sort_priority(expr: str | None) -> list[str]:
    """Parse --sort expression into ordered list of full metric names.

    Each comma-separated token is an abbreviation from _SORT_ABBR_TO_FULL.
    Unmentioned metrics are appended at the end in _DEFAULT_SORT_PRIORITY order.

    Examples:
      "EP,RF,R,P"  -> Expected Payoff, Recovery Factor, Result, Profit, ...
      "EP"          -> Expected Payoff, Result, Profit Factor, ...
      None          -> _DEFAULT_SORT_PRIORITY (full 9-metric chain)
    """
    if not expr:
        return list(_DEFAULT_SORT_PRIORITY)

    mentioned: list[str] = []
    for token in expr.split(","):
        token = token.strip().upper()
        if token in _SORT_ABBR_TO_FULL:
            mentioned.append(_SORT_ABBR_TO_FULL[token])
        else:
            print(
                f"Warning: unknown sort abbreviation '{token}', ignoring",
                file=sys.stderr,
            )

    seen = set(mentioned)
    for m in _DEFAULT_SORT_PRIORITY:
        if m not in seen:
            mentioned.append(m)
    return mentioned


def _sort_key(rec: dict, priority: list[str]) -> tuple:
    """Multi-key sort key for a pass record.

    Each metric in ``priority`` contributes one sort level. The returned
    flat tuple feeds Python's stable ``list.sort()``.

    None values sort after all present values (sentinel ``(1, 0.0)``
    vs ``(0, signed_value)``).

    Parameters
    ----------
    rec : dict
        A pass record with ``Result``, ``Trades`` (top-level keys) and
        ``perf_metrics`` (inner dict for the remaining metrics).
    priority : list[str]
        Ordered list of full metric names (output of _parse_sort_priority).

    Returns
    -------
    tuple
        Flat tuple suitable for use as ``key`` in ``sorted()``.
        Each level is ``(is_none, signed_value)``.
    """
    parts: list[tuple[int, float]] = []
    for name in priority:
        if name == "Trades":
            v = rec.get("Trades")
        elif name == "Result":
            v = rec.get("Result")
        else:
            v = rec.get("perf_metrics", {}).get(name)

        asc = name not in _SORT_ASCENDING  # everything desc except DD
        if v is None:
            parts.append((1, 0.0))  # push to the very end
        else:
            # desc -> negative value; asc -> positive value
            parts.append((0, v if asc else -v))
    return tuple(parts)


def find_outliers(
    df: pd.DataFrame,
    sigma: float = 2.0,
    top_outliers: int = 10,
    top_normal: int = 5,
    sort_priority: list[str] | None = None,
) -> dict:
    """Per-pass z-score outlier scan across the 8 performance metrics.

    Two disjoint pass sets are returned:

      set_outliers — passes with AT LEAST ONE performance metric whose
        z-score crosses ±sigma in the "strongly-strong" direction
        (higher-is-better: z >= +sigma; lower-is-better Equity DD %:
        z <= -sigma). Sorted by ``sort_priority``; top ``top_outliers`` shown.

      set_normal — passes with NO performance-metric outlier. Sorted by
        ``sort_priority``; top ``top_normal`` shown.

    Both sets EXCLUDE passes whose Trades count is itself a low-side
    outlier (z <= -sigma). Such passes have too few trades to trust
    their performance numbers — including them would inflate the
    outlier set with cheap-pass artifacts.

    Also returns the per-metric mean / std / sigma threshold table so
    the user can judge whether the outlier counts are meaningful.

    Parameters
    ----------
    df : pd.DataFrame
        Parsed optimization report.
    sigma : float
        z-score threshold for outlier detection (default 2.0).
    top_outliers : int
        Max passes to return in set_outliers (default 10).
    top_normal : int
        Max passes to return in set_normal (default 5).
    sort_priority : list[str] | None
        Ordered list of full metric names for the multi-key sort.
        None (= default) uses ``_DEFAULT_SORT_PRIORITY``.

    Returns
    -------
    dict
        See output shape below.
    """
    if sort_priority is None:
        sort_priority = _parse_sort_priority(None)
    out: dict = {"sigma": sigma, "n_passes": int(len(df)), "sort_priority": list(sort_priority)}

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

    # Sort eligible passes by the configured priority chain
    eligible.sort(key=lambda r: _sort_key(r, sort_priority))

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


def _fmt_sort_priority(priority: list[str]) -> str:
    """Compact sort-priority string for display.

    Example output: ``R↓, EP↓, PF↓, RF↓, …``
    """
    rev_lookup = {full: abbr for abbr, full in _SORT_ABBR_TO_FULL.items()}
    parts: list[str] = []
    for name in priority:
        abbr = rev_lookup.get(name, name)
        arrow = "↑" if name in _SORT_ASCENDING else "↓"
        parts.append(f"{abbr}{arrow}")
    if len(parts) > 5:
        parts = parts[:5] + ["…"]
    return ", ".join(parts)


# ── Failure-set analysis (per-column value distribution over failing passes) ──
#
# A pass is "failing" when ANY of the following holds (an OR chain — a single
# failure is enough to drop the pass from the deployable set):
#   - Profit           < 0
#   - Profit Factor    < 1
#   - Expected Payoff  < 0.1
#   - Equity DD %      > 60
#   - Recovery Factor  < 1
#   - Sharpe Ratio     < 1
#
# These thresholds are independent of the run (not z-scores), which makes the
# failure set interpretable on its own — a pass satisfying every criterion is
# deployment-grade on absolute terms, not only relative to this run.

_FAILURE_CRITERIA: list[dict] = [
    # {"metric": MT5 column, "op": "lt"/"gt", "threshold": float}
    {"metric": "Profit",          "op": "lt", "threshold": 0.0},
    {"metric": "Profit Factor",   "op": "lt", "threshold": 1.0},
    {"metric": "Expected Payoff", "op": "lt", "threshold": 0.1},
    {"metric": "Equity DD %",     "op": "gt", "threshold": 60.0},
    {"metric": "Recovery Factor", "op": "lt", "threshold": 1.0},
    {"metric": "Sharpe Ratio",    "op": "lt", "threshold": 1.0},
]


def _row_fails(row: pd.Series, present_metrics: list[str]) -> dict:
    """Return {criterion_name: bool} for each criterion; missing metric = False.

    A criterion that references a metric absent from the report (rare — only
    happens for hand-built reports) defaults to False so we don't false-flag.
    """
    flags: dict[str, bool] = {}
    for c in _FAILURE_CRITERIA:
        m = c["metric"]
        if m not in present_metrics:
            flags[c["metric"]] = False
            continue
        v = row[m]
        if pd.isna(v):
            # NaN on a failure-defining metric — treat as "unknown, don't fail"
            flags[c["metric"]] = False
            continue
        v_f = float(v)
        if c["op"] == "lt":
            flags[m] = v_f < c["threshold"]
        else:  # "gt"
            flags[m] = v_f > c["threshold"]
    return flags


def find_failures(df: pd.DataFrame) -> dict:
    """Per-parameter value distribution over the failure set.

    A pass is in the failure set iff it triggers at least one criterion in
    ``_FAILURE_CRITERIA``. For each input parameter column (everything after
    ``Trades``), we tally how many failing passes hold each value, plus the
    percentage relative to the failure set size.

    Two complementary percentages are reported:
      - pct_of_failures = count_value / n_failures × 100   (share of the failure set)
      - pct_in_failures_vs_global = count_value / global_count_value × 100
        (how concentrated the failures are in this value, vs the run as a whole).
        ">100% impossible; <100% means the value is under-represented in
        failures; >100% does not occur because every failing pass holds some
        value of every param. Skipped when global_count_value == 0."

    Returns:
        dict with keys:
          - env_card, n_passes, n_failures, n_passing
          - criteria: dict criterion_name -> {metric, op, threshold, n_triggered}
          - per_param: dict param_name -> list of
              {"value": str, "count": int, "pct_of_failures": float,
               "global_count": int, "pct_of_global": float}
          - failing_passes: summary list of top failing passes (Pass id,
            triggered criteria, key metric values, parameter values) for
            cross-reference with `outliers`.
    """
    out: dict = {}
    if df.empty:
        out["error"] = "No pass rows"
        return out

    # Resolve which metric columns are actually present in this report.
    present_metrics = [c["metric"] for c in _FAILURE_CRITERIA if c["metric"] in df.columns]
    out["missing_criteria_metrics"] = sorted(
        {c["metric"] for c in _FAILURE_CRITERIA} - set(present_metrics)
    )

    # Per-row failure flags.
    per_row_flags: list[tuple[int, dict, set[str]]] = []
    criteria_trigger_count: dict[str, int] = {m: 0 for m in present_metrics}
    for idx, row in df.iterrows():
        flags = _row_fails(row, present_metrics)
        triggered = {m for m, failed in flags.items() if failed}
        per_row_flags.append((idx, flags, triggered))
        for m in triggered:
            criteria_trigger_count[m] += 1

    failing_idx = [idx for idx, _, trig in per_row_flags if trig]
    n_failures = len(failing_idx)
    n_passes = len(df)

    out["n_passes"] = n_passes
    out["n_failures"] = n_failures
    out["n_passing"] = n_passes - n_failures
    out["failure_rate_pct"] = round(100.0 * n_failures / n_passes, 2) if n_passes else 0.0

    out["criteria"] = [
        {
            "metric": c["metric"],
            "op": c["op"],
            "threshold": c["threshold"],
            "n_triggered": criteria_trigger_count.get(c["metric"], 0),
            "human": _format_criterion(c),
        }
        for c in _FAILURE_CRITERIA
    ]

    pcols = _param_cols(df)
    out["params"] = list(pcols)

    per_param: dict = {}
    if n_failures == 0:
        # Avoid divide-by-zero; emit empty distributions.
        for p in pcols:
            per_param[p] = []
    else:
        failing_df = df.loc[failing_idx]
        for p in pcols:
            counts = (
                failing_df[p]
                .value_counts(dropna=False)
                .reset_index(name="count")
            )
            counts.columns = ["value", "count"]  # first col is the param name
            # Global counts (across all passes) for the pct_of_global column.
            global_counts = (
                df[p].value_counts(dropna=False).to_dict()
            )
            records: list[dict] = []
            for _, r in counts.iterrows():
                v = r["value"]
                cnt = int(r["count"])
                gc = int(global_counts.get(v, 0))
                rec = {
                    "value": _fmt_param_value(v),
                    "count": cnt,
                    "pct_of_failures": round(100.0 * cnt / n_failures, 2),
                    "global_count": gc,
                }
                if gc > 0:
                    rec["pct_of_global"] = round(100.0 * cnt / gc, 2)
                else:
                    rec["pct_of_global"] = None
                records.append(rec)
            # Sort: descending count, then by the value itself for stable output.
            records.sort(key=lambda d: (-d["count"], str(d["value"])))
            per_param[p] = records
    out["per_param"] = per_param

    # Top failing passes (≤10) for cross-reference with `outliers`.
    failing_records: list[dict] = []
    for idx, flags, triggered in per_row_flags:
        if not triggered:
            continue
        row = df.loc[idx]
        rec = {
            "Pass": int(row["Pass"]) if "Pass" in df.columns and pd.notna(row["Pass"]) else None,
            "Result": float(row["Result"]) if "Result" in df.columns and pd.notna(row["Result"]) else None,
            "Profit": float(row["Profit"]) if "Profit" in df.columns and pd.notna(row["Profit"]) else None,
            "Expected Payoff": float(row["Expected Payoff"]) if "Expected Payoff" in df.columns and pd.notna(row["Expected Payoff"]) else None,
            "Profit Factor": float(row["Profit Factor"]) if "Profit Factor" in df.columns and pd.notna(row["Profit Factor"]) else None,
            "Recovery Factor": float(row["Recovery Factor"]) if "Recovery Factor" in df.columns and pd.notna(row["Recovery Factor"]) else None,
            "Sharpe Ratio": float(row["Sharpe Ratio"]) if "Sharpe Ratio" in df.columns and pd.notna(row["Sharpe Ratio"]) else None,
            "Equity DD %": float(row["Equity DD %"]) if "Equity DD %" in df.columns and pd.notna(row["Equity DD %"]) else None,
            "Trades": int(row["Trades"]) if "Trades" in df.columns and pd.notna(row["Trades"]) else None,
            "triggered": sorted(triggered),
            "n_triggered": len(triggered),
            "params": {p: _fmt_param_value(row[p]) for p in pcols},
        }
        failing_records.append(rec)

    # Sort: most-triggered first, then by Result ascending, then by Equity DD % desc.
    def _fail_sort_key(r: dict) -> tuple:
        return (
            -r["n_triggered"],
            r["Result"] if r["Result"] is not None else 0.0,
            -(r["Equity DD %"] if r["Equity DD %"] is not None else 0.0),
        )
    failing_records.sort(key=_fail_sort_key)
    out["failing_passes_top"] = failing_records[:10]
    out["failing_passes_total"] = len(failing_records)

    return out


def _format_criterion(c: dict) -> str:
    """Human-readable criterion expression: 'Profit Factor < 1'."""
    op_str = "<" if c["op"] == "lt" else ">"
    return f"{c['metric']} {op_str} {c['threshold']}"


def _fmt_param_value(v) -> str:
    """Render a pandas value as a compact, JSON-friendly string."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "<NA>"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def print_failures(env: Env, df: pd.DataFrame, out: dict) -> None:
    """Pretty-print the failure-set analysis as a text report.

    Layout:
      Header card (env + n_passes / n_failures / n_passing / failure_rate)
      Criteria table (one row per criterion with the triggered count)
      Per-parameter distribution tables (sorted by descending count)
      Top failing passes cross-reference (≤10)

    Each parameter table shows:
      value          count    pct_of_failures   global_count   pct_of_global
    where pct_of_global is the share of all passes with that parameter value
    that ended up failing — a concentration measure that complements the
    within-failure-set share.
    """
    print("=" * 78)
    print("  Optimization Failure-Set Analysis  "
          "(per-param value distribution over failing passes)")
    print("=" * 78)
    print(f"  EA: {env.ea_name or '(unknown)'}  Symbol: {env.symbol or '(unknown)'}  "
          f"Period: {env.period or '(unknown)'}")
    print(f"  Date range: {env.date_from} → {env.date_to}")
    print()

    if "error" in out:
        print(f"  ERROR: {out['error']}")
        return

    if out.get("missing_criteria_metrics"):
        print(f"  ⚠️  Missing criteria metrics in report: "
              f"{', '.join(out['missing_criteria_metrics'])} — those criteria cannot fire")

    # Summary
    print(f"  Passes total:        {out['n_passes']}")
    print(f"  Passes failing:      {out['n_failures']}  "
          f"({out['failure_rate_pct']:.2f}% of total)")
    print(f"  Passes passing:      {out['n_passing']}")
    print()

    # Criteria table
    print("  Criteria (a pass fails if ANY one fires — OR chain):")
    print(f"  {'Criterion':<28} {'Triggered':>12} {'% of passes':>14}")
    print("  " + "─" * 58)
    for c in out["criteria"]:
        pct = (100.0 * c["n_triggered"] / out["n_passes"]) if out["n_passes"] else 0.0
        print(f"  {c['human']:<28} {c['n_triggered']:>12} {pct:>13.2f}%")
    print()

    # Per-parameter tables
    if not out["per_param"]:
        print("  No parameters to tabulate.")
    elif out["n_failures"] == 0:
        print("  Failure set is empty — every pass satisfies all criteria.")
        print("  (Parameter tables would be meaningless; skipped.)")
    else:
        for p, records in out["per_param"].items():
            self_width = max(len(p), 12)
            print("=" * 78)
            print(f"  Parameter: {p}   ({len(records)} distinct values in failure set)")
            print("=" * 78)
            print(f"  {'value':<{self_width}} {'count':>7} "
                  f"{'pct_of_failures':>16} {'global_count':>14} {'pct_of_global':>14}")
            print("  " + "─" * (self_width + 4 + 7 + 16 + 14 + 14))
            for r in records:
                pct_g = r.get("pct_of_global")
                pct_g_str = f"{pct_g:>13.2f}%" if pct_g is not None else f"{'n/a':>14}"
                print(f"  {str(r['value'])[:self_width]:<{self_width}} "
                      f"{r['count']:>7} "
                      f"{r['pct_of_failures']:>15.2f}% "
                      f"{r['global_count']:>14} "
                      f"{pct_g_str}")
            print()

    # Top failing passes cross-reference
    if out.get("failing_passes_top"):
        n_top = len(out["failing_passes_top"])
        n_total = out.get("failing_passes_total", n_top)
        print("=" * 78)
        print(f"  TOP FAILING PASSES — most-triggered first, top {n_top} of {n_total}")
        print("=" * 78)
        for rec in out["failing_passes_top"]:
            pass_str = f"Pass {rec['Pass']:<5}" if rec["Pass"] is not None else "Pass ?    "
            res_str = f"Result={rec['Result']:.2f}" if rec["Result"] is not None else "Result=?"
            trig = ", ".join(rec["triggered"])
            print(f"  {pass_str} {res_str}  "
                  f"({rec['n_triggered']} criteria: {trig})")
            # Key metrics
            metric_parts = []
            for label, key, fmt in [
                ("Profit", "Profit", "{:.1f}"),
                ("EP", "Expected Payoff", "{:.3f}"),
                ("PF", "Profit Factor", "{:.2f}"),
                ("RF", "Recovery Factor", "{:.2f}"),
                ("Sharpe", "Sharpe Ratio", "{:.2f}"),
                ("EqDD%", "Equity DD %", "{:.2f}"),
                ("Trades", "Trades", "{}"),
            ]:
                v = rec.get(key)
                if v is None:
                    continue
                if key == "Trades":
                    metric_parts.append(f"{label}={int(v)}")
                else:
                    metric_parts.append(f"{label}={fmt.format(v)}")
            if metric_parts:
                print(f"           Metrics:   " + "  ".join(metric_parts))
            # Params (compact)
            if rec["params"]:
                pparts = [f"{p}={v}" for p, v in rec["params"].items()]
                lines = []
                cur, cur_len = [], 0
                for part in pparts:
                    if cur and cur_len + len(part) + 2 > 70:
                        lines.append(", ".join(cur))
                        cur, cur_len = [part], len(part)
                    else:
                        cur.append(part)
                        cur_len += len(part) + 2
                if cur:
                    lines.append(", ".join(cur))
                print(f"           Params:    {lines[0]}")
                for extra in lines[1:]:
                    print(f"                      {extra}")
            print()
    elif out["n_failures"] > 0:
        print("  Top failing passes: skipped (empty result set).")
    print()

    # Interpretation
    print("  Interpretation:")
    print("    A pass is in the failure set when ANY criterion fires (OR chain).")
    print("    For each parameter, pct_of_failures is the share of failing")
    print("    passes that hold that value; pct_of_global is the share of")
    print("    ALL passes with that value that ended up failing — a")
    print("    concentration measure.")
    print("    A single value where pct_of_global is large (>50%) is a")
    print("    smoking gun for the parameter; values near the global average")
    print("    are pure sampling noise.")


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
    sort_priority = out.get("sort_priority", list(_DEFAULT_SORT_PRIORITY))
    sort_fmt = _fmt_sort_priority(sort_priority)
    print(f"  Sort priority: {sort_fmt}")
    print(f"  Set A (>=1 perf outlier): {c['outliers']} passes")
    print(f"  Set B (no perf outlier):   {c['normal']} passes")
    if c["excluded_low_trades"]:
        print(f"  Excluded (Trades z<=-σ, too few trades to trust): {c['excluded_low_trades']} passes")
    print()

    pcols = _param_cols(df)

    # Set A
    if out["set_outliers"]:
        print("=" * 78)
        print(f"  SET A — Passes with at least one performance-metric outlier")
        print(f"          (top {len(out['set_outliers'])}; "
              f"sort: {sort_fmt}; {c['outliers']} total eligible)")
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
        print(f"  SET B — Passes with no performance-metric outlier "
              f"(top {len(out['set_normal'])}; sort: {sort_fmt})")
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

# Sub-command catalogue kept at module level so the position-order validator
# (``_validate_argv_position``) stays in sync with what argparse actually
# accepts.
_VALID_SUBCOMMANDS = {"report", "analyze", "outliers", "failures"}


def _validate_argv_position(argv: list[str], prog: str = "") -> None:
    """Reject any argv layout where a sub-command is NOT the first token.

    Target layout — mandatory:
        {prog} [--help] SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]

    Specifically:
      - The very first non-flag token must be one of ``_VALID_SUBCOMMANDS``.
      - ``--help``/``-h`` is the only flag allowed before the sub-command
        (so `*.py --help` reaches argparse's help path without confusion).
      - ``-o``/``--output`` is a sub-command-level flag — it MUST come after
        SUB_COMMAND. We enforce that here so the user gets a clear error
        instead of an argparse stack trace.

    Exits with a clear error message + usage hint. Skipped when the user only
    passed ``--help``/``-h`` (in which case argparse prints its own usage).
    """
    if argv in ([], ["--help"], ["-h"]):
        return  # argparse will handle --help cleanly

    # Find the first non-flag token after skipping leading --help.
    i = 0
    if argv and argv[0] in ("--help", "-h"):
        return

    # The first token must be the sub-command — no global flags before it
    # other than --help. We strictly enforce this; even a leading --json is
    # rejected, telling the user to move it after the sub-command.
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
    # positional. We accept any "short-form" pattern that looks like a flag
    # (starts with "-" but isn't a bare "-") — including -o OUT, --json,
    # --sigma 2.5, --top-outliers 10, etc. The cursor advances by 2 when the
    # flag looks like it takes a value (no leading "=" yet consumed and the
    # next token doesn't start with "-"); otherwise just by 1.
    j = 1
    # Flags that take NO value (presence-only).
    no_value_flags = {"--json"}
    while j < len(argv) and argv[j].startswith("-"):
        tok = argv[j]
        # --top-outliers=N or --top-outliers N style
        if "=" in tok:
            j += 1
            continue
        if tok in no_value_flags:
            j += 1
            continue
        # Anything else takes a value: -o OUT, --sigma 2.5, --sort EP,...
        if tok in ("-o", "--output"):
            # The mandatory OUTPUT_FILE value comes right after.
            if j + 1 < len(argv) and not argv[j + 1].startswith("-"):
                j += 2
            else:
                # argparse will print a friendly error for missing -o value.
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


def _emit_json(obj: dict, output_path: str | None) -> None:
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


def main() -> None:
    prog = Path(sys.argv[0]).name
    _validate_argv_position(sys.argv[1:], prog=prog)

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Parse MT5 Strategy Tester Optimization XML report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Target CLI layout (mandatory):
  %(prog)s [--help] SUB_COMMAND INPUT_FILE [OPTIONS] [-o OUTPUT_FILE]

Sub-commands:
  report     Default text report (env card + parameter cardinalities).
  analyze    Full analysis: parameter effect, duplicates, best passes, trade
             distribution.
  outliers   Per-pass z-score outlier scan on the 8 performance metrics.
             Splits passes into "has at least one strong outlier" vs "no
             outlier"; both sorted by the configured priority.
  failures   Failure-set analysis: per-parameter value distribution over
             passes that fail at least one of 6 absolute criteria.

Sub-command flags (always come AFTER the sub-command and INPUT_FILE):
  --json            Emit JSON instead of the default text report.
  -o OUTPUT_FILE    Write output to OUTPUT_FILE instead of stdout. Encoding
                    is JSON when --json is set, otherwise text.

Examples:
  # Default text report, written to a file
  %(prog)s report jobs/foo/ReportOptimizer-*.xml -o report.txt

  # Full JSON analysis
  %(prog)s analyze jobs/foo/ReportOptimizer-*.xml --json -o analysis.json

  # Outlier scan with custom sigma + write output
  %(prog)s outliers jobs/foo/ReportOptimizer-*.xml --sigma 2.5 -o outliers.txt

  # Failure-set analysis
  %(prog)s failures jobs/foo/ReportOptimizer-*.xml
  %(prog)s failures jobs/foo/ReportOptimizer-*.xml --json -o failures.json
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="SUB_COMMAND", required=True)

    def _add_shared(sub_parser):
        """Add the flags every sub-command understands."""
        sub_parser.add_argument(
            "report", help="Path to ReportOptimizer-*.xml file",
        )
        sub_parser.add_argument(
            "--json", action="store_true",
            help="Emit JSON instead of the default text report",
        )
        sub_parser.add_argument(
            "-o", "--output", dest="output", default=None, metavar="OUTPUT_FILE",
            help="Write output to OUTPUT_FILE (default: stdout). Encoding is "
                 "auto-detected: --json => JSON, otherwise text.",
        )

    # ── report ──
    p_report = sub.add_parser(
        "report",
        help="Default text report (env card + parameter cardinalities).",
        description="Default text report: env card (EA / Symbol / Period / dates / "
                    "deposit / leverage / MT5 build), then per-parameter "
                    "cardinalities. Use `analyze` for parameter-effect analysis.",
    )
    _add_shared(p_report)

    # ── analyze ──
    p_an = sub.add_parser(
        "analyze",
        help="Full analysis (parameter effect, duplicates, best passes, trade distribution).",
        description="Full optimization analysis: orthogonality, per-parameter "
                    "effect/dead-param detection, duplicates, best passes by "
                    "Profit/PF/RF/Custom, trade-count distribution + correlations. "
                    "Emit JSON when --json is set (recommended for downstream "
                    "processing); otherwise emit a text report.",
    )
    _add_shared(p_an)

    # ── outliers ──
    p_out = sub.add_parser(
        "outliers",
        help="Per-pass z-score outlier scan on the 8 performance metrics. "
             "Splits passes into a 'strongly-strong' set (at least one metric with |z|>=σ "
             "in the favourable direction) and a 'no-outlier' set, both sorted by the "
             "configured priority (default: R↓, EP↓, PF↓, RF↓, …) and printed with the "
             "metrics group + the input-parameter group.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: sigma=2, top 10 outlier passes, top 5 normal passes
  %(prog)s outliers INPUT_FILE

  # Custom sort: priority by EP, then RF, then R, then P; rest in default order
  %(prog)s outliers INPUT_FILE --sort EP,RF,R,P

  # Single priority metric; all others follow in default order
  %(prog)s outliers INPUT_FILE --sort EP

  # Tighter sigma threshold and custom top-N
  %(prog)s outliers INPUT_FILE --sigma 3 --top-outliers 5

  # JSON output for further processing
  %(prog)s outliers INPUT_FILE --json

For higher-is-better metrics (Profit, Profit Factor, Recovery Factor,
Sharpe Ratio, Expected Payoff, Custom, Result), an outlier is z >= +σ.
For lower-is-better (Equity DD %), the criterion is z <= -σ. Passes whose
Trades count is itself a low-side outlier (z <= -σ) are excluded
first — they have too few trades to trust.

Sort abbreviations (for --sort):
  R=Result  P=Profit  EP=Expected Payoff  PF=Profit Factor  RF=Recovery Factor
  SR=Sharpe Ratio  C=Custom  DD=Equity DD %  T=Trades
  Default priority: R↓, EP↓, PF↓, RF↓, SR↓, P↓, DD↑, C↓, T↓
  (↓ = descending, ↑ = ascending; Equity DD % ascends — lower is better)
""",
    )
    _add_shared(p_out)
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
        "--sort", type=str, default=None,
        help="Comma-separated sort priority using metric abbreviations "
             "(e.g. 'EP,RF,R,P'). Default: full chain R↓,EP↓,PF↓,RF↓,SR↓,P↓,DD↑,C↓,T↓. "
             "Unmentioned metrics append in default order. "
             "Abbreviations: R=Result P=Profit EP=Expected Payoff PF=Profit Factor "
             "RF=Recovery Factor SR=Sharpe Ratio C=Custom DD=Equity DD %% T=Trades",
    )

    # ── failures ──
    p_fail = sub.add_parser(
        "failures",
        help="Failure-set analysis: per-parameter value distribution over passes "
             "that fail at least one of 6 absolute criteria (Profit<0, PF<1, "
             "EP<0.1, EqDD%%>60, RF<1, Sharpe<1).",
        description="Failure-set analysis: a pass is in the failure set when ANY of "
                    "6 absolute criteria fires (an OR chain — a single failure is "
                    "enough to drop the pass from the deployable set). For each "
                    "input parameter column, tabulate count + pct_of_failures + "
                    "pct_of_global (the share of all passes with that value that "
                    "ended up failing — a concentration measure).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: text report (criteria table + per-param value tables + top-10 fails)
  %(prog)s failures INPUT_FILE

  # JSON output for downstream piping
  %(prog)s failures INPUT_FILE --json

  # Save text report to a file
  %(prog)s failures INPUT_FILE -o failures_report.txt

A single parameter value where pct_of_global > 50% is a smoking gun: nearly
every pass with that setting fails. Drop it from the optimization grid.
""",
    )
    _add_shared(p_fail)

    args = parser.parse_args()
    output_path = getattr(args, "output", None)

    path = Path(args.report)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    env, df = parse_report(path)

    # ── dispatch ──
    if args.cmd == "report":
        if args.json:
            payload = {
                "env": asdict(env),
                "pass_count": int(len(df)),
                "columns": list(df.columns),
                "passes": df.where(pd.notnull(df), None).to_dict("records"),
            }
            _emit_json(payload, output_path)
        else:
            text = _capture_stdout(print_report, env, df)
            _emit_text(text, output_path)
        return

    if args.cmd == "analyze":
        analyze_data = analyze(df, env)
        if args.json:
            payload = {
                "env": asdict(env),
                "pass_count": int(len(df)),
                "columns": list(df.columns),
                "passes": df.where(pd.notnull(df), None).to_dict("records"),
                "analyze": analyze_data,
            }
            _emit_json(payload, output_path)
        else:
            text = _capture_stdout(print_analyze, env, df, analyze_data)
            _emit_text(text, output_path)
        return

    if args.cmd == "outliers":
        out_data = find_outliers(
            df,
            sigma=args.sigma,
            top_outliers=args.top_outliers,
            top_normal=args.top_normal,
            sort_priority=_parse_sort_priority(args.sort),
        )
        if args.json:
            payload = {
                "env": asdict(env),
                "pass_count": int(len(df)),
                "columns": list(df.columns),
                "outliers": out_data,
            }
            _emit_json(payload, output_path)
        else:
            text = _capture_stdout(print_outliers, env, df, out_data)
            _emit_text(text, output_path)
        return

    if args.cmd == "failures":
        fail_data = find_failures(df)
        if args.json:
            payload = {
                "env": asdict(env),
                "pass_count": int(len(df)),
                "columns": list(df.columns),
                "failures": fail_data,
            }
            _emit_json(payload, output_path)
        else:
            text = _capture_stdout(print_failures, env, df, fail_data)
            _emit_text(text, output_path)
        return

    # argparse with required=True on the subparsers group guarantees we never
    # get here, but be explicit for future maintenance.
    parser.error(f"unknown sub-command: {args.cmd}")


if __name__ == "__main__":
    main()
