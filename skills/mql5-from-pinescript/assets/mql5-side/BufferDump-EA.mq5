//+------------------------------------------------------------------+
//|                                             BufferDump-EA.mq5    |
//|  Parity harness: dumps OHLC + all buffers of a custom indicator   |
//|  (via iCustom, default inputs) over the whole tester history, so  |
//|  a Python reference implementation of the Pine original can be    |
//|  compared bar-by-bar (skills/mql5-from-pinescript parity check).  |
//|                                                                    |
//|  Run headlessly:                                                   |
//|    mql5_helper.py init-ini BufferDump-EA.mq5 --symbol .. --model 0 |
//|    mql5_helper.py tester <ini> -o OUTDIR                           |
//|  Output: <terminal>/MQL5/Files/<InpOutFile> (or common folder),    |
//|  ASCENDING by time:                                                |
//|    time,open,high,low,close,b0,b1,...   (EMPTY_VALUE printed raw)  |
//|  Buffer order = the indicator's BUF_* define order.                |
//+------------------------------------------------------------------+
#property copyright "mql5-from-pinescript parity harness"
#property version   "1.00"
#property strict

input string InpIndicator = "AdaptiveDecyclerSupertrend"; // iCustom name (no path/ext)
input int    InpBuffers   = 16;                           // buffers to dump
input string InpOutFile   = "parity_0002.csv";            // output file name
input bool   InpUseCommon = true;                         // FILE_COMMON (else per-terminal)

int g_handle = INVALID_HANDLE;

//+------------------------------------------------------------------+
int OnInit()
  {
   g_handle = INVALID_HANDLE;
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   if(g_handle == INVALID_HANDLE)
     {
      g_handle = iCustom(_Symbol, _Period, InpIndicator);
      if(g_handle == INVALID_HANDLE)
         PrintFormat("BufferDump: iCustom(%s) failed err=%d", InpIndicator, GetLastError());
     }
   static int ticks = 0;
   ticks++;
   if(ticks == 100)
     {
      double probe[];
      int cp = CopyBuffer(g_handle, 0, 0, 3, probe);
      PrintFormat("probe#100: handle=%d BarsCalculated=%d bc_err=%d CopyBuffer=%d cb_err=%d",
                  g_handle, BarsCalculated(g_handle), GetLastError(), cp, GetLastError());
     }
  }

//+------------------------------------------------------------------+
//| Bulk export after the test: one CopyBuffer pass per buffer        |
//+------------------------------------------------------------------+
double OnTester()
  {
   if(g_handle == INVALID_HANDLE)
     {
      g_handle = iCustom(_Symbol, _Period, InpIndicator);
      if(g_handle == INVALID_HANDLE)
        {
         Print("BufferDump: iCustom failed");
         return(1.0);
        }
     }
   //--- pump: request data first (tester indicators may calculate lazily)
   double pump[];
   int pcp = CopyBuffer(g_handle, 0, 0, 3, pump);
   PrintFormat("OnTester pump: CopyBuffer=%d err=%d", pcp, GetLastError());
   //--- let the indicator finish its calculation
   int need = iBars(_Symbol, _Period);
   if(need < 100)
     {
      PrintFormat("BufferDump: only %d bars", need);
      return(1.0);
     }
   int calc = BarsCalculated(g_handle);
   if(calc <= 0)
     {
      PrintFormat("BufferDump: indicator not calculated (calc=%d err=%d)", calc, GetLastError());
      return(1.0);
     }
   datetime t[];
   double   o[], h[], l[], c[];
   ArraySetAsSeries(t, true);
   ArraySetAsSeries(o, true);
   ArraySetAsSeries(h, true);
   ArraySetAsSeries(l, true);
   ArraySetAsSeries(c, true);
   int got = MathMin(need, calc);
   if(CopyTime(_Symbol, _Period, 0, got, t) != got ||
      CopyOpen(_Symbol, _Period, 0, got, o) != got ||
      CopyHigh(_Symbol, _Period, 0, got, h) != got ||
      CopyLow(_Symbol, _Period, 0, got, l) != got ||
      CopyClose(_Symbol, _Period, 0, got, c) != got)
     {
      PrintFormat("BufferDump: Copy* failed err=%d", GetLastError());
      return(1.0);
     }
   //--- all[k*got + i] = buffer k at series index i (0 = newest)
   int nb = InpBuffers;
   double all[];
   ArrayResize(all, nb * got);
   ArraySetAsSeries(all, false);
   for(int k = 0; k < nb; k++)
     {
      double tmp[];
      ArraySetAsSeries(tmp, true);   // align with the as-series time/OHLC arrays
      int copied = CopyBuffer(g_handle, k, 0, got, tmp);
      for(int i = 0; i < got; i++)
         all[k * got + i] = (i < copied) ? tmp[i] : EMPTY_VALUE;
     }
   //--- write ASCENDING by time (oldest first)
   uint flags = FILE_WRITE | FILE_TXT | FILE_ANSI | (InpUseCommon ? FILE_COMMON : 0);
   int fh = FileOpen(InpOutFile, flags, "\n");
   if(fh == INVALID_HANDLE)
     {
      PrintFormat("BufferDump: FileOpen(%s) failed err=%d", InpOutFile, GetLastError());
      return(1.0);
     }
   string header = "time,open,high,low,close";
   for(int k = 0; k < nb; k++)
      header += ",b" + IntegerToString(k);
   FileWrite(fh, header);
   for(int i = got - 1; i >= 0; i--)
     {
      string row = TimeToString(t[i], TIME_DATE | TIME_MINUTES) + "," +
                   DoubleToString(o[i], 8) + "," + DoubleToString(h[i], 8) + "," +
                   DoubleToString(l[i], 8) + "," + DoubleToString(c[i], 8);
      for(int k = 0; k < nb; k++)
        {
         double v = all[k * got + i];
         row += "," + (IsNaVal(v) ? "EMPTY" : DoubleToString(v, 8));
        }
      FileWrite(fh, row);
     }
   FileClose(fh);
   PrintFormat("BufferDump: wrote %d bars x %d buffers -> %s", got, nb, InpOutFile);
   return(0.0);
  }

//+------------------------------------------------------------------+
bool IsNaVal(const double v)
  {
   return(v >= EMPTY_VALUE - 0.5 || v <= -EMPTY_VALUE + 0.5 || v != v);
  }
//+------------------------------------------------------------------+
