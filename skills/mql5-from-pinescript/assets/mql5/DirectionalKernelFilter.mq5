//+------------------------------------------------------------------+
//|                                    DirectionalKernelFilter.mq5    |
//|  MQL5 port of the open-source Pine Script indicator               |
//|  "Directional Kernel Filter [BackQuant]" by BackQuant             |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 directional-kernel-filter.pine (124 lines, v6)     |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0003-directional-kernel-filter.md                  |
//|  Mapping     : skills/mql5-from-pinescript/references/             |
//|                 pine-to-mql5.md                                    |
//|                                                                    |
//|  Original (c) BackQuant, licensed under MPL-2.0                    |
//|  https://mozilla.org/MPL/2.0/                                      |
//|  This port is a derivative work distributed under MPL-2.0          |
//|  (file-level copyleft; keep this header).                          |
//|                                                                    |
//|  Deviations D1-D5 in the port record. Headlines:                   |
//|    D1 ribbon fill color follows the LATEST trend, not per-bar      |
//|    D2 Pine plotcandle() candle painting not supported (no-op)      |
//|    D3 Pine bgcolor() background tint not supported (no-op)         |
//|    D4 input.source approximated by ENUM_PINE_SOURCE                |
//|    D5 tooltips not carried into MQL5 inputs                        |
//+------------------------------------------------------------------+
#property copyright "(c) BackQuant - MPL-2.0 - MQL5 port"
#property link      "https://www.tradingview.com/script/5AnxLyjj-Directional-Kernel-Filter-BackQuant/"
#property version   "1.00"
#property description "Directional Kernel Filter - MQL5 port"
#property indicator_chart_window
#property indicator_buffers 13
#property indicator_plots   10

//+------------------------------------------------------------------+
//| Enums (before the inputs that use them)                           |
//+------------------------------------------------------------------+
enum ENUM_PINE_SOURCE
  {
   SRC_CLOSE        = 0,   // close
   SRC_OPEN         = 1,   // open
   SRC_HIGH         = 2,   // high
   SRC_LOW          = 3,   // low
   SRC_MEDIAN_HL2   = 4,   // hl2 (median)
   SRC_TYPICAL_HLC3 = 5,   // hlc3 (typical)
   SRC_WEIGHTED     = 6    // hlcc4 (weighted)
  };

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs 1:1 (same defaults, same groups)  |
//+------------------------------------------------------------------+
input group "Core Calculation Settings"
input ENUM_PINE_SOURCE InpSource       = SRC_CLOSE;  // Source (D4)
input int            InpFastLen        = 18;         // Fast Kernel Length
input int            InpSlowLen        = 35;         // Slow
input double         InpKernelWidth    = 0.35;       // Kernel Width
input double         InpDirStrength    = 3.5;        // Directional Weight
input int            InpNormLen        = 14;         // Normalization Length (ATR)

input group "Plotting and Coloring"
input color          InpLongColor      = (color)0x00FF00; // Long Color (Pine #00ff00)
input color          InpShortColor     = (color)0x0000FF; // Short Color (Pine #ff0000)
input int            InpLineWidth      = 3;          // Line Width
input bool           InpShowRibbon     = true;       // Show Trend Ribbon?
input bool           InpShowBase       = false;      // Show Base Kernel?
input bool           InpPaintCandles   = false;      // Paint Candles to Trend? (NO-OP, D2)
input bool           InpBgCol          = false;      // Background Color? (NO-OP, D3)

input group "Alerts"
input bool           InpEnableAlerts   = true;       // Confirmed-bar alerts (Pine alertcondition)

//+------------------------------------------------------------------+
//| Buffer / plot indices                                             |
//+------------------------------------------------------------------+
#define BUF_FAST        0    // value buffer of the fast-kernel plot
#define BUF_FAST_CLR    1    // color index of the fast-kernel plot
#define BUF_SLOW        2    // value buffer of the slow-kernel plot
#define BUF_SLOW_CLR    3    // color index of the slow-kernel plot
#define BUF_FILL_F      4
#define BUF_FILL_S      5
#define BUF_BASE        6
#define BUF_ATR         7
#define BUF_TREND       8
#define BUF_FAST_DIR    9
#define BUF_SLOW_DIR   10
#define BUF_ADJ        11
#define BUF_SPREAD     12

#define PLOT_FAST       0
#define PLOT_SLOW       1
#define PLOT_RIBBON     2
#define PLOT_BASE       3
#define PLOT_ATR        4
#define PLOT_TREND      5
#define PLOT_FAST_DIR   6
#define PLOT_SLOW_DIR   7
#define PLOT_ADJ        8
#define PLOT_SPREAD     9

//+------------------------------------------------------------------+
//| Indicator buffers                                                 |
//+------------------------------------------------------------------+
double bFast[];
double bFastClr[];
double bSlow[];
double bSlowClr[];
double bFillF[];
double bFillS[];
double bBase[];
double bAtr[];
double bTrend[];
double bFastDir[];
double bSlowDir[];
double bAdjust[];
double bSpread[];

//--- bind-time initializer: as-series + EMPTY for every data buffer
#define INIT_BUFFER(arr) { ArraySetAsSeries(arr, true); ArrayInitialize(arr, EMPTY_VALUE); }

//--- chart series (as-series copies of the OnCalculate inputs)
datetime g_time[];
double   g_open[];
double   g_high[];
double   g_low[];
double   g_close[];

//--- derived config (OnInit)
int      g_atrN;
double   g_mintick;
bool     g_ribbonVisible;
color    g_bg;
color    g_ribbonBull;
color    g_ribbonBear;

//+------------------------------------------------------------------+
//| Helpers                                                           |
//+------------------------------------------------------------------+
bool IsNa(const double v)
  {
   return(v >= EMPTY_VALUE - 0.5 || v <= -EMPTY_VALUE + 0.5);
  }

uint ColR(const color c) { return(((uint)c) & 0xFF); }
uint ColG(const color c) { return(((uint)c) >> 8) & 0xFF; }
uint ColB(const color c) { return(((uint)c) >> 16) & 0xFF; }

//--- Pine color.new(base, transp) emulated by blending toward chart bg
color BlendToBg(const color base, const int transp)
  {
   if(transp <= 0)   return(base);
   if(transp >= 100) return(g_bg);
   double k = transp / 100.0;
   double s = 1.0 - k;
   uint r = (uint)MathRound(ColR(base) * s + ColR(g_bg) * k);
   uint g = (uint)MathRound(ColG(base) * s + ColG(g_bg) * k);
   uint b = (uint)MathRound(ColB(base) * s + ColB(g_bg) * k);
   return((color)(((b & 0xFF) << 16) | ((g & 0xFF) << 8) | (r & 0xFF)));
  }

//--- Pine input.source
double SrcAt(const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return(EMPTY_VALUE);
   switch(InpSource)
     {
      case SRC_OPEN:         return(g_open[i]);
      case SRC_HIGH:         return(g_high[i]);
      case SRC_LOW:          return(g_low[i]);
      case SRC_MEDIAN_HL2:   return((g_high[i] + g_low[i]) / 2.0);
      case SRC_TYPICAL_HLC3: return((g_high[i] + g_low[i] + g_close[i]) / 3.0);
      case SRC_WEIGHTED:     return((g_high[i] + g_low[i] + 2.0 * g_close[i]) / 4.0);
      default:               return(g_close[i]);
     }
  }

//--- ta.atr = Wilder RMA (NOT iATR - SMA of TR), SMA-seeded
double CalcAtr(const int i)
  {
   int sz = ArraySize(g_time);
   int n  = g_atrN;
   if(n < 1)
      return(EMPTY_VALUE);
   int seed = sz - 1 - n;
   if(seed < 0 || i > seed)
      return(EMPTY_VALUE);
   if(i == seed)
     {
      double sum = 0.0;
      for(int j = i; j < i + n; j++)
        {
         if(j + 1 >= sz)
            return(EMPTY_VALUE);
         double hl = g_high[j] - g_low[j];
         double hc = MathAbs(g_high[j] - g_close[j + 1]);
         double lc = MathAbs(g_low[j] - g_close[j + 1]);
         sum += MathMax(hl, MathMax(hc, lc));
        }
      return(sum / n);
     }
   double prev = bAtr[i + 1];
   if(IsNa(prev) || i + 1 >= sz)
      return(EMPTY_VALUE);
   double hl = g_high[i] - g_low[i];
   double hc = MathAbs(g_high[i] - g_close[i + 1]);
   double lc = MathAbs(g_low[i] - g_close[i + 1]);
   double tr = MathMax(hl, MathMax(hc, lc));
   return((prev * (n - 1) + tr) / n);
  }

//+------------------------------------------------------------------+
//| Base Gaussian kernel at bar b (window function - no history)      |
//+------------------------------------------------------------------+
double BaseKernel(const int b, const int L)
  {
   int    sz = ArraySize(g_time);
   double bw = MathMax(1.0, (double)L * InpKernelWidth);
   double vsum = 0.0;
   double wsum = 0.0;
   for(int k = 0; k < L; k++)
     {
      int j = b + k;
      if(j >= sz)
         break;                      // Pine: `not na(source[i])` skips the rest
      double v = SrcAt(j);
      if(IsNa(v))
         continue;
      double d = (double)k / bw;
      double w = MathExp(-0.5 * d * d);
      vsum += v * w;
      wsum += w;
     }
   return(wsum > 0.0 ? vsum / wsum : EMPTY_VALUE);
  }

//+------------------------------------------------------------------+
//| Directional kernel filter at bar i (Pine directionalKernel())      |
//| Returns the filtered value; outs = base kernel + prior direction. |
//+------------------------------------------------------------------+
double DirKernel(const int i, const int L, double &base_out, double &dir_out)
  {
   int    sz = ArraySize(g_time);
   base_out = BaseKernel(i, L);
   dir_out  = EMPTY_VALUE;

   //--- priorDirection = nz(base[1] - base[2]) - bases are window functions
   double b1 = (i + 1 < sz) ? BaseKernel(i + 1, L) : EMPTY_VALUE;
   double b2 = (i + 2 < sz) ? BaseKernel(i + 2, L) : EMPTY_VALUE;
   double prior_dir = (!IsNa(b1) && !IsNa(b2)) ? (b1 - b2) : 0.0;
   double a1 = (i + 1 < sz) ? bAtr[i + 1] : EMPTY_VALUE;
   double a0 = (!IsNa(a1) ? a1 : ((i < sz && !IsNa(bAtr[i])) ? bAtr[i] : EMPTY_VALUE));
   if(IsNa(a0))
     {
      //--- Pine: nz(norm[1], norm) still na during ATR warm-up -> the whole
      //--- chain degrades to `base`
      return(base_out);
     }
   double prior_norm = prior_dir / MathMax(a0, g_mintick);
   prior_norm = MathMax(-1.0, MathMin(1.0, prior_norm));
   dir_out = prior_norm;

   //--- directionally re-weighted pass
   double bw = MathMax(1.0, (double)L * InpKernelWidth);
   double a_cur = (i < sz && !IsNa(bAtr[i])) ? bAtr[i] : EMPTY_VALUE;
   if(IsNa(a_cur))
      return(base_out);              // Pine degrades to base when norm is na
   double vsum = 0.0;
   double wsum = 0.0;
   for(int k = 0; k < L; k++)
     {
      int j = i + k;
      if(j >= sz)
         break;
      double v = SrcAt(j);
      if(IsNa(v))
         continue;
      if(k < L - 1)
        {
         double v_next = SrcAt(j + 1);
         if(IsNa(v_next))
            return(base_out);        // Pine: localMove na poisons the sums
         double local_move = v - v_next;
         double local_den = MathMax(IsNa(bAtr[j]) ? a_cur : bAtr[j], g_mintick);
         double local_norm = local_move / local_den;
         local_norm = MathMax(-1.0, MathMin(1.0, local_norm));
         double alignment = prior_norm * local_norm;
         double exponent = MathMax(-3.0, MathMin(3.0, InpDirStrength * alignment));
         double w = MathExp(exponent);
         double d = (double)k / bw;
         w *= MathExp(-0.5 * d * d);
         vsum += v * w;
         wsum += w;
        }
      else
        {
         double d = (double)k / bw;
         double w = MathExp(-0.5 * d * d);   // localMove = 0 -> exp(0)=1
         vsum += v * w;
         wsum += w;
        }
     }
   return(wsum > 0.0 ? vsum / wsum : base_out);
  }

//+------------------------------------------------------------------+
//| Alert gate: exactly once per closed bar, realtime only            |
//+------------------------------------------------------------------+
class CSignalGate
  {
private:
   datetime m_last_time;

public:
                     CSignalGate() : m_last_time(0) {}

   void              Reset(void)             { m_last_time = 0; }
   void              Process(const int i, const bool allow_alert);
  };

void CSignalGate::Process(const int i, const bool allow_alert)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;
   datetime t = g_time[i];
   if(t <= m_last_time)            // idempotence guard
      return;
   m_last_time = t;
   if(!allow_alert || !InpEnableAlerts)
      return;
   if(IsNa(bTrend[i]))
      return;
   int t0 = (int)MathRound(bTrend[i]);
   int t1 = (i + 1 < sz && !IsNa(bTrend[i + 1])) ? (int)MathRound(bTrend[i + 1]) : 0;
   if(t0 == 1 && t1 == -1)
      Alert("Directional Kernel Trend Filter turned bullish ", _Symbol);
   if(t0 == -1 && t1 == 1)
      Alert("Directional Kernel Trend Filter turned bearish ", _Symbol);
  }

CSignalGate g_gate;

//+------------------------------------------------------------------+
//| Per-bar computation (trend is var-state: full pass runs oldest -> |
//| newest; the forming bar recomputes from the previous bar's final) |
//+------------------------------------------------------------------+
void ComputeBar(const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;

   bAtr[i] = CalcAtr(i);

   double fast_base, fast_dir, slow_base, slow_dir;
   double fast = DirKernel(i, InpFastLen, fast_base, fast_dir);
   double slow = DirKernel(i, InpSlowLen, slow_base, slow_dir);
   bBase[i]     = fast_base;
   bFast[i]     = fast;
   bSlow[i]     = slow;
   bFastDir[i]  = fast_dir;
   bSlowDir[i]  = slow_dir;
   bAdjust[i]   = (!IsNa(fast) && !IsNa(fast_base)) ? fast - fast_base : EMPTY_VALUE;
   bSpread[i]   = (!IsNa(fast) && !IsNa(slow)) ? fast - slow : EMPTY_VALUE;

   //--- trend state (Pine `var int trend`: 1 / -1 / hold, seed 0)
   int prev_trend = (i + 1 < sz && !IsNa(bTrend[i + 1])) ? (int)MathRound(bTrend[i + 1]) : 0;
   int trend = prev_trend;
   if(fast > slow)
      trend = 1;
   else if(fast < slow)
      trend = -1;
   bTrend[i]     = (double)trend;
   bFastClr[i]   = (trend == 1) ? 0.0 : 1.0;
   bSlowClr[i]   = (trend == 1) ? 0.0 : 1.0;
   bFillF[i]     = g_ribbonVisible ? fast : EMPTY_VALUE;
   bFillS[i]     = g_ribbonVisible ? slow : EMPTY_VALUE;
  }

//+------------------------------------------------------------------+
//| Plot setup helpers                                                |
//+------------------------------------------------------------------+
void SetupColorLinePlot(const int p, const color c_bull, const color c_bear,
                        const int w, const string label)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_COLOR_LINE);
   PlotIndexSetInteger(p, PLOT_COLOR_INDEXES, 2);
   PlotIndexSetInteger(p, PLOT_LINE_COLOR, 0, c_bull);
   PlotIndexSetInteger(p, PLOT_LINE_COLOR, 1, c_bear);
   PlotIndexSetInteger(p, PLOT_LINE_WIDTH, w);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
  }

void SetupNonePlot(const int p, const string label, const bool show = true)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_NONE);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetInteger(p, PLOT_SHOW_DATA, show ? 1 : 0);
  }

//+------------------------------------------------------------------+
//| Initialization                                                     |
//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpFastLen < 3 || InpSlowLen < 5 || InpKernelWidth < 0.05 ||
      InpKernelWidth > 1.0 || InpDirStrength < 0.0 || InpDirStrength > 5.0 ||
      InpNormLen < 2 || InpLineWidth < 1 || InpLineWidth > 6)
      return(INIT_PARAMETERS_INCORRECT);

   g_atrN = InpNormLen;
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   g_mintick = (tickSize > 0.0) ? tickSize : _Point;
   g_ribbonVisible = InpShowRibbon;

   long bg_res = 0;
   ChartGetInteger(0, CHART_COLOR_BACKGROUND, 0, bg_res);
   g_bg = (color)(bg_res & 0xFFFFFF);
   g_ribbonBull = BlendToBg(InpLongColor, 82);
   g_ribbonBear = BlendToBg(InpShortColor, 82);
   long fg_res = 0;
   ChartGetInteger(0, CHART_COLOR_FOREGROUND, 0, fg_res);
   color fg = (color)(fg_res & 0xFFFFFF);

   IndicatorSetString(INDICATOR_SHORTNAME,
                      "Directional Kernel " + IntegerToString(InpFastLen) + "/" +
                      IntegerToString(InpSlowLen) + " [BackQuant]");

   //--- bind buffers (order matches the buffer indices above)
   SetIndexBuffer(BUF_FAST,      bFast,      INDICATOR_DATA);
   SetIndexBuffer(BUF_FAST_CLR,  bFastClr,   INDICATOR_COLOR_INDEX);
   SetIndexBuffer(BUF_SLOW,      bSlow,      INDICATOR_DATA);
   SetIndexBuffer(BUF_SLOW_CLR,  bSlowClr,   INDICATOR_COLOR_INDEX);
   SetIndexBuffer(BUF_FILL_F,    bFillF,     INDICATOR_DATA);
   SetIndexBuffer(BUF_FILL_S,    bFillS,     INDICATOR_DATA);
   SetIndexBuffer(BUF_BASE,      bBase,      INDICATOR_DATA);
   SetIndexBuffer(BUF_ATR,       bAtr,       INDICATOR_DATA);
   SetIndexBuffer(BUF_TREND,     bTrend,     INDICATOR_DATA);
   SetIndexBuffer(BUF_FAST_DIR,  bFastDir,   INDICATOR_DATA);
   SetIndexBuffer(BUF_SLOW_DIR,  bSlowDir,   INDICATOR_DATA);
   SetIndexBuffer(BUF_ADJ,       bAdjust,    INDICATOR_DATA);
   SetIndexBuffer(BUF_SPREAD,    bSpread,    INDICATOR_DATA);

   INIT_BUFFER(bFast)
   INIT_BUFFER(bFastClr)
   INIT_BUFFER(bSlow)
   INIT_BUFFER(bSlowClr)
   INIT_BUFFER(bFillF)
   INIT_BUFFER(bFillS)
   INIT_BUFFER(bBase)
   INIT_BUFFER(bAtr)
   INIT_BUFFER(bTrend)
   INIT_BUFFER(bFastDir)
   INIT_BUFFER(bSlowDir)
   INIT_BUFFER(bAdjust)
   INIT_BUFFER(bSpread)

   //--- kernels (trend-colored), ribbon (input-controlled), base kernel
   SetupColorLinePlot(PLOT_FAST, InpLongColor, InpShortColor, InpLineWidth,
                      "Fast Directional Kernel");
   SetupColorLinePlot(PLOT_SLOW, BlendToBg(InpLongColor, 60), BlendToBg(InpShortColor, 60),
                      2, "Slow Directional Kernel");
   if(!InpShowRibbon)
      PlotIndexSetInteger(PLOT_SLOW, PLOT_DRAW_TYPE, DRAW_NONE);
   PlotIndexSetInteger(PLOT_RIBBON, PLOT_DRAW_TYPE, DRAW_FILLING);
   PlotIndexSetString(PLOT_RIBBON, PLOT_LABEL, "Directional Kernel Ribbon");
   PlotIndexSetDouble(PLOT_RIBBON, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetInteger(PLOT_BASE, PLOT_DRAW_TYPE, InpShowBase ? DRAW_LINE : DRAW_NONE);
   PlotIndexSetInteger(PLOT_BASE, PLOT_LINE_COLOR, BlendToBg(fg, 60));
   PlotIndexSetInteger(PLOT_BASE, PLOT_LINE_WIDTH, 1);
   PlotIndexSetString(PLOT_BASE, PLOT_LABEL, "Base Gaussian Kernel");
   PlotIndexSetDouble(PLOT_BASE, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   //--- data-window diagnostics (ATR + trend hidden: not in Pine's window)
   SetupNonePlot(PLOT_ATR,      "ATR (Wilder)", false);
   SetupNonePlot(PLOT_TREND,    "Trend", false);
   SetupNonePlot(PLOT_FAST_DIR, "Fast Reference Direction");
   SetupNonePlot(PLOT_SLOW_DIR, "Slow Reference Direction");
   SetupNonePlot(PLOT_ADJ,      "Directional Adjustment");
   SetupNonePlot(PLOT_SPREAD,   "Kernel Spread");

   g_gate.Reset();
   ChartRedraw(0);
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Deinit                                                            |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   ChartRedraw(0);
  }

//+------------------------------------------------------------------+
//| Main: full backfill on prev_calculated==0, otherwise compute the  |
//| forming bar and run the alert gate once per new bar.              |
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
   if(rates_total < 3)
      return(0);

   ArraySetAsSeries(time, true);
   ArraySetAsSeries(open, true);
   ArraySetAsSeries(high, true);
   ArraySetAsSeries(low, true);
   ArraySetAsSeries(close, true);
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

   if(prev_calculated == 0 || rates_total < prev_calculated)
     {
      g_gate.Reset();
      for(int i = rates_total - 1; i >= 0; i--)
        {
         ComputeBar(i);                // oldest -> newest: ATR + trend order
         if(i >= 1)
            g_gate.Process(i, false);  // backfill: never alert
        }
     }
   else
     {
      int k = rates_total - prev_calculated;
      if(k > rates_total - 1)
         k = rates_total - 1;
      if(k > 0)
        {
         for(int j = k - 1; j >= 0; j--)
            ComputeBar(j);
         for(int j = k; j >= 1; j--)
            g_gate.Process(j, true);   // realtime closed bars only
        }
      else
        {
         ComputeBar(0);
        }
     }

   //--- D1: ribbon color follows the LATEST trend (2 static colors)
   int t0 = IsNa(bTrend[0]) ? -1 : (int)MathRound(bTrend[0]);
   color rc = (t0 == 1) ? g_ribbonBull : g_ribbonBear;
   PlotIndexSetInteger(PLOT_RIBBON, PLOT_LINE_COLOR, 0, rc);
   PlotIndexSetInteger(PLOT_RIBBON, PLOT_LINE_COLOR, 1, rc);

   if(prev_calculated == 0 || rates_total - prev_calculated > 0)
      ChartRedraw(0);
   return(rates_total);
  }
//+------------------------------------------------------------------+
