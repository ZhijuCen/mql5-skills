//+------------------------------------------------------------------+
//|                                  MACDPullbackSniper-EA.mq5         |
//|  MQL5 port of the open-source Pine strategy                        |
//|  "MACD Pullback Sniper | Trend + ADX Filtered Strategy"            |
//|  by blitz_locked                                                   |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 macd-pullback-sniper.pine (119 lines, v6)           |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0005-macd-pullback-sniper.md                        |
//|  Author tips: trending markets, higher timeframes (1H/4H/Daily);   |
//|  sizing unit note fits crypto & stocks                             |
//|  (assets/mql5-side/0005-macd-pullback-sniper.ini uses BTCUSD H4)    |
//|                                                                    |
//|  Original (c) blitz_locked, licensed under MPL-2.0                 |
//|  https://mozilla.org/MPL/2.0/ (file-level copyleft - keep header)  |
//|                                                                    |
//|  Execution model: signal on the confirmed bar -> market order on   |
//|  the next bar's first tick; SL/TP anchored to the FILL price with  |
//|  the signal bar's ATR (exactly the Pine re-anchoring behaviour).    |
//|  Deviations D1-D6: port record.                                     |
//+------------------------------------------------------------------+
#property copyright "(c) blitz_locked - MPL-2.0 - MQL5 port"
#property link      "https://www.tradingview.com/script/V87nRt9v-MACD-Pullback-Sniper-Trend-ADX-Filtered-Strategy/"
#property version   "1.00"
#property description "MACD Pullback Sniper - MQL5 EA port"
#property strict

#include "strategy-common.mqh"

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs (same defaults, same groups)       |
//+------------------------------------------------------------------+
input group "MACD"
input int            InpFastLen   = 12;           // Fast EMA
input int            InpSlowLen   = 26;           // Slow EMA
input int            InpSignalLen = 9;            // Signal EMA

input group "Filters"
input bool           InpUseTrend  = true;         // Trend filter (price vs EMA)
input int            InpTrendLen  = 200;          // Trend EMA length
input bool           InpUseZero   = true;         // Zero-line filter
input bool           InpUseAdx    = true;         // ADX filter
input int            InpAdxLen    = 14;           // ADX length
input double         InpAdxMin    = 20.0;         // ADX minimum

input group "Risk"
input int            InpAtrLen    = 14;           // ATR length
input double         InpSlMult    = 2.0;          // Stop distance (x ATR)
input double         InpRrRatio   = 2.0;          // Reward : Risk
input double         InpRiskPct   = 1.0;          // Risk per trade (% of equity)
input double         InpMaxLev    = 1.0;          // Max position size (x equity)
input bool           InpExitCross = true;         // Exit on opposite MACD cross

input group "General"
input bool           InpAllowShort = true;        // Allow shorts
input datetime       InpStartDate = D'2018.01.01 00:00:00'; // Start date
input datetime       InpEndDate   = D'2069.12.31 23:59:59'; // End date

input group "Trading"
input long           InpMagic       = 40005;      // Magic number
input int            InpHistoryBars = 50000;      // History bars for warm-up

//+------------------------------------------------------------------+
//| Per-bar state                                                      |
//+------------------------------------------------------------------+
struct S5Vals
  {
   double macd;
   double sig;
   double adx;
   double atr;
   double tEma;
  };

CPineSeries g_series;
S5Vals      g_val[];
CEma        g_fastEma;
CEma        g_slowEma;
CEma        g_sigEma;
CEma        g_trendEma;
CRma        g_atrSm;
CAdxState   g_adx;
int         g_barSeq = 0;
bool        g_inited = false;

//+------------------------------------------------------------------+
color Rgb(const uint rrggbb)
  {
   uint r = (rrggbb >> 16) & 0xFF;
   uint g = (rrggbb >> 8) & 0xFF;
   uint b = (rrggbb) & 0xFF;
   return((color)((b << 16) | (g << 8) | r));
  }

//+------------------------------------------------------------------+
//| ta.crossover / ta.crossunder (na anywhere -> false, like Pine)     |
//+------------------------------------------------------------------+
bool CrossOver(const double a0, const double a1, const double b0, const double b1)
  {
   if(IsNa(a0) || IsNa(a1) || IsNa(b0) || IsNa(b1))
      return(false);
   return(a0 > b0 && a1 <= b1);
  }

bool CrossUnder(const double a0, const double a1, const double b0, const double b1)
  {
   if(IsNa(a0) || IsNa(a1) || IsNa(b0) || IsNa(b1))
      return(false);
   return(a0 < b0 && a1 >= b1);
  }

//+------------------------------------------------------------------+
//| Compute the newest closed bar into g_val (chronological, once)     |
//+------------------------------------------------------------------+
void ComputeBar()
  {
   int n = g_series.Count();
   if(n < 1)
      return;
   PineBar b = g_series.Get(0);
   bool   hasPrev = (n >= 2);

   //--- MACD: fast/slow EMAs -> macd -> signal EMA (seeded on first
   //--- DEFINED macd value; Pine's chain is na until the EMAs exist)
   g_fastEma.Update(b.c);
   g_slowEma.Update(b.c);
   double macd = (g_fastEma.Defined() && g_slowEma.Defined())
                 ? g_fastEma.Value() - g_slowEma.Value() : EMPTY_VALUE;
   if(!IsNa(macd))
      g_sigEma.Update(macd);
   double sig = g_sigEma.Defined() ? g_sigEma.Value() : EMPTY_VALUE;

   //--- ATR (Wilder RMA of TR) + ADX (Pine ta.dmi(len,len))
   double tr = hasPrev ? TrueRangeAt(b, g_series.Get(1).c) : (b.h - b.l);
   g_atrSm.Update(tr);
   double adx = g_adx.Update(b.h, b.l, tr);

   //--- trend EMA
   g_trendEma.Update(b.c);

   S5Vals v;
   v.macd = macd;
   v.sig  = sig;
   v.adx  = adx;
   v.atr  = g_atrSm.Value();
   v.tEma = g_trendEma.Value();
   ArrayResize(g_val, n);
   g_val[n - 1] = v;
  }

//+------------------------------------------------------------------+
//| Signal + trade management on one confirmed bar                     |
//+------------------------------------------------------------------+
void OnClosedBar()
  {
   int n = g_series.Count();
   if(n < 2)
      return;
   int seq = n - 1;
   g_barSeq = seq;
   PineBar b0 = g_series.Get(0);
   S5Vals  v  = g_val[n - 1];
   S5Vals  vp = g_val[n - 2];

   //--- MACD signal-line crosses
   bool bullCross = CrossOver(v.macd, vp.macd, v.sig, vp.sig);
   bool bearCross = CrossUnder(v.macd, vp.macd, v.sig, vp.sig);

   //--- filters (Pine: na makes the comparison false)
   bool inRange = (b0.time >= InpStartDate && b0.time <= InpEndDate);
   bool trendLongOk  = (!InpUseTrend || (!IsNa(v.tEma) && b0.c > v.tEma));
   bool trendShortOk = (!InpUseTrend || (!IsNa(v.tEma) && b0.c < v.tEma));
   bool zeroLongOk   = (!InpUseZero  || (!IsNa(v.macd) && v.macd < 0));
   bool zeroShortOk  = (!InpUseZero  || (!IsNa(v.macd) && v.macd > 0));
   bool adxOk        = (!InpUseAdx   || (!IsNa(v.adx) && v.adx > InpAdxMin));

   bool longSig  = bullCross && trendLongOk && zeroLongOk && adxOk && inRange;
   bool shortSig = bearCross && trendShortOk && zeroShortOk && adxOk && inRange
                   && InpAllowShort;

   //--- exit on opposite cross (Pine: unless it is a valid reversal entry)
   bool isBuy;
   if(InpExitCross)
     {
      if(bearCross && HaveOursByMagic(InpMagic, isBuy) && isBuy && !shortSig)
         CloseOursByMagic(InpMagic, "MACD cross");
      if(bullCross && HaveOursByMagic(InpMagic, isBuy) && !isBuy && !longSig)
         CloseOursByMagic(InpMagic, "MACD cross");
     }

   //--- sizing: fixed % risk, capped at maxLev x equity (Pine f_qty)
   double stopDist = EMPTY_VALUE;
   if(!IsNa(v.atr) && v.atr > 0.0)
      stopDist = v.atr * InpSlMult;
   double lots = 0.0;
   if((longSig || shortSig) && !IsNa(stopDist) && stopDist > 0.0)
     {
      lots = LotsFromRiskPct(InpRiskPct, stopDist);
      if(lots > 0.0)
        {
         double contract = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_CONTRACT_SIZE);
         if(contract > 0.0 && b0.c > 0.0)
           {
            double maxLots = InpMaxLev * AccountInfoDouble(ACCOUNT_EQUITY) / (b0.c * contract);
            if(lots > maxLots)
               lots = ClampLots(maxLots);
           }
        }
     }

   //--- entries (fill-anchored SL/TP: the Pine script re-anchors the
   //--- bracket to position_avg_price with the SIGNAL bar's entryAtr)
   if(longSig && lots > 0.0 && !EntryPending())
     {
      EnterWithBracket(true, lots, EMPTY_VALUE, EMPTY_VALUE,
                       stopDist, stopDist * InpRrRatio, InpMagic, "MACD-Sniper Long");
      MarkerArrow("MP_", seq, true, b0.time, b0.l, Rgb(0x008080));   // color.teal
     }
   else if(shortSig && lots > 0.0 && !EntryPending())
     {
      EnterWithBracket(false, lots, EMPTY_VALUE, EMPTY_VALUE,
                       stopDist, stopDist * InpRrRatio, InpMagic, "MACD-Sniper Short");
      MarkerArrow("MP_", seq, false, b0.time, b0.h, Rgb(0xFF0000));  // color.red
     }
  }

//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpFastLen < 1 || InpSlowLen < 1 || InpSignalLen < 1 ||
      InpTrendLen < 2 || InpAdxLen < 1 || InpAdxMin < 1 ||
      InpAtrLen < 1 || InpSlMult < 0.1 || InpRrRatio < 0.5 ||
      InpRiskPct < 0.1 || InpRiskPct > 10.0 || InpMaxLev < 0.1 ||
      InpHistoryBars < 500)
      return(INIT_PARAMETERS_INCORRECT);

   g_fastEma.Init(InpFastLen);
   g_slowEma.Init(InpSlowLen);
   g_sigEma.Init(InpSignalLen);
   g_trendEma.Init(InpTrendLen);
   g_atrSm.Init(InpAtrLen);
   g_adx.Init(InpAdxLen);
   g_series.Reset();
   ArrayFree(g_val);
   g_barSeq = 0;
   g_inited = false;
   ResetPending();
   ObjectsDeleteAll(0, "MP_");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   ObjectsDeleteAll(0, "MP_");
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   RetryPendingEntry();                       // market-closed queue (D7)
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
      PrintFormat("MACD-Sniper: warm-up over %d bars (seq=%d)", g_series.Count(), g_barSeq);
      return;
     }
   if(SeriesAppendClosed(g_series))
     {
      ComputeBar();
      OnClosedBar();
     }
  }
//+------------------------------------------------------------------+
