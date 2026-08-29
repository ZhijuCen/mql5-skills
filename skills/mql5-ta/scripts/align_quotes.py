#!/usr/bin/env python3
"""align_quotes.py — Quote alignment & mixed-timeframe detection for mql5-ta.

Input: MT5-exported quote files (nominally TSV, fields wrapped in <...>),
but any delimited text (tab/comma/semicolon) with bracketed or plain
headers is accepted.

What it does
------------
1. Parse & normalize: sniff delimiter, strip <...> from headers, merge
   <DATE> + <TIME> into a datetime index, sort ascending, drop duplicates.
2. Detect sampling regime: MT5 quote vendors may backfill OLD history at a
   COARSER timeframe than the file's nominal timeframe (e.g. an "M1" file
   whose older half is actually H1-spaced bars). Users cannot spot this by
   eye. We infer per-bar spacing and report contiguous coarse segments.
   Session gaps (overnight maintenance, weekends) are excluded from this
   classification — a gap is only an anomaly if it is a small multiple
   (>= 2x, <= session threshold) of the nominal timeframe.
3. Align to a target timeframe (per skill rule):
   - target == nominal (or finer): coarse segments CANNOT be synthesized
     upward -> they are DROPPED (kept only in the report).
   - target coarser than every segment: the WHOLE file is aggregated
     (open=first, high=max, low=min, close=last, tickvol=sum, vol=sum,
     spread=mean) so the coarse part is fully utilized.
4. Validate: OHLC sanity (high >= max(open, close), low <= min(open, close)),
   residual duplicate timestamps, non-ascending order.

Usage
-----
  python align_quotes.py FILE                    # report only (auto TF)
  python align_quotes.py FILE --tf H1 --out aligned.tsv
  python align_quotes.py FILE --json

Timeframe syntax: M<n>, H<n>, D1, W1, MN1 (as in MT5).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

SESSION_GAP_MINUTES = 6 * 60  # spacing above this is a session gap, not a TF anomaly

TF_MINUTES = {}
for n in range(1, 60):
    TF_MINUTES[f"M{n}"] = n
for n in range(1, 25):
    TF_MINUTES[f"H{n}"] = n * 60
TF_MINUTES.update({"D1": 1440, "W1": 10080, "MN1": 43200})


def tf_to_minutes(tf: str) -> int:
    tf = tf.upper()
    if tf not in TF_MINUTES:
        raise ValueError(f"Unknown timeframe {tf!r}; use e.g. M1 M5 M15 H1 H4 D1 W1 MN1")
    return TF_MINUTES[tf]


def read_quotes(path: Path) -> pd.DataFrame:
    """Read an MT5 quote export; tolerate delimiter and header variations."""
    with open(path, encoding="utf-8-sig") as fh:
        first = fh.readline()
    delim = "\t"
    for cand in ("\t", ";", ","):
        if first.count(cand) >= first.count(delim):
            delim = cand
    df = pd.read_csv(path, sep=delim, encoding="utf-8-sig")
    df.columns = [c.strip().strip("<>").lower() for c in df.columns]
    need = {"date", "open", "high", "low", "close"}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns {missing}; got {list(df.columns)}")
    if "time" in df.columns:
        ts = pd.to_datetime(df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M:%S")
        df = df.drop(columns=["time"])
    else:
        ts = pd.to_datetime(df["date"], format="%Y.%m.%d")
    df = df.drop(columns=["date"])
    df.insert(0, "datetime", ts)
    n0 = len(df)
    df = df.sort_values("datetime").drop_duplicates(subset="datetime", keep="first")
    df = df.reset_index(drop=True)
    df.attrs["dropped_rows"] = n0 - len(df)
    return df


def spacing_series(ts: pd.Series) -> pd.Series:
    return ts.diff().dt.total_seconds().div(60)  # minutes


def detect_segments(df: pd.DataFrame, nominal_min: int) -> list[dict]:
    """Find contiguous coarse segments (spacing = k*nominal, k >= 2, not a session gap)."""
    ts = df["datetime"]
    sp = spacing_series(ts)
    session = sp > SESSION_GAP_MINUTES
    multiple = (sp / nominal_min).round(2)
    coarse = (
        (sp >= 2 * nominal_min)
        & (sp <= SESSION_GAP_MINUTES)
        & ~session
        & (multiple == multiple.round())  # clean k*nominal, not an arbitrary gap
    )
    segments: list[dict] = []
    i = 0
    n = len(df)
    while i < n:
        if not coarse.iloc[i]:
            i += 1
            continue
        j = i
        while j + 1 < n:
            nxt = j + 1
            # continue through coarse bars AND stray fine bars (< 60s-class spacing)
            if coarse.iloc[nxt] or (sp.iloc[nxt] < nominal_min and not session.iloc[nxt]):
                j += 1
                continue
            break
        segments.append(
            {
                "start": ts.iloc[i].strftime("%Y.%m.%d %H:%M:%S"),
                "end": ts.iloc[j].strftime("%Y.%m.%d %H:%M:%S"),
                "end_coarse": ts.iloc[j - 1 if not coarse.iloc[j] else j].strftime("%Y.%m.%d %H:%M:%S"),
                "bars": int(j - i + 1),
                "coarse_bars": int(coarse.iloc[i : j + 1].sum()),
                "inferred_tf_minutes": int(sp.iloc[i : j + 1][coarse.iloc[i : j + 1]].median()),
            }
        )
        i = j + 1
    # drop insignificant runs (isolated missing-bar gaps) and merge across session gaps
    segments = [s for s in segments if s["coarse_bars"] >= 3]
    merged: list[dict] = []
    for s in segments:
        if merged and pd.Timestamp(s["start"]) - pd.Timestamp(merged[-1]["end"]) > pd.Timedelta(minutes=SESSION_GAP_MINUTES):
            prev = merged[-1]
            prev["end"] = s["end"]
            prev["end_coarse"] = s["end_coarse"]
            prev["bars"] += s["bars"]
            prev["coarse_bars"] += s["coarse_bars"]
        else:
            merged.append(s)
    return merged


def dominant_tf(df: pd.DataFrame) -> int:
    sp = spacing_series(df["datetime"]).dropna()
    regular = sp[(sp >= 1) & (sp <= SESSION_GAP_MINUTES)]
    if regular.empty:
        raise ValueError("Cannot infer timeframe: too few bars")
    return int(regional_mode(regular))


def regional_mode(s: pd.Series) -> float:
    return s.mode().iloc[0]


def aggregate(df: pd.DataFrame, minutes: int) -> pd.DataFrame:
    keys = {"datetime": "first"}
    agg = {"open": "first", "high": "max", "low": "min", "close": "last"}
    for col in ("tickvol", "vol"):
        if col in df.columns:
            agg[col] = "sum"
    if "spread" in df.columns:
        agg["spread"] = "mean"
    g = df.set_index("datetime").resample(f"{minutes}min").agg(agg).dropna(subset=["close"])
    return g.reset_index()


def validate(df: pd.DataFrame) -> dict:
    bad_ohlc = int(((df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))).sum())
    return {
        "rows": len(df),
        "sorted_ascending": bool(df["datetime"].is_monotonic_increasing),
        "duplicate_timestamps": int(df["datetime"].duplicated().sum()),
        "ohlc_violations": bad_ohlc,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("--tf", default=None, help="Target timeframe (M1..MN1). Default: auto (nominal, drop coarser segments).")
    ap.add_argument("--out", type=Path, default=None, help="Write aligned quotes as MT5-style TSV.")
    ap.add_argument("--json", action="store_true", help="JSON report instead of text.")
    ns = ap.parse_args()

    df = read_quotes(ns.file)
    nominal = dominant_tf(df)
    nominal_tf = next(k for k, v in TF_MINUTES.items() if v == nominal)
    segments = detect_segments(df, nominal)
    report = {
        "file": str(ns.file),
        "nominal_tf": nominal_tf,
        "nominal_minutes": nominal,
        "dropped_rows_on_parse": df.attrs.get("dropped_rows", 0),
        "coarse_segments": segments,
        "validation": validate(df),
    }

    target_min = nominal if ns.tf is None else tf_to_minutes(ns.tf)
    target_tf = next(k for k, v in TF_MINUTES.items() if v == target_min)
    coarsest = max([s["inferred_tf_minutes"] for s in segments], default=0)

    if ns.tf is None or target_min == nominal:
        action = "drop-coarse" if segments else "keep-all"
        if segments:
            keep_start = pd.Timestamp(segments[-1]["end"]) + pd.Timedelta(minutes=nominal)
            aligned = df[df["datetime"] >= keep_start].reset_index(drop=True)
        else:
            aligned = df
    elif target_min >= coarsest:
        action = "aggregate-all"
        aligned = aggregate(df, target_min)
    else:
        action = "drop-coarse"
        keep_start = pd.Timestamp(segments[-1]["end"]) + pd.Timedelta(minutes=nominal)
        fine = df[df["datetime"] >= keep_start].reset_index(drop=True)
        aligned = aggregate(fine, target_min)
    report["action"] = action
    report["target_tf"] = target_tf
    report["aligned_rows"] = len(aligned)

    if ns.out is not None:
        out = aligned.copy()
        dt = out.pop("datetime")
        out.insert(0, "DATE", dt.dt.strftime("%Y.%m.%d"))
        out.insert(1, "TIME", dt.dt.strftime("%H:%M:%S"))
        out.columns = [f"<{c.upper()}>" for c in out.columns]
        for col, default in (("<TICKVOL>", 0), ("<VOL>", 0), ("<SPREAD>", 0)):
            if col not in out.columns:
                out[col] = default
            out[col] = out[col].round().astype("int64")
        out.to_csv(ns.out, sep="\t", index=False)
        report["out_file"] = str(ns.out)

    if ns.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"file           : {report['file']}")
        print(f"nominal TF     : {report['nominal_tf']}")
        print(f"dropped on parse: {report['dropped_rows_on_parse']} (duplicate/out-of-order)")
        print(f"validation     : {report['validation']}")
        if segments:
            print(f"WARNING: {len(segments)} coarse segment(s) detected (nominal {nominal_tf}):")
            for s in segments:
                print(f"  {s['start']} .. {s['end_coarse']}  bars={s['bars']}  tf≈{TF_MINUTES_key(s['inferred_tf_minutes'])}")
        else:
            print("no coarse segments detected")
        print(f"action         : {report['action']} -> target {report['target_tf']}, {report['aligned_rows']} rows")
        if ns.out:
            print(f"written        : {report['out_file']}")
    return 0


def TF_MINUTES_key(minutes: int) -> str:
    return next((k for k, v in TF_MINUTES.items() if v == minutes), f"{minutes}min")


if __name__ == "__main__":
    sys.exit(main())
