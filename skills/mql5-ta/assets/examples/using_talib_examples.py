
"""Comprehensive TA-Lib examples for the mql5-ta skill.

Covers the three coverage classes from references/indicator-mappings/:

  1. Same-name counterparts  (iMA/iBands/iRSI/iATR/iStochastic/iSAR/...)
  2. Name traps & adaptors   (iMomentum->ROC, iMACD SMA-signal, iADXWilder)
  3. MQL5-only compositions  (iAO/iAC/iAlligator/iBullsPower/iIchimoku...)

Usage:
  uv run python assets/examples/using_talib_examples.py [-i QUOTES.csv]

Default input: assets/quotes/XAUUSD_M1_202608240100_202608282354.csv
(mixed-timeframe data: try the file under quotes/abnormals/ with --tf H1).
"""

from argparse import ArgumentParser
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import talib

SCRIPTS = Path(__file__).parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from align_quotes import aggregate, read_quotes, validate  # noqa: E402


def load(path: Path, tf: str | None) -> pd.DataFrame:
    df = read_quotes(path)
    print(f"loaded {len(df)} rows from {path.name}")
    report = validate(df)
    if report["ohlc_violations"] or report["duplicate_timestamps"]:
        raise ValueError(f"validation failed: {report}")
    if tf:  # aggregate the whole series to the target timeframe
        minutes = {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240}[tf]
        df = aggregate(df, minutes)
        print(f"aggregated to {tf}: {len(df)} rows")
    return df


def class1_same_name(df: pd.DataFrame) -> pd.DataFrame:
    """iMA / iBands / iRSI / iATR / iStochastic / iWPR / iSAR / iCCI."""
    out = pd.DataFrame(index=df.index)
    high, low, close = df["high"], df["low"], df["close"]

    # iMA(10, MODE_SMA, PRICE_CLOSE)  <->  talib.SMA
    out["MA_SMA10"] = talib.SMA(close, 10)
    # iMA(10, MODE_EMA) <-> talib.EMA;  MODE_LWMA <-> talib.WMA
    out["MA_EMA10"] = talib.EMA(close, 10)
    out["MA_LWMA10"] = talib.WMA(close, 10)
    # MODE_SMMA has no TA-Lib function:
    out["MA_SMMA10"] = close.ewm(alpha=1 / 10, adjust=False).mean()

    # iBands(20, 0, 2.0) <-> BBANDS -> (upper, middle, lower); MQL5 buffers are BASE/UPPER/LOWER
    upper, middle, lower = talib.BBANDS(close, 20, 2, 2)
    out["BB_BASE"], out["BB_UPPER"], out["BB_LOWER"] = middle, upper, lower

    # iRSI(14) / iATR(14) / iCCI(14) / iWPR(14) <-> RSI / ATR / CCI / WILLR
    out["RSI14"] = talib.RSI(close, 14)
    out["ATR14"] = talib.ATR(high, low, close, 14)
    out["CCI14"] = talib.CCI(high, low, close, 14)
    out["WPR14"] = talib.WILLR(high, low, close, 14)

    # iSAR(0.02, 0.2) <-> SAR
    out["SAR"] = talib.SAR(high, low, 0.02, 0.2)

    # iStochastic(5, 3, 3) <-> STOCH (slowk_matype=0 SMA = MQL5 behaviour)
    k, d = talib.STOCH(high, low, close, 5, 3, 0, 3, 0)
    out["STOCH_K"], out["STOCH_D"] = k, d
    return out


def class2_traps(df: pd.DataFrame) -> pd.DataFrame:
    """iMomentum->ROC (not MOM); iMACD SMA-signal; iADX -> iADXWilder."""
    out = pd.DataFrame(index=df.index)
    high, low, close = df["high"], df["low"], df["close"]
    vol = df["tickvol"]  # real volume is 0 for FX/CFD — use tick volume

    # iMomentum(14) = close/close[14]*100 == talib.ROC; talib.MOM is a DIFFERENCE
    out["MOMENTUM14"] = talib.ROC(close, 14)
    out["MOM14_differs"] = talib.MOM(close, 14)  # shown to contrast, NOT equal

    # iMACD(12,26,9): main = EMA12-EMA26 (same); signal = SMA(main, 9) in MQL5,
    # while talib.MACD smooths with EMA. For parity compute manually:
    macd = talib.EMA(close, 12) - talib.EMA(close, 26)
    out["MACD_MAIN"] = macd
    out["MACD_SIG_MQL5"] = talib.SMA(macd, 9)   # MQL5 iMACD SIGNAL_LINE
    out["MACD_SIG_TALIB"] = talib.MACD(close, 12, 26, 9)[1]  # differs!
    # iOsMA == talib macd_hist == main - signal
    out["OSMA"] = macd - out["MACD_SIG_MQL5"]

    # iADX uses non-Wilder smoothing; talib.ADX matches iADXWilder instead
    out["ADX14_WILDER"] = talib.ADX(high, low, close, 14)
    out["PLUSDI14"] = talib.PLUS_DI(high, low, close, 14)
    out["MINUSDI14"] = talib.MINUS_DI(high, low, close, 14)

    # iChaikin is the Chaikin A/D Oscillator <-> ADOSC (NOT Chaikin Volatility)
    out["CHAIKIN_ADOSC"] = talib.ADOSC(high, low, close, vol, 3, 10)
    return out


def class3_compose(df: pd.DataFrame) -> pd.DataFrame:
    """MQL5-only indicators composed from primitives (ascending series)."""
    out = pd.DataFrame(index=df.index)
    high, low, close = df["high"], df["low"], df["close"]
    median = (high + low) / 2

    def smma(s: pd.Series, n: int) -> pd.Series:  # MODE_SMMA / Wilder
        return s.ewm(alpha=1 / n, adjust=False).mean()

    # iAO = SMA(median,5) - SMA(median,34);  iAC = AO - SMA(AO,5)
    ao = median.rolling(5).mean() - median.rolling(34).mean()
    out["AO"], out["AC"] = ao, ao - ao.rolling(5).mean()

    # iAlligator: SMMA(median, 13/8/5) shifted forward 8/5/3
    out["GATOR_JAWS"] = smma(median, 13).shift(-8)
    out["GATOR_TEETH"] = smma(median, 8).shift(-5)
    out["GATOR_LIPS"] = smma(median, 5).shift(-3)

    # iBullsPower / iBearsPower (EMA close, 13)
    ema13 = talib.EMA(close, 13)
    out["BULLS13"] = high - ema13
    out["BEARS13"] = low - ema13

    # iIchimoku(9, 26, 52): Senkou plotted 26 ahead, Chikou 26 back
    def hl_range(n: int) -> pd.Series:
        return (high.rolling(n).max() + low.rolling(n).min()) / 2

    tenkan, kijun = hl_range(9), hl_range(26)
    out["ICHIMOKU_TENKAN"] = tenkan
    out["ICHIMOKU_KIJUN"] = kijun
    out["ICHIMOKU_SENKOU_A"] = ((tenkan + kijun) / 2).shift(-26)
    out["ICHIMOKU_SENKOU_B"] = hl_range(52).shift(-26)
    out["ICHIMOKU_CHIKOU"] = close.shift(26)

    # iFractals: 5-bar pattern; EMPTY_VALUE -> NaN
    up = high == high.rolling(5, center=True).max()
    dn = low == low.rolling(5, center=True).min()
    out["FRACTAL_UP"] = high.where(up)
    out["FRACTAL_DOWN"] = low.where(dn)

    # iDeMarker(14), SMMA smoothing
    prev_high, prev_low = high.shift(1), low.shift(1)
    demax, demin = (high - prev_high).clip(lower=0), (prev_low - low).clip(lower=0)
    smax, smin = smma(demax, 14), smma(demin, 14)
    out["DEMARKER14"] = smax / (smax + smin)
    return out


def class4_talib_only(df: pd.DataFrame) -> pd.DataFrame:
    """TA-Lib functions with no MQL5 native handle."""
    out = pd.DataFrame(index=df.index)
    o, h, l, c = (df[k] for k in ("open", "high", "low", "close"))
    out["CDL_ENGULFING"] = talib.CDLENGULFING(o, h, l, c)  # +100/-100/0
    out["CDL_DOJI"] = talib.CDLDOJI(o, h, l, c)
    out["HT_TRENDMODE"] = talib.HT_TRENDMODE(c)  # needs ~63 bars warm-up
    out["LINREG_SLOPE14"] = talib.LINEARREG_SLOPE(c, 14)
    out["MEDPRICE"] = talib.MEDPRICE(h, l)
    return out


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path,
                        default=Path(__file__).parents[1] / "quotes/XAUUSD_M1_202608240100_202608282354.csv")
    parser.add_argument("--tf", default=None, help="aggregate to M1/M5/M15/H1/H4")
    ns = parser.parse_args()

    df = load(ns.input, ns.tf)
    frames = {
        "1 same-name  ": class1_same_name(df),
        "2 traps      ": class2_traps(df),
        "3 compose    ": class3_compose(df),
        "4 talib-only ": class4_talib_only(df),
    }
    for name, out in frames.items():
        first_valid = max(out.notna().idxmax())  # last indicator's lookback head
        print(f"\n=== class {name} ({len(out.columns)} cols, "
              f"NaN head ends at row {first_valid}) ===")
        print(out.dropna(how="all").tail(3).to_string())


if __name__ == "__main__":
    main()
