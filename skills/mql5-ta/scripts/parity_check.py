#!/usr/bin/env python3
"""parity_check.py — numeric parity: MQL5 indicator export vs TA-Lib.

Compares the CSV written by assets/mql5-side/TAParity-S.mq5 (bars + MQL5
indicator values, same range) against TA-Lib recomputations from the very
same bars. Verdicts per indicator:

  PASS        identical within tolerance after trimming the NaN/EMPTY head
  EXPECTED    difference is documented (e.g. iADX non-Wilder vs talib.ADX)
  FAIL        undocumented mismatch -> investigate

Usage:
  uv run python scripts/parity_check.py MQL5/Files/ta_parity_XAUUSD_M1.csv
  uv run python scripts/parity_check.py --selftest          # checker self-test
  uv run python scripts/parity_check.py FILE --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import talib

# tolerances: values printed with 10 decimals; float noise only
ATOL, RTOL = 1e-6, 1e-6

# History-seeded indicators (EMA/SMMA/Wilder/MACD) depend on ALL bars before
# the export window; their seed difference decays geometrically but needs a
# burn-in before |diff| falls below tolerance (RSI14 needs ~212 bars,
# ADXW ~191, MACD ~164, EMA10 ~61). Compare only after this many bars.
BURN_IN = 250

# MT5 column -> (recompute fn, class).  class: "exact" | "expected_diff"
MAPS: dict[str, tuple] = {}  # filled by build_maps()


def build_maps():
    def smma(s: pd.Series, n: int) -> pd.Series:
        return s.ewm(alpha=1 / n, adjust=False).mean()

    def macd_main(c):
        return talib.EMA(c, 12) - talib.EMA(c, 26)

    def macd_sig(c):
        return talib.SMA(macd_main(c), 9)  # MQL5 signal = SMA of main

    def true_range(h, l, c):
        pc = c.shift(1)
        return pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)

    def stoch_k_mql5(h, l, c, v):
        """MQL5 iStochastic MAIN: numerator & denominator are smoothed
        SEPARATELY (classic MT4 implementation), not SMA of raw %K."""
        num = (c - l.rolling(5).min()).rolling(3).mean()
        den = (h.rolling(5).max() - l.rolling(5).min()).rolling(3).mean()
        return num / den * 100

    def stoch_d_mql5(h, l, c, v):
        return stoch_k_mql5(h, l, c, v).rolling(3).mean()

    MAPS.update(
        {
            "RSI14": (lambda h, l, c, v: talib.RSI(c, 14), "exact"),
            "ATR14_SMA_TR": (lambda h, l, c, v: true_range(h, l, c).rolling(14).mean(), "exact"),
            "ATR14_WILDER": (lambda h, l, c, v: talib.ATR(h, l, c, 14), "expected_diff"),
            "CCI14": (lambda h, l, c, v: talib.CCI(h, l, c, 14), "exact"),
            "WILLR14": (lambda h, l, c, v: talib.WILLR(h, l, c, 14), "exact"),
            "STOCH_K": (stoch_k_mql5, "exact"),
            "STOCH_D": (stoch_d_mql5, "exact"),
            "SMA10": (lambda h, l, c, v: talib.SMA(c, 10), "exact"),
            "EMA10": (lambda h, l, c, v: talib.EMA(c, 10), "exact"),
            "SMMA10": (lambda h, l, c, v: smma(c, 10), "exact"),
            "LWMA10": (lambda h, l, c, v: talib.WMA(c, 10), "exact"),
            "MACD_MAIN": (lambda h, l, c, v: macd_main(c), "exact"),
            "MACD_SIG": (lambda h, l, c, v: macd_sig(c), "exact"),
            "OSMA": (lambda h, l, c, v: macd_main(c) - macd_sig(c), "exact"),
            "ADXW14": (lambda h, l, c, v: talib.ADX(h, l, c, 14), "exact"),
            "PLUSDI14": (lambda h, l, c, v: talib.PLUS_DI(h, l, c, 14), "exact"),
            "MINUSDI14": (lambda h, l, c, v: talib.MINUS_DI(h, l, c, 14), "exact"),
            "ADX14_STD": (lambda h, l, c, v: talib.ADX(h, l, c, 14), "expected_diff"),
        }
    )


EMPTY_VALUE = 1.7976931348623157e308  # MQL5 EMPTY_VALUE (DBL_MAX)


def load_export(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df = df.sort_values("time").reset_index(drop=True)  # ascending
    for col in df.columns[1:]:
        df.loc[df[col] >= EMPTY_VALUE / 2, col] = np.nan  # EMPTY_VALUE -> NaN
    return df


# export column alias: MAPS key -> column name in the TAParity-S CSV
EXPORT_COL = {"ATR14_SMA_TR": "ATR14", "ATR14_WILDER": "ATR14"}


def compare(df: pd.DataFrame) -> list[dict]:
    h, l, c, v = df["high"], df["low"], df["close"], df["tickvol"]
    results = []
    for name, (fn, klass) in MAPS.items():
        col = EXPORT_COL.get(name, name)
        if col not in df.columns:
            results.append({"indicator": name, "verdict": "MISSING", "class": klass})
            continue
        mt5 = pd.Series(df[col].astype(float)).reset_index(drop=True)
        tal = pd.Series(np.asarray(fn(h, l, c, v), dtype=float)).reset_index(drop=True)
        # burn-in: history-seeded indicators need warm-up before seed diffs decay
        mt5.iloc[:BURN_IN] = np.nan
        tal.iloc[:BURN_IN] = np.nan
        # trim heads: from the first index where BOTH sides are valid
        valid = mt5.notna() & tal.notna()
        if not valid.any():
            results.append({"indicator": name, "verdict": "NO_OVERLAP", "class": klass})
            continue
        m, t = mt5[valid], tal[valid]
        diff = (m - t).abs()
        tol = ATOL + RTOL * t.abs()
        bad = diff > tol
        max_rel = float((diff / t.abs().clip(lower=1e-12)).max())
        verdict = "PASS" if not bad.any() else klass.upper() if klass == "expected_diff" else "FAIL"
        results.append(
            {
                "indicator": name,
                "verdict": verdict,
                "class": klass,
                "compared": int(valid.sum()),
                "max_abs_diff": float(diff.max()),
                "max_rel_diff": max_rel,
                "n_violations": int(bad.sum()),
                "first_violation_row": int(np.flatnonzero(bad.to_numpy())[0]) if bad.any() else None,
            }
        )
    return results


def selftest() -> pd.DataFrame:
    """Feed TA-Lib values as the fake 'MT5 export' -> all must PASS,
    except the EXPECTED pair which we deliberately perturb."""
    rng = np.random.default_rng(7)
    n = 600
    close = 2000 + np.cumsum(rng.normal(0, 0.5, n))
    high = close + np.abs(rng.normal(0, 0.3, n))
    low = close - np.abs(rng.normal(0, 0.3, n))
    vol = rng.integers(100, 900, n).astype(float)
    df = pd.DataFrame({"time": pd.date_range("2024-01-01", periods=n, freq="1min"),
                       "open": close, "high": high, "low": low, "close": close, "tickvol": vol})
    build_maps()
    for name, (fn, _) in MAPS.items():
        col = EXPORT_COL.get(name, name)
        if col in df.columns:
            continue  # ATR14 alias: one fake column serves both entries
        df[col] = np.asarray(fn(df["high"], df["low"], df["close"], df["tickvol"]), dtype=float)
    df["ADX14_STD"] = df["ADX14_STD"] * 1.5  # fake the documented difference
    return df


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path, nargs="?", help="CSV from TAParity-S.mq5")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    ns = ap.parse_args()
    build_maps()

    df = selftest() if ns.selftest else load_export(ns.file)
    results = compare(df)

    if ns.json:
        print(json.dumps({"source": "selftest" if ns.selftest else str(ns.file), "results": results},
                         indent=2, ensure_ascii=False))
    else:
        print(f"{'indicator':<12} {'verdict':<9} {'class':<14} {'n':>5} {'max_abs':>12} {'max_rel':>10} {'viol':>5}")
        for r in results:
            print(f"{r['indicator']:<12} {r['verdict']:<9} {r['class']:<14} "
                  f"{r.get('compared', 0):>5} {r.get('max_abs_diff', float('nan')):>12.3e} "
                  f"{r.get('max_rel_diff', float('nan')):>10.2e} {r.get('n_violations', 0):>5}")
        fails = [r for r in results if r["verdict"] in ("FAIL", "MISSING", "NO_OVERLAP")]
        print(f"\n{len(results) - len(fails)}/{len(results)} OK"
              + (f"; PROBLEMS: {[r['indicator'] for r in fails]}" if fails else ""))
    return 0 if ns.selftest else int(any(r["verdict"] == "FAIL" for r in results))


if __name__ == "__main__":
    sys.exit(main())
