# Finding the maximum and minimum values in a timeseries

Among the group of functions for working with time series of quotes, there are two that provide the simplest aggregate processing: searching for the maximum and minimum values of the series at a given interval, respectively iHighest and iLowest.

int iHighest(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIESMODE type, int count = WHOLE_ARRAY, int offset = 0)

int iLowest(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIESMODE type, int count = WHOLE_ARRAY, int offset = 0)

The functions return the index of the largest/smallest value for a specific timeseries type, which is specified by a pair of symbol/timeframe parameters, as well as the ENUM_SERIESMODE enumeration element (it describes the quote fields already familiar to us).

| Identifier | Description |
| --- | --- |
| MODE_OPEN | Opening price |
| MODE_LOW | High price |
| MODE_HIGH | Low price |
| MODE_CLOSE | Closing price |
| MODE_VOLUME | Tick volume |
| MODE_REAL_VOLUME | Real volume |
| MODE_SPREAD | Spread |

The offset parameter specifies the index at which to start the search. Numbering is carried out as in a timeseries, that is, the increase in offset results in a shift to the past, and the 0-th index means the current bar (this is the default value). The number of analyzed bars is specified in the count parameter (WHOLE_ARRAY by default).

In case of an error, the functions return -1. Use [GetLastError](/en/book/common/environment/env_last_error) to find the error code.

To demonstrate how one of these functions works (iHighest), let's modify the example from the previous section on estimating the real sizes of spreads by bars and compare the results. Of course, they must match. The new version of the script is attached in the file SeriesSpreadHighest.mq5.

The changes affected the structure SpreadPerBar and the work cycle inside OnStart.

Fields have been added to the structure that allow you to understand how the new function works. Due to the nature of the algorithm, they are not obligatory.

```
struct SpreadPerBar
{
   datetime time;
   int spread;
   int max; // through index of the M1 bar with a spread, the value of which is maximum
            // among all M1-bars within the current bar of the higher timeframe
   int num; // number of M1 bars in the current bar of the higher timeframe
   int pos; // initial index of the M1 bar within the current bar of the higher timeframe
};

```

The main transformations affected OnStart, but they are localized inside the loop (all other code fragments remained unchanged).

```
   for(int i = 0; i < BarCount; ++i)
   {
      const datetime next = iTime(WorkSymbol, TimeFrame, i);
      const datetime prev = iTime(WorkSymbol, TimeFrame, i + 1);
      ...

```

The borders of the current bar, prev and next, are defined as before. However, instead of copying the timeseries elements between these labels into its own array spreads, and the subsequent call of ArrayMaximum for it, we determine the indexes and the number of M1 bars that form the current bar of the higher timeframe. This is done in the following way.

The iBarShift function allows you to find out the offset (variable p) in the history of M1, where the right border of the bar with time next - 1 is located. The bars function calculates the number of M1 bars (variable n) falling between prev and next - 1. These two values become parameters in the iHighest function call made to find the maximum value of type MODE_SPREAD, among n M1 bars, starting from the index p. If the maximum is found without problems (m > -1), it remains for us to take the corresponding value using iSpread and place it in a structure.

```
      const int p = iBarShift(WorkSymbol, PERIOD_M1, next - 1);
      const int n = Bars(WorkSymbol, PERIOD_M1, prev, next - 1);
      const int m = iHighest(WorkSymbol, PERIOD_M1, MODE_SPREAD, n, p);
      if(m > -1)
      {
         peaks[i].spread = iSpread(WorkSymbol, PERIOD_M1, m);
         peaks[i].time = prev;
         peaks[i].max = m;
         peaks[i].num = n;
         peaks[i].pos = p;
      }
   }

```

When outputting the array with the results to the log, we will now additionally see the indexes of M1 bars, where the bar of the higher timeframe "begins" and where the maximum spread was found in it. The word "begins" is in quotation marks, because as new M1 bars arrive, these indexes will increase, and the virtual "beginning" of each will shift, although the opening times of historical bars, of course, remain constant.

```
Maximal speeds per intraday bar
Processed 100 bars on EURUSD PERIOD_H1
               [time] [spread] [max] [num] [pos]
[ 0] 2021.10.12 15:00        0     7    60     7
[ 1] 2021.10.12 14:00        1    89    60    67
[ 2] 2021.10.12 13:00        1   181    60   127
[ 3] 2021.10.12 12:00        1   213    60   187
[ 4] 2021.10.12 11:00        1   248    60   247
[ 5] 2021.10.12 10:00        0   307    60   307
[ 6] 2021.10.12 09:00        1   385    60   367
[ 7] 2021.10.12 08:00        2   469    60   427
[ 8] 2021.10.12 07:00        2   497    60   487
[ 9] 2021.10.12 06:00        1   550    60   547
[10] 2021.10.12 05:00        1   616    60   607
[11] 2021.10.12 04:00        1   678    60   667
[12] 2021.10.12 03:00        1   727    60   727
[13] 2021.10.12 02:00        4   820    60   787
[14] 2021.10.12 01:00       16   906    60   847
[15] 2021.10.12 00:00       65   956    60   907
[16] 2021.10.11 23:00       15   967    60   967
[17] 2021.10.11 22:00        2  1039    60  1027
[18] 2021.10.11 21:00        1  1090    60  1087
[19] 2021.10.11 20:00        1  1148    60  1147
[20] 2021.10.11 19:00        2  1210    60  1207
[21] 2021.10.11 18:00        1  1313    60  1267
[22] 2021.10.11 17:00        1  1345    60  1327
[23] 2021.10.11 16:00        1  1411    60  1387
[24] 2021.10.11 15:00        2  1461    60  1447
[25] 2021.10.11 14:00        1  1526    60  1507
...

```

For example, at the time the script was launched, the bar with the label 2021.10.12 14:00 started from the 67th bar M1 (i.e. it was opened 67 minutes ago), and the M1 bar with the maximum spread inside this H1 bar was found under the index 89. Obviously, this index should be less than the number of the M1 bar where the previous H1 bar started: 2021.10.12 13:00 — it was marked 127 minutes ago. In this H1 bar, in turn, the maximum spread for the 181 index was found. And this is less than the index 187 for an even older bar 2021.10.12 12:00.

Indexes in the pos and max columns are constantly increasing because we walk around the bars in order from the present to the past. The num column will almost have 60  since most H1 bars are made up of 60 M1 bars. But this is not always the case. For example, below are incomplete hourly bars, consisting of fewer minutes: this can be either the consequences of an earlier market close due to the holiday schedule, or real gaps in trading activity (lack of liquidity).

```
...
[38] 2021.10.11 01:00       20  2346    60  2287
[39] 2021.10.11 00:00       85  2404    58  2347
[40] 2021.10.08 23:00       15  2406    55  2405
[41] 2021.10.08 22:00        2  2463    60  2460
...

```
