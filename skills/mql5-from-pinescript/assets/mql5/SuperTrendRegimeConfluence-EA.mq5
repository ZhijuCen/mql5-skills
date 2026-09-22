//+------------------------------------------------------------------+
//|                               SuperTrendRegimeConfluence-EA.mq5    |
//|  MQL5 port of the open-source Pine strategy                        |
//|  "SuperTrend Regime Confluence" by DefinedEdge                     |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 supertrend-regime-confluence.pine (372 lines, v6)   |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0004-supertrend-regime-confluence.md                |
//|  Author-recommended instrument: BTCUSDT, 4H                        |
//|  (assets/mql5-side/0004-supertrend-regime-confluence.ini)           |
//|                                                                    |
//|  Original (c) DefinedEdge, licensed under MPL-2.0                  |
//|  https://mozilla.org/MPL/2.0/ (file-level copyleft - keep header)  |
//|                                                                    |
//|  Execution model: signal on the confirmed bar -> market order on   |
//|  the next bar's first tick (TV broker-emulator next-bar-open       |
//|  fill); the bracket is attached on the fill tick using ABSOLUTE    |
//|  levels anchored to the SIGNAL bar's close (exactly the Pine       |
//|  strategy.exit arguments). Trail parameters are frozen at entry    |
//|  (the Pine script only passes them once, inside the entry block).  |
//|  Deviations D1-D8: port record.                                     |
//+------------------------------------------------------------------+
#property copyright "(c) DefinedEdge - MPL-2.0 - MQL5 port"
#property link      "https://www.tradingview.com/script/mpjNqADq-SuperTrend-Regime-Confluence/"
#property version   "1.00"
#property description "SuperTrend Regime Confluence - MQL5 EA port"
#property strict

#include "strategy-common.mqh"

//+------------------------------------------------------------------+
//| Enums (Pine input.string options)                                 |
//+------------------------------------------------------------------+
enum ENUM_SIZE_MODE
  {
   SIZE_RISK_PCT   = 0,   // Risk %
   SIZE_EQUITY_PCT = 1,   // Equity %
   SIZE_FIXED      = 2    // Fixed Units
  };

enum ENUM_SL_MODE
  {
   SL_ATR       = 0,      // ATR
   SL_PERCENT   = 1,      // Percent
   SL_SUPERTREND = 2      // SuperTrend
  };

enum ENUM_TP_MODE
  {
   TP_RR      = 0,        // RR
   TP_PERCENT = 1,        // Percent
   TP_NONE    = 2         // None
  };

//--- regime codes (Pine: 0 = ranging, 1 = trending, 2 = volatile)
#define REG_RANGING   0
#define REG_TRENDING  1
#define REG_VOLATILE  2

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs (same defaults, same groups)       |
//+------------------------------------------------------------------+
input group "SuperTrend"
input int            InpAtLen      = 10;          // ATR Length
input double         InpBaseMult   = 3.0;         // Base Multiplier
input int            InpSrcMode    = 0;           // Source (0=hl2,1=close; Pine default hl2)

input group "Regime Detection"
input int            InpRegLen     = 40;          // Regime Lookback
input int            InpAdxLen     = 14;          // ADX Length
input double         InpAdxThr     = 20;          // ADX Trend Threshold
input bool           InpAdaptive   = true;        // Adaptive Multiplier

input group "Signal Engine"
input int            InpTrendLen   = 50;          // Trend EMA Length
input int            InpVolLen     = 20;          // Volume MA Length
input int            InpMinScore   = 65;          // Min Signal Score

input group "Position Sizing"
input ENUM_SIZE_MODE InpSizeMode   = SIZE_RISK_PCT; // Sizing Mode
input double         InpRiskPct    = 5.0;         // Risk % per Trade
input double         InpEqPct      = 15.0;        // Equity % (notional)
input double         InpFixedQty   = 1.0;         // Fixed Units
input bool           InpNoLev      = true;        // Cap at No Leverage (90% equity)

input group "Risk Management"
input ENUM_SL_MODE   InpSlMode     = SL_ATR;      // Stop Loss Mode
input double         InpSlAtr      = 6.0;         // SL ATR Multiplier
input double         InpSlPct      = 3.0;         // SL Percent
input ENUM_TP_MODE   InpTpMode     = TP_RR;       // Take Profit Mode
input double         InpTpRR       = 2.5;         // TP Risk:Reward
input double         InpTpPct      = 6.0;         // TP Percent
input bool           InpTrail      = false;       // Trailing Stop
input double         InpTrailAtr   = 2.5;         // Trail ATR Mult

input group "Trade Filters"
input bool           InpTrendF     = true;        // EMA Trend Filter
input bool           InpRegF       = true;        // Skip Ranging
input bool           InpVolF       = true;        // Volume Filter
input int            InpSigCD      = 5;           // Cooldown (bars)
input bool           InpLongs      = true;        // Allow Longs
input bool           InpShorts     = true;        // Allow Shorts

input group "Backtest"
input datetime       InpBtFrom     = D'2015.01.01'; // From
input datetime       InpBtTo       = D'2035.01.01'; // To

input group "Visuals"
input bool           InpSGlow      = true;        // Band Glow Effect (NO-OP, D6)
input bool           InpSRegBg     = true;        // Regime Background (NO-OP, D6)
input bool           InpShowLbl    = true;        // Show score labels

input group "Colors"
input color          InpCBull      = (color)0x819908; // Bull (Pine #089981)
input color          InpCBear      = (color)0x4536F2; // Bear (Pine #f23645)

input group "Trading"
input long           InpMagic       = 40004;      // Magic number
input int            InpHistoryBars = 50000;      // History bars for warm-up

//+------------------------------------------------------------------+
//| Per-bar state (append-only; last element = newest closed bar)      |
//+------------------------------------------------------------------+
struct STVals
  {
   double atr;
   double atrMa;
   double atrRatio;
   double adx;
   double adaptMult;
   double band;
   double trendMa;
   double volMa;
   int    dir;
   int    regime;
  };

CPineSeries g_series;
STVals      g_val[];
CRma        g_atrSm;
CAdxState   g_adx;
CEma        g_trendEma;
int         g_barSeq       = 0;   // Pine bar_index (counts appended bars)
int         g_lastEntryBar = 0;
datetime    g_fillTime     = 0;
double      g_entrySlDist  = 0;   // frozen at entry (Pine passes them once)
double      g_entryAtr     = 0;
bool        g_inited       = false;

//+------------------------------------------------------------------+
//| Pine #RRGGBB -> MQL5 color (0x00BBGGRR)                           |
//+------------------------------------------------------------------+
color Rgb(const uint rrggbb)
  {
   uint r = (rrggbb >> 16) & 0xFF;
   uint g = (rrggbb >> 8) & 0xFF;
   uint b = (rrggbb) & 0xFF;
   return((color)((b << 16) | (g << 8) | r));
  }

//+------------------------------------------------------------------+
double SrcPrice(const PineBar &b)
  {
   return(InpSrcMode == 0 ? (b.h + b.l) / 2.0 : b.c);   // Pine hl2 default
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
   int    prevDir0 = 1;
   double prevBandInit = EMPTY_VALUE;
   if(hasPrev)
     {
      prevDir0    = g_val[n - 2].dir;
      prevBandInit = g_val[n - 2].band;
     }
   STVals v;

   //--- ATR (Wilder RMA of TR; first bar TR = h-l like Pine ta.tr)
   double tr = hasPrev ? TrueRangeAt(b, g_series.Get(1).c) : (b.h - b.l);
   g_atrSm.Update(tr);
   v.atr = g_atrSm.Value();

   //--- ATR ratio over the regime lookback window
   double atrSum = 0.0;
   bool   atrOk  = !IsNa(v.atr);
   for(int k = 0; k < InpRegLen; k++)
     {
      double a = (k == 0 ? v.atr : (k < n ? g_val[n - 1 - k].atr : EMPTY_VALUE));
      if(IsNa(a)) { atrOk = false; break; }
      atrSum += a;
     }
   v.atrMa    = (atrOk && InpRegLen > 0) ? atrSum / InpRegLen : EMPTY_VALUE;
   v.atrRatio = (!IsNa(v.atrMa) && v.atrMa > 0.0) ? v.atr / v.atrMa : 1.0;

   //--- manual ADX (Pine ta.dmi(len,len))
   v.adx = g_adx.Update(b.h, b.l, tr);

   //--- regime sequence (Pine `var`, evaluated per bar in order)
   if(v.atrRatio > 1.4)
      v.regime = REG_VOLATILE;
   else if(!IsNa(v.adx) && v.adx < InpAdxThr && v.atrRatio < 0.9)
      v.regime = REG_RANGING;
   else
      v.regime = REG_TRENDING;

   //--- adaptive multiplier, clamped to [0.5x, 2x] base
   double mult = InpBaseMult;
   if(InpAdaptive)
     {
      if(v.regime == REG_VOLATILE)
         mult = InpBaseMult * (1.0 + (v.atrRatio - 1.0) * 0.4);
      else if(v.regime == REG_RANGING)
         mult = InpBaseMult * 0.85;
     }
   v.adaptMult = MathMax(MathMin(mult, InpBaseMult * 2.0), InpBaseMult * 0.5);

   //--- SuperTrend band / direction sequence (Pine var stBand / stDir)
   int    prevDir = prevDir0;
   double src     = SrcPrice(b);
   if(IsNa(v.atr))
     {
      //--- Pine: bases are na while ATR warms up -> band stays na, no flips
      v.band = EMPTY_VALUE;
      v.dir  = prevDir;
     }
   else
     {
      double upperBase = src + v.adaptMult * v.atr;
      double lowerBase = src - v.adaptMult * v.atr;
      double prevBand  = !IsNa(prevBandInit) ? prevBandInit
                         : (prevDir == 1 ? lowerBase : upperBase);
      int    dir  = prevDir;
      double band;
      if(dir == 1)
        {
         band = MathMax(lowerBase, prevBand);
         if(b.c < band) { dir = -1; band = upperBase; }
        }
      else
        {
         band = MathMin(upperBase, prevBand);
         if(b.c > band) { dir = 1; band = lowerBase; }
        }
      v.band = band;
      v.dir  = dir;
     }

   //--- trend EMA + volume MA
   g_trendEma.Update(b.c);
   v.trendMa = g_trendEma.Value();
   double vSum = 0.0;
   for(int k = 0; k < InpVolLen; k++)
      vSum += (k < n ? g_series.Get(k).v : 0.0);
   v.volMa = (n >= InpVolLen) ? vSum / InpVolLen : EMPTY_VALUE;

   ArrayResize(g_val, n);
   g_val[n - 1] = v;
  }

//+------------------------------------------------------------------+
//| Composite confluence score0-100 (Pine scoreSignal)                 |
//+------------------------------------------------------------------+
int ScoreSignal(const bool isBull, const int n)
  {
   PineBar b0 = g_series.Get(0);
   STVals v = g_val[n - 1];
   double safeAtr = IsNa(v.atr) ? 0.001 : v.atr;

   //--- F1: volume surge (0-20)
   double vRat = (!IsNa(v.volMa) && v.volMa > 0.0) ? b0.v / v.volMa : 1.0;
   int score = (vRat >= 2.5 ? 20 : vRat >= 1.5 ? 14 : vRat >= 1.0 ? 8 : 3);

   //--- F2: displacement beyond the band (0-25)
   double disp = EMPTY_VALUE;
   if(!IsNa(v.band))
      disp = isBull ? (b0.c - v.band) : (v.band - b0.c);
   if(!IsNa(disp))
     {
      double dispAtr = disp / safeAtr;
      score += (dispAtr >= 1.5 ? 25 : dispAtr >= 0.8 ? 18 : dispAtr >= 0.3 ? 12 : dispAtr > 0 ? 5 : 0);
     }

   //--- F3: EMA trend alignment (0-20)
   bool   trendUp = !IsNa(v.trendMa) && b0.c > v.trendMa;
   bool   trendDn = !IsNa(v.trendMa) && b0.c < v.trendMa;
   bool   aligned = isBull ? trendUp : trendDn;
   double emaDist = !IsNa(v.trendMa) ? MathAbs(b0.c - v.trendMa) / safeAtr : EMPTY_VALUE;
   if(aligned && !IsNa(emaDist) && emaDist > 0.5)
      score += 20;
   else if(aligned)
      score += 14;
   else if(!IsNa(emaDist) && emaDist < 0.3)
      score += 8;
   else
      score += 2;

   //--- F4: regime quality (0-15)
   score += (v.regime == REG_TRENDING ? 15 : v.regime == REG_VOLATILE ? 8 : 3);

   //--- F5: band distance held before the flip (0-20)
   double prevDist = 0.0;
   if(n >= 2 && !IsNa(g_val[n - 2].band))
      prevDist = MathAbs(g_series.Get(1).c - g_val[n - 2].band) / safeAtr;
   score += (prevDist >= 2.0 ? 20 : prevDist >= 1.0 ? 14 : prevDist >= 0.5 ? 8 : 3);

   return((int)MathMin(MathRound((double)score), 100.0));
  }

//+------------------------------------------------------------------+
bool TrendGateOk(const bool isBull, const STVals &v, const double closePx)
  {
   if(!InpTrendF)
      return(true);
   if(IsNa(v.trendMa))
      return(false);
   return(isBull ? closePx > v.trendMa : closePx < v.trendMa);
  }

//+------------------------------------------------------------------+
void CloseOurs(const string cmt)
  {
   CTrade trade;
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetTypeFillingBySymbol(_Symbol);
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if(PositionGetInteger(POSITION_MAGIC) != InpMagic)
         continue;
      if(!trade.PositionClose(ticket))
         PrintFormat("%s: close failed retcode=%d", cmt, trade.ResultRetcode());
     }
  }

//+------------------------------------------------------------------+
bool HaveOurs(bool &isBuy)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if(PositionGetInteger(POSITION_MAGIC) != InpMagic)
         continue;
      isBuy = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY);
      return(true);
     }
   return(false);
  }

//+------------------------------------------------------------------+
//| Trailing stop (params frozen at entry - Pine passes them once)     |
//+------------------------------------------------------------------+
void ManageTrailing()
  {
   bool isBuy;
   if(!HaveOurs(isBuy))
      return;
   if(IsNa(g_entryAtr) || g_entryAtr <= 0.0 || g_entrySlDist <= 0.0 || g_fillTime == 0)
      return;
   //--- extremes of CLOSED bars since the fill bar
   double ext = isBuy ? -DBL_MAX : DBL_MAX;
   int n = g_series.Count();
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
   double fill = PositionGetDouble(POSITION_PRICE_OPEN);
   bool armed = isBuy ? (ext >= fill + g_entrySlDist)
                      : (ext <= fill - g_entrySlDist);
   if(!armed)
      return;
   double offset = g_entryAtr * InpTrailAtr;
   double newStop = isBuy ? ext - offset : ext + offset;
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
      PrintFormat("ST-Regime: trail modify failed retcode=%d", trade.ResultRetcode());
  }

//+------------------------------------------------------------------+
//| Score label at the entry bar (Pine label.new with score)           |
//+------------------------------------------------------------------+
void ScoreLabel(const int seq, const double yPrice, const int score, const bool isBull)
  {
   string name = "SC_t" + IntegerToString(seq);
   if(ObjectFind(0, name) >= 0)
      return;
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, g_series.Get(0).time, yPrice))
      return;
   bool bright = score >= 70;
   color clr = bright ? (isBull ? Rgb(0x00E676) : Rgb(0xFF5252)) : Rgb(0x546E7A);
   ObjectSetString(0, name, OBJPROP_TEXT,
                   (bright ? "* " : "o ") + IntegerToString(score));
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
  }

//+------------------------------------------------------------------+
//| One confirmed-bar evaluation (Pine block gated by isconfirmed)     |
//+------------------------------------------------------------------+
void OnClosedBar()
  {
   int n = g_series.Count();
   if(n < 2)
      return;
   int seq = n - 1;
   g_barSeq = seq;
   PineBar b0 = g_series.Get(0);
   STVals v = g_val[n - 1];
   STVals vp = g_val[n - 2];

   bool flip = (v.dir != vp.dir);
   bool inWin = (b0.time >= InpBtFrom && b0.time <= InpBtTo);
   bool cdOk  = ((seq - g_lastEntryBar) > InpSigCD);

   //--- stop / target distances (Pine recomputes them every bar)
   double slDist = EMPTY_VALUE;
   if(InpSlMode == SL_ATR)
      slDist = IsNa(v.atr) ? EMPTY_VALUE : v.atr * InpSlAtr;
   else if(InpSlMode == SL_PERCENT)
      slDist = b0.c * InpSlPct / 100.0;
   else
      slDist = IsNa(v.band) ? EMPTY_VALUE : MathAbs(b0.c - v.band);
   double tpDist = EMPTY_VALUE;
   if(InpTpMode == TP_RR)
      tpDist = IsNa(slDist) ? EMPTY_VALUE : slDist * InpTpRR;
   else if(InpTpMode == TP_PERCENT)
      tpDist = b0.c * InpTpPct / 100.0;
   else
      tpDist = 0.0;

   //--- entry signals (score + gates, direction toggles)
   bool longSig = false, shortSig = false;
   int  sigScore = 0;
   if(flip && inWin && cdOk)
     {
      if(v.dir == 1 && InpLongs)
        {
         sigScore = ScoreSignal(true, n);
         bool passScore = sigScore >= InpMinScore;
         bool passTrend = TrendGateOk(true, v, b0.c);
         bool passReg   = (!InpRegF || v.regime != REG_RANGING);
         bool passVol   = (!InpVolF || (!IsNa(v.volMa) && b0.v > v.volMa));
         if(passScore && passTrend && passReg && passVol)
            longSig = true;
        }
      else if(v.dir == -1 && InpShorts)
        {
         sigScore = ScoreSignal(false, n);
         bool passScore = sigScore >= InpMinScore;
         bool passTrend = TrendGateOk(false, v, b0.c);
         bool passReg   = (!InpRegF || v.regime != REG_RANGING);
         bool passVol   = (!InpVolF || (!IsNa(v.volMa) && b0.v > v.volMa));
         if(passScore && passTrend && passReg && passVol)
            shortSig = true;
        }
     }

   //--- position sizing (Pine f_posQty) + no-leverage cap
   double lots = 0.0;
   if((longSig || shortSig) && !IsNa(slDist) && slDist > 0.0)
     {
      if(InpSizeMode == SIZE_RISK_PCT)
         lots = LotsFromRiskPct(InpRiskPct, slDist);
      else if(InpSizeMode == SIZE_EQUITY_PCT)
         lots = LotsFromEquityPct(InpEqPct, b0.c);
      else
         lots = ClampLots(InpFixedQty);
      if(InpNoLev && lots > 0.0)
        {
         double contract = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_CONTRACT_SIZE);
         if(contract > 0.0 && b0.c > 0.0)
           {
            double maxLots = 0.90 * AccountInfoDouble(ACCOUNT_EQUITY) / (b0.c * contract);
            if(lots > maxLots)
               lots = ClampLots(maxLots);
           }
        }
     }

   //--- execute long (Pine: absolute levels from the SIGNAL bar's close)
   if(longSig && lots > 0.0 && !EntryPending())
     {
      double slAbs = b0.c - slDist;
      double tpAbs = (InpTpMode != TP_NONE && !IsNa(tpDist)) ? b0.c + tpDist : EMPTY_VALUE;
      EnterWithBracket(true, lots, slAbs, tpAbs, 0.0, 0.0, InpMagic, "ST-Regime Long");
      g_lastEntryBar = seq;
      g_fillTime     = iTime(_Symbol, _Period, 0);
      g_entrySlDist  = slDist;
      g_entryAtr     = IsNa(v.atr) ? 0.0 : v.atr;
      if(InpShowLbl)
         ScoreLabel(seq, IsNa(v.band) ? b0.c : v.band, sigScore, true);
     }
   //--- execute short
   else if(shortSig && lots > 0.0 && !EntryPending())
     {
      double slAbs = b0.c + slDist;
      double tpAbs = (InpTpMode != TP_NONE && !IsNa(tpDist)) ? b0.c - tpDist : EMPTY_VALUE;
      EnterWithBracket(false, lots, slAbs, tpAbs, 0.0, 0.0, InpMagic, "ST-Regime Short");
      g_lastEntryBar = seq;
      g_fillTime     = iTime(_Symbol, _Period, 0);
      g_entrySlDist  = slDist;
      g_entryAtr     = IsNa(v.atr) ? 0.0 : v.atr;
      if(InpShowLbl)
         ScoreLabel(seq, IsNa(v.band) ? b0.c : v.band, sigScore, false);
     }

   //--- SuperTrend flip exit (Pine: after the entry blocks)
   if(InpSlMode == SL_SUPERTREND && flip)
     {
      bool isBuy;
      if(HaveOurs(isBuy) && ((isBuy && v.dir == -1) || (!isBuy && v.dir == 1)))
         CloseOurs("ST Flip");
     }

   //--- trailing (evaluated per closed bar, like calc_on_every_tick=false)
   if(InpTrail)
      ManageTrailing();
  }

//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpAtLen < 1 || InpAtLen > 50 || InpBaseMult < 0.5 || InpBaseMult > 10.0 ||
      InpRegLen < 10 || InpRegLen > 100 || InpAdxLen < 5 || InpAdxLen > 50 ||
      InpAdxThr < 10 || InpAdxThr > 40 || InpTrendLen < 10 || InpTrendLen > 200 ||
      InpVolLen < 5 || InpVolLen > 50 || InpMinScore < 0 || InpMinScore > 90 ||
      InpRiskPct < 0.1 || InpRiskPct > 10.0 || InpEqPct < 1.0 || InpEqPct > 100.0 ||
      InpFixedQty < 0.0 || InpSlAtr < 0.5 || InpSlAtr > 10.0 ||
      InpSlPct < 0.5 || InpSlPct > 15.0 || InpTpRR < 0.5 || InpTpRR > 10.0 ||
      InpTpPct < 0.5 || InpTpPct > 25.0 || InpTrailAtr < 0.5 || InpTrailAtr > 8.0 ||
      InpSigCD < 0 || InpSigCD > 50 || InpHistoryBars < 500)
      return(INIT_PARAMETERS_INCORRECT);

   g_atrSm.Init(InpAtLen);
   g_adx.Init(InpAdxLen);
   g_trendEma.Init(InpTrendLen);
   g_series.Reset();
   ArrayFree(g_val);
   g_barSeq       = 0;
   g_lastEntryBar = 0;
   g_fillTime     = 0;
   g_entrySlDist  = 0;
   g_entryAtr     = 0;
   g_inited       = false;
   ResetPending();
   ObjectsDeleteAll(0, "SC_");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   ObjectsDeleteAll(0, "SC_");
  }

//+------------------------------------------------------------------+
//| Main: backfill once for warm-up state, then one evaluation per     |
//| newly closed bar (orders hit the next bar's first tick).           |
//+------------------------------------------------------------------+
void OnTick()
  {
   RetryPendingEntry();                       // market-closed queue (D9)
   if(!g_inited)
     {
      PineBar loaded[];
      int got = SeriesLoadClosed(loaded, InpHistoryBars);
      if(got < 100)
         return;                              // retry on the next tick
      ArrayFree(g_val);
      for(int i = 0; i < got; i++)            // append + compute, oldest first
        {
         g_series.Append(loaded[i]);
         ComputeBar();
        }
      ArrayFree(loaded);
      g_barSeq = g_series.Count() - 1;
      g_inited = true;
      PrintFormat("ST-Regime: warm-up over %d bars (seq=%d)", g_series.Count(), g_barSeq);
      return;
     }
   if(SeriesAppendClosed(g_series))
     {
      ComputeBar();                    // newest closed bar state
      OnClosedBar();                   // signals -> next-bar-open entries
     }
  }
//+------------------------------------------------------------------+
