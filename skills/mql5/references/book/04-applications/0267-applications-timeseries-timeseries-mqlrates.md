# Getting quotes as an array of MqlRates structures

To request an array of quotes that includes all bar characteristics, use the CopyRates function which has multiple overloads.

int CopyRates(const string symbol, ENUM_TIMEFRAMES timeframe, int offset, int count, MqlRates &rates[])

int CopyRates(const string symbol, ENUM_TIMEFRAMES timeframe, datetime start, int count, MqlRates &rates[])

int CopyRates(const string symbol, ENUM_TIMEFRAMES timeframe, datetime start, datetime stop, MqlRates &rates[])

The function gets into the rates array historical data for the specified parameters: symbol, timeframe, and time range specified either by bar numbers or values start/stop of type datetime.

The function returns the number of array elements copied, or -1 in case of an error, the code of which can be found from [_LastError](/en/book/common/environment/env_last_error). In particular, an error will occur if a non-existent symbol is specified, the interval does not contain data on the server, or it goes beyond the limit on the number of bars on the chart ([TerminalInfoInteger](/en/book/common/environment/env_bar_lang) (TERMINAL_MAXBARS)).

The basics of working with this function are common to all Copy functions and were outlined in the section [Overview of Copy-functions for obtaining arrays of quotes](/en/book/applications/timeseries/timeseries_copy_funcs_overview).

Inline Type Structure MqlRates is described as follows:

```
struct MqlRates
{
   datetime time;         // bar opening time
   double   open;         // opening price
   double   high;         // maximum price per bar
   double   low;          // minimum price per bar
   double   close;        // closing price
   long     tick_volume;  // tick volume per bar
   int      spread;       // minimum spread per bar in points
   long     real_volume;  // exchange volume per bar
};

```

Let's try to apply the function for calculating the average size of bars in the script SeriesStats.mq5. In the input variables, we will provide the ability to select a working symbol, timeframe, the number of analyzed bars, and the initial offset to the past (0 means analysis from the current bar).

```
input string WorkSymbol = NULL; // Symbol (leave empty for current)
input ENUM_TIMEFRAMES TimeFrame = PERIOD_CURRENT;
input int BarOffset = 0;
input int BarCount = 10000;
 
void OnStart()
{
   MqlRates rates[];
   double range = 0, move = 0; // calculate the range and price movement in bars
   
   PrintFormat("Requesting %d bars on %s %s", 
      BarCount, StringLen(WorkSymbol) > 0 ? WorkSymbol : _Symbol, 
      EnumToString(TimeFrame == PERIOD_CURRENT ? _Period : TimeFrame));
   
   // request all information about BarCount bars to the MqlRates array
   const int n = PRTF(CopyRates(WorkSymbol, TimeFrame, BarOffset, BarCount, rates));
   
   // in the loop we calculate the average for the range and movement
   for(int i = 0; i < n; ++i)
   {
      range += (rates[i].high - rates[i].low) / n;
      move += (fmax(rates[i].open, rates[i].close)
             - fmin(rates[i].open, rates[i].close)) / n;
   }
   
   PrintFormat("Stats per bar: range=%f, movement=%f", range, move);
   PrintFormat("Dates: %s - %s", 
      TimeToString(rates[0].time), TimeToString(rates[n - 1].time));
}

```

Having thrown the script on the EURUSD,H1 chart, we can get approximately the following result.

```
Requesting 100000 bars on EURUSD PERIOD_H1
CopyRates(WorkSymbol,TimeFrame,BarOffset,BarCount,rates)=20018 / ok
Stats per bar: range=0.001280, movement=0.000621
Dates: 2018.07.19 15:00 - 2021.10.11 17:00

```

Since the terminal had a limit of 20,000 bars, a request for 100,000 bars could return only 20018 (the limit and newly formed bars after the session started). The very first element of the array (with index 0) contains a bar with the time 2018.07.19 15:00, and the last one – 2021.10.11 17:00.

According to the statistics, the average range of the bar during this time was 128 points, and the movement between open and close was 62 points.

When requesting information using a start and end date (start/stop) keep in mind that both boundaries are treated inclusively. Therefore, to set an interval corresponding to any bar of a higher timeframe, one should subtract 1 second from the right border. We will apply this technique in the example SeriesSpread.mq5 in the section [Reading price, volume, spread, and time by bar index](/en/book/applications/timeseries/timeseries_single_value).
