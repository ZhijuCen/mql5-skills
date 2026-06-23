# Reading price, volume, spread, and time by bar index

Sometimes you need to find out information not about a sequence of bars but only about one bar. In theory, this can be done by using the previously discussed Copy functions, specifying in them the quantity (parameter count) equal to 1, but this is not very convenient. A simpler version is offered by the following functions, which return one value of a certain type for a bar by its number in the timeseries.

All functions have a similar prototype but different names and return types. Historically, names begin with the prefix i, that is, have the form iValue (these functions belong to a large group of built-in technical indicators: after all, the characteristics of quotes are the primary source for technical analysis, and almost all indicators are their derivatives, hence the letter i).

type iValue(const string symbol, ENUM_TIMEFRAMES timeframe, int offset)

Here type corresponds to one of the types datetime, double, long, or int, depending on the specific function. Symbol and timeframe identify the requested timeseries. Required bar index offset is passed in timeseries notation: 0 means the most recent, right bar (usually not completed yet), and higher numbers mean older bars. As in the case of Copy functions, NULL and 0 can be used to set the symbol and period to be equal to the properties of the current chart.

Because i functions are equivalent to calling Copy functions, all features of requesting timeseries from different types of programs, described in the section [Overview of Copy functions for obtaining arrays of quotes](/en/book/applications/timeseries/timeseries_copy_funcs_overview) are applicable to them.

| Function | Description |
| --- | --- |
| iTime | Bar opening time |
| iOpen | Bar opening price |
| iHigh | Bar high price |
| iLow | Bar low price |
| iClose | Bar closing price |
| iTickVolume | Bar tick volume (similar to iVolume) |
| iVolume | Bar tick volume (similar to iTickVolume) |
| iRealVolume | Real trading volume of the bar |
| iSpread | Minimum bar spread (in pips) |

The functions return the requested value or 0 on error (unfortunately, 0 can be a real value in some cases). To get more information about the error, call the [GetLastError](/en/book/common/environment/env_last_error) function.

The functions do not cache the results. On each call, they return actual data from the timeseries for the specified symbol/period. This means that in the absence of ready data (on the first call, or after a loss of synchronization), the function may take some time to prepare the result.

As an example, let's try to obtain a more or less realistic estimate of the spread size for each bar. The minimum spread value is stored in the quotes, which can cause unreasonably high expectations when designing trading strategies. To obtain absolutely accurate values of the average, median or maximum spread per bar, it would be necessary to analyze real ticks, but we have not yet learned how to work with them. And besides, it would be a very resource-intensive process. A more rational approach is to analyze spreads on the lower M1 timeframe: for bars of higher timeframes, it is enough to look for the maximum spread in the inside bars of M1. Of course, strictly speaking, it will not be the maximum, but the maximum of the minimum values, but given the transience of minute readings, we may hope to detect characteristic spread expansions at least on some M1 bars, and this is enough to get an acceptable ratio of analysis accuracy and speed.

One of the versions of the algorithm is implemented in the script SeriesSpread.mq5. In the input variables, you can set the symbol, timeframe, and the number of bars for analysis. By default, the symbol of the current chart and its period are processed (should be greater than M1).

```
input string WorkSymbol = NULL; // Symbol (leave empty for current)
input ENUM_TIMEFRAMES TimeFrame = PERIOD_CURRENT;
input int BarCount = 100;

```

Since only information about its time and spread is important for each bar, a special structure with two fields was described. We could use the standard MqlRates structure and add "maximum" spreads to some unused field (for example, real_volume for Forex symbols), but then the data for most fields would be copied and memory would be wasted.

```
struct SpreadPerBar
{
   datetime time;
   int spread;
};

```

Using the new structure type, we prepare the peaks array to calculate the data of the specified number of bars.

```
void OnStart()
{
   SpreadPerBar peaks[];
   ArrayResize(peaks, BarCount);
   ZeroMemory(peaks);
   ...

```

Further along, the main part of the algorithm is executed in the bar loop. For each bar, we used the function iTime to determine two timestamps that define the boundaries of the bar. In fact, this is the opening time of the i-th bar and the neighboring (i+1)-th bar. Given the principles of indexing, we can say that the (i+1)th bar is the previous bar (older, see variable prev) and i-th is the next one (newer, see variable next). The bar opening time belongs to only one bar, that is, the label prev is contained in the (i+1)-th bar, and the label next is in the i-th one. Thus, when processing each bar, its right border should be excluded from the interval [prev;next).

We are interested in spreads on a one-minute timeframe, and therefore we will use the CopySpread function for PERIOD_M1. In this case, the half-open interval is achieved by setting the start/stop parameters to the exact prev value and the next value reduced by 1 second. Spread information is copied to the dynamic array spreads (memory for it is allocated by the function itself).

```
   for(int i = 0; i < BarCount; ++i)
   {
      int spreads[]; // receiving array for M1 spreads inside the i-th bar
      const datetime next = iTime(WorkSymbol, TimeFrame, i);
      const datetime prev = iTime(WorkSymbol, TimeFrame, i + 1);
      const int n = CopySpread(WorkSymbol, PERIOD_M1, prev, next - 1, spreads);
      const int m = ArrayMaximum(spreads);
      if(m > -1)
      {
         peaks[i].spread = spreads[m];
         peaks[i].time = prev;
      }
   }

```

Then, we find the maximum value in this array and save it in the appropriate structure SpreadPerBar along with the bar time. Please note that the zero incomplete bar is not included in the analysis (you can supplement the algorithm if necessary).

After the loop is completed, we output an array of structures to the journal.

```
   PrintFormat("Maximal speeds per intraday bar\nProcessed %d bars on %s %s", 
      BarCount, StringLen(WorkSymbol) > 0 ? WorkSymbol : _Symbol, 
      EnumToString(TimeFrame == PERIOD_CURRENT ? _Period : TimeFrame));
   ArrayPrintM(peaks);

```

By running the script on the EURUSD,H1 chart, we will get spread statistics inside hourly bars (abridged):

```
Maximal speeds per intraday bar
Processed 100 bars on EURUSD PERIOD_H1
[ 0] 2021.10.12 14:00        1
[ 1] 2021.10.12 13:00        1
[ 2] 2021.10.12 12:00        1
[ 3] 2021.10.12 11:00        1
[ 4] 2021.10.12 10:00        0
[ 5] 2021.10.12 09:00        1
[ 6] 2021.10.12 08:00        2
[ 7] 2021.10.12 07:00        2
[ 8] 2021.10.12 06:00        1
[ 9] 2021.10.12 05:00        1
[10] 2021.10.12 04:00        1
[11] 2021.10.12 03:00        1
[12] 2021.10.12 02:00        4
[13] 2021.10.12 01:00       16
[14] 2021.10.12 00:00       65
[15] 2021.10.11 23:00       15
[16] 2021.10.11 22:00        2
[17] 2021.10.11 21:00        1
[18] 2021.10.11 20:00        1
[19] 2021.10.11 19:00        2
[20] 2021.10.11 18:00        1
[21] 2021.10.11 17:00        1
[22] 2021.10.11 16:00        1
[23] 2021.10.11 15:00        2
[24] 2021.10.11 14:00        1

```

There is an obvious increase in spreads at night: for example, close to midnight, quotes contain spreads of 7-15 points, and in our measurements, they are 15-65. However, non-zero values are also found in other periods, although the metrics of hourly bars usually contain zeros.
