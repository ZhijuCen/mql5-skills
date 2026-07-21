#!/usr/bin/env python3
"""Parse an MQL5 calendar binary file (MqlCalendarValue[]) to a pandas DataFrame.

The binary format used by the article 22196 "ExportCalendarForTester"
pattern is a raw dump of `MqlCalendarValue[]` written via
`FileWriteArray()` (see
https://www.mql5.com/en/articles/22196 and the
`#resource "\\Files\\...bin" as MqlCalendarValue ...` consumption pattern
in ImportCalendarValidation-EA.mq5).

Each record is **128 bytes** on disk:

    struct MqlCalendarValue {        // 80-byte struct per MQL5 docs
        ulong               id;                  //  8  bytes  @  0
        ulong               event_id;            //  8  bytes  @  8
        datetime            time;                //  8  bytes  @ 16
        datetime            period;              //  8  bytes  @ 24
        int                 revision;            //  4  bytes  @ 32
        long                actual_value;        //  8  bytes  @ 36
        long                prev_value;          //  8  bytes  @ 44
        long                revised_prev_value;  //  8  bytes  @ 52
        long                forecast_value;      //  8  bytes  @ 60
        ENUM_CALENDAR_EVENT_IMPACT  impact_type;  //  4  bytes  @ 68
    };

    // + 56 bytes padding at the tail (FileWriteArray uses 8-byte
    // alignment; the struct of 80 bytes is padded to 128 in the file).

Layout reference:
    skills/mql5/references/docs/01-constants/0186-constants-structures-mqlcalendar.md

Field semantics (per MQL5 docs):
    id                  value ID (unique per release of an event value)
    event_id            event ID (e.g. 840030016 = Nonfarm Payrolls);
                        the first 3 digits encode the ISO 3166-1
                        numeric country code (840 = USA).
    time                event timestamp — Unix seconds, as stored by
                        the MetaTrader server. Display this as UTC or
                        convert in the calling code; this script
                        returns it as a tz-naive pandas Timestamp.
    period              reporting period (start of the period the
                        indicator describes, e.g. 2024-01-01 00:00:00
                        for a January release).
    revision            revision of the published value relative to
                        the reporting period (0 = first release).
    actual_value        actual published value × 10^6, or LONG_MIN
                        (-9223372036854775808) if not set.
    prev_value          previous value × 10^6, or LONG_MIN.
    revised_prev_value  revised previous value × 10^6, or LONG_MIN.
    forecast_value      forecast value × 10^6, or LONG_MIN.
    impact_type         ENUM_CALENDAR_EVENT_IMPACT (0 = NA,
                        1 = positive, 2 = negative — only the actual
                        market reaction is recorded, NOT the event's
                        pre-announced importance).

Usage:
    python parse_mql_calendar_bin.py PATH [--head N] [--tail N]
                                                  [--nfp-id 840030016]

    PATH            path to the .bin file (the script picks the most
                    recent USD_calendar_test_res*.bin from the project's
                    resources/ directory when omitted).
    --head N        print the first N rows of the DataFrame.
    --tail N        print the last N rows.
    --nfp-id ID     event_id of "the main release" (default 840030016
                    = Nonfarm Payrolls). Prints all release timestamps.

The script does NOT shift timestamps — `time` is the broker-server
local timestamp as written by MetaTrader; convert in your own code if
you need UTC or any specific timezone.
"""

from __future__ import annotations

import argparse
import glob
import os
import struct
import sys
from pathlib import Path

import pandas as pd


# ── Layout ──────────────────────────────────────────────────────────────
# `struct.calcsize("<QQqqiqqqqi56x") == 128`. Each record is exactly 128
# bytes on disk (see module docstring for the rationale).
RECORD_SIZE = 128
RECORD_FMT = "<QQqqiqqqqi56x"  # ulong ulong datetime datetime int long×4 enum + 56B tail

# MQL5 encodes missing values as LONG_MIN. Python ints do not overflow,
# so we can compare directly to this constant.
LONG_MIN = -9_223_372_036_854_775_808

# Field names, in struct order. Kept in sync with MqlCalendarValue
# in references/docs/01-constants/0186-constants-structures-mqlcalendar.md
# (note: "id" is renamed to "value_id" to disambiguate from
# CalendarEvent.id; "time" stays as "time" because pandas Timestamp
# is the natural type).
COLUMNS = [
    "value_id",
    "event_id",
    "time",
    "period",
    "revision",
    "actual_value",
    "prev_value",
    "revised_prev_value",
    "forecast_value",
    "impact_type",
]


def read_calendar_bin(path: str | os.PathLike) -> pd.DataFrame:
    """Read `path` as a sequence of MqlCalendarValue records.

    Returns a DataFrame whose columns exactly mirror the C struct
    fields of MqlCalendarValue (see module docstring).
    """
    data = Path(path).read_bytes()
    if len(data) % RECORD_SIZE != 0:
        raise ValueError(
            f"{path}: file size {len(data)} bytes is not a multiple of "
            f"record size {RECORD_SIZE}; the file is not in the "
            f"MqlCalendarValue[] binary format."
        )
    n_records = len(data) // RECORD_SIZE

    rows: list[tuple] = []
    for i in range(n_records):
        chunk = data[i * RECORD_SIZE : (i + 1) * RECORD_SIZE]
        rows.append(struct.unpack(RECORD_FMT, chunk))

    df = pd.DataFrame(rows, columns=COLUMNS)
    # Convert Unix seconds → pandas Timestamps (tz-naive — see docstring).
    df["time"] = pd.to_datetime(df["time"], unit="s", utc=False)
    df["period"] = pd.to_datetime(df["period"], unit="s", utc=False)
    # The four `*value` fields are MQL5 `long` × 10^6 — see module
    # docstring §5. LONG_MIN marks "not set"; everything else is a
    # real value that needs the ×10^-6 un-scale to be human-readable.
    # pandas does not have an int NaN, so the float dtype with NaN is
    # the honest representation of the unset / set dichotomy.
    for col in ("actual_value", "prev_value", "revised_prev_value",
                "forecast_value"):
        df[col] = df[col].where(df[col] != LONG_MIN).astype("float64") / 1e6
    return df


def default_path() -> str | None:
    """Pick the most recent USD_calendar_test_res*.bin under resources/.

    The repository ships outputs at
        resources/artical-22196-MetaQuotes/outputs/USD_calendar_test_res*.bin
    """
    candidates = glob.glob(
        "resources/artical-22196-MetaQuotes/outputs/USD_calendar_test_res*.bin"
    )
    if not candidates:
        return None
    # Sort by mtime so the newest exported file wins.
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Parse an MQL5 calendar binary file (MqlCalendarValue[]) "
            "to a pandas DataFrame and print head/tail + NFP release times."
        )
    )
    p.add_argument(
        "path",
        nargs="?",
        default=None,
        help=(
            "Path to the .bin file. If omitted, picks the most recent "
            "USD_calendar_test_res*.bin under resources/."
        ),
    )
    p.add_argument(
        "--head",
        type=int,
        default=5,
        help="Print the first N rows of the DataFrame (default 5).",
    )
    p.add_argument(
        "--tail",
        type=int,
        default=5,
        help="Print the last N rows of the DataFrame (default 5).",
    )
    p.add_argument(
        "--nfp-id",
        type=int,
        default=840030016,
        help=(
            "event_id of the main NFP release to list timestamps for "
            "(default 840030016 = Nonfarm Payrolls per "
            "resources/calendar-events.csv)."
        ),
    )
    args = p.parse_args(argv)

    path = args.path or default_path()
    if not path:
        print(
            "error: no .bin file specified and none found under "
            "resources/artical-22196-MetaQuotes/outputs/",
            file=sys.stderr,
        )
        return 2
    if not os.path.exists(path):
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    df = read_calendar_bin(path)

    print(f"file:                 {path}")
    print(f"file size:            {os.path.getsize(path)} bytes")
    print(f"record size:          {RECORD_SIZE} bytes (struct + padding)")
    print(f"records:              {len(df)}")
    print(f"time range:           {df['time'].min()}  →  {df['time'].max()}")
    print(f"unique event_id:      {df['event_id'].nunique()}")
    print(f"impact_type counts:   "
          f"NA={int((df['impact_type'] == 0).sum().item())}, "
          f"positive={int((df['impact_type'] == 1).sum().item())}, "
          f"negative={int((df['impact_type'] == 2).sum().item())}")
    n_set = int(df["actual_value"].notna().sum().item())
    print(f"actual_value set:     {n_set} / {len(df)}")
    print()

    # head / tail
    print(f"---- head({args.head}) ----")
    print(df.head(args.head).to_string(index=False))
    print()
    print(f"---- tail({args.tail}) ----")
    print(df.tail(args.tail).to_string(index=False))
    print()

    # NFP release times
    nfp = df.loc[df["event_id"] == args.nfp_id, "time"].sort_values()
    if nfp.empty:
        print(
            f"---- event_id={args.nfp_id} release times ----\n"
            f"(none — event_id={args.nfp_id} not in this file)"
        )
    else:
        print(
            f"---- event_id={args.nfp_id} release times "
            f"({len(nfp)} releases) ----"
        )
        # Print one per line; the script does NOT shift timezones —
        # these are the broker-server local timestamps as written.
        # Trim the long history dump to first 3 + last 12 so the
        # output stays scannable when NFP has 200+ releases.
        N_HEAD = 3
        N_TAIL = 12
        if len(nfp) > N_HEAD + N_TAIL:
            for t in nfp.iloc[:N_HEAD]:
                print(t)
            omitted = len(nfp) - N_HEAD - N_TAIL
            print(f"  ... ({omitted} releases omitted) ...")
            for t in nfp.iloc[-N_TAIL:]:
                print(t)
        else:
            for t in nfp:
                print(t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())