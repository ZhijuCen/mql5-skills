//+------------------------------------------------------------------+
//|                               AdaptiveDecyclerSupertrend.mq5      |
//|  MQL5 port of the open-source Pine Script indicator               |
//|  "Adaptive Decycler Supertrend" by SchizoQuant                    |
//|                                                                    |
//|  Pine source : skills/mql5-from-pinescript/assets/pine-scripts/    |
//|                 adaptive-decycler-supertrend.pine (105 lines, v6)  |
//|  Port record : skills/mql5-from-pinescript/references/ports/       |
//|                 0002-adaptive-decycler-supertrend.md               |
//|  Mapping     : skills/mql5-from-pinescript/references/             |
//|                 pine-to-mql5.md                                    |
//|                                                                    |
//|  Original (c) SchizoQuant, licensed under MPL-2.0                 |
//|  https://mozilla.org/MPL/2.0/                                      |
//|  This port is a derivative work distributed under MPL-2.0          |
//|  (file-level copyleft; keep this header).                          |
//|                                                                    |
//|  Deviations D1-D4 in the port record. Headlines:                   |
//|    D1 RMS-band fill color follows the LATEST regime, not per-bar   |
//|    D2 Pine barcolor() not supported by MQL5 indicators (no-op)     |
//|    D3 plotshape text LONG/SHORT omitted (DRAW_ARROW has no text)   |
//|    D4 input.source approximated by ENUM_PINE_SOURCE (ohlc4 exact)  |
//+------------------------------------------------------------------+
#property copyright "(c) SchizoQuant - MPL-2.0 - MQL5 port"
#property link      "https://www.tradingview.com/script/vEWWRSv8-Adaptive-Decycler-Supertrend-SchizoQuant/"
#property version   "1.00"
#property description "Adaptive Decycler Supertrend - MQL5 port"
#property indicator_chart_window
#property indicator_buffers 16
#property indicator_plots   14

//+------------------------------------------------------------------+
//| Enums (before the inputs that use them)                           |
//+------------------------------------------------------------------+
enum ENUM_PINE_SOURCE
  {
   SRC_CLOSE       = 0,   // close
   SRC_OPEN        = 1,   // open
   SRC_HIGH        = 2,   // high
   SRC_LOW         = 3,   // low
   SRC_MEDIAN_HL2  = 4,   // hl2 (median)
   SRC_TYPICAL_HLC3 = 5,  // hlc3 (typical)
   SRC_WEIGHTED    = 6    // hlcc4 (weighted - closest to Pine ohlc4)
  };

//+------------------------------------------------------------------+
//| Inputs - mirror the Pine inputs 1:1 (same defaults, same groups)  |
//+------------------------------------------------------------------+
input group "Adaptive Decycler"
input ENUM_PINE_SOURCE InpSource      = SRC_CLOSE;   // Source (D4: ohlc4 -> weighted)
input int            InpMinCutoff     = 15;          // Minimum Cutoff
input int            InpMaxCutoff     = 50;          // Maximum Cutoff
input int            InpEffLength     = 10;          // Efficiency Length

input group "Supertrend Bands"
input int            InpRmsLength     = 20;          // Residual RMS Length
input double         InpUpperMult     = 2.0;         // Upper Multiplier
input double         InpLowerMult     = 2.6;         // Lower Multiplier

input group "Visualization"
input bool           InpShowDecycler  = true;        // Show Decycler
input bool           InpShowEnvelope  = false;       // Show RMS Envelope
input bool           InpShowFill      = true;        // Show Envelope Fill
input bool           InpShowSignals   = true;        // Show Signals
input bool           InpColorBars     = true;        // Color Bars (NO-OP, D2)

input group "Color Settings"
input color          InpLongColor     = (color)0x14FF39; // Bullish Color (Pine #39FF14)
input color          InpShortColor    = (color)0xE22B8A; // Bearish Color (Pine #8A2BE2)

input group "Alerts"
input bool           InpEnableAlerts  = true;        // Confirmed-bar alerts (Pine alertcondition)

//+------------------------------------------------------------------+
//| Buffer / plot indices                                             |
//+------------------------------------------------------------------+
#define BUF_TRAIL_BULL   0
#define BUF_TRAIL_BEAR   1
#define BUF_DECYCLER     2    // value buffer of the decycler plot
#define BUF_DEC_COLOR    3    // color-index buffer of the decycler plot
#define BUF_UPPER        4
#define BUF_LOWER        5
#define BUF_FILL_U       6
#define BUF_FILL_V       7
#define BUF_LONG_SIG     8
#define BUF_SHORT_SIG    9
#define BUF_TRAIL       10    // unconditional trail (logic + data window)
#define BUF_EFF          11
#define BUF_CUTOFF       12
#define BUF_RESID        13
#define BUF_RMS          14
#define BUF_SQ           15

#define PLOT_TRAIL_BULL  0
#define PLOT_TRAIL_BEAR  1
#define PLOT_DECYCLER    2
#define PLOT_UPPER       3
#define PLOT_LOWER       4
#define PLOT_FILL        5
#define PLOT_LONG        6
#define PLOT_SHORT       7
#define PLOT_TRAIL       8
#define PLOT_EFF         9
#define PLOT_CUTOFF     10
#define PLOT_RESID      11
#define PLOT_RMS        12
#define PLOT_SQ         13

//+------------------------------------------------------------------+
//| Indicator buffers                                                 |
//+------------------------------------------------------------------+
double bTrailBull[];
double bTrailBear[];
double bDecycler[];
double bDecColor[];
double bUpper[];
double bLower[];
double bFillU[];
double bFillV[];
double bLongSig[];
double bShortSig[];
double bTrail[];
double bEfficiency[];
double bCutoff[];
double bResidual[];
double bRms[];
double bSQ[];

//--- bind-time initializer: as-series + EMPTY for every data buffer
#define INIT_BUFFER(arr) { ArraySetAsSeries(arr, true); ArrayInitialize(arr, EMPTY_VALUE); }

//--- chart series (as-series copies of the OnCalculate inputs)
datetime g_time[];
double   g_open[];
double   g_high[];
double   g_low[];
double   g_close[];

//--- derived config (OnInit)
int      g_fastLimit;
int      g_slowLimit;
double   g_mintick;
bool     g_fillVisible;
color    g_fillBull;
color    g_fillBear;
color    g_bg;          // chart background (read in OnInit)

//+------------------------------------------------------------------+
//| Helpers                                                           |
//+------------------------------------------------------------------+
bool IsNa(const double v)
  {
   return(v >= EMPTY_VALUE - 0.5 || v <= -EMPTY_VALUE + 0.5);
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

//--- Pine input.source: value of the source series at bar i (EMPTY if i invalid)
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

//--- Pine nz(series[k], fallback): look k bars back, fall back to bar `cur`
double SrcNz(const int i, const int cur)
  {
   double v = SrcAt(i);
   if(!IsNa(v))
      return(v);
   return(SrcAt(cur));
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
   if(t <= m_last_time)          // idempotence guard
      return;
   m_last_time = t;
   if(!allow_alert || !InpEnableAlerts)
      return;
   if(!IsNa(bLongSig[i]))
      Alert("Adaptive Decycler Supertrend Long Signal on ", _Symbol);
   if(!IsNa(bShortSig[i]))
      Alert("Adaptive Decycler Supertrend Short Signal on ", _Symbol);
  }

CSignalGate g_gate;

//+------------------------------------------------------------------+
//| Per-bar computation (chronological state: decycler recursion and  |
//| SQ/trail are var-state - full pass runs oldest -> newest, the     |
//| forming bar is recomputed every tick from the previous bar's      |
//| final values, exactly like Pine's bar-by-bar evaluation).         |
//+------------------------------------------------------------------+
void ComputeBar(const int i)
  {
   int sz = ArraySize(g_time);
   if(i < 0 || i >= sz)
      return;

   //--- source with Pine nz() warm-up fallbacks
   double s0 = SrcAt(i);                                   // src
   double s1 = SrcNz(i + 1, i);                            // nz(src[1], src)
   double sEff = SrcNz(i + InpEffLength, i);               // nz(src[effLen], src)

   //--- directional efficiency over the lookback
   double direction = MathAbs(s0 - sEff);
   double noise = 0.0;
   for(int k = 0; k < InpEffLength; k++)
      noise += MathAbs(SrcNz(i + k, i) - SrcNz(i + k + 1, i));
   double efficiency = noise > 0.0 ? direction / noise : 0.0;
   efficiency = MathMax(0.0, MathMin(1.0, efficiency));
   bEfficiency[i] = efficiency;

   //--- adaptive cutoff -> smoothing coefficient (Ehlers-style alpha)
   double cutoff = (double)g_slowLimit - efficiency * (double)(g_slowLimit - g_fastLimit);
   bCutoff[i] = cutoff;
   double angle = 2.0 * M_PI / cutoff;
   double cosine = MathCos(angle);
   double alpha = MathAbs(cosine) > 0.000001
                  ? (cosine + MathSin(angle) - 1.0) / cosine : 1.0;
   alpha = MathMax(0.0, MathMin(1.0, alpha));

   //--- adaptive decycler (IIR recursion, seed = src at the oldest bar)
   double prevDec = (i + 1 < sz) ? bDecycler[i + 1] : EMPTY_VALUE;
   bDecycler[i] = IsNa(prevDec) ? s0 : alpha * 0.5 * (s0 + s1) + (1.0 - alpha) * prevDec;

   //--- residual RMS envelope
   double residual = s0 - bDecycler[i];
   bResidual[i] = residual;
   double energy = 0.0;
   bool   energy_ok = true;
   for(int k = 0; k < InpRmsLength; k++)
     {
      int j = i + k;
      if(j >= sz || IsNa(bResidual[j]))
        {
         energy_ok = false;
         break;
        }
      energy += bResidual[j] * bResidual[j];
     }
   double rms = energy_ok ? MathSqrt(energy / InpRmsLength) : 0.0;
   rms = MathMax(rms, g_mintick);              // Pine: max(rms, syminfo.mintick)
   bRms[i] = rms;
   double upper = bDecycler[i] + rms * InpUpperMult;
   double lower = bDecycler[i] - rms * InpLowerMult;
   bUpper[i] = upper;
   bLower[i] = lower;

   //--- Supertrend regime (Pine `var` state, recomputed from bar-1 finals)
   int    prev_sq = (i + 1 < sz && !IsNa(bSQ[i + 1]))
                    ? (int)MathRound(bSQ[i + 1])
                    : (s0 >= bDecycler[i] ? 1 : -1);       // nz(SQ[1], SQ)
   double prev_trail = (i + 1 < sz && !IsNa(bTrail[i + 1]))
                       ? bTrail[i + 1]
                       : (prev_sq == 1 ? lower : upper);   // nz(trendTrail[1], env)
   bool   long_flip  = (prev_sq == -1 && s0 > prev_trail);
   bool   short_flip = (prev_sq == 1 && s0 < prev_trail);
   int    sq = long_flip ? 1 : (short_flip ? -1 : prev_sq);
   double trail;
   if(sq == 1)
      trail = long_flip ? lower : MathMax(lower, prev_trail);
   else
      trail = short_flip ? upper : MathMin(upper, prev_trail);
   bSQ[i]     = (double)sq;
   bTrail[i]  = trail;
   bool long_sig  = (i + 1 < sz && sq == 1 && prev_sq != 1);
   bool short_sig = (i + 1 < sz && sq == -1 && prev_sq != -1);

   //--- display buffers
   bTrailBull[i] = (sq == 1) ? trail : EMPTY_VALUE;          // plot.style_linebr
   bTrailBear[i] = (sq == -1) ? trail : EMPTY_VALUE;
   bFillU[i]     = g_fillVisible ? upper : EMPTY_VALUE;
   bFillV[i]     = g_fillVisible ? lower : EMPTY_VALUE;
   bLongSig[i]   = long_sig ? g_low[i] : EMPTY_VALUE;
   bShortSig[i]  = short_sig ? g_high[i] : EMPTY_VALUE;
   bDecColor[i]  = (sq == 1) ? 0.0 : 1.0;
  }

//+------------------------------------------------------------------+
//| Plot setup helpers                                                |
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

void SetupNonePlot(const int p, const string label, const bool show = true)
  {
   PlotIndexSetInteger(p, PLOT_DRAW_TYPE, DRAW_NONE);
   PlotIndexSetString(p, PLOT_LABEL, label);
   PlotIndexSetDouble(p, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetInteger(p, PLOT_SHOW_DATA, (int)show);
  }

//+------------------------------------------------------------------+
//| Initialization                                                     |
//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpMinCutoff < 6 || InpMaxCutoff < 7 || InpEffLength < 2 ||
      InpRmsLength < 2 || InpUpperMult < 0.1 || InpLowerMult < 0.1)
      return(INIT_PARAMETERS_INCORRECT);

   g_fastLimit = MathMin(InpMinCutoff, InpMaxCutoff);
   g_slowLimit = MathMax(InpMinCutoff, InpMaxCutoff);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);  // double property
   g_mintick = (tickSize > 0.0) ? tickSize : _Point;
   g_fillVisible = (InpShowFill && InpShowEnvelope);
   g_fillBull = BlendToBg(InpLongColor, 93);
   g_fillBear = BlendToBg(InpShortColor, 93);

   long res = 0;
   ChartGetInteger(0, CHART_COLOR_BACKGROUND, 0, res);
   g_bg = (color)(res & 0xFFFFFF);

   IndicatorSetString(INDICATOR_SHORTNAME,
                      "Adaptive Decycler Supertrend " + IntegerToString(InpMinCutoff) + "/" +
                      IntegerToString(InpMaxCutoff));

   //--- bind buffers (order matches the buffer indices above)
   SetIndexBuffer(BUF_TRAIL_BULL, bTrailBull,   INDICATOR_DATA);
   SetIndexBuffer(BUF_TRAIL_BEAR, bTrailBear,   INDICATOR_DATA);
   SetIndexBuffer(BUF_DECYCLER,   bDecycler,    INDICATOR_DATA);
   SetIndexBuffer(BUF_DEC_COLOR,  bDecColor,    INDICATOR_COLOR_INDEX);
   SetIndexBuffer(BUF_UPPER,      bUpper,       INDICATOR_DATA);
   SetIndexBuffer(BUF_LOWER,      bLower,       INDICATOR_DATA);
   SetIndexBuffer(BUF_FILL_U,     bFillU,       INDICATOR_DATA);
   SetIndexBuffer(BUF_FILL_V,     bFillV,       INDICATOR_DATA);
   SetIndexBuffer(BUF_LONG_SIG,   bLongSig,     INDICATOR_DATA);
   SetIndexBuffer(BUF_SHORT_SIG,  bShortSig,    INDICATOR_DATA);
   SetIndexBuffer(BUF_TRAIL,      bTrail,       INDICATOR_DATA);
   SetIndexBuffer(BUF_EFF,        bEfficiency,  INDICATOR_DATA);
   SetIndexBuffer(BUF_CUTOFF,     bCutoff,      INDICATOR_DATA);
   SetIndexBuffer(BUF_RESID,      bResidual,    INDICATOR_DATA);
   SetIndexBuffer(BUF_RMS,        bRms,         INDICATOR_DATA);
   SetIndexBuffer(BUF_SQ,         bSQ,          INDICATOR_DATA);

   INIT_BUFFER(bTrailBull)
   INIT_BUFFER(bTrailBear)
   INIT_BUFFER(bDecycler)
   INIT_BUFFER(bDecColor)
   INIT_BUFFER(bUpper)
   INIT_BUFFER(bLower)
   INIT_BUFFER(bFillU)
   INIT_BUFFER(bFillV)
   INIT_BUFFER(bLongSig)
   INIT_BUFFER(bShortSig)
   INIT_BUFFER(bTrail)
   INIT_BUFFER(bEfficiency)
   INIT_BUFFER(bCutoff)
   INIT_BUFFER(bResidual)
   INIT_BUFFER(bRms)
   INIT_BUFFER(bSQ)

   //--- Layer plots
   SetupLinePlot(PLOT_TRAIL_BULL, InpLongColor, 2, "Bullish Supertrend");
   SetupLinePlot(PLOT_TRAIL_BEAR, InpShortColor, 2, "Bearish Supertrend");
   //--- decycler: per-bar regime color -> DRAW_COLOR_LINE (hidden on input off)
   PlotIndexSetInteger(PLOT_DECYCLER, PLOT_DRAW_TYPE,
                       InpShowDecycler ? DRAW_COLOR_LINE : DRAW_NONE);
   PlotIndexSetInteger(PLOT_DECYCLER, PLOT_COLOR_INDEXES, 2);
   PlotIndexSetInteger(PLOT_DECYCLER, PLOT_LINE_COLOR, 0, BlendToBg(InpLongColor, 35));
   PlotIndexSetInteger(PLOT_DECYCLER, PLOT_LINE_COLOR, 1, BlendToBg(InpShortColor, 35));
   PlotIndexSetInteger(PLOT_DECYCLER, PLOT_LINE_WIDTH, 2);
   PlotIndexSetString(PLOT_DECYCLER, PLOT_LABEL, "Adaptive Decycler");
   PlotIndexSetDouble(PLOT_DECYCLER, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   //--- RMS envelope (visibility = input, values always computed for logic)
   SetupLinePlot(PLOT_UPPER, BlendToBg(InpShortColor, 70), 1, "Upper RMS Band");
   SetupLinePlot(PLOT_LOWER, BlendToBg(InpLongColor, 70), 1, "Lower RMS Band");
   if(!InpShowEnvelope)
     {
      PlotIndexSetInteger(PLOT_UPPER, PLOT_DRAW_TYPE, DRAW_NONE);
      PlotIndexSetInteger(PLOT_LOWER, PLOT_DRAW_TYPE, DRAW_NONE);
     }
   //--- band fill (values go EMPTY when hidden; colors follow latest regime = D1)
   PlotIndexSetInteger(PLOT_FILL, PLOT_DRAW_TYPE, DRAW_FILLING);
   PlotIndexSetString(PLOT_FILL, PLOT_LABEL, "RMS Band Fill");
   PlotIndexSetDouble(PLOT_FILL, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   //--- signals (MPL: no LONG/SHORT text, D3)
   SetupArrowPlot(PLOT_LONG, 241, 6, 1, InpLongColor, "Long Signal");
   SetupArrowPlot(PLOT_SHORT, 242, -6, 1, InpShortColor, "Short Signal");
   if(!InpShowSignals)
     {
      PlotIndexSetInteger(PLOT_LONG, PLOT_DRAW_TYPE, DRAW_NONE);
      PlotIndexSetInteger(PLOT_SHORT, PLOT_DRAW_TYPE, DRAW_NONE);
     }
   //--- data-window only
   SetupNonePlot(PLOT_TRAIL,   "Supertrend Trail");
   SetupNonePlot(PLOT_EFF,     "Efficiency");
   SetupNonePlot(PLOT_CUTOFF,  "Adaptive Cutoff");
   SetupNonePlot(PLOT_RESID,   "Decycler Residual");
   SetupNonePlot(PLOT_RMS,     "Residual RMS");
   SetupNonePlot(PLOT_SQ,      "Regime");

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
         ComputeBar(i);                 // oldest -> newest: recursion order
         if(i >= 1)
            g_gate.Process(i, false);   // backfill: never alert
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
            g_gate.Process(j, true);    // realtime closed bars only
        }
      else
        {
         ComputeBar(0);
        }
     }

   //--- D1: band fill color follows the LATEST regime (2 static colors)
   int sq0 = IsNa(bSQ[0]) ? 1 : (int)MathRound(bSQ[0]);
   color fc = (sq0 == 1) ? g_fillBull : g_fillBear;
   PlotIndexSetInteger(PLOT_FILL, PLOT_LINE_COLOR, 0, fc);
   PlotIndexSetInteger(PLOT_FILL, PLOT_LINE_COLOR, 1, fc);

   if(prev_calculated == 0 || rates_total - prev_calculated > 0)
      ChartRedraw(0);
   return(rates_total);
  }
//+------------------------------------------------------------------+
