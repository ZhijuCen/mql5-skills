#!/usr/bin/env python3
"""
Verify SL/TP calculation formulas from MQL5 documentation.

Two symbol types:
  - XAUUSD: CFD Leverage mode  → Profit = (close-open) * ContractSize * Lots
  - USDJPY: Forex mode          → Profit = (close-open) * ContractSize * Lots
    (but profit currency = JPY, so dollar-equivalent needs conversion)

Bid prices used:  XAUUSD=4121.28,  USDJPY=161.561

Target CLI layout:
  verify_sl_tp_formulas.py [--help] verify [SYMBOL ...] [-o OUTPUT_FILE]

Where [SYMBOL ...] is one or more symbol names (default: XAUUSD USDJPY).
Use -o OUTPUT_FILE to write the report to a file instead of stdout.
"""

from __future__ import annotations
import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

# ── Spec loader ──────────────────────────────────────────────────────

SPEC_DIR = Path(__file__).resolve().parent.parent / "references" / "symbol-spec"


@dataclass
class SymbolSpec:
    name: str
    digits: int
    contract_size: float
    calc_mode: str
    tick_size: float
    tick_value: float
    stops_level: int
    profit_currency: str
    lot_min: float
    lot_max: float
    lot_step: float

    @property
    def point(self) -> float:
        """SYMBOL_POINT = 10^(-digits)"""
        return 10 ** (-self.digits)

    @classmethod
    def from_csv(cls, path: Path) -> "SymbolSpec":
        rows: dict[str, str] = {}
        with open(path, newline="") as f:
            for row in csv.reader(f):
                if len(row) >= 2:
                    rows[row[0].strip()] = row[1].strip()
        return cls(
            name=path.stem.replace("specs-", ""),
            digits=int(rows["Digits"]),
            contract_size=float(rows["Contract size"]),
            calc_mode=rows["Calculation"],
            tick_size=float(rows["Tick size"]),
            tick_value=float(rows["Tick value"]),
            stops_level=int(rows["Stops level"]),
            profit_currency=rows["Profit currency"],
            lot_min=float(rows["Minimal volume"]),
            lot_max=float(rows["Maximal volume"]),
            lot_step=float(rows["Volume step"]),
        )


# ── Core formulas ────────────────────────────────────────────────────
#
# Key distinction:
#   PointValue  = value of 1 POINT move for 1 lot  (in profit currency)
#   loss = number_of_points * PointValue * Lots
#
# Therefore:
#   number_of_points = loss / (PointValue * Lots)
#   sl_distance_price = number_of_points * point
#
# When profit_currency != account_currency, we must convert:
#   max_loss_profcy = balance * risk_pct / 100 * fx_rate_to_profcy
#

def point_value(spec: SymbolSpec) -> float:
    """
    MPM::PointValue: value of 1 POINT move for 1 lot, in profit currency.

    Forex/CFD:   point * ContractSize     (since Profit = delta * ContractSize * Lots)
    Futures:     point * TickValue / TickSize
    """
    mode = spec.calc_mode.lower()
    if "forex" in mode or "cfd" in mode or "stock" in mode:
        return spec.point * spec.contract_size
    elif "future" in mode:
        return spec.point * spec.tick_value / spec.tick_size
    raise ValueError(f"Unsupported calc mode: {spec.calc_mode}")


def risk_amount(
    balance_usd: float,
    risk_pct: float,
    spec: SymbolSpec,
    fx_rate: float,
) -> float:
    """
    Convert risk from account currency (USD) to profit currency.

    fx_rate: how many units of profit_currency per 1 USD
             e.g. USDJPY=161.561 → fx_rate=161.561
                  XAUUSD (USD=USD) → fx_rate=1.0
    """
    return balance_usd * risk_pct / 100.0 * fx_rate


def calc_sl_from_risk(
    spec: SymbolSpec,
    max_loss_profcy: float,   # risk budget in profit currency
    lots: float,
    open_price: float,
    direction: str,  # "BUY" or "SELL"
) -> float:
    """
    Given risk budget (in profit currency) and lot size, compute SL price.

    points     = max_loss / (PointValue * Lots)     (number of points)
    sl_price   = open_price ± points * point

    BUY:  SL = open - points * point
    SELL: SL = open + points * point
    """
    pv = point_value(spec)
    points = max_loss_profcy / (pv * lots)
    sl_distance_price = points * spec.point

    if direction == "BUY":
        sl = open_price - sl_distance_price
    else:
        sl = open_price + sl_distance_price
    return round(sl, spec.digits)


def calc_lots_from_sl(
    spec: SymbolSpec,
    max_loss_profcy: float,   # risk budget in profit currency
    open_price: float,
    sl_price: float,
) -> float:
    """
    Given a fixed SL price, compute lot size so that loss == max_loss_profcy.

    sl_distance_price = abs(open - sl)
    points     = sl_distance_price / point
    Lots       = max_loss / (PointValue * points)

    Then normalize to lot_step, clamp to [lot_min, lot_max].
    """
    sl_distance_price = abs(open_price - sl_price)
    if sl_distance_price == 0:
        return 0.0
    pv = point_value(spec)
    points = sl_distance_price / spec.point
    raw_lots = max_loss_profcy / (pv * points)

    # Normalize to lot_step
    normed = int(raw_lots / spec.lot_step) * spec.lot_step
    normed = max(normed, spec.lot_min)
    normed = min(normed, spec.lot_max)
    return round(normed, 8)


def calc_profit(
    spec: SymbolSpec, lots: float, open_price: float, close_price: float
) -> float:
    """
    Profit in profit currency (from OrderCalcProfit formulas).
    """
    mode = spec.calc_mode.lower()
    if "forex" in mode or "cfd" in mode or "stock" in mode:
        return (close_price - open_price) * spec.contract_size * lots
    elif "future" in mode:
        return (close_price - open_price) * spec.tick_value / spec.tick_size * lots
    raise ValueError(f"Unsupported: {spec.calc_mode}")


# ── Display helpers ──────────────────────────────────────────────────

SEP = "─" * 72
PCY = " "  # profit currency suffix


def fmt(v: float, d: int) -> str:
    return f"{v:,.{d}f}"


def run_tests(
    spec: SymbolSpec, bid: float, account_balance: float, fx_rate: float
):
    pc = spec.profit_currency  # e.g. "JPY" or "USD"

    print(f"\n{SEP}")
    print(f"  Symbol: {spec.name}  |  Calc Mode: {spec.calc_mode}")
    print(f"  Digits={spec.digits}  ContractSize={spec.contract_size}")
    print(f"  Point={spec.point}  TickSize={spec.tick_size}  TickValue={spec.tick_value}")
    print(f"  Profit currency: {pc}  |  FX rate: {fx_rate} {pc}/USD")
    print(SEP)

    pv = point_value(spec)
    print(f"  PointValue = {pv}  ({pc} per 1-point move, 1 lot)")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 1: SL → Profit round-trip (verify formula correctness)
    # ─────────────────────────────────────────────────────────────────
    print("  TEST 1: SL→Profit round-trip (fixed lots=0.10)")
    lots = 0.10

    for sl_distance_pts in [100, 500, 1000, 2000]:
        sl_dist_price = sl_distance_pts * spec.point
        sl_buy = round(bid - sl_dist_price, spec.digits)
        loss_buy = calc_profit(spec, lots, bid, sl_buy)

        print(f"    SL dist={sl_distance_pts:>5} pts  "
              f"-> price dist={sl_dist_price}  "
              f"BUY SL={fmt(sl_buy, spec.digits)}  "
              f"loss={fmt(loss_buy, spec.digits)} {pc}")

    # Also verify with Ask = Bid + spread
    spread_pts = 12 if spec.name == "XAUUSD" else 3
    ask = round(bid + spread_pts * spec.point, spec.digits)
    print(f"    (Ask={fmt(ask, spec.digits)}, spread={spread_pts} pts)")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 2: Risk% → SL price (forward direction)
    # ─────────────────────────────────────────────────────────────────
    print(f"  TEST 2: Risk%→SL  (Balance={fmt(account_balance, 2)} USD, Lots=0.10)")
    for risk_pct in [0.5, 1.0, 2.0, 5.0]:
        ml = risk_amount(account_balance, risk_pct, spec, fx_rate)
        for direction in ["BUY", "SELL"]:
            price = bid if direction == "BUY" else ask
            sl = calc_sl_from_risk(spec, ml, lots, price, direction)

            # Verify: compute actual loss at this SL
            actual_loss = calc_profit(spec, lots, price, sl)

            print(f"    Risk={risk_pct}% {direction:4s}  "
                  f"SL={fmt(sl, spec.digits)}  "
                  f"target loss={fmt(ml, 2)} {pc}  "
                  f"actual loss={fmt(actual_loss, 2)} {pc}  "
                  f"diff={fmt(abs(actual_loss) - ml, 6)}")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 3: Fixed SL price → Lot size (reverse direction)
    # ─────────────────────────────────────────────────────────────────
    risk_pct = 1.0
    ml = risk_amount(account_balance, risk_pct, spec, fx_rate)
    print(f"  TEST 3: Fixed SL→Lots  (Balance={fmt(account_balance, 2)} USD, Risk={risk_pct}%)")
    print(f"          risk budget = {fmt(ml, 2)} {pc}")
    for sl_distance_pts in [100, 500, 1000, 2000]:
        sl_dist_price = sl_distance_pts * spec.point
        sl_buy = round(bid - sl_dist_price, spec.digits)
        lots_calc = calc_lots_from_sl(spec, ml, bid, sl_buy)

        if lots_calc > 0:
            actual_loss = calc_profit(spec, lots_calc, bid, sl_buy)
        else:
            actual_loss = 0.0

        print(f"    SL dist={sl_distance_pts:>5} pts  "
              f"SL={fmt(sl_buy, spec.digits)}  "
              f"lots calc={lots_calc:.4f}  "
              f"actual loss={fmt(actual_loss, 2)} {pc}  "
              f"diff={fmt(abs(actual_loss) - ml, 6)}")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 4: Cross-verify — forward vs reverse should match
    # ─────────────────────────────────────────────────────────────────
    print("  TEST 4: Cross-verify forward↔reverse")
    test_cases = [
        (0.5, 500),
        (1.0, 1000),
        (2.0, 1500),
    ]
    for risk_pct, sl_pts in test_cases:
        ml = risk_amount(account_balance, risk_pct, spec, fx_rate)
        sl_dist_price = sl_pts * spec.point
        sl_buy = round(bid - sl_dist_price, spec.digits)

        # Forward: risk% → SL (with lots=0.10)
        lots_fwd = 0.10
        sl_fwd = calc_sl_from_risk(spec, ml, lots_fwd, bid, "BUY")

        # Reverse: SL → lots
        lots_rev = calc_lots_from_sl(spec, ml, bid, sl_buy)

        # Forward loss check
        loss_fwd = calc_profit(spec, lots_fwd, bid, sl_fwd)

        # Reverse loss check
        loss_rev = calc_profit(spec, lots_rev, bid, sl_buy)

        print(f"    Risk={risk_pct}% SL dist={sl_pts}pts  budget={fmt(ml, 2)} {pc}")
        print(f"      Forward:  SL={fmt(sl_fwd, spec.digits)}  lots={lots_fwd:.2f}  "
              f"loss={fmt(loss_fwd, 2)} {pc} (budget={fmt(ml, 2)})")
        print(f"      Reverse:  lots={lots_rev:.4f}  "
              f"loss={fmt(loss_rev, 2)} {pc} (budget={fmt(ml, 2)})")
        print(f"      Δloss = {fmt(abs(loss_fwd) - ml, 6)}  "
              f"(forward vs budget)")
    print()


# ── Main ─────────────────────────────────────────────────────────────

# Default bid prices used in the verification (chosen to be representative;
# the formulas don't depend on the bid value but the report does).
_DEFAULT_BIDS = {"XAUUSD": 4121.28, "USDJPY": 161.561}

_VALID_SUBCOMMANDS = {"verify"}


def _validate_argv_position(argv: list[str], prog: str = "") -> None:
    """Reject any argv layout where the sub-command is NOT the first token.

    Target layout — mandatory:
        {prog} [--help] SUB_COMMAND [SYMBOL ...] [-o OUTPUT_FILE]

    Mirrors the validator in parse_optimizer_report.py / parse_tester_report.py
    so the project's scripts all share the same CLI rules.
    """
    if argv in ([], ["--help"], ["-h"]):
        return
    if argv and argv[0] in ("--help", "-h"):
        return
    if not argv or argv[0].startswith("-"):
        print(
            f"Error: {prog} requires a sub-command as the first argument.\n"
            f"  Expected layout:  {prog} SUB_COMMAND [SYMBOL ...] [-o OUTPUT_FILE]\n"
            f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
            file=sys.stderr,
        )
        sys.exit(2)
    sub = argv[0]
    if sub not in _VALID_SUBCOMMANDS:
        if sub.startswith("-"):
            print(
                f"Error: flags must come AFTER the sub-command.\n"
                f"  Expected layout:  {prog} SUB_COMMAND [SYMBOL ...] [-o OUTPUT_FILE]\n"
                f"  Got: {' '.join(argv)}\n"
                f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
                file=sys.stderr,
            )
            sys.exit(2)
        print(
            f"Error: unknown sub-command '{sub}'.\n"
            f"  Expected layout:  {prog} SUB_COMMAND [SYMBOL ...] [-o OUTPUT_FILE]\n"
            f"  Valid sub-commands: {', '.join(sorted(_VALID_SUBCOMMANDS))}",
            file=sys.stderr,
        )
        sys.exit(2)


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


def main(argv: list[str] | None = None) -> None:
    prog = Path(sys.argv[0]).name
    _validate_argv_position(sys.argv[1:], prog=prog)
    parser = argparse.ArgumentParser(
        description="Verify SL/TP calculation formulas from MQL5 documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Target CLI layout:
  %(prog)s [--help] verify [SYMBOL ...] [-o OUTPUT_FILE]

Examples:
  # Default: run all bundled symbols (XAUUSD, USDJPY), print to stdout
  %(prog)s verify

  # Run a single symbol, write output to a file
  %(prog)s verify XAUUSD -o verify_xauusd.txt

  # Run both bundled symbols, write output to a file
  %(prog)s verify XAUUSD USDJPY -o verify_all.txt

Available bundled symbols: XAUUSD, USDJPY.
Bids are taken from a hardcoded reference set (XAUUSD=4121.28, USDJPY=161.561).
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="SUB_COMMAND", required=True)

    p_verify = sub.add_parser(
        "verify",
        help="Run the SL/TP formula verification tests for one or more symbols.",
        description="Run the bundled SL/TP formula verification suite for one "
                    "or more symbol names (default: XAUUSD USDJPY). Each symbol "
                    "is loaded from references/symbol-spec/<NAME>.csv and "
                    "exercised through four tests: SL→Profit round-trip, "
                    "Risk%%→SL forward direction, fixed-SL→Lots reverse, and "
                    "forward↔reverse cross-verification. Plus a bonus "
                    "USDJPY-currency walkthrough and a XAUUSD lots-sensitivity "
                    "sweep.",
    )
    p_verify.add_argument(
        "symbols", nargs="*", default=["XAUUSD", "USDJPY"],
        metavar="SYMBOL",
        help="One or more symbol names from references/symbol-spec/. "
             "Default (when omitted): XAUUSD USDJPY.",
    )
    p_verify.add_argument(
        "-o", "--output", dest="output", default=None, metavar="OUTPUT_FILE",
        help="Write the verification report to OUTPUT_FILE "
             "(default: stdout).",
    )

    args = parser.parse_args(argv)

    if args.cmd != "verify":
        parser.error(f"unknown sub-command: {args.cmd}")

    BALANCE = 10000.0  # USD demo account

    specs: dict[str, SymbolSpec] = {}
    bids: dict[str, float] = {}
    for name in args.symbols:
        csv_path = SPEC_DIR / f"specs-{name}.csv"
        if not csv_path.exists():
            print(
                f"Error: no symbol-spec CSV for '{name}' "
                f"(expected at {csv_path})",
                file=sys.stderr,
            )
            sys.exit(1)
        specs[name] = SymbolSpec.from_csv(csv_path)
        if name in _DEFAULT_BIDS:
            bids[name] = _DEFAULT_BIDS[name]
        else:
            # Fallback bid of 0.0; the SL→Profit round-trip still works
            # but Risk%→SL walkthroughs need a positive bid. Warn.
            bids[name] = 0.0
            print(
                f"Warning: '{name}' has no bundled bid price; using 0.0. "
                f"Risk%→SL walkthroughs may yield non-meaningful numbers.",
                file=sys.stderr,
            )

    # FX rates: profit_currency per 1 USD
    # XAUUSD: profit=USD → rate=1.0
    # USDJPY: profit=JPY → rate=USDJPY_bid
    fx_rates: dict[str, float] = {}
    for name in args.symbols:
        spec = specs[name]
        if spec.profit_currency.upper() == "USD":
            fx_rates[name] = 1.0
        else:
            # profit_currency per 1 USD = bid (for FX; good enough for the demo)
            fx_rates[name] = bids[name]

    def render_report() -> str:
        """Run the full verification report; return it as a string."""
        import io
        buf = io.StringIO()
        saved = sys.stdout
        sys.stdout = buf
        try:
            print("=" * 72)
            print("  MQL5 SL/TP Formula Verification")
            print(f"  Account Balance: {BALANCE:,.2f} USD")
            print("=" * 72)

            for name in args.symbols:
                run_tests(specs[name], bids[name], BALANCE, fx_rates[name])

            if "USDJPY" in specs:
                # Special: USDJPY — currency conversion walkthrough
                print(SEP)
                print("  USDJPY: Currency Conversion Walkthrough")
                print(SEP)
                jpy_spec = specs["USDJPY"]
                jpy_rate = bids["USDJPY"]
                _lots, _risk_pct = 0.10, 1.0

                target_usd = BALANCE * _risk_pct / 100.0           # = 100.00 USD
                target_jpy = target_usd * jpy_rate                 # = 16,156.10 JPY

                ml_jpy = risk_amount(BALANCE, _risk_pct, jpy_spec, jpy_rate)
                sl_fwd = calc_sl_from_risk(jpy_spec, ml_jpy, _lots, bids["USDJPY"], "BUY")

                loss_jpy = calc_profit(jpy_spec, _lots, bids["USDJPY"], sl_fwd)
                loss_usd = loss_jpy / jpy_rate

                print(f"  Risk={_risk_pct}%, Lots={_lots}, Balance={fmt(BALANCE, 2)} USD")
                print()
                print(f"  Step 1: risk budget (USD)  = {fmt(BALANCE, 2)} × {_risk_pct}% = {fmt(target_usd, 2)} USD")
                print(f"  Step 2: convert to JPY     = {fmt(target_usd, 2)} × {jpy_rate} = {fmt(target_jpy, 2)} JPY")
                print(f"  Step 3: points = budget / (PointValue × Lots)")
                print(f"          = {fmt(target_jpy, 2)} / ({point_value(jpy_spec):.1f} × {_lots}) = {target_jpy / (point_value(jpy_spec) * _lots):.1f} pts")
                print(f"          SL dist = {target_jpy / (point_value(jpy_spec) * _lots):.1f} x {jpy_spec.point} = "
                      f"{target_jpy / (point_value(jpy_spec) * _lots) * jpy_spec.point:.4f} price")
                print(f"          SL = {bids['USDJPY']} - {target_jpy / (point_value(jpy_spec) * _lots) * jpy_spec.point:.4f} = "
                      f"{fmt(sl_fwd, jpy_spec.digits)}")
                print()
                print(f"  Step 4: actual loss = {fmt(loss_jpy, 2)} JPY")
                print(f"  Step 5: loss in USD = {fmt(loss_jpy, 2)} / {jpy_rate} = {fmt(loss_usd, 2)} USD")
                print()
                print(f"  Result: target {fmt(target_usd, 2)} USD ≈ actual {fmt(loss_usd, 2)} USD  "
                      f"(diff={fmt(abs(loss_usd) - target_usd, 4)} USD, "
                      f"from NormalizeDouble rounding)")
                print()

            if "XAUUSD" in specs:
                # Special: XAUUSD lots sensitivity for 1% risk
                print(SEP)
                print("  XAUUSD: Lots vs SL distance for 1% risk ($100 target loss)")
                print(SEP)
                xau = specs["XAUUSD"]
                ml_usd = risk_amount(BALANCE, 1.0, xau, 1.0)
                for lots in [0.01, 0.05, 0.10, 0.50, 1.00, 2.00]:
                    pv = point_value(xau)
                    points = ml_usd / (pv * lots)
                    sl_dist_price = points * xau.point
                    sl_dist_pts = int(points)
                    sl = round(bids["XAUUSD"] - sl_dist_price, xau.digits)

                    actual_loss = calc_profit(xau, lots, bids["XAUUSD"], sl)

                    print(f"    Lots={lots:>5.2f}  "
                          f"SL dist={sl_dist_pts:>6} pts ({sl_dist_price:.2f} price)  "
                          f"SL={fmt(sl, xau.digits)}  "
                          f"loss={fmt(actual_loss, 2)} USD  "
                          f"diff={fmt(abs(actual_loss) - ml_usd, 6)}")
        finally:
            sys.stdout = saved
        return buf.getvalue()

    text = render_report()
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
