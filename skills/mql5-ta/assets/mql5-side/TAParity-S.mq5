//+------------------------------------------------------------------+
//|                                                  TAParity-S.mq5  |
//|  mql5-ta skill: numeric parity export.                           |
//|  Exports the last N bars of XAUUSD M1 together with MQL5 values  |
//|  of the mapped indicators (same bars, same range) so that        |
//|  scripts/parity_check.py can compare them against TA-Lib.        |
//|  Usage: drag onto any chart of a LIVE terminal (symbol/timeframe |
//|  of the export are fixed by inputs, not by the chart).           |
//|  Output: MQL5/Files/ta_parity_XAUUSD_M1.csv, ASCENDING by time,  |
//|  header: time,open,high,low,close,tickvol,<indicator columns>.   |
//+------------------------------------------------------------------+
#property script_show_inputs
#property strict

input string         InpSymbol   = "XAUUSD";       // Symbol
input ENUM_TIMEFRAMES InpTF      = PERIOD_M1;      // Timeframe
input int            InpBars     = 1000;           // Bars to export

#define NIND 17

string ind_name[NIND] = {
   "RSI14", "ATR14", "CCI14", "WILLR14",          // Wilder / classic oscillators
   "STOCH_K", "STOCH_D",                          // iStochastic
   "SMA10", "EMA10", "SMMA10", "LWMA10",          // iMA methods
   "MACD_MAIN", "MACD_SIG", "OSMA",               // iMACD / iOsMA (SMA signal!)
   "ADXW14", "PLUSDI14", "MINUSDI14",             // iADXWilder
   "ADX14_STD"                                    // iADX (expected to differ from talib)
};
string handles_desc[NIND] = {
   "iRSI(14)", "iATR(14)", "iCCI(14)", "iWPR(14)",
   "iStochastic(5,3,3) MAIN", "iStochastic(5,3,3) SIGNAL",
   "iMA(10,SMA,CLOSE)", "iMA(10,EMA,CLOSE)", "iMA(10,SMMA,CLOSE)", "iMA(10,LWMA,CLOSE)",
   "iMACD(12,26,9) MAIN", "iMACD(12,26,9) SIGNAL", "iOsMA(12,26,9)",
   "iADXWilder(14) MAIN", "iADXWilder(14) +DI", "iADXWilder(14) -DI",
   "iADX(14) MAIN"
};

//+------------------------------------------------------------------+
int OnStart()
{
   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   int got = CopyRates(InpSymbol, InpTF, 0, InpBars, rates);
   if(got <= 0)
   {
      PrintFormat("TAParity: CopyRates failed (err %d)", GetLastError());
      return 1;
   }
   PrintFormat("TAParity: %d bars %s %s (%s .. %s)", got, InpSymbol,
               EnumToString(InpTF),
               TimeToString(rates[0].time), TimeToString(rates[got-1].time));

   // one handle per (buffer) row; ADXWilder needs 3 buffers, Stochastic 2
   int h_rsi   = iRSI(InpSymbol, InpTF, 14, PRICE_CLOSE);
   int h_atr   = iATR(InpSymbol, InpTF, 14);
   int h_cci   = iCCI(InpSymbol, InpTF, 14, PRICE_TYPICAL);
   int h_wpr   = iWPR(InpSymbol, InpTF, 14);
   int h_stoch = iStochastic(InpSymbol, InpTF, 5, 3, 3, MODE_SMA, STO_LOWHIGH);
   int h_maS   = iMA(InpSymbol, InpTF, 10, 0, MODE_SMA,  PRICE_CLOSE);
   int h_maE   = iMA(InpSymbol, InpTF, 10, 0, MODE_EMA,  PRICE_CLOSE);
   int h_maSm  = iMA(InpSymbol, InpTF, 10, 0, MODE_SMMA, PRICE_CLOSE);
   int h_maL   = iMA(InpSymbol, InpTF, 10, 0, MODE_LWMA, PRICE_CLOSE);
   int h_macd  = iMACD(InpSymbol, InpTF, 12, 26, 9, PRICE_CLOSE);
   int h_osma  = iOsMA(InpSymbol, InpTF, 12, 26, 9, PRICE_CLOSE);
   int h_adxw  = iADXWilder(InpSymbol, InpTF, 14);
   int h_adx   = iADX(InpSymbol, InpTF, 14);

   int handles[] = {h_rsi, h_atr, h_cci, h_wpr, h_stoch, h_stoch,
                    h_maS, h_maE, h_maSm, h_maL,
                    h_macd, h_macd, h_osma,
                    h_adxw, h_adxw, h_adxw, h_adx};
   int buffers[] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0};

   double all[];                            // all[k*got + i] = indicator k at bar i
   ArrayResize(all, NIND * got);
   ArraySetAsSeries(all, false);
   double tmp[];
   ArraySetAsSeries(tmp, false);
   for(int k = 0; k < NIND; k++)
   {
      if(CopyBuffer(handles[k], buffers[k], 0, got, tmp) != got)
      {
         PrintFormat("TAParity: CopyBuffer %s failed (err %d) - need chart history",
                     ind_name[k], GetLastError());
         return 2;
      }
      for(int i = 0; i < got; i++)
         all[k * got + i] = tmp[i];
   }

   string fname = "ta_parity_" + InpSymbol + "_" + StringSubstr(EnumToString(InpTF), 7) + ".csv";
   int f = FileOpen(fname, FILE_WRITE|FILE_CSV|FILE_ANSI, ',');
   if(f == INVALID_HANDLE)
   {
      PrintFormat("TAParity: cannot open %s (err %d)", fname, GetLastError());
      return 3;
   }
   string header = "time,open,high,low,close,tickvol";
   for(int k = 0; k < NIND; k++)
      header += "," + ind_name[k];
   FileWrite(f, header);

   for(int i = 0; i < got; i++)            // ascending by time
   {
      string row = TimeToString(rates[i].time, TIME_DATE|TIME_MINUTES) + "," +
                   DoubleToString(rates[i].open, 5) + "," +
                   DoubleToString(rates[i].high, 5) + "," +
                   DoubleToString(rates[i].low, 5) + "," +
                   DoubleToString(rates[i].close, 5) + "," +
                   IntegerToString(rates[i].tick_volume);
      for(int k = 0; k < NIND; k++)
         row += "," + DoubleToString(all[k * got + i], 10);
      FileWrite(f, row);
   }
   FileClose(f);
   PrintFormat("TAParity: wrote %s (%d rows)", fname, got);
   return 0;
}
//+------------------------------------------------------------------+
