//+------------------------------------------------------------------+
//|                                           ModernIchimokuCloud.mq5 |
//|  MQL5 port of the open-source Pine Script indicator               |
//|  "Modern Ichimoku Cloud [GBB]" v0.5 by GoodBadBitcoin.            |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 modern-ichimoku-cloud.pine  (410 lines, v6)        |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0001-modern-ichimoku-cloud.md                      |
//|  Mapping     : skills/mql5-from-pinescript/references/             |
//|                 pine-to-mql5.md                                    |
//|                                                                    |
//|  Layers (same as Pine):                                            |
//|    0 - five Ichimoku lines (9/26/52/26) + displaced cloud          |
//|    1 - ATR-normalised geometry, percentile grades                  |
//|    2 - qualified TK / Kumo / twist events                          |
//|    3 - flat-run support/resistance levels as chart objects         |
//|    4 - HTF readout, stats table, confirmed-bar alerts              |
//|                                                                    |
//|  Deviations D1-D10 are documented in the port record. Headlines:   |
//|    D1 fill transparency emulated globally (DRAW_FILLING = 2 colors)|
//|    D2 bgcolor() -> corner label (indicator cannot tint the chart)  |
//|    D3 twist markers pixel-shifted, not window-anchored             |
//|    ATR: Wilder RMA computed inline (iATR is SMA - would not match) |
//+------------------------------------------------------------------+
#property copyright "MQL5 port - see port record 0001"
#property link      "https://www.tradingview.com/script/jJAqvJP5-Modern-Ichimoku-Cloud-GBB/"
#property version   "1.00"
#property description "Modern Ichimoku Cloud [GBB] - MQL5 port (Layers 0-4)"
#property indicator_chart_window
#property indicator_buffers 28
#property indicator_plots   27

//+------------------------------------------------------------------+
//| Enums (must precede the inputs that use them)                     |
//+------------------------------------------------------------------+
enum ENUM_PALETTE
  {
   PALETTE_GBB     = 0,   // GBB
   PALETTE_CLASSIC = 1,   // Classic
   PALETTE_MONO    = 2    // Mono
  };

enum ENUM_THEME
  {
   THEME_AUTO  = 0,   // Auto
   THEME_DARK  = 1,   // Dark
   THEME_LIGHT = 2    // Light
  };

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs 1:1 (same defaults, same groups)  |
//+------------------------------------------------------------------+
input group "Classic"
input bool           InpClassicMode   = false;        // Classic mode (forces Layers 1-3 off)
input int            InpTenkanLen     = 9;            // Tenkan-sen
input int            InpKijunLen      = 26;           // Kijun-sen
input int            InpSenkouBLen    = 52;           // Senkou B
input int            InpDisplacement  = 26;           // Displacement

input group "Geometry (Layer 1)"
input bool           InpInGeom        = true;         // Normalised geometry (ATR units, percentile grades)
input int            InpAtrLen        = 0;            // ATR length (0 = Kijun)
input int            InpPctLen        = 150;          // Percentile window
input int            InpPctThin       = 30;           // Thin <= pct
input int            InpPctThk        = 70;           // Thick >= pct
input int            InpPctVThk       = 90;           // Very thick >= pct
input bool           InpShowGradeLabel= true;         // Grade label on last bar

input group "Signals (Layer 2)"
input bool           InpInQualified   = true;         // Qualified signals
input double         InpPcMin         = 1.0;          // Min price-to-cloud distance (ATR), KUMO events
input double         InpChkMin        = 1.0;          // Min Chikou momentum (ATR)
input bool           InpUseHtfFilt    = false;        // Require HTF cloud agreement
input bool           InpShowMarkers   = true;         // Show event markers
input bool           InpShowRaw       = true;         // Show unqualified events

input group "Flat levels (Layer 3)"
input bool           InpInFlat        = true;         // Flat-line levels
input int            InpFlatMinK      = 6;            // Kijun flat min bars
input int            InpFlatMinB      = 8;            // Senkou B flat min bars
input double         InpTouchTol      = 0.05;         // Touch tolerance (ATR)
input int            InpMaxAgeMul     = 3;            // Max age (x Kijun bars)
input int            InpMaxLevels     = 60;           // Max live level objects
input bool           InpHideExpired   = true;         // Hide expired levels

input group "HTF & table (Layer 4)"
input bool           InpInHtf         = true;         // HTF readout (was bgcolor wash in Pine)
input ENUM_TIMEFRAMES InpHtfPeriod    = PERIOD_CURRENT; // HTF (PERIOD_CURRENT = auto 4x chart)
input bool           InpShowTable     = false;        // Stats table
input int            InpStatsH2       = 10;           // Second stats horizon (bars)
input bool           InpTableExpanded = false;        // Expanded stats table (counts)

input group "Style"
input ENUM_PALETTE   InpPalette       = PALETTE_GBB;  // Palette
input ENUM_THEME     InpTheme         = THEME_AUTO;   // Theme

input group "Alerts"
input bool           InpEnableAlerts  = true;         // Confirmed-bar alerts (Pine alertcondition)

//+------------------------------------------------------------------+
//| Buffer indices (30)                                               |
//+------------------------------------------------------------------+
#define BUF_TENKAN       0
#define BUF_KIJUN        1
#define BUF_CHIKOU       2
#define BUF_SPANA        3
#define BUF_SPANB        4
#define BUF_FILLA        5
#define BUF_FILLB        6
#define BUF_MK_TK_BULL   7
#define BUF_MK_TK_BEAR   8
#define BUF_MK_KU_UP     9
#define BUF_MK_KU_DN    10
#define BUF_MK_RAW_BULL 11
#define BUF_MK_RAW_BEAR 12
#define BUF_MK_TW_BULL  13
#define BUF_MK_TW_BEAR  14
#define BUF_ATR         15
#define BUF_THICK       16
#define BUF_TK          17
#define BUF_PC          18
#define BUF_CHK         19
#define BUF_GRADE       20
#define BUF_GRADE_PROJ  21
#define BUF_QUAL_DIR    22
#define BUF_TK_GRADE    23
#define BUF_HTF_POS     24
#define BUF_FLAT_K      25
#define BUF_FLAT_B      26
#define BUF_EV_BITS     27

//--- plot indices (27): 0-4 lines, 5 filling, 6-13 arrows, 14-26 DRAW_NONE
#define PLOT_TENKAN      0
#define PLOT_KIJUN       1
#define PLOT_CHIKOU      2
#define PLOT_SPANA       3
#define PLOT_SPANB       4
#define PLOT_FILL        5
#define PLOT_MK_TK_BULL  6
#define PLOT_MK_TK_BEAR  7
#define PLOT_MK_KU_UP    8
#define PLOT_MK_KU_DN    9
#define PLOT_MK_RAW_BULL 10
#define PLOT_MK_RAW_BEAR 11
#define PLOT_MK_TW_BULL  12
#define PLOT_MK_TW_BEAR  13
#define PLOT_ATR        14
#define PLOT_THICK      15
#define PLOT_TK         16
#define PLOT_PC         17
#define PLOT_CHK        18
#define PLOT_GRADE      19
#define PLOT_GRADE_PROJ 20
#define PLOT_QUAL_DIR   21
#define PLOT_TK_GRADE   22
#define PLOT_HTF_POS    23
#define PLOT_FLAT_K     24
#define PLOT_FLAT_B     25
#define PLOT_EV_BITS    26

//--- event bit flags (bEvBits)
#define EV_TK_BULL   1
#define EV_TK_BEAR   2
#define EV_TK_BULL_Q 4
#define EV_TK_BEAR_Q 8
#define EV_KU_UP    16
#define EV_KU_DN    32
#define EV_KU_UP_Q  64
#define EV_KU_DN_Q 128
#define EV_TW_BULL 256
#define EV_TW_BEAR 512

//--- level states
#define LVL_LIVE      0
#define LVL_TOUCHED   1
#define LVL_EXPIRED   2

//+------------------------------------------------------------------+
//| Indicator buffers                                                 |
//+------------------------------------------------------------------+
double bTenkan[];
double bKijun[];
double bChikou[];
double bSpanA[];
double bSpanB[];
double bFillA[];
double bFillB[];
double bTkBullM[];
double bTkBearM[];
double bKumoUpM[];
double bKumoDnM[];
double bRawBullM[];
double bRawBearM[];
double bTwBullM[];
double bTwBearM[];
double bAtr[];
double bThick[];
double bTkSpread[];
double bPc[];
double bChk[];
double bGrade[];
double bGradeProj[];
double bQualDir[];
double bTkGrade[];
double bHtfPos[];
double bFlatK[];
double bFlatB[];
double bEvBits[];

//+------------------------------------------------------------------+
//| Chart series (as-series copies of the OnCalculate inputs)         |
//+------------------------------------------------------------------+
datetime g_time[];
double   g_open[];
double   g_high[];
double   g_low[];
double   g_close[];

//--- derived configuration (OnInit)
bool     g_useL1;
bool     g_useL2;
bool     g_useL3;
int      g_off;       // displacement - 1
int      g_atrN;
int      g_maxAge;

//--- palette (OnInit)
color    g_bg;
color    g_colTenkan, g_colKijun, g_colSpanA, g_colSpanB, g_colChikou;
color    g_colBull, g_colBear, g_colRaw, g_colTwist;
color    g_colWashUp, g_colWashDn, g_colWashIn;
color    g_cloudUp, g_cloudDn;   // fill bases (blend target for transp)

//--- HTF series (rebuilt when history grows)
ENUM_TIMEFRAMES g_htfTf        = PERIOD_CURRENT;
bool     g_htfActive           = false;
bool     g_htfBuilt            = false;
int      g_htfCount            = 0;
int      g_htfPtr              = 0;
datetime g_htfTime[];
double   g_htfHigh[], g_htfLow[], g_htfClose[], g_htfRawA[], g_htfRawB[];

//+------------------------------------------------------------------+
//| Small helpers                                                     |
//+------------------------------------------------------------------+
bool IsNa(const double v)
  {
   return(v >= EMPTY_VALUE - 0.5 || v <= -EMPTY_VALUE + 0.5);
  }

int SignD(const double v)
  {
   if(v > 0.0) return(1);
   if(v < 0.0) return(-1);
   return(0);
  }

//--- Pine #RRGGBB literal -> MQL5 color (0x00BBGGRR)
color Rgb(const uint rrggbb)
  {
   uint r = (rrggbb >> 16) & 0xFF;
   uint g = (rrggbb >> 8) & 0xFF;
   uint b = (rrggbb) & 0xFF;
   return((color)((b << 16) | (g << 8) | r));
  }

uint ColR(const color c) { return(((uint)c) & 0xFF); }
uint ColG(const color c) { return(((uint)c) >> 8) & 0xFF; }
uint ColB(const color c) { return(((uint)c) >> 16) & 0xFF; }

//--- Pine color.new(base, transp) emulated by blending toward chart bg (D1)
color BlendToBg(const color base, const int transp)
  {
   if(transp <= 0)  return(base);
   if(transp >= 100) return(g_bg);
   double k = transp / 100.0;
   double s = 1.0 - k;
   uint r = (uint)MathRound(ColR(base) * s + ColR(g_bg) * k);
   uint g = (uint)MathRound(ColG(base) * s + ColG(g_bg) * k);
   uint b = (uint)MathRound(ColB(base) * s + ColB(g_bg) * k);
   return((color)(((b & 0xFF) << 16) | ((g & 0xFF) << 8) | (r & 0xFF)));
  }

//--- ta.highest(high, n) / ta.lowest(low, n) midpoint, EMPTY on warm-up
double MidRange(const double &hi[], const double &lo[], const int i, const int n, const int sz)
  {
   if(n < 1 || i < 0 || i + n - 1 >= sz)
      return(EMPTY_VALUE);
   double hh = -DBL_MAX;
   double ll =  DBL_MAX;
   for(int j = i; j < i + n; j++)
     {
      if(hi[j] > hh) hh = hi[j];
      if(lo[j] < ll) ll = lo[j];
     }
   return((hh + ll) / 2.0);
  }

//--- cloud UNDER bar i: span buffers store RAW values, the +g_off forward
//--- displacement is applied by PLOT_SHIFT when drawing; the value shown at
//--- bar i is therefore the span computed g_off bars ago (= Pine senkouA[off]
//--- / "spanAcur")
double DispAt(const double &arr[], const int i, const int sz)
  {
   int j = i + g_off;
   return(j < sz ? arr[j] : EMPTY_VALUE);
  }

//--- true range of bar i (needs close[i+1])
double TrueRangeAt(const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i + 1 >= sz)
      return(EMPTY_VALUE);
   double hl = g_high[i] - g_low[i];
   double hc = MathAbs(g_high[i] - g_close[i + 1]);
   double lc = MathAbs(g_low[i]  - g_close[i + 1]);
   return(MathMax(hl, MathMax(hc, lc)));
  }

//--- ta.crossover / ta.crossunder (0 = current bar, 1 = previous bar)
bool CrossOver(const double a0, const double a1, const double b0, const double b1)
  {
   if(IsNa(a0) || IsNa(a1) || IsNa(b0) || IsNa(b1)) return(false);
   return(a0 > b0 && a1 <= b1);
  }

bool CrossUnder(const double a0, const double a1, const double b0, const double b1)
  {
   if(IsNa(a0) || IsNa(a1) || IsNa(b0) || IsNa(b1)) return(false);
   return(a0 < b0 && a1 >= b1);
  }

//--- forward declarations (MQL5 requires declaration before use)
int    PercentileRank(const int p, const int n);
double CalcAtr(const int i);
void   Percentiles3Proj(const int i, double &r1, double &r2, double &r3);
bool   Qualify(const int bar_dir, const int dir, const bool is_kumo,
               const double pc, const double chk, const int htf_pos);

//--- ta.percentile_nearest_rank x3 over one sorted window (D8: full window required)
void Percentiles3(const double &src[], const int i, const int len,
                  const int p1, const int p2, const int p3,
                  double &r1, double &r2, double &r3)
  {
   r1 = EMPTY_VALUE;
   r2 = EMPTY_VALUE;
   r3 = EMPTY_VALUE;
   int sz = ArraySize(src);
   if(len < 1 || i < 0 || i + len - 1 >= sz)
      return;
   double win[];
   ArrayResize(win, len);
   int n = 0;
   for(int j = i; j <= i + len - 1; j++)
     {
      if(!IsNa(src[j]))
        {
         win[n] = src[j];
         n++;
        }
     }
   if(n < len)                 // guard: every window slot must be valid (D8)
      return;
   ArraySort(win);             // local array: not a series, ascending
   r1 = win[PercentileRank(p1, n) - 1];
   r2 = win[PercentileRank(p2, n) - 1];
   r3 = win[PercentileRank(p3, n) - 1];
  }

int PercentileRank(const int p, const int n)
  {
   int r = (int)MathCeil(p / 100.0 * n);
   if(r < 1) r = 1;
   if(r > n) r = n;
   return(r);
  }

//--- Pine f_grade
int GradeOf(const double x, const double lo, const double mid, const double hi)
  {
   if(IsNa(x) || IsNa(lo) || IsNa(mid) || IsNa(hi)) return(-1);
   if(x >= hi)  return(3);
   if(x >= mid) return(2);
   if(x <= lo)  return(0);
   return(1);
  }

string GradeTxt(const int g)
  {
   if(g == 0)  return("thin");
   if(g == 1)  return("normal");
   if(g == 2)  return("thick");
   if(g == 3)  return("very thick");
   return("n/a");
  }

//--- "PERIOD_H4" -> "H4"
string TfName(const ENUM_TIMEFRAMES tf)
  {
   string s = EnumToString(tf);
   if(StringFind(s, "PERIOD_") == 0)
      return(StringSubstr(s, 7));
   return(s);
  }

//--- Pine input.timeframe "" (auto 4x) -> nearest MT5 timeframe >= 4x (D6)
ENUM_TIMEFRAMES ResolveHtf()
  {
   if(InpHtfPeriod != PERIOD_CURRENT)
      return(InpHtfPeriod);
   long target = 4 * PeriodSeconds(_Period);
   if(target <= 60)     return(PERIOD_M1);
   if(target <= 120)    return(PERIOD_M2);
   if(target <= 180)    return(PERIOD_M3);
   if(target <= 240)    return(PERIOD_M4);
   if(target <= 300)    return(PERIOD_M5);
   if(target <= 360)    return(PERIOD_M6);
   if(target <= 600)    return(PERIOD_M10);
   if(target <= 720)    return(PERIOD_M12);
   if(target <= 900)    return(PERIOD_M15);
   if(target <= 1200)   return(PERIOD_M20);
   if(target <= 1800)   return(PERIOD_M30);
   if(target <= 3600)   return(PERIOD_H1);
   if(target <= 7200)   return(PERIOD_H2);
   if(target <= 10800)  return(PERIOD_H3);
   if(target <= 14400)  return(PERIOD_H4);
   if(target <= 21600)  return(PERIOD_H6);
   if(target <= 28800)  return(PERIOD_H8);
   if(target <= 43200)  return(PERIOD_H12);
   if(target <= 86400)  return(PERIOD_D1);
   if(target <= 604800) return(PERIOD_W1);
   return(PERIOD_MN1);
  }

//+------------------------------------------------------------------+
//| HTF series: build / refresh (Pine request.security replacement)   |
//+------------------------------------------------------------------+
void EnsureHtf()
  {
   ENUM_TIMEFRAMES tf = ResolveHtf();
   g_htfTf = tf;
   g_htfActive = (InpInHtf && PeriodSeconds(tf) > PeriodSeconds(_Period));
   if(!g_htfActive)
     {
      g_htfCount = 0;
      return;
     }
   int sz = ArraySize(g_time);
   int need = (int)(sz * (double)PeriodSeconds(_Period) / (double)PeriodSeconds(tf)) + g_off + 128;
   if(need < 256) need = 256;
   if(g_htfBuilt && g_htfCount >= need)
      return;
   int count = need + need / 4 + 256;
   ArrayResize(g_htfTime, count);
   ArrayResize(g_htfHigh, count);
   ArrayResize(g_htfLow, count);
   ArrayResize(g_htfClose, count);
   ArrayResize(g_htfRawA, count);
   ArrayResize(g_htfRawB, count);
   ArraySetAsSeries(g_htfTime, true);
   ArraySetAsSeries(g_htfHigh, true);
   ArraySetAsSeries(g_htfLow, true);
   ArraySetAsSeries(g_htfClose, true);
   ArraySetAsSeries(g_htfRawA, true);
   ArraySetAsSeries(g_htfRawB, true);
   int ct = CopyTime(_Symbol, tf, 0, count, g_htfTime);
   int ch = CopyHigh(_Symbol, tf, 0, count, g_htfHigh);
   int cl = CopyLow(_Symbol, tf, 0, count, g_htfLow);
   int cc = CopyClose(_Symbol, tf, 0, count, g_htfClose);
   int got = MathMin(MathMin(ct, ch), MathMin(cl, cc));
   if(got <= 0)
     {
      g_htfCount = 0;
      g_htfActive = false;
      return;
     }
   g_htfCount = got;
   for(int h = g_htfCount - 1; h >= 0; h--)
     {
      double t = MidRange(g_htfHigh, g_htfLow, h, InpTenkanLen, g_htfCount);
      double k = MidRange(g_htfHigh, g_htfLow, h, InpKijunLen, g_htfCount);
      double b = MidRange(g_htfHigh, g_htfLow, h, InpSenkouBLen, g_htfCount);
      g_htfRawA[h] = (IsNa(t) || IsNa(k)) ? EMPTY_VALUE : (t + k) / 2.0;
      g_htfRawB[h] = b;
     }
   g_htfBuilt = true;
   g_htfPtr   = g_htfCount - 1;
  }

//--- latest HTF bar with time <= t; evaluate with Pine's extra [1] margin (D7)
int HtfPosAt(const datetime t)
  {
   if(!g_htfActive || g_htfCount == 0)
      return(0);
   int ptr = g_htfPtr;
   if(ptr < 0 || ptr >= g_htfCount)
      ptr = g_htfCount - 1;
   while(ptr > 0 && g_htfTime[ptr - 1] <= t)
      ptr--;
   g_htfPtr = ptr;
   if(g_htfTime[ptr] > t)
      return(0);
   int ha = ptr + 1 + g_off;   // spans: (h - 1 - displacement) in Pine terms
   int hc = ptr + 1;           // close: h - 1
   if(ha >= g_htfCount || hc >= g_htfCount)
      return(0);
   double a = g_htfRawA[ha];
   double b = g_htfRawB[ha];
   double c = g_htfClose[hc];
   if(IsNa(a) || IsNa(b) || IsNa(c))
      return(0);
   double u = a > b ? a : b;
   double l = a < b ? a : b;
   if(c > u) return(1);
   if(c < l) return(-1);
   return(0);
  }

//+------------------------------------------------------------------+
//| Per-bar computation (shift-invariant values; index 0 refreshed    |
//| every tick, other bars computed once - see pine-to-mql5.md §4)    |
//+------------------------------------------------------------------+
void ComputeBar(const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;
   double o = g_open[i];
   double h = g_high[i];
   double l = g_low[i];
   double c = g_close[i];
   bool   has_prev = (i + 1 < sz);

   //--- Layer 0: five lines -----------------------------------------------
   bTenkan[i] = MidRange(g_high, g_low, i, InpTenkanLen, sz);
   bKijun[i]  = MidRange(g_high, g_low, i, InpKijunLen, sz);
   //--- Senkou spans stored RAW; the +g_off forward displacement (Pine
   //--- offset = displacement - 1) is applied by PLOT_SHIFT on the line and
   //--- fill plots - the exact pattern of the official Indicators/Examples/
   //--- Ichimoku.mq5. This is what extends the cloud g_off bars BEYOND the
   //--- last bar; a value-remap alone only reproduces the in-chart alignment.
   bSpanA[i]  = (IsNa(bTenkan[i]) || IsNa(bKijun[i])) ? EMPTY_VALUE : (bTenkan[i] + bKijun[i]) / 2.0;
   bSpanB[i]  = MidRange(g_high, g_low, i, InpSenkouBLen, sz);

   //--- ATR (Wilder RMA, SMA-seeded - NOT iATR) ---------------------------
   bAtr[i] = CalcAtr(i);

   //--- displaced spans + chikou ------------------------------------------
   bFillA[i]  = bSpanA[i];
   bFillB[i]  = bSpanB[i];
   //--- chikou stored RAW too; drawn with a NEGATIVE PLOT_SHIFT, exactly
   //--- like Indicators/Examples/Ichimoku.mq5 (Pine offset = -g_off) -------
   bChikou[i] = g_close[i];

   //--- Layer 1: normalised geometry --------------------------------------
   double A        = bAtr[i];
   bool   atr_ok   = (!IsNa(A) && A > 0.0);
   double dispA    = DispAt(bSpanA, i, sz);
   double dispB    = DispAt(bSpanB, i, sz);
   bool   span_ok  = (!IsNa(dispA) && !IsNa(dispB));
   bool   geo_ok   = (span_ok && atr_ok);
   double upper    = span_ok ? MathMax(dispA, dispB) : EMPTY_VALUE;
   double lower    = span_ok ? MathMin(dispA, dispB) : EMPTY_VALUE;

   bThick[i] = geo_ok ? MathAbs(dispA - dispB) / A : EMPTY_VALUE;
   bTkSpread[i] = (!IsNa(bTenkan[i]) && !IsNa(bKijun[i]) && atr_ok)
                  ? (bTenkan[i] - bKijun[i]) / A : EMPTY_VALUE;
   bPc[i] = geo_ok ? (c > upper ? (c - upper) / A : (c < lower ? (c - lower) / A : 0.0))
                   : EMPTY_VALUE;
   bChk[i] = (atr_ok && i + g_off < sz)
             ? (c - g_close[i + g_off]) / A : EMPTY_VALUE;
   double thick_proj = (atr_ok && !IsNa(bSpanA[i]) && !IsNa(bSpanB[i]))
                       ? MathAbs(bSpanA[i] - bSpanB[i]) / A : EMPTY_VALUE;

   //--- percentile grades (bar_index >= pctLen, else -1) -------------------
   int    bar_index = sz - 1 - i;
   bool   pct_ready = (g_useL1 && bar_index >= InpPctLen);
   if(pct_ready)
     {
      double p1, p2, p3, q1, q2, q3;
      Percentiles3(bThick, i, InpPctLen, InpPctThin, InpPctThk, InpPctVThk, p1, p2, p3);
      Percentiles3Proj(i, q1, q2, q3);
      bGrade[i]     = (double)GradeOf(bThick[i], p1, p2, p3);
      bGradeProj[i] = (double)GradeOf(thick_proj, q1, q2, q3);
     }
   else
     {
      bGrade[i]     = -1.0;
      bGradeProj[i] = -1.0;
     }

   //--- Layer 2: raw events ------------------------------------------------
   int cloud_pos = span_ok ? (c > upper ? 1 : (c < lower ? -1 : 0)) : 0;
   bool tk_bull = false, tk_bear = false;
   bool ku_up   = false, ku_dn   = false;
   bool tw_bull = false, tw_bear = false;
   if(has_prev)
     {
      tk_bull = CrossOver(bTenkan[i], bTenkan[i + 1], bKijun[i], bKijun[i + 1]);
      tk_bear = CrossUnder(bTenkan[i], bTenkan[i + 1], bKijun[i], bKijun[i + 1]);
      tw_bull = CrossOver(bSpanA[i], bSpanA[i + 1], bSpanB[i], bSpanB[i + 1]);
      tw_bear = CrossUnder(bSpanA[i], bSpanA[i + 1], bSpanB[i], bSpanB[i + 1]);
      double pA1 = DispAt(bSpanA, i + 1, sz);
      double pB1 = DispAt(bSpanB, i + 1, sz);
      if(span_ok && !IsNa(pA1) && !IsNa(pB1))
        {
         double p_up = MathMax(pA1, pB1);
         double p_dn = MathMin(pA1, pB1);
         ku_up = (c > upper && g_close[i + 1] <= p_up);
         ku_dn = (c < lower && g_close[i + 1] >= p_dn);
        }
     }
   //--- classic grade of a TK cross (strong / neutral / weak by cloud) -----
   int tk_grade = -1;
   if(tk_bull)
      tk_grade = (cloud_pos > 0 ? 2 : (cloud_pos == 0 ? 1 : 0));
   else if(tk_bear)
      tk_grade = (cloud_pos < 0 ? 2 : (cloud_pos == 0 ? 1 : 0));
   bTkGrade[i] = (double)tk_grade;

   //--- qualification ------------------------------------------------------
   int    htf_pos = HtfPosAt(g_time[i]);
   bHtfPos[i] = (double)htf_pos;
   int    bar_dir = SignD(c - o);
   bool   q_bull = Qualify(bar_dir, 1, false, bPc[i], bChk[i], htf_pos);
   bool   q_bear = Qualify(bar_dir, -1, false, bPc[i], bChk[i], htf_pos);
   bool   q_up   = Qualify(bar_dir, 1, true,  bPc[i], bChk[i], htf_pos);
   bool   q_dn   = Qualify(bar_dir, -1, true,  bPc[i], bChk[i], htf_pos);
   bool   tk_bull_q = tk_bull && (!g_useL2 || q_bull);
   bool   tk_bear_q = tk_bear && (!g_useL2 || q_bear);
   bool   ku_up_q   = ku_up   && (!g_useL2 || q_up);
   bool   ku_dn_q   = ku_dn   && (!g_useL2 || q_dn);
   int    qual_dir  = (tk_bull_q || ku_up_q) ? 1 : ((tk_bear_q || ku_dn_q) ? -1 : 0);
   bQualDir[i] = (double)qual_dir;

   //--- markers (plotshape replacement) ------------------------------------
   bool mk = (InpShowMarkers && !InpClassicMode);
   bTkBullM[i]   = (mk && tk_bull_q)    ? l : EMPTY_VALUE;
   bTkBearM[i]   = (mk && tk_bear_q)    ? h : EMPTY_VALUE;
   bKumoUpM[i]   = (mk && ku_up_q)      ? l : EMPTY_VALUE;
   bKumoDnM[i]   = (mk && ku_dn_q)      ? h : EMPTY_VALUE;
   bRawBullM[i]  = (mk && InpShowRaw && g_useL2 && ((tk_bull && !tk_bull_q) || (ku_up && !ku_up_q))) ? l : EMPTY_VALUE;
   bRawBearM[i]  = (mk && InpShowRaw && g_useL2 && ((tk_bear && !tk_bear_q) || (ku_dn && !ku_dn_q))) ? h : EMPTY_VALUE;
   bTwBullM[i]   = (mk && tw_bull)      ? l : EMPTY_VALUE;
   bTwBearM[i]   = (mk && tw_bear)      ? h : EMPTY_VALUE;

   //--- packed event flags (for the closed-bar state machine) --------------
   int ev = 0;
   if(tk_bull)   ev |= EV_TK_BULL;
   if(tk_bear)   ev |= EV_TK_BEAR;
   if(tk_bull_q) ev |= EV_TK_BULL_Q;
   if(tk_bear_q) ev |= EV_TK_BEAR_Q;
   if(ku_up)     ev |= EV_KU_UP;
   if(ku_dn)     ev |= EV_KU_DN;
   if(ku_up_q)   ev |= EV_KU_UP_Q;
   if(ku_dn_q)   ev |= EV_KU_DN_Q;
   if(tw_bull)   ev |= EV_TW_BULL;
   if(tw_bear)   ev |= EV_TW_BEAR;
   bEvBits[i] = (double)ev;

   //--- Layer 3: flat-run lengths ------------------------------------------
   int fk = 1;
   int fb = 1;
   if(has_prev && !IsNa(bKijun[i]) && !IsNa(bKijun[i + 1]) && bKijun[i] == bKijun[i + 1])
      fk = (IsNa(bFlatK[i + 1]) ? 0 : (int)MathRound(bFlatK[i + 1])) + 1;
   if(has_prev && !IsNa(bSpanB[i]) && !IsNa(bSpanB[i + 1]) && bSpanB[i] == bSpanB[i + 1])
      fb = (IsNa(bFlatB[i + 1]) ? 0 : (int)MathRound(bFlatB[i + 1])) + 1;
   bFlatK[i] = (double)fk;
   bFlatB[i] = (double)fb;
  }

//--- ATR for bar i: SMA seed at the oldest computable bar, RMA elsewhere
double CalcAtr(const int i)
  {
   int sz = ArraySize(g_time);
   int n  = g_atrN;
   if(n < 1)
      return(EMPTY_VALUE);
   int seed = sz - 1 - n;
   if(seed < 0)
      return(EMPTY_VALUE);
   if(i > seed)
      return(EMPTY_VALUE);
   if(i == seed)
     {
      double sum = 0.0;
      for(int j = i; j < i + n; j++)
        {
         double tr = TrueRangeAt(j);
         if(IsNa(tr))
            return(EMPTY_VALUE);
         sum += tr;
        }
      return(sum / n);
     }
   double prev = bAtr[i + 1];
   double tr   = TrueRangeAt(i);
   if(IsNa(prev) || IsNa(tr))
      return(EMPTY_VALUE);
   return((prev * (n - 1) + tr) / n);
  }

//--- percentiles of the projected-thickness series (needs its own window)
void Percentiles3Proj(const int i, double &r1, double &r2, double &r3)
  {
   r1 = EMPTY_VALUE;
   r2 = EMPTY_VALUE;
   r3 = EMPTY_VALUE;
   int sz = ArraySize(g_time);
   int len = InpPctLen;
   if(len < 1 || i < 0 || i + len - 1 >= sz)
      return;
   double win[];
   ArrayResize(win, len);
   int n = 0;
   for(int j = i; j <= i + len - 1; j++)
     {
      if(j >= 0 && j < sz && !IsNa(bAtr[j]) && bAtr[j] > 0.0 && !IsNa(bSpanA[j]) && !IsNa(bSpanB[j]))
        {
         win[n] = MathAbs(bSpanA[j] - bSpanB[j]) / bAtr[j];
         n++;
        }
     }
   if(n < len)
      return;
   ArraySort(win);
   r1 = win[PercentileRank(InpPctThin, n) - 1];
   r2 = win[PercentileRank(InpPctThk, n) - 1];
   r3 = win[PercentileRank(InpPctVThk, n) - 1];
  }

//--- Pine f_qual
bool Qualify(const int bar_dir, const int dir, const bool is_kumo,
             const double pc, const double chk, const int htf_pos)
  {
   bool ok_dir = (bar_dir == dir);
   bool ok_pc  = is_kumo ? (!IsNa(pc) && MathAbs(pc) >= InpPcMin)
                         : (!IsNa(pc) && pc != 0.0);
   bool ok_chk = (!IsNa(chk) && SignD(chk) == dir && MathAbs(chk) >= InpChkMin);
   bool ok_htf = (!InpUseHtfFilt || (g_htfActive && htf_pos == dir));
   return(ok_dir && ok_pc && ok_chk && ok_htf);
  }

//+------------------------------------------------------------------+
//| Stateful engine: var-state of the Pine script (layers 3+4,        |
//| running counters, alerts, labels/table). Runs exactly once per    |
//| closed bar, in chronological order.                               |
//+------------------------------------------------------------------+
class CIchimokuEngine
  {
private:
   //--- flat-level objects (Pine array<line> + counters)
   string   m_lvl_name[];
   double   m_lvl_val[];
   int      m_lvl_kind[];
   int      m_lvl_state[];
   int      m_lvl_seq[];
   int      m_serial;
   int      m_bar_seq;
   datetime m_last_time;
   bool     m_tbl_made;
   //--- running stats (Pine var counters)
   int      m_n_tk_raw, m_n_tk_q, m_n_ku_raw, m_n_ku_q, m_n_tw;
   int      m_n_scored1, m_n_hit1, m_n_scored2, m_n_hit2;
   double   m_sum_fwd_all, m_sum_fwd_ev;
   int      m_n_fwd_all, m_n_fwd_ev;
   int      m_n_lvl_k, m_n_lvl_b, m_n_touch_k, m_n_touch_b;

   void     AddLevel(const double lvl, const int seg, const int kind, const int i);
   void     SetCell(const int col, const int row, const string txt, const color clr);
   void     KillTable();
   void     UpdateGradeLabel();
   void     UpdateHtfLabel();

public:
             CIchimokuEngine() : m_serial(0), m_bar_seq(0), m_last_time(0), m_tbl_made(false) {}
            ~CIchimokuEngine() {}

   void     Reset();
   void     ProcessBar(const int i, const bool allow_alert);
   void     UpdateLabels();
  };

//+------------------------------------------------------------------+
void CIchimokuEngine::Reset()
  {
   ArrayFree(m_lvl_name);
   ArrayFree(m_lvl_val);
   ArrayFree(m_lvl_kind);
   ArrayFree(m_lvl_state);
   ArrayFree(m_lvl_seq);
   m_serial   = 0;
   m_bar_seq  = 0;
   m_last_time = 0;
   m_tbl_made = false;
   m_n_tk_raw = m_n_tk_q = m_n_ku_raw = m_n_ku_q = m_n_tw = 0;
   m_n_scored1 = m_n_hit1 = m_n_scored2 = m_n_hit2 = 0;
   m_sum_fwd_all = 0.0;
   m_sum_fwd_ev  = 0.0;
   m_n_fwd_all = m_n_fwd_ev = 0;
   m_n_lvl_k = m_n_lvl_b = m_n_touch_k = m_n_touch_b = 0;
   ObjectsDeleteAll(0, "MIC_");
  }

//+------------------------------------------------------------------+
//| One closed bar: level objects + running counters + alerts          |
//+------------------------------------------------------------------+
void CIchimokuEngine::ProcessBar(const int i, const bool allow_alert)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;
   datetime t = g_time[i];
   if(t <= m_last_time)            // idempotence guard (pine-to-mql5.md §4.2)
      return;
   m_last_time = t;
   m_bar_seq++;
   bool flat_touch = false;

   //--- Layer 3: live levels (touch -> expire -> extend), then new levels ---
   if(g_useL3)
     {
      bool atr_ok = !IsNa(bAtr[i]);
      double tol  = InpTouchTol * (atr_ok ? bAtr[i] : 0.0);
      int n = ArraySize(m_lvl_val);
      for(int idx = 0; idx < n; idx++)
        {
         if(m_lvl_state[idx] != LVL_LIVE)
            continue;
         double lvl = m_lvl_val[idx];
         color  base = (m_lvl_kind[idx] == 0) ? g_colKijun : g_colSpanB;
         bool touched = (atr_ok && g_low[i] - tol <= lvl && lvl <= g_high[i] + tol);
         if(touched)
           {
            m_lvl_state[idx] = LVL_TOUCHED;
            ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_TIME, 1, t);
            ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_COLOR, base);
            flat_touch = true;
            if(m_lvl_kind[idx] == 0) m_n_touch_k++;
            else                     m_n_touch_b++;
           }
         else if(m_bar_seq - m_lvl_seq[idx] >= g_maxAge)
           {
            m_lvl_state[idx] = LVL_EXPIRED;
            ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_TIME, 1, t);
            ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_STYLE, STYLE_DOT);
            if(InpHideExpired)
               ObjectDelete(0, m_lvl_name[idx]);
            else
               ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_COLOR, BlendToBg(base, 80));
           }
         else
           {
            ObjectSetInteger(0, m_lvl_name[idx], OBJPROP_TIME, 1, t);
           }
        }
      //--- new levels on the first bar the line moves after a flat run
      if(i + 1 < sz)
        {
         if(!IsNa(bKijun[i]) && !IsNa(bKijun[i + 1]) && bKijun[i] != bKijun[i + 1] &&
            !IsNa(bFlatK[i + 1]) && bFlatK[i + 1] >= InpFlatMinK)
           {
            AddLevel(bKijun[i + 1], (int)MathRound(bFlatK[i + 1]), 0, i);
            m_n_lvl_k++;
           }
         if(!IsNa(bSpanB[i]) && !IsNa(bSpanB[i + 1]) && bSpanB[i] != bSpanB[i + 1] &&
            !IsNa(bFlatB[i + 1]) && bFlatB[i + 1] >= InpFlatMinB)
           {
            AddLevel(bSpanB[i + 1], (int)MathRound(bFlatB[i + 1]), 1, i);
            m_n_lvl_b++;
           }
        }
     }

   //--- Layer 4b: running counters (scored H bars after each event) --------
   int ev = IsNa(bEvBits[i]) ? 0 : (int)MathRound(bEvBits[i]);
   bool tk_bull   = (ev & EV_TK_BULL)   != 0;
   bool tk_bear   = (ev & EV_TK_BEAR)   != 0;
   bool tk_bull_q = (ev & EV_TK_BULL_Q) != 0;
   bool tk_bear_q = (ev & EV_TK_BEAR_Q) != 0;
   bool ku_up     = (ev & EV_KU_UP)     != 0;
   bool ku_dn     = (ev & EV_KU_DN)     != 0;
   bool ku_up_q   = (ev & EV_KU_UP_Q)   != 0;
   bool ku_dn_q   = (ev & EV_KU_DN_Q)   != 0;
   bool tw_bull   = (ev & EV_TW_BULL)   != 0;
   bool tw_bear   = (ev & EV_TW_BEAR)   != 0;

   if(tk_bull || tk_bear)      m_n_tk_raw++;
   if(tk_bull_q || tk_bear_q)  m_n_tk_q++;
   if(ku_up || ku_dn)          m_n_ku_raw++;
   if(ku_up_q || ku_dn_q)      m_n_ku_q++;
   if(tw_bull || tw_bear)      m_n_tw++;

   int bar_index = sz - 1 - i;
   int h1 = InpDisplacement;
   int h2 = InpStatsH2;
   if(bar_index >= h1 && i + h1 < sz)
     {
      int d1 = IsNa(bQualDir[i + h1]) ? 0 : (int)MathRound(bQualDir[i + h1]);
      if(d1 != 0)
        {
         m_n_scored1++;
         if(SignD(g_close[i] - g_close[i + h1]) == d1)
            m_n_hit1++;
        }
      double atr1 = bAtr[i + h1];
      double fwd  = EMPTY_VALUE;
      if(!IsNa(atr1) && atr1 != 0.0)
        {
         double hh = EMPTY_VALUE, ll = EMPTY_VALUE;
         if(i + h1 - 1 < sz)
           {
            hh = g_high[i];
            ll = g_low[i];
            for(int j = i + 1; j <= i + h1 - 1; j++)
              {
               if(g_high[j] > hh) hh = g_high[j];
               if(g_low[j]  < ll) ll  = g_low[j];
              }
            fwd = (hh - ll) / atr1;
           }
        }
      if(!IsNa(fwd))
        {
         m_sum_fwd_all += fwd;
         m_n_fwd_all++;
         if(d1 != 0)
           {
            m_sum_fwd_ev += fwd;
            m_n_fwd_ev++;
           }
        }
     }
   if(bar_index >= h2 && i + h2 < sz)
     {
      int d2 = IsNa(bQualDir[i + h2]) ? 0 : (int)MathRound(bQualDir[i + h2]);
      if(d2 != 0)
        {
         m_n_scored2++;
         if(SignD(g_close[i] - g_close[i + h2]) == d2)
            m_n_hit2++;
        }
     }

   //--- Alerts: confirmed bars only, realtime only (D9) --------------------
   if(allow_alert && InpEnableAlerts)
     {
      string base = "MKumo " + _Symbol + " " + TfName(_Period) + ": ";
      string g    = IntegerToString((int)MathRound(bGrade[i]));
      if(tk_bull_q) Alert(base + "qualified TK cross BULL, grade " + g);
      if(tk_bear_q) Alert(base + "qualified TK cross BEAR, grade " + g);
      if(ku_up_q)   Alert(base + "qualified Kumo breakout UP, grade " + g);
      if(ku_dn_q)   Alert(base + "qualified Kumo breakout DOWN, grade " + g);
      if(tw_bull)   Alert(base + "Kumo twist BULL (projected cloud)");
      if(tw_bear)   Alert(base + "Kumo twist BEAR (projected cloud)");
      if(flat_touch && g_useL3) Alert(base + "flat level touched");
     }
  }

//+------------------------------------------------------------------+
//| Create one flat level as an OBJ_TREND (FIFO capped)                |
//+------------------------------------------------------------------+
void CIchimokuEngine::AddLevel(const double lvl, const int seg, const int kind, const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;
   int cnt = ArraySize(m_lvl_val);
   if(cnt >= InpMaxLevels)
     {
      ObjectDelete(0, m_lvl_name[0]);
      ArrayRemove(m_lvl_name, 0, 1);
      ArrayRemove(m_lvl_val, 0, 1);
      ArrayRemove(m_lvl_kind, 0, 1);
      ArrayRemove(m_lvl_state, 0, 1);
      ArrayRemove(m_lvl_seq, 0, 1);
      cnt--;
     }
   int i1 = i + seg;
   if(i1 > sz - 1) i1 = sz - 1;
   string name = "MIC_lvl" + IntegerToString(m_serial++);
   color  base = (kind == 0) ? g_colKijun : g_colSpanB;
   int    flat_min = (kind == 0) ? InpFlatMinK : InpFlatMinB;
   int    width = (seg >= 2 * flat_min) ? 2 : 1;
   if(!ObjectCreate(0, name, OBJ_TREND, 0, g_time[i1], lvl, g_time[i], lvl))
      return;
   ObjectSetInteger(0, name, OBJPROP_COLOR,      BlendToBg(base, 15));
   ObjectSetInteger(0, name, OBJPROP_STYLE,      STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_WIDTH,      width);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT,   false);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT,  false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN,     true);
   ObjectSetInteger(0, name, OBJPROP_BACK,       false);
   int cnt2 = ArraySize(m_lvl_val);
   ArrayResize(m_lvl_name, cnt2 + 1);
   ArrayResize(m_lvl_val,  cnt2 + 1);
   ArrayResize(m_lvl_kind, cnt2 + 1);
   ArrayResize(m_lvl_state, cnt2 + 1);
   ArrayResize(m_lvl_seq,  cnt2 + 1);
   m_lvl_name[cnt2]  = name;
   m_lvl_val[cnt2]   = lvl;
   m_lvl_kind[cnt2]  = kind;
   m_lvl_state[cnt2] = LVL_LIVE;
   m_lvl_seq[cnt2]   = m_bar_seq;
  }

//+------------------------------------------------------------------+
//| Per-tick overlays: grade label, HTF readout, stats table            |
//+------------------------------------------------------------------+
void CIchimokuEngine::UpdateLabels()
  {
   UpdateGradeLabel();
   UpdateHtfLabel();

   if(InpShowTable && !m_tbl_made)
      m_tbl_made = true;
   if(!InpShowTable && m_tbl_made)
     {
      KillTable();
      m_tbl_made = false;
     }
   if(!m_tbl_made)
      return;

   int h1 = InpDisplacement;
   int h2 = InpStatsH2;
   color col_dim = BlendToBg(clrWhite, 40);
   color col_val = clrWhite;
   string hit1 = "-";
   string hit2 = "-";
   if(m_n_scored1 > 0)
     {
      double v = 100.0 * m_n_hit1 / m_n_scored1;
      hit1 = DoubleToString(v, 1) + "% (" + IntegerToString(m_n_scored1) + ")";
      col_val = (v >= 50.0) ? g_colBull : clrWhite;
     }
   color col_h1 = col_val;
   color col_h2 = col_dim;
   if(m_n_scored1 == 0) col_h1 = col_dim;
   if(m_n_scored2 > 0)
     {
      double v = 100.0 * m_n_hit2 / m_n_scored2;
      hit2 = DoubleToString(v, 1) + "% (" + IntegerToString(m_n_scored2) + ")";
      col_h2 = (v >= 50.0) ? g_colBull : clrWhite;
     }
   else
      col_h2 = col_dim;

   string rng = "-";
   if(m_n_fwd_ev > 0 && m_n_fwd_all > 0 && m_sum_fwd_all > 0.0)
      rng = DoubleToString((m_sum_fwd_ev / m_n_fwd_ev) / (m_sum_fwd_all / m_n_fwd_all), 2) + "x";

   //--- expired = created - touched - still live (per kind)
   int live_k = 0, live_b = 0;
   int n = ArraySize(m_lvl_val);
   for(int idx = 0; idx < n; idx++)
     {
      if(m_lvl_state[idx] != LVL_LIVE)
         continue;
      if(m_lvl_kind[idx] == 0) live_k++;
      else                     live_b++;
     }
   int exp_k = MathMax(m_n_lvl_k - m_n_touch_k - live_k, 0);
   int exp_b = MathMax(m_n_lvl_b - m_n_touch_b - live_b, 0);
   int retired = m_n_touch_k + m_n_touch_b + exp_k + exp_b;
   string touch = "-";
   if(retired > 0)
      touch = DoubleToString(100.0 * (m_n_touch_k + m_n_touch_b) / retired, 1) + "%";

   string q_lbl = g_useL2 ? "qualified" : "raw";
   SetCell(0, 0, "Hit rate @" + IntegerToString(h1) + " (" + q_lbl + ")", col_dim);
   SetCell(1, 0, hit1, col_h1);
   SetCell(0, 1, "Hit rate @" + IntegerToString(h2), col_dim);
   SetCell(1, 1, hit2, col_h2);
   SetCell(0, 2, "Range multiple @" + IntegerToString(h1), col_dim);
   SetCell(1, 2, rng, col_dim);
   SetCell(0, 3, "Touch rate (retired levels)", col_dim);
   SetCell(1, 3, touch, col_dim);

   string htf_txt = "off";
   color  htf_col = col_dim;
   if(g_htfActive)
     {
      int p = (int)MathRound(bHtfPos[0]);
      htf_txt = (p > 0 ? "above cloud" : (p < 0 ? "below cloud" : "inside cloud"));
      htf_col = (p > 0 ? g_colWashUp : (p < 0 ? g_colWashDn : g_colWashIn));
     }
   SetCell(0, 4, "HTF " + TfName(g_htfTf), col_dim);
   SetCell(1, 4, htf_txt, htf_col);

   if(InpTableExpanded)
     {
      SetCell(0, 5,  "TK cross raw / " + q_lbl, col_dim);
      SetCell(1, 5,  IntegerToString(m_n_tk_raw) + " / " + IntegerToString(m_n_tk_q), col_dim);
      SetCell(0, 6,  "Kumo break raw / " + q_lbl, col_dim);
      SetCell(1, 6,  IntegerToString(m_n_ku_raw) + " / " + IntegerToString(m_n_ku_q), col_dim);
      SetCell(0, 7,  "Twists", col_dim);
      SetCell(1, 7,  IntegerToString(m_n_tw), col_dim);
      SetCell(0, 8,  "Kijun levels created / touched / expired", col_dim);
      SetCell(1, 8,  IntegerToString(m_n_lvl_k) + " / " + IntegerToString(m_n_touch_k) + " / " + IntegerToString(exp_k), col_dim);
      SetCell(0, 9,  "Senkou B levels created / touched / expired", col_dim);
      SetCell(1, 9,  IntegerToString(m_n_lvl_b) + " / " + IntegerToString(m_n_touch_b) + " / " + IntegerToString(exp_b), col_dim);
     }
  }

//+------------------------------------------------------------------+
//| Grade label on the last bar (Pine label -> OBJ_TEXT, D5)           |
//+------------------------------------------------------------------+
void CIchimokuEngine::UpdateGradeLabel()
  {
   bool want = (g_useL1 && InpShowGradeLabel);
   int found = ObjectFind(0, "MIC_grade");
   if(!want)
     {
      if(found >= 0) ObjectDelete(0, "MIC_grade");
      return;
     }
   int sz = ArraySize(g_time);
   if(sz < 1)
      return;
   double anchor = g_close[0];
   double dA0 = DispAt(bSpanA, 0, sz);
   double dB0 = DispAt(bSpanB, 0, sz);
   if(!IsNa(dA0) && !IsNa(dB0))
      anchor = MathMax(dA0, dB0);
   string txt = "Kumo " + GradeTxt((int)MathRound(bGrade[0]));
   if(!IsNa(bThick[0]))
      txt += " (" + DoubleToString(bThick[0], 2) + " ATR)";
   if(!IsNa(bPc[0]))
      txt += "  ·  price " + DoubleToString(bPc[0], 2) + " ATR from cloud";
   if(!IsNa(bChk[0]))
      txt += "  ·  chikou " + DoubleToString(bChk[0], 2) + " ATR";
   if(found < 0)
     {
      if(!ObjectCreate(0, "MIC_grade", OBJ_TEXT, 0, g_time[0], anchor))
         return;
      ObjectSetInteger(0, "MIC_grade", OBJPROP_FONTSIZE, 9);
      ObjectSetString(0, "MIC_grade", OBJPROP_FONT, "Arial");
      ObjectSetInteger(0, "MIC_grade", OBJPROP_COLOR, BlendToBg(clrWhite, 20));
      ObjectSetInteger(0, "MIC_grade", OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, "MIC_grade", OBJPROP_HIDDEN, true);
     }
   ObjectSetInteger(0, "MIC_grade", OBJPROP_TIME,  g_time[0]);
   ObjectSetDouble(0, "MIC_grade", OBJPROP_PRICE, anchor);
   ObjectSetString(0, "MIC_grade", OBJPROP_TEXT, txt);
  }

//+------------------------------------------------------------------+
//| HTF corner readout (replaces Pine bgcolor wash, D2)                |
//+------------------------------------------------------------------+
void CIchimokuEngine::UpdateHtfLabel()
  {
   int found = ObjectFind(0, "MIC_htf");
   if(!InpInHtf)
     {
      if(found >= 0) ObjectDelete(0, "MIC_htf");
      return;
     }
   string txt;
   color  clr;
   if(!g_htfActive)
     {
      txt = "HTF wash off: " + TfName(g_htfTf) + " is not above the chart timeframe";
      clr = BlendToBg(clrWhite, 55);
     }
   else
     {
      int p = (int)MathRound(bHtfPos[0]);
      txt = "HTF " + TfName(g_htfTf) + (p > 0 ? ": above cloud" : (p < 0 ? ": below cloud" : ": inside cloud"));
      clr = (p > 0 ? g_colWashUp : (p < 0 ? g_colWashDn : g_colWashIn));
     }
   if(found < 0)
     {
      if(!ObjectCreate(0, "MIC_htf", OBJ_LABEL, 0, 0, 0))
         return;
      ObjectSetInteger(0, "MIC_htf", OBJPROP_CORNER, CORNER_RIGHT_UPPER);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_XDISTANCE, 10);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_YDISTANCE, 4);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_FONTSIZE, 9);
      ObjectSetString(0, "MIC_htf", OBJPROP_FONT, "Arial");
      ObjectSetInteger(0, "MIC_htf", OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_HIDDEN, true);
      ObjectSetInteger(0, "MIC_htf", OBJPROP_BACK, false);
     }
   ObjectSetString(0, "MIC_htf", OBJPROP_TEXT, txt);
   ObjectSetInteger(0, "MIC_htf", OBJPROP_COLOR, clr);
  }

//+------------------------------------------------------------------+
//| One stats-table cell (Pine table -> OBJ_LABEL grid, D5)            |
//+------------------------------------------------------------------+
void CIchimokuEngine::SetCell(const int col, const int row, const string txt, const color clr)
  {
   string name = "MIC_tbl" + IntegerToString(row * 2 + col);
   if(ObjectFind(0, name) < 0)
     {
      if(!ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0))
         return;
      ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_RIGHT_UPPER);
      ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER);
      ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
      ObjectSetString(0, name, OBJPROP_FONT, "Arial");
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
      ObjectSetInteger(0, name, OBJPROP_BACK, false);
      ObjectSetInteger(0, name, OBJPROP_XDISTANCE, (col == 1) ? 10 : 170);
      ObjectSetInteger(0, name, OBJPROP_YDISTANCE, 24 + row * 14);
     }
   ObjectSetString(0, name, OBJPROP_TEXT, txt);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
  }

//+------------------------------------------------------------------+
void CIchimokuEngine::KillTable()
  {
   for(int row = 0; row < 10; row++)
     {
      ObjectDelete(0, "MIC_tbl" + IntegerToString(row * 2));
      ObjectDelete(0, "MIC_tbl" + IntegerToString(row * 2 + 1));
     }
  }

//--- the one engine instance
CIchimokuEngine g_engine;

//+------------------------------------------------------------------+
//| Plot setup helpers                                                 |
//+------------------------------------------------------------------+
void SetupLinePlot(const int p, const color c, const int w, const string label)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_LINE);
   PlotIndexSetInteger(p, PLOT_LINE_COLOR, c);
   PlotIndexSetInteger(p, PLOT_LINE_WIDTH, w);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
  }

void SetupArrowPlot(const int p, const int code, const int shift_px, const int w,
                    const color c, const string label)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_ARROW);
   PlotIndexSetInteger(p, PLOT_ARROW, (uchar)code);
   PlotIndexSetInteger(p, PLOT_ARROW_SHIFT, shift_px);
   PlotIndexSetInteger(p, PLOT_LINE_WIDTH, w);
   PlotIndexSetInteger(p, PLOT_LINE_COLOR, c);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
  }

void SetupNonePlot(const int p, const string label)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_NONE);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
  }

//+------------------------------------------------------------------+
//| Palette (Pine ternaries, literal colors in Pine #RRGGBB)           |
//+------------------------------------------------------------------+
void SetupPalette()
  {
   long res = 0;
   ChartGetInteger(0, CHART_COLOR_BACKGROUND, 0, res);
   g_bg = (color)(res & 0xFFFFFF);
   double lum = (0.299 * ColR(g_bg) + 0.587 * ColG(g_bg) + 0.114 * ColB(g_bg)) / 255.0;
   bool light = (InpTheme == THEME_LIGHT || (InpTheme == THEME_AUTO && lum > 0.5));
   bool mono  = (InpPalette == PALETTE_MONO);
   bool classic = (InpPalette == PALETTE_CLASSIC);

   g_colTenkan = classic ? Rgb(0x2962FF) : (mono ? (light ? Rgb(0x424242) : Rgb(0xE0E0E0))
                                                 : (light ? Rgb(0x0D9488) : Rgb(0x2DD4BF)));
   g_colKijun  = classic ? Rgb(0xB71C1C) : (mono ? (light ? Rgb(0x757575) : Rgb(0x9E9E9E))
                                                 : (light ? Rgb(0xB45309) : Rgb(0xFFB020)));
   g_colSpanA  = classic ? Rgb(0xA5D6A7) : (mono ? (light ? Rgb(0x616161) : Rgb(0xBDBDBD))
                                                 : (light ? Rgb(0xB8860B) : Rgb(0xFFD60A)));
   g_colSpanB  = classic ? Rgb(0xEF9A9A) : (mono ? (light ? Rgb(0x9E9E9E) : Rgb(0x757575))
                                                 : (light ? Rgb(0xD92507) : Rgb(0xFF3814)));
   g_colChikou = classic ? Rgb(0x43A047) : (mono ? (light ? Rgb(0x212121) : Rgb(0xFFFFFF))
                                                 : (light ? Rgb(0x1D6FB8) : Rgb(0x94D2FF)));
   g_colBull   = classic ? Rgb(0x43A047) : (mono ? (light ? Rgb(0x212121) : Rgb(0xFFFFFF))
                                                 : (light ? Rgb(0xA16207) : Rgb(0xFFD60A)));
   g_colBear   = classic ? Rgb(0xF44336) : (mono ? (light ? Rgb(0x9E9E9E) : Rgb(0xBDBDBD))
                                                 : (light ? Rgb(0xCC2000) : Rgb(0xFF3814)));
   g_colRaw    = BlendToBg(Rgb(0x9E9E9E), 55);
   g_colTwist  = mono   ? (light ? Rgb(0x424242) : Rgb(0xE0E0E0))
                        : (light ? Rgb(0xD6336C) : Rgb(0xFF8FAB));
   g_colWashUp = mono ? Rgb(0x9E9E9E) : (light ? Rgb(0xB8860B) : Rgb(0xFFD60A));
   g_colWashDn = mono ? Rgb(0x616161) : (light ? Rgb(0xD92507) : Rgb(0xFF3814));
   g_colWashIn = mono ? Rgb(0x757575) : (light ? Rgb(0xB45309) : Rgb(0xFFB020));
   g_cloudUp   = classic ? Rgb(0x43A047) : g_colSpanA;
   g_cloudDn   = classic ? Rgb(0xF44336) : g_colSpanB;
  }

//+------------------------------------------------------------------+
//| Initialization                                                     |
//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpTenkanLen < 1 || InpKijunLen < 1 || InpSenkouBLen < 1 || InpDisplacement < 1 ||
      InpAtrLen < 0 || InpPctLen < 10 || InpStatsH2 < 1 || InpStatsH2 > 500 ||
      InpPctThin < 0 || InpPctThin > 100 || InpPctThk < 0 || InpPctThk > 100 ||
      InpPctVThk < 0 || InpPctVThk > 100 || InpFlatMinK < 2 || InpFlatMinB < 2 ||
      InpMaxAgeMul < 1 || InpMaxLevels < 5 || InpMaxLevels > 400 || InpTouchTol < 0.0)
      return(INIT_PARAMETERS_INCORRECT);

   //--- derived config (Pine: classic mode forces Layers 1-3 off)
   g_useL1   = (!InpClassicMode && InpInGeom);
   g_useL2   = (!InpClassicMode && InpInQualified);
   g_useL3   = (!InpClassicMode && InpInFlat);
   g_off     = InpDisplacement - 1;
   g_atrN    = (InpAtrLen > 0 ? InpAtrLen : InpKijunLen);
   g_maxAge  = InpMaxAgeMul * InpKijunLen;

   IndicatorSetString(INDICATOR_SHORTNAME,
                      "MKumo [GBB] " + TfName(_Period) + " (MQL5 port)");
   SetupPalette();

   //--- bind buffers
   SetIndexBuffer(BUF_TENKAN,      bTenkan,    INDICATOR_DATA);
   SetIndexBuffer(BUF_KIJUN,       bKijun,     INDICATOR_DATA);
   SetIndexBuffer(BUF_CHIKOU,      bChikou,    INDICATOR_DATA);
   SetIndexBuffer(BUF_SPANA,       bSpanA,     INDICATOR_DATA);
   SetIndexBuffer(BUF_SPANB,       bSpanB,     INDICATOR_DATA);
   SetIndexBuffer(BUF_FILLA,       bFillA,     INDICATOR_DATA);
   SetIndexBuffer(BUF_FILLB,       bFillB,     INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_TK_BULL,  bTkBullM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_TK_BEAR,  bTkBearM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_KU_UP,    bKumoUpM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_KU_DN,    bKumoDnM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_RAW_BULL, bRawBullM,  INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_RAW_BEAR, bRawBearM,  INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_TW_BULL,  bTwBullM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_MK_TW_BEAR,  bTwBearM,   INDICATOR_DATA);
   SetIndexBuffer(BUF_ATR,         bAtr,       INDICATOR_DATA);
   SetIndexBuffer(BUF_THICK,       bThick,     INDICATOR_DATA);
   SetIndexBuffer(BUF_TK,          bTkSpread,  INDICATOR_DATA);
   SetIndexBuffer(BUF_PC,          bPc,        INDICATOR_DATA);
   SetIndexBuffer(BUF_CHK,         bChk,       INDICATOR_DATA);
   SetIndexBuffer(BUF_GRADE,       bGrade,     INDICATOR_DATA);
   SetIndexBuffer(BUF_GRADE_PROJ,  bGradeProj, INDICATOR_DATA);
   SetIndexBuffer(BUF_QUAL_DIR,    bQualDir,   INDICATOR_DATA);
   SetIndexBuffer(BUF_TK_GRADE,    bTkGrade,   INDICATOR_DATA);
   SetIndexBuffer(BUF_HTF_POS,     bHtfPos,    INDICATOR_DATA);
   SetIndexBuffer(BUF_FLAT_K,      bFlatK,     INDICATOR_DATA);
   SetIndexBuffer(BUF_FLAT_B,      bFlatB,     INDICATOR_DATA);
   SetIndexBuffer(BUF_EV_BITS,     bEvBits,    INDICATOR_DATA);

#define INIT_BUFFER(arr) { ArraySetAsSeries(arr, true); ArrayInitialize(arr, EMPTY_VALUE); }
   INIT_BUFFER(bTenkan)
   INIT_BUFFER(bKijun)
   INIT_BUFFER(bChikou)
   INIT_BUFFER(bSpanA)
   INIT_BUFFER(bSpanB)
   INIT_BUFFER(bFillA)
   INIT_BUFFER(bFillB)
   INIT_BUFFER(bTkBullM)
   INIT_BUFFER(bTkBearM)
   INIT_BUFFER(bKumoUpM)
   INIT_BUFFER(bKumoDnM)
   INIT_BUFFER(bRawBullM)
   INIT_BUFFER(bRawBearM)
   INIT_BUFFER(bTwBullM)
   INIT_BUFFER(bTwBearM)
   INIT_BUFFER(bAtr)
   INIT_BUFFER(bThick)
   INIT_BUFFER(bTkSpread)
   INIT_BUFFER(bPc)
   INIT_BUFFER(bChk)
   INIT_BUFFER(bGrade)
   INIT_BUFFER(bGradeProj)
   INIT_BUFFER(bQualDir)
   INIT_BUFFER(bTkGrade)
   INIT_BUFFER(bHtfPos)
   INIT_BUFFER(bFlatK)
   INIT_BUFFER(bFlatB)
   INIT_BUFFER(bEvBits)

   //--- plot styles (layer 0 lines)
   SetupLinePlot(PLOT_TENKAN, g_colTenkan, 2, "Tenkan-sen");
   SetupLinePlot(PLOT_KIJUN,  g_colKijun,  3, "Kijun-sen");
   SetupLinePlot(PLOT_CHIKOU, BlendToBg(g_colChikou, 25), 1, "Chikou");
   //--- Chikou drawn backwards into the past: negative PLOT_SHIFT, exactly
   //--- like Indicators/Examples/Ichimoku.mq5 (Pine offset = -g_off)
   PlotIndexSetInteger(PLOT_CHIKOU, PLOT_SHIFT, -g_off);
   SetupLinePlot(PLOT_SPANA,  g_colSpanA,  2, "Senkou A");
   SetupLinePlot(PLOT_SPANB,  g_colSpanB,  2, "Senkou B");
   //--- forward displacement (Pine offset = displacement - 1): a positive
   //--- PLOT_SHIFT moves points to the RIGHT / into the future, including
   //--- beyond the last bar - MQL5 Book: "positive shifts to the right";
   //--- the official Indicators/Examples/Ichimoku.mq5 does exactly this
   PlotIndexSetInteger(PLOT_SPANA, PLOT_SHIFT, g_off);
   PlotIndexSetInteger(PLOT_SPANB, PLOT_SHIFT, g_off);
   //--- cloud fill (2 dynamic colors; per-tick alpha emulation = D1)
   PlotIndexSetInteger(PLOT_FILL, PLOT_DRAW_TYPE, DRAW_FILLING);
   PlotIndexSetInteger(PLOT_FILL, PLOT_SHIFT, g_off);
   PlotIndexSetString(PLOT_FILL, PLOT_LABEL, "Kumo fill A;Kumo fill B");
   PlotIndexSetDouble(PLOT_FILL, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   //--- markers
   SetupArrowPlot(PLOT_MK_TK_BULL, 217, 6, 1, g_colBull, "TK bull (qualified)");
   SetupArrowPlot(PLOT_MK_TK_BEAR, 218, -6, 1, g_colBear, "TK bear (qualified)");
   SetupArrowPlot(PLOT_MK_KU_UP,   241, 6, 2, g_colBull, "KUMO up (qualified)");
   SetupArrowPlot(PLOT_MK_KU_DN,   242, -6, 2, g_colBear, "KUMO down (qualified)");
   SetupArrowPlot(PLOT_MK_RAW_BULL,159, 6, 1, g_colRaw,  "Unqualified bull event");
   SetupArrowPlot(PLOT_MK_RAW_BEAR,159, -6, 1, g_colRaw,  "Unqualified bear event");
   SetupArrowPlot(PLOT_MK_TW_BULL, 241, 60, 1, BlendToBg(g_colTwist, 20), "Twist bull");
   SetupArrowPlot(PLOT_MK_TW_BEAR, 242, -60, 1, BlendToBg(g_colTwist, 20), "Twist bear");
   //--- data-window only
   SetupNonePlot(PLOT_ATR,        "ATR (Wilder)");
   SetupNonePlot(PLOT_THICK,      "Thick");
   SetupNonePlot(PLOT_TK,         "TK");
   SetupNonePlot(PLOT_PC,         "PC");
   SetupNonePlot(PLOT_CHK,        "CHK");
   SetupNonePlot(PLOT_GRADE,      "Grade");
   SetupNonePlot(PLOT_GRADE_PROJ, "GradeProj");
   SetupNonePlot(PLOT_QUAL_DIR,   "QualDir");
   SetupNonePlot(PLOT_TK_GRADE,   "TKGrade");
   SetupNonePlot(PLOT_HTF_POS,    "HTFPos");
   SetupNonePlot(PLOT_FLAT_K,     "FlatRun K");
   SetupNonePlot(PLOT_FLAT_B,     "FlatRun B");
   SetupNonePlot(PLOT_EV_BITS,    "Events(bits)");

   g_htfBuilt = false;
   g_engine.Reset();
   ChartRedraw(0);
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Deinit: remove every object this indicator created                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   ObjectsDeleteAll(0, "MIC_");
   ChartRedraw(0);
  }

//+------------------------------------------------------------------+
//| Main: full backfill on prev_calculated==0, otherwise compute the   |
//| forming bar, run the closed-bar state machine once per new bar.    |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
   if(rates_total < 2)
      return(0);

   ArraySetAsSeries(time, true);
   ArraySetAsSeries(open, true);
   ArraySetAsSeries(high, true);
   ArraySetAsSeries(low, true);
   ArraySetAsSeries(close, true);
   //--- series-aligned copies (MQL5 has no array assignment operator; ArrayCopy
   //--- with both arrays flagged as series keeps index 0 = newest on both sides)
   ArrayFree(g_time);
   ArrayFree(g_open);
   ArrayFree(g_high);
   ArrayFree(g_low);
   ArrayFree(g_close);
   ArraySetAsSeries(g_time, true);
   ArraySetAsSeries(g_open, true);
   ArraySetAsSeries(g_high, true);
   ArraySetAsSeries(g_low, true);
   ArraySetAsSeries(g_close, true);
   ArrayCopy(g_time, time);
   ArrayCopy(g_open, open);
   ArrayCopy(g_high, high);
   ArrayCopy(g_low, low);
   ArrayCopy(g_close, close);

   EnsureHtf();

   if(prev_calculated == 0 || rates_total < prev_calculated)
     {
      //--- full pass: Pine re-runs the whole series; state must restart
      g_engine.Reset();
      for(int i = rates_total - 1; i >= 0; i--)
        {
         ComputeBar(i);
         if(i >= 1)
            g_engine.ProcessBar(i, false);   // backfill: accumulate, never alert (rule 3)
        }
     }
   else
     {
      int k = rates_total - prev_calculated;
      if(k > rates_total - 1)
         k = rates_total - 1;
      if(k > 0)
        {
         //--- bars born since the last call: compute oldest-of-batch first
         for(int j = k - 1; j >= 0; j--)
            ComputeBar(j);
         //--- newly closed bars: state machine, chronological, realtime alerts
         for(int j = k; j >= 1; j--)
            g_engine.ProcessBar(j, true);
        }
      else
        {
         ComputeBar(0);
        }
     }

   //--- overlays: cloud fill colors (D1), grade label, HTF readout, table
   int gp = IsNa(bGradeProj[0]) ? -1 : (int)MathRound(bGradeProj[0]);
   int tr;
   if(!g_useL1)       tr = 68;
   else if(gp == 3)   tr = 50;
   else if(gp == 2)   tr = 58;
   else if(gp == 1)   tr = 68;
   else if(gp == 0)   tr = 78;
   else               tr = 74;
   PlotIndexSetInteger(PLOT_FILL, PLOT_LINE_COLOR, 0, BlendToBg(g_cloudUp, tr));
   PlotIndexSetInteger(PLOT_FILL, PLOT_LINE_COLOR, 1, BlendToBg(g_cloudDn, tr));

   g_engine.UpdateLabels();

   if(prev_calculated == 0 || rates_total - prev_calculated > 0)
      ChartRedraw(0);

   return(rates_total);
  }
//+------------------------------------------------------------------+
