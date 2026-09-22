#!/usr/bin/env python3
"""Numeric parity check: port 0002 (Adaptive Decycler Supertrend).

Reads the BufferDump-EA tester export (CSV, ascending by time,
time,OHLC,b0..b15) and recomputes every value from the Pine semantics,
then compares bar-by-bar against the MQL5 indicator buffers.

Buffer order = the .mq5 BUF_* defines:
 0 trailBull, 1 trailBear, 2 decycler, 3 decColor, 4 upper, 5 lower,
 6 fillU, 7 fillV, 8 longSig, 9 shortSig, 10 trail, 11 efficiency,
 12 cutoff, 13 residual, 14 rms, 15 sq

Usage: uv run python scripts/check_0002_parity.py <parity.csv> [--tol 1e-6]
Exit: 0 all columns pass, 1 divergence found (first bar per column printed)
"""
import argparse
import math
import sys

EMPTY = 2147483647.0

# Pine inputs (defaults of the port AND the original)
SRC = "close"
MIN_CUT, MAX_CUT = 15, 50
EFF_LEN = 10
RMS_LEN = 20
UP_MULT, LO_MULT = 2.0, 2.6
SHOW_DEC, SHOW_ENV, SHOW_FILL, SHOW_SIG = True, False, False, False
MINTICK = None  # derived from first price step if needed; dumped side uses
# SYMBOL_TRADE_TICK_SIZE of XAUUSD = 0.01 (IC Markets-style) -> read from csv? no:
# use 0.01; if the terminal's tick size differs the rms floor column alone may
# diverge, which the report will show explicitly.

TICK = 0.01

COLS = ["trailBull", "trailBear", "decycler", "decColor", "upper", "lower",
        "fillU", "fillV", "longSig", "shortSig", "trail", "efficiency",
        "cutoff", "residual", "rms", "sq"]


def is_empty(v):
    return v == "EMPTY" or (isinstance(v, float) and v >= EMPTY - 0.5)


def load(path):
    rows = []
    with open(path, "rb") as fh:
        head = fh.read(2)
        enc = "utf-16" if head in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    with open(path, encoding=enc) as fh:
        header = fh.readline().strip().split(",")
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 5:
                continue
            rows.append({
                "time": p[0],
                "o": float(p[1]), "h": float(p[2]),
                "l": float(p[3]), "c": float(p[4]),
                "buf": [p[5 + k] if 5 + k < len(p) else "EMPTY"
                        for k in range(len(COLS))],
            })
    return header, rows


def reference(rows):
    """Transcribe the Pine source bar-by-bar, oldest -> newest."""
    n = len(rows)
    out = {c: [None] * n for c in COLS}
    decycler = [None] * n
    trail = [None] * n
    sq = [None] * n
    fast = min(MIN_CUT, MAX_CUT)
    slow = max(MIN_CUT, MAX_CUT)
    for i in range(n):                      # i = chronological index
        src = rows[i]["c"]

        # --- efficiency
        prev = lambda k: (rows[i - k]["c"] if i - k >= 0 else src)
        direction = abs(src - prev(EFF_LEN))
        noise = sum(abs(prev(k) - prev(k + 1)) for k in range(EFF_LEN))
        eff = max(0.0, min(1.0, direction / noise)) if noise > 0 else 0.0
        out["efficiency"][i] = eff

        # --- adaptive cutoff + alpha
        cutoff = slow - eff * (slow - fast)
        out["cutoff"][i] = cutoff
        angle = 2.0 * math.pi / cutoff
        cosv = math.cos(angle)
        alpha = (cosv + math.sin(angle) - 1.0) / cosv if abs(cosv) > 1e-6 else 1.0
        alpha = max(0.0, min(1.0, alpha))

        # --- decycler (seed at the FIRST dumped bar, like the indicator)
        if i == 0:
            decycler[i] = src
        else:
            decycler[i] = alpha * 0.5 * (src + rows[i - 1]["c"]) \
                + (1.0 - alpha) * decycler[i - 1]
        out["decycler"][i] = decycler[i]

        # --- residual RMS envelope
        resid = src - decycler[i]
        out["residual"][i] = resid
        if i - (RMS_LEN - 1) >= 0:
            energy = sum((src2 - decycler[j]) ** 2
                         for j, src2 in
                         ((j, rows[j]["c"]) for j in range(i - RMS_LEN + 1, i + 1)))
            rms = math.sqrt(energy / RMS_LEN)
        else:
            rms = 0.0
        rms = max(rms, TICK)
        out["rms"][i] = rms
        upper = decycler[i] + rms * UP_MULT
        lower = decycler[i] - rms * LO_MULT
        out["upper"][i] = upper
        out["lower"][i] = lower

        # --- SQ / trail (Pine var-state)
        if i == 0:
            prev_sq = 1 if src >= decycler[i] else -1
            prev_trail = lower if prev_sq == 1 else upper
        else:
            prev_sq = sq[i - 1]
            prev_trail = trail[i - 1] if trail[i - 1] is not None else \
                (lower if prev_sq == 1 else upper)
        long_f = prev_sq == -1 and src > prev_trail
        short_f = prev_sq == 1 and src < prev_trail
        cur_sq = 1 if long_f else (-1 if short_f else prev_sq)
        if cur_sq == 1:
            tr = lower if long_f else max(lower, prev_trail)
        else:
            tr = upper if short_f else min(upper, prev_trail)
        sq[i] = cur_sq
        trail[i] = tr
        out["sq"][i] = float(cur_sq)
        out["trail"][i] = tr
        out["trailBull"][i] = tr if cur_sq == 1 else None
        out["trailBear"][i] = tr if cur_sq == -1 else None
        long_sig = i > 0 and cur_sq == 1 and prev_sq != 1
        short_sig = i > 0 and cur_sq == -1 and prev_sq != -1
        out["longSig"][i] = rows[i]["l"] if long_sig else None
        out["shortSig"][i] = rows[i]["h"] if short_sig else None
        out["decColor"][i] = 0.0 if cur_sq == 1 else 1.0
        fill_on = SHOW_FILL and SHOW_ENV
        out["fillU"][i] = upper if fill_on else None
        out["fillV"][i] = lower if fill_on else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--tol", type=float, default=1e-6)
    args = ap.parse_args()

    header, rows = load(args.csv)
    if len(rows) < 100:
        print(f"FAIL only {len(rows)} rows")
        return 1
    print(f"rows={len(rows)}  range {rows[0]['time']} .. {rows[-1]['time']}")
    ref = reference(rows)

    fails = 0
    for k, col in enumerate(COLS):
        first, count, maxdiff = None, 0, 0.0
        for i in range(len(rows)):
            raw = rows[i]["buf"][k]
            mql_na = is_empty(raw)
            rv = ref[col][i]
            ref_na = rv is None
            if mql_na != ref_na:
                count += 1
                if first is None:
                    first = (rows[i]["time"], f"na-mismatch mql_na={mql_na} ref={rv}")
                continue
            if mql_na:
                continue
            d = abs(float(raw) - rv)
            denom = max(1.0, abs(rv))
            maxdiff = max(maxdiff, d / denom)
            if d / denom > args.tol:
                count += 1
                if first is None:
                    first = (rows[i]["time"], f"mql={float(raw):.10g} ref={rv:.10g}")
        if count == 0:
            print(f"PASS  {col:11s} max_rel_diff={maxdiff:.3g}")
        else:
            fails += 1
            print(f"FAIL  {col:11s} divergences={count} first={first} "
                  f"max_rel_diff={maxdiff:.3g}")
    print()
    print("ALL PASS" if fails == 0 else f"{fails} COLUMNS DIVERGE")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
