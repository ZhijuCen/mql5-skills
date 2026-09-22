//+------------------------------------------------------------------+
//|                                            AuroraKamaTrend-EA.mq5  |
//|  MQL5 port of the Pine strategy "Aurora KAMA Trend"                |
//|  (TradingView: "Aurora KAMA | KAMA Adaptive Trend Strategy")       |
//|  by blitz_locked                                                   |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 aurora-kama.pine (179 lines, v6)                    |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0006-aurora-kama.md                                 |
//|  Author tips: DAILY bars on liquid trending instruments            |
//|  (BTCUSD, ES1!, SPY, QQQ)                                          |
//|  (assets/mql5-side/0006-aurora-kama.ini uses BTCUSD D1)             |
//|                                                                    |
//|  License: the Pine source carries NO license declaration           |
//|  (TV open-source access); credited to blitz_locked, ported for     |
//|  personal research use - see PROVENANCE.md.                        |
//|                                                                    |
//|  Execution model: signal on the confirmed bar -> market order on   |
//|  the next bar's first tick; fixed % stop anchored to the fill      |
//|  price; delayed trailing stop re-evaluated on each closed bar      |
//|  (Pine calc_on_order_fills = false). Deviations D1-D6: port record.|
//+------------------------------------------------------------------+
#property link      "https://www.tradingview.com/script/kbYTJ8V2-Aurora-KAMA-KAMA-Adaptive-Trend-Strategy/"
#property version   "1.00"
#property description "Aurora KAMA Trend - MQL5 EA port"
#property strict

#include "strategy-common.mqh"

//+------------------------------------------------------------------+
//| Enums                                                              |
//+------------------------------------------------------------------+
enum ENUM_DIR_MODE
  {
   DIR_LONG  = 0,   // Long
   DIR_SHORT = 1,   // Short
   DIR_BOTH  = 2    // Long and Short
  };

enum ENUM_KAMA_SRC
  {
   SRC_CLOSE = 0,   // close
   SRC_HL2   = 1,   // hl2
   SRC_HLC3  = 2    // hlc3
  };

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs (same defaults, same groups)       |
//+------------------------------------------------------------------+
input group "KAMA Settings"
input ENUM_KAMA_SRC InpSrc         = SRC_CLOSE;   // Source
input int            InpKamaLen     = 10;          // Efficiency Ratio Length
input int            InpKamaFast    = 2;           // Fast EMA Length
input int            InpKamaSlow    = 30;          // Slow EMA Length

input group "Trend Confirmation"
input int            InpRisingLen   = 3;           // KAMA Rising Persistence (bars)
input int            InpFallingLen  = 3;           // KAMA Falling Persistence (bars)
input bool           InpUseSma      = true;        // Use Long-Term Trend Filter
input int            InpSmaLen      = 200;         // Trend Filter SMA Length

input group "Trade Management"
input ENUM_DIR_MODE  InpDirection   = DIR_BOTH;    // Trade Direction
input int            InpBarsBetween = 5;           // Minimum Bars Between Entries

input group "Risk Management"
input bool           InpUseStop     = true;        // Use Fixed Stop Loss %
input double         InpStopPct     = 4.0;         // Stop Loss %
input bool           InpUseTrail    = true;        // Use Delayed Trailing Stop
input double         InpTrailPct    = 6.0;         // Trailing Stop %
input int            InpTrailDelay  = 5;           // Delay Trailing by N Bars

input group "Trading"
input double         InpQtyPct      = 25.0;        // Entry size (% of equity, Pine default)
input long           InpMagic       = 40006;       // Magic number
input int            InpHistoryBars = 50000;       // History bars for warm-up

//+------------------------------------------------------------------+
//| Per-bar state                                                      |
//+------------------------------------------------------------------+
struct S6Vals
  {
   double kama;
   double sma;
  };

CPineSeries g_series;
S6Vals      g_val[];
int         g_barSeq       = 0;
int         g_lastTradeBar = INT_MIN;   // Pine var na -> sentinel (na = never traded)
datetime    g_fillTime     = 0;
datetime    g_fillBarTime  = 0;         // open time of the fill bar (delay reference)
bool        g_hadPos       = false;
bool        g_wasLong      = false;
bool        g_inited       = false;

//+------------------------------------------------------------------+
color Rgb(const uint rrggbb)
  {
   uint r = (rrggbb >> 16) & 0xFF;
   uint g = (rrggbb >> 8) & 0xFF;
   uint b = (rrggbb) & 0xFF;
   return((color)((b << 16) | (g << 8) | r));
  }

//+------------------------------------------------------------------+
double SrcAt(const PineBar &b)
  {
   if(InpSrc == SRC_HL2)
      return((b.h + b.l) / 2.0);
   if(InpSrc == SRC_HLC3)
      return((b.h + b.l + b.c) / 3.0);
   return(b.c);
  }

//+------------------------------------------------------------------+
//| Kaufman's Adaptive Moving Average (Pine kama())                    |
//| - first bar seeds with the source (Pine: na(result[1]) -> source)  |
//| - before the ER window fills, Pine's volatility is na -> the       |
//|   ternary falls back to er = 0 -> sc = slowSC^2 (tiny creep)       |
//+------------------------------------------------------------------+
void ComputeBar()
  {
   int n = g_series.Count();
   if(n < 1)
      return;
   PineBar b = g_series.Get(0);
   double src = SrcAt(b);

   double change = EMPTY_VALUE;
   double vol    = EMPTY_VALUE;
   if(n > InpKamaLen)
     {
      change = MathAbs(src - SrcAt(g_series.Get(InpKamaLen)));
      double sum = 0.0;
      for(int k = 0; k < InpKamaLen; k++)
         sum += MathAbs(SrcAt(g_series.Get(k)) - SrcAt(g_series.Get(k + 1)));
      vol = sum;
     }
   double er = 0.0;
   if(!IsNa(vol) && vol != 0.0 && !IsNa(change))
      er = change / vol;
   double fastSC = 2.0 / (InpKamaFast + 1);
   double slowSC = 2.0 / (InpKamaSlow + 1);
   double sc = MathPow(er * (fastSC - slowSC) + slowSC, 2.0);

   double kama;
   if(n == 1)
      kama = src;                                  // Pine seed
   else
      kama = g_val[n - 2].kama + sc * (src - g_val[n - 2].kama);

   //--- long-term SMA filter (Pine ta.sma: na until the window fills)
   double sma = EMPTY_VALUE;
   if(n >= InpSmaLen)
     {
      double sum = 0.0;
      for(int k = 0; k < InpSmaLen; k++)
         sum += g_series.Get(k).c;
      sma = sum / InpSmaLen;
     }

   ArrayResize(g_val, n);
   g_val[n - 1].kama = kama;
   g_val[n - 1].sma  = sma;
  }

//+------------------------------------------------------------------+
//| ta.rising / ta.falling: `len` consecutive strict comparisons       |
//| (all `len + 1` values must be strictly monotonic)                  |
//+------------------------------------------------------------------+
bool KamaRising(const int len)
  {
   if(g_series.Count() < len + 1)
      return(false);
   for(int k = 0; k < len; k++)
     {
      if(g_val[g_series.Count() - 1 - k].kama <= g_val[g_series.Count() - 2 - k].kama)
         return(false);
     }
   return(true);
  }

bool KamaFalling(const int len)
  {
   if(g_series.Count() < len + 1)
      return(false);
   for(int k = 0; k < len; k++)
     {
      if(g_val[g_series.Count() - 1 - k].kama >= g_val[g_series.Count() - 2 - k].kama)
         return(false);
     }
   return(true);
  }

//+------------------------------------------------------------------+
//| Delayed trailing stop (params are % of the FILL price = avg)       |
//+------------------------------------------------------------------+
void ManageTrailing()
  {
   bool isBuy;
   if(!InpUseTrail || !HaveOursByMagic(InpMagic, isBuy))
      return;
   if(g_fillTime == 0 || g_fillBarTime == 0)
      return;
   //--- delay gate: bars since the fill bar closed (Pine entry_bar_index)
   int barsClosedSinceFill = 0;
   int n = g_series.Count();
   for(int i = n - 1; i >= 0; i--)
     {
      if(g_series.At(i).time < g_fillBarTime)
         break;
      barsClosedSinceFill++;
     }
   //--- the fill bar itself counts as bar 0 once it has closed; while it
   //--- is still forming the count is -1 (not yet armed regardless)
   if(barsClosedSinceFill - 1 < InpTrailDelay)
      return;
   double fill = PositionGetDouble(POSITION_PRICE_OPEN);
   double trailDist = fill * InpTrailPct / 100.0;
   double ext = isBuy ? -DBL_MAX : DBL_MAX;
   bool any = false;
   for(int i = n - 1; i >= 0; i--)
     {
      PineBar b = g_series.At(i);
      if(b.time < g_fillTime)
         break;
      any = true;
      if(isBuy) { if(b.h > ext) ext = b.h; }
      else      { if(b.l < ext) ext = b.l; }
     }
   if(!any)
      return;
   bool armed = isBuy ? (ext >= fill + trailDist) : (ext <= fill - trailDist);
   if(!armed)
      return;
   double newStop = isBuy ? ext - trailDist : ext + trailDist;
   double curSL = PositionGetDouble(POSITION_SL);
   double curTP = PositionGetDouble(POSITION_TP);
   bool better = isBuy ? (curSL <= 0.0 || newStop > curSL + _Point)
                       : (curSL <= 0.0 || newStop < curSL - _Point);
   if(!better)
      return;
   CTrade trade;
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetTypeFillingBySymbol(_Symbol);
   if(!trade.PositionModify(_Symbol,
                            NormalizeDouble(newStop, (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)),
                            curTP))
      PrintFormat("Aurora-KAMA: trail modify failed retcode=%d", trade.ResultRetcode());
  }

//+------------------------------------------------------------------+
//| Apply the exact fixed-% stop from the FILL price (Pine uses        |
//| position_avg_price * stopPct/100 - recomputed after the fill)      |
//+------------------------------------------------------------------+
void ApplyFixedStop()
  {
   if(!InpUseStop)
      return;
   bool isBuy;
   if(!HaveOursByMagic(InpMagic, isBuy))
      return;
   double fill = PositionGetDouble(POSITION_PRICE_OPEN);
   double dist = fill * InpStopPct / 100.0;
   double sl = isBuy ? fill - dist : fill + dist;
   double tp = PositionGetDouble(POSITION_TP);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double stopPts = (double)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL) * _Point;
   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   if(stopPts > 0.0)
     {
      if(isBuy && sl > bid - stopPts)
         sl = NormalizeDouble(bid - stopPts - _Point, digits);
      if(!isBuy && sl < ask + stopPts)
         sl = NormalizeDouble(ask + stopPts + _Point, digits);
     }
   double curSL = PositionGetDouble(POSITION_SL);
   if(MathAbs(curSL - sl) < _Point)
      return;
   CTrade trade;
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetTypeFillingBySymbol(_Symbol);
   if(!trade.PositionModify(_Symbol, NormalizeDouble(sl, digits), tp))
      PrintFormat("Aurora-KAMA: stop modify failed retcode=%d", trade.ResultRetcode());
  }

//+------------------------------------------------------------------+
//| One confirmed-bar evaluation                                       |
//+------------------------------------------------------------------+
void OnClosedBar()
  {
   int n = g_series.Count();
   if(n < 2)
      return;
   int seq = n - 1;
   g_barSeq = seq;
   PineBar b0 = g_series.Get(0);
   S6Vals  v  = g_val[n - 1];

   //--- exit marker: position observed flat after being in one
   bool isBuy;
   if(g_hadPos && !HaveOursByMagic(InpMagic, isBuy))
     {
      MarkerCircle("AK_", seq, g_wasLong, b0.time, b0.c);
      g_hadPos = false;
     }

   //--- signals
   bool kamaRising  = KamaRising(InpRisingLen);
   bool kamaFalling = KamaFalling(InpFallingLen);
   bool longTrendOk  = (!InpUseSma || (!IsNa(v.sma) && b0.c > v.sma));
   bool shortTrendOk = (!InpUseSma || (!IsNa(v.sma) && b0.c < v.sma));
   bool allowLong  = (InpDirection == DIR_LONG || InpDirection == DIR_BOTH);
   bool allowShort = (InpDirection == DIR_SHORT || InpDirection == DIR_BOTH);
   bool cooldownOk = (g_lastTradeBar == INT_MIN) || ((seq - g_lastTradeBar) >= InpBarsBetween);

   bool longSig  = kamaRising && longTrendOk && allowLong && cooldownOk;
   bool shortSig = kamaFalling && shortTrendOk && allowShort && cooldownOk;

   //--- entries (flip: the opposite side is closed by EnterWithBracket)
   bool hadPosBefore = HaveOursByMagic(InpMagic, isBuy);
   if(longSig && !hadPosBefore && !EntryPending())
     {
      double lots = LotsFromEquityPct(InpQtyPct, b0.c);
      if(lots > 0.0)
        {
         double slDist = InpUseStop ? b0.c * InpStopPct / 100.0 : 0.0;
         EnterWithBracket(true, lots, EMPTY_VALUE, EMPTY_VALUE, slDist, 0.0,
                          InpMagic, "Aurora-KAMA Long");
         g_lastTradeBar = seq;
         g_fillTime     = iTime(_Symbol, _Period, 0);
         g_fillBarTime  = g_fillTime;
         ApplyFixedStop();          // re-anchor to the real fill price
         MarkerArrow("AK_", seq, true, b0.time, b0.l, (color)0x76FF03); // #00e676
        }
     }
   else if(shortSig && !hadPosBefore && !EntryPending())
     {
      double lots = LotsFromEquityPct(InpQtyPct, b0.c);
      if(lots > 0.0)
        {
         double slDist = InpUseStop ? b0.c * InpStopPct / 100.0 : 0.0;
         EnterWithBracket(false, lots, EMPTY_VALUE, EMPTY_VALUE, slDist, 0.0,
                          InpMagic, "Aurora-KAMA Short");
         g_lastTradeBar = seq;
         g_fillTime     = iTime(_Symbol, _Period, 0);
         g_fillBarTime  = g_fillTime;
         ApplyFixedStop();
         MarkerArrow("AK_", seq, false, b0.time, b0.h, (color)0x5252FF); // #ff5252
        }
     }

   //--- state for the next bar
   bool nowIn;
   if(HaveOursByMagic(InpMagic, nowIn))
     {
      g_hadPos  = true;
      g_wasLong = nowIn;
     }

   //--- trailing (per closed bar, like calc_on_every_tick = false)
   if(InpUseTrail && g_hadPos)
      ManageTrailing();
  }

//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpKamaLen < 2 || InpKamaFast < 1 || InpKamaSlow < 1 ||
      InpRisingLen < 1 || InpFallingLen < 1 || InpSmaLen < 2 ||
      InpBarsBetween < 0 || InpStopPct < 0.1 || InpTrailPct < 0.1 ||
      InpTrailDelay < 0 || InpQtyPct < 1.0 || InpQtyPct > 100.0 ||
      InpHistoryBars < 500)
      return(INIT_PARAMETERS_INCORRECT);

   g_series.Reset();
   ArrayFree(g_val);
   g_barSeq       = 0;
   g_lastTradeBar = INT_MIN;
   g_fillTime     = 0;
   g_fillBarTime  = 0;
   g_hadPos       = false;
   g_wasLong      = false;
   g_inited       = false;
   ResetPending();
   ObjectsDeleteAll(0, "AK_");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   ObjectsDeleteAll(0, "AK_");
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   RetryPendingEntry();                       // market-closed queue (D8)
   if(!g_inited)
     {
      PineBar loaded[];
      int got = SeriesLoadClosed(loaded, InpHistoryBars);
      if(got < 100)
         return;
      ArrayFree(g_val);
      for(int i = 0; i < got; i++)
        {
         g_series.Append(loaded[i]);
         ComputeBar();
        }
      ArrayFree(loaded);
      g_barSeq = g_series.Count() - 1;
      g_inited = true;
      PrintFormat("Aurora-KAMA: warm-up over %d bars (seq=%d)", g_series.Count(), g_barSeq);
      return;
     }
   if(SeriesAppendClosed(g_series))
     {
      ComputeBar();
      OnClosedBar();
     }
  }
//+------------------------------------------------------------------+
