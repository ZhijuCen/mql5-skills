# Working with real tick arrays in MqlTick structures

MetaTrader 5 provides the ability to work not only with the history of quotes (bars) but also with the history of real ticks. From the user interface, all historical data is available in the Symbols dialog. It has three tabs: Specification, Bars, and Ticks. When a specific element is selected in the tree-like list of symbols on the first tab, then when switching to tabs Bars and Ticks you can request quotes in the form of bars or ticks, respectively.

From MQL programs, the history of real ticks is also available using the CopyTicks and CopyTicksRange functions.

int CopyTicks(const string symbol, MqlTick &ticks[], uint flags = COPY_TICKS_ALL, ulong from = 0, uint count = 0)

int CopyTicksRange(const string symbol, MqlTick &ticks[], uint flags = COPY_TICKS_ALL, ulong from = 0, ulong to = 0)

Both functions request ticks for the specified instrument symbol into the array ticks passed by reference. Structure MqlTick contains all information about one tick and is described in MQL5 as follows:

```
struct MqlTick
{
   datetime time;        // time of this price update
   double   bid;         // current Bid price
   double   ask;         // current Ask price
   double   last;        // Last trade price
   ulong    volume;      // volume for Last price
   long     time_msc;    // time of this price update in milliseconds
   uint     flags;       // flags (which fields of the structure have changed)
   double   volume_real; // volume for the Last price with increased accuracy
};

```

The flags field is intended for storing a bit mask of signs, which fields in the tick structure contain changed values.

| Constant | Value | Description |
| --- | --- | --- |
| TICK_FLAG_BID | 2 | Bid price changed |
| TICK_FLAG_ASK | 4 | Ask price changed |
| TICK_FLAG_LAST | 8 | Last price changed |
| TICK_FLAG_VOLUME | 16 | Volume changed |
| TICK_FLAG_BUY | 32 | Tick was generated as a result of a buy trade |
| TICK_FLAG_SELL | 64 | Tick was generated as a result of a sell trade |

This was required because every tick always fills in all fields, regardless of whether the data has changed compared to the previous tick. This allows you to always have the current state of prices at any time without looking for previous values in the tick history. For example, only the Bid price could change with a tick, but in addition to the new price, other parameters will be indicated in the structure: previous Ask, Last, volume and so on.

At the same time, you should keep in mind that, depending on the type of instrument, some fields in ticks can always be zero (and the corresponding mask bits are never set for them). In particular, for Forex instruments, as a rule, the last, volume, volume_real fields remain empty.

The receiving ticks array can be of fixed size or dynamic. The functions will copy no more ticks into a fixed array than the size of the array, regardless of the actual number of ticks in the requested time interval (specified by the from/to parameters in the CopyTicksRange function) or in the count parameter of the CopyTicks function. In the ticks array, the oldest ticks are placed first, and the newest ticks are placed last.

In the parameters of both functions, time readings are specified as milliseconds since 01.01.1970 00:00:00. In the CopyTicks function, the range of requested ticks is set by the initial from and the number of ticks count, and in CopyTicksRange it is set by from and to (both values are included).

In other words, CopyTicksRange is designed to receive ticks in a specific interval, and their number is not known in advance. CopyTicks guarantees no more than count ticks but does not allow you to determine in advance what time interval these ticks will cover.

Chronological order of from and to values in CopyTicksRange is not important: the function will give ticks in any case, starting from the minimum of the two values, and ending with the maximum.

The CopyTicks function evaluates the from parameter as the left border with the minimum time and counts from it count ticks to the future. However, there is an important exception: from = 0 (by default) is treated as the current moment in time, and ticks are counted from it into the past. This makes it possible to always get the specified number of last ticks. When count = 0 (by default), the function copies no more than 2000 ticks.

Both functions return the number of copied ticks or -1 in case of an error. In particular, GetLastError may return the following error codes:

- ERR_HISTORY_TIMEOUT — tick synchronization timeout has expired, the function returned everything it had.
- ERR_HISTORY_SMALL_BUFFER — the static buffer is too small, so it gives as much as fits in the array.
- ERR_NOT_ENOUGH_MEMORY — failed to allocate the required amount of memory to get the history of ticks from the specified range into a dynamic array.

The flags parameter defines the type of ticks requested.

| Constant | Value | Description |
| --- | --- | --- |
| COPY_TICKS_INFO | 1 | Ticks caused by changes of  Bid  and/or  Ask 
 (TICK_FLAG_BID, TICK_FLAG_ASK) |
| COPY_TICKS_TRADE | 2 | Ticks with of  Last  and  Volume  changes 
 (TICK_FLAG_LAST, TICK_FLAG_VOLUME, TICK_FLAG_BUY, TICK_FLAG_SELL) |
| COPY_TICKS_ALL | 3 | All ticks |

For any request types, the remaining fields of the MqlTick structure, which do not match the flags, will contain the previous actual values. For example, if only information ticks (COPY_TICKS_INFO) were requested, the remaining fields will still be filled in them. It means that if only the Bid price has changed, the last known values will be written in the ask and volume fields. To find out what has changed in the tick, analyze its flags field (there will be either the value TICK_FLAG_BID, or TICK_FLAG_ASK, or a combination of both). If a tick has zero values of the Bid and Ask prices, and the flags indicate that these prices have changed (flags == TICK_FLAG_BID | TICK_FLAG_ASK), then this indicates the emptying of the order book.

Similarly, if trading ticks were requested (COPY_TICKS_TRADE), the last known price values will be recorded in their bid and ask fields. In this case, the flags field may have a combination of TICK_FLAG_LAST, TICK_FLAG_VOLUME, TICK_FLAG_BUY, TICK_FLAG_SELL.

When requesting COPY_TICKS_ALL, all ticks are returned.

Calling any of the CopyTicks/CopyTicksRange functions checks the synchronization of the tick base stored on the hard disk for the given symbol. If there are not enough ticks in the local database, then the missing ticks will be automatically downloaded from the trade server. In this case, ticks will be synchronized taking into account the oldest date from the query parameters and up to the current moment. After that, all incoming ticks for this symbol will go to the tick database and keep it up to date in a synchronized state.

Tick data is much larger than minute quotes. When you first request a tick history or start testing [by real ticks](/en/book/automation/tester/tester_ticks), downloading them can take a long time. The history of tick data is stored in files in the internal TKC format in the directory {terminal_dir}/bases/{server_name}/ticks/{symbol_name}. Each file contains information for one month.

In indicators, the functions return the result immediately, that is, they copy the available ticks by symbol and start the background process of tick base synchronization if there is not enough data. All indicators on one symbol work in one common [thread](/en/book/applications/runtime/runtime_threads), so they don't have a right to wait for the synchronization to complete. After the end of synchronization, the next call of the function will return all the requested ticks.

In Expert Advisors and scripts, functions can wait for up to 45 seconds for a result: unlike an indicator, each Expert Advisor and script runs in its own thread and therefore can wait for synchronization to complete within a timeout. If during this time ticks are still not synchronized in the required amount, then only available ticks will be returned, and synchronization will continue in the background.

Recall that real-time ticks are broadcast to charts as events: indicators receive notifications of new ticks in the [OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate) handler, while Expert Advisors receive them in the [OnTick](/en/book/automation/experts/experts_ontick) handler. It should be borne in mind that the system does not guarantee the delivery of all events. If new ticks arrive in the terminal while the program is processing the current OnCalculate/OnTick event, new events for this "busy" program may not be added to its queue (see section [Overview of event handling functions](/en/book/applications/runtime/runtime_events_overview)). Moreover, several ticks can arrive at the same time, but only one event will be generated for each MQL program: the current market state event. In this case, you can use the CopyTicks function to request all ticks that have come since the previous processing of the event. Here is what this algorithm looks like in pseudocode:

```
void processAllTicks()
{
   static ulong prev = 0;
   if(!prev)
   {
      MqlTick ticks[];
      const int n = CopyTicks(_Symbol, ticks, COPY_TICKS_ALL, prev + 1, 1000000);
      if(n > 0)
      {
         prev = ticks[n - 1].time_msc;
         ... // processing all missed ticks
      }
   }
   else
   {
      MqlTick tick;
      SymbolInfoTick(_Symbol, tick);
      prev = tick.time_msc;
      ... // processing the first tick
   }
} 

```

The SymbolInfoTick function used here populates a single MqlTick structure passed by reference with the last tick data. We will study it in a separate [section](/en/book/automation/symbols/symbols_tick).

Note that when calling CopyTicks, one millisecond is added to the old timestamp prev. This ensures that the previous tick is not processed again. However, if there were several ticks within one millisecond corresponding to prev, this algorithm will skip them. If you want to cover absolutely all ticks, you should remember the number of available ticks with the prev time while updating the prev variable. On the next CopyTicks call, query ticks from the prev moment and skip (ignore in the array) the number of "old" ticks.

However, please note that the above algorithm is not required by every MQL program. Most of them do not analyze each tick, while the current price state corresponding to the last known tick is quickly broadcast to charts in the [events](/en/book/applications/runtime/runtime_events_overview) model and is available through [symbol](/en/book/automation/symbols/symbols_info) and [chart](/en/book/applications/charts/charts_properties_overview) properties.

To demonstrate the functions, let's consider two examples, one for each function. For both examples, a common header file TickEnum.mqh was developed, where the above constants for requested tick flags and tick status flags are summarized into two enumerations.

```
enum COPY_TICKS
{
   ALL_TICKS = /* -1 */ COPY_TICKS_ALL,    // all ticks
   INFO_TICKS = /* 1 */ COPY_TICKS_INFO,   // info ticks
   TRADE_TICKS = /* 2 */ COPY_TICKS_TRADE, // trade ticks
};
 
enum TICK_FLAGS
{
   TF_BID = /* 2 */ TICK_FLAG_BID, 
   TF_ASK = /* 4 */ TICK_FLAG_ASK, 
   TF_BID_ASK = TICK_FLAG_BID | TICK_FLAG_ASK, 
   
   TF_LAST = /* 8 */ TICK_FLAG_LAST, 
   TF_BID_LAST = TICK_FLAG_BID | TICK_FLAG_LAST, 
   TF_ASK_LAST = TICK_FLAG_ASK | TICK_FLAG_LAST, 
   TF_BID_ASK_LAST = TF_BID_ASK | TICK_FLAG_LAST, 
   
   TF_VOLUME = /* 16 */ TICK_FLAG_VOLUME, 
   TF_LAST_VOLUME = TICK_FLAG_LAST | TICK_FLAG_VOLUME, 
   TF_BID_VOLUME = TICK_FLAG_BID | TICK_FLAG_VOLUME, 
   TF_BID_ASK_VOLUME = TF_BID_ASK | TICK_FLAG_VOLUME, 
   TF_BID_ASK_LAST_VOLUME = TF_BID_ASK | TF_LAST_VOLUME, 
   
   TF_BUY = /* 32 */ TICK_FLAG_BUY, 
   TF_SELL = /* 64 */ TICK_FLAG_SELL, 
   TF_BUY_SELL = TICK_FLAG_BUY | TICK_FLAG_SELL, 
   TF_LAST_VOLUME_BUY = TF_LAST_VOLUME | TICK_FLAG_BUY, 
   TF_LAST_VOLUME_SELL = TF_LAST_VOLUME | TICK_FLAG_SELL, 
   TF_LAST_VOLUME_BUY_SELL = TF_BUY_SELL | TF_LAST_VOLUME, 
   ...
};

```

The use of enumerations makes type checking in source code more rigorous, and it also makes it easier to display the meaning of values as strings with [EnumToString](/en/book/common/conversions/conversions_enums). In addition, the most popular combinations of flags have been added to the TICK_FLAGS enumeration to optimize the visualization or filtering of ticks. It is not possible to give enumeration elements the same names as built-in constants, as a name conflict occurs.

The first script SeriesTicksStats.mq5 uses the CopyTicks function to count the number of ticks with different flags set to a given history depth.

In the input parameters, you can set the working symbol (chart symbol by default), the number of analyzed ticks, and the request mode from COPY_TICKS.

```
input string WorkSymbol = NULL; // Symbol (leave empty for current)
input int TickCount = 10000;
input COPY_TICKS TickType = ALL_TICKS;

```

The statistics of the occurrence of each flag (each bit in the bit mask) in the tick properties are collected in the TickFlagStats structure.

```
struct TickFlagStats
{
   TICK_FLAGS flag; // mask with bit (one or more)
   int count;       // number of ticks with this bit in the flags field 
   string legend;   // bit description
};

```

The OnStart function describes an array of TickFlagStats structures with a size of 8 elements: 6 of them (from 1 to 6 inclusive) are used for the corresponding TICK_FLAG bits, and the other two are used for bit combinations (see below). Using a simple loop, elements for individual standard bits/flags are filled in the array, and after the loop, two combined masks are filled (in the 0th element, ticks will be counted with a simultaneous change of Bid and Ask, and in the 7th element we count ticks with simultaneous Buy and Sell deals).

```
void OnStart()
{
   TickFlagStats stats[8] = {};
   for(int k = 1; k < 7; ++k)
   {
      stats[k].flag = (TICK_FLAGS)(1 << k);
      stats[k].legend = EnumToString(stats[k].flag);
   }
   stats[0].flag = TF_BID_ASK;  // combination of BID AND ASK
   stats[7].flag = TF_BUY_SELL; // combination of BUY AND SELL
   stats[0].legend = "TF_BID_ASK (COMBO)";
   stats[7].legend = "TF_BUY_SELL (COMBO)";
   ...

```

We will entrust all the main work to the auxiliary function CalcTickStats, passing input parameters and a prepared array for collecting statistics to it. After that, it remains to display the counted numbers in the journal.

```
   const int count = CalcTickStats(TickType, 0, TickCount, stats);
   PrintFormat("%s stats requested: %d (got: %d) on %s", 
      EnumToString(TickType),
      TickCount, count, StringLen(WorkSymbol) > 0 ? WorkSymbol : _Symbol);
   ArrayPrint(stats);
}

```

The CalcTickStats function itself is very interesting.

```
int CalcTickStats(const string symbol, const COPY_TICKS type, 
   const datetime start, const int count, 
   TickFlagStats &stats[])
{
   MqlTick ticks[];
   ResetLastError();
   const int nf = ArraySize(stats);
   const int nt = CopyTicks(symbol, ticks, type, start * 1000, count);
   if(nt > -1 && _LastError == 0)
   {
      PrintFormat("Ticks range: %s'%03d - %s'%03d", 
         TimeToString(ticks[0].time, TIME_DATE | TIME_SECONDS),
         ticks[0].time_msc % 1000, 
         TimeToString(ticks[nt - 1].time, TIME_DATE | TIME_SECONDS),
         ticks[nt - 1].time_msc % 1000);
      
      // loop through ticks
      for(int j = 0; j < nt; ++j)
      {
         // loop through TICK_FLAGs (2 4 8 16 32 64) and combinations
         for(int k = 0; k < nf; ++k)
         {
            if((ticks[j].flags & stats[k].flag) == stats[k].flag)
            {
               stats[k].count++;
            }
         }
      }
   }
   return nt;
}

```

It uses CopyTicks to request ticks of the specified symbol, of a specific type, starting from the start date, in the amount of count items. The start parameter is of the type datetime, and it must be converted to milliseconds when passed to CopyTicks. Recall that if start = 0 (which is the case here, in the OnStart function), the system will return the last ticks, counting from the current time. Therefore, each time the script is called, the statistics will most likely be updated due to the arrival of new ticks. The only possible exceptions are requests on weekends or those for low-liquid instruments.

If CopyTicks executes without errors, our code logs the time range covered by the received ticks.

Finally, in the loop, we go through all the ticks and count the number of bitwise matches in the tick flags and element masks in the array of statistical structures TickFlagStats prepared in advance.

It is advisable to run the script on instruments where there is information about real volumes and deals in order to test all modes from the COPY_TICKS enumeration (remember, they correspond to the constants for the flags parameter in CopyTicks: COPY_TICKS_INFO, COPY_TICKS_TRADE and COPY_TICKS_ALL).

Here is an example of log entries when requesting statistics for 100000 ticks of all types (TickType = ALL_TICKS):

```
Ticks range: 2021.10.11 07:39:53'278 - 2021.10.13 11:51:29'428
ALL_TICKS stats requested: 100000 (got: 100000) on YNDX.MM
    [flag] [count]              [legend]
[0]      6   11323 "TF_BID_ASK (COMBO)" 
[1]      2   26700 "TF_BID"             
[2]      4   33541 "TF_ASK"             
[3]      8   51082 "TF_LAST"            
[4]     16   51082 "TF_VOLUME"          
[5]     32   25654 "TF_BUY"             
[6]     64   28802 "TF_SELL"            
[7]     96    3374 "TF_BUY_SELL (COMBO)"

```

Here is what you get when requesting only information ticks (TickType = INFO_TICKS).

```
Ticks range: 2021.10.07 07:08:24'692 - 2021.10.13 11:54:01'297
INFO_TICKS stats requested: 100000 (got: 100000) on YNDX.MM
    [flag] [count]              [legend]
[0]      6   23115 "TF_BID_ASK (COMBO)" 
[1]      2   60860 "TF_BID"             
[2]      4   62255 "TF_ASK"             
[3]      8       0 "TF_LAST"            
[4]     16       0 "TF_VOLUME"          
[5]     32       0 "TF_BUY"             
[6]     64       0 "TF_SELL"            
[7]     96       0 "TF_BUY_SELL (COMBO)"

```

Here you can check the accuracy of the calculations: the sum of the numbers for TF_BID and TF_ASK minus the matches TF_BID_ASK (COMBO) gives exactly 100000 (total number of ticks). Ticks with volumes and Last prices did not get into the result, as it was expected.

Now let's run the script again, exclusively for trading ticks (TickType = TRADE_TICKS).

```
Ticks range: 2021.10.06 20:43:40'024 - 2021.10.13 11:52:40'044
TRADE_TICKS stats requested: 100000 (got: 100000) on YNDX.MM
    [flag] [count]              [legend]
[0]      6       0 "TF_BID_ASK (COMBO)" 
[1]      2       0 "TF_BID"             
[2]      4       0 "TF_ASK"             
[3]      8  100000 "TF_LAST"            
[4]     16  100000 "TF_VOLUME"          
[5]     32   51674 "TF_BUY"             
[6]     64   55634 "TF_SELL"            
[7]     96    7308 "TF_BUY_SELL (COMBO)"

```

All ticks had TF_LAST and TF_VOLUME flags, and trade direction mixing happened 7308 times. Again, the sum of TF_BUY and TF_SELL minus their combination coincides with the total number of ticks.

The second script SeriesTicksDeltaVolume.mq5 uses the CopyTicksRange function to calculate the volume deltas on each bar. As you know, MetaTrader 5 quotes contain only impersonal volumes, in which purchases and sales are combined in one value for each bar. However, the presence of a history of real ticks allows you to calculate separately the sums of buy and sell volumes, as well as their difference. These characteristics are additional important factors for making trading decisions.

The input parameters contain similar settings as in the first script, in particular, the symbol name for analysis, and the tick request mode. True, in this case, you will additionally need to specify a timeframe, because volume deltas should be calculated bar by bar. The current chart timeframe will be used by default. The BarCount parameter is used to specify the number of calculated bars.

```
input string WorkSymbol = NULL; // Symbol (leave empty for current)
input ENUM_TIMEFRAMES TimeFrame = PERIOD_CURRENT;
input int BarCount = 100;
input COPY_TICKS TickType = INFO_TICKS;

```

Statistics for each bar are stored in the DeltaVolumePerBar structure.

```
struct DeltaVolumePerBar
{
   datetime time; // bar time
   ulong buy;     // net volume of buy operations
   ulong sell;    // net sell operations
   long delta;    // volume difference
};

```

The OnStart function describes an array of such structures, while its size is allocated for the specified number of bars.

```
void OnStart()
{
   DeltaVolumePerBar deltas[];
   ArrayResize(deltas, BarCount);
   ZeroMemory(deltas);
   ...

```

And here is the main algorithm.

```
   for(int i = 0; i < BarCount; ++i)
   {
      MqlTick ticks[];
      const datetime next = iTime(WorkSymbol, TimeFrame, i);
      const datetime prev = iTime(WorkSymbol, TimeFrame, i + 1);
      ResetLastError();
      const int n = CopyTicksRange(WorkSymbol, ticks, COPY_TICKS_ALL, 
         prev * 1000, next * 1000 - 1);
      if(n > -1 && _LastError == 0)
      {
         ...
      }
   }

```

In the loop through bars, we get the time range for each bar: prev and next (0th incomplete bar is not processed). When calling CopyTicksRange for this interval, remember to translate datetime into milliseconds and subtract 1 millisecond from the right border, since this time belongs to the next bar. In the absence of errors, we process the array of received ticks in a loop.

```
         deltas[i].time = prev; // remember the bar time
         for(int j = 0; j < n; ++j)
         {
            // when real volumes can be available, take them from ticks
            if(TickType == TRADE_TICKS)
            {
               // separately accumulate volumes for buy and sell deals
               if((ticks[j].flags & TICK_FLAG_BUY) != 0)
               {
                  deltas[i].buy += ticks[j].volume;
               }
               if((ticks[j].flags & TICK_FLAG_SELL) != 0)
               {
                  deltas[i].sell += ticks[j].volume;
               }
            }
            // when there are no real volumes, we evaluate them by the price movement up/down
            else
            if(TickType == INFO_TICKS && j > 0)
            {
               if((ticks[j].flags & (TICK_FLAG_ASK | TICK_FLAG_BID)) != 0)
               {
                  const long d = (long)(((ticks[j].ask + ticks[j].bid)
                               - (ticks[j - 1].ask + ticks[j - 1].bid)) / _Point);
                  if(d > 0) deltas[i].buy += d;
                  else deltas[i].sell += -d;
               }
            }
         }
         deltas[i].delta = (long)(deltas[i].buy - deltas[i].sell);

```

If analysis by trading ticks (TRADE_TICKS) was requested in the script settings, check the presence of the TICK_FLAG_BUY and TICK_FLAG_SELL flags, and if at least one of them is set, take into account the volume from the volume field in the corresponding variable of the DeltaVolumePerBar structure. This mode is suitable only for stock instruments. For Forex instruments, volumes and trade direction flags are not filled, and therefore a different approach should be used.

If information ticks (INFO_TICKS) available for all instruments are specified in the settings, the algorithm is based on the following empirical rules. As you know, buying pushes the price up, and selling pushes it down. Therefore, we can assume that if the average price Ask+Bid moved up in a new tick relative to the previous one, a buy operation was executed on it, and if the price moved down, there was a sell operation. Volume can be roughly estimated as the number of points passed ([_Point](/en/book/common/environment/env_variables)).

The calculation results are displayed simply as an array of structures with collected statistics.

```
   PrintFormat("Delta volumes per intraday bar\nProcessed %d bars on %s %s %s", 
      BarCount, StringLen(WorkSymbol) > 0 ? WorkSymbol : _Symbol, 
      EnumToString(TimeFrame == PERIOD_CURRENT ? _Period : TimeFrame),
      EnumToString(TickType));
   ArrayPrint(deltas);
}

```

Below are some logs for the TRADE_TICKS and INFO_TICKS modes.

```
Delta volumes per intraday bar
Processed 100 bars on YNDX.MM PERIOD_H1 TRADE_TICKS
                  [time] [buy] [sell] [delta]
[ 0] 2021.10.13 11:00:00  7912  14169   -6257
[ 1] 2021.10.13 10:00:00  8470  11467   -2997
[ 2] 2021.10.13 09:00:00 10830  13047   -2217
[ 3] 2021.10.13 08:00:00 23682  19478    4204
[ 4] 2021.10.13 07:00:00 14538  11600    2938
[ 5] 2021.10.12 20:00:00  2132   4786   -2654
[ 6] 2021.10.12 19:00:00  9173  13775   -4602
[ 7] 2021.10.12 18:00:00  1297   1719    -422
[ 8] 2021.10.12 17:00:00  3803   2995     808
[ 9] 2021.10.12 16:00:00  6743   7045    -302
[10] 2021.10.12 15:00:00 17286  37286  -20000
[11] 2021.10.12 14:00:00 33263  54157  -20894
[12] 2021.10.12 13:00:00 56060  52659    3401
[13] 2021.10.12 12:00:00 12832  10489    2343
[14] 2021.10.12 11:00:00  7530   6092    1438
[15] 2021.10.12 10:00:00  6268  25201  -18933
...

```

The values, of course, are significantly different, but the point is not in absolute values: in the absence of exchange volumes, even such an emulation of splitting and delta dynamics allows us to look at the market behavior from a different angle.

```
Delta volumes per intraday bar
Processed 100 bars on YNDX.MM PERIOD_H1 INFO_TICKS
                  [time]  [buy] [sell] [delta]
[ 0] 2021.10.13 11:00:00   1939   2548    -609
[ 1] 2021.10.13 10:00:00   2222   2400    -178
[ 2] 2021.10.13 09:00:00   2903   2909      -6
[ 3] 2021.10.13 08:00:00   4489   4060     429
[ 4] 2021.10.13 07:00:00   4999   4285     714
[ 5] 2021.10.12 20:00:00   1444   1556    -112
[ 6] 2021.10.12 19:00:00   5464   5867    -403
[ 7] 2021.10.12 18:00:00   2522   2653    -131
[ 8] 2021.10.12 17:00:00   2111   2017      94
[ 9] 2021.10.12 16:00:00   4617   6096   -1479
[10] 2021.10.12 15:00:00   5716   5411     305
[11] 2021.10.12 14:00:00  10044  10866    -822
[12] 2021.10.12 13:00:00  10893  11178    -285
[13] 2021.10.12 12:00:00   2822   2783      39
[14] 2021.10.12 11:00:00   2070   1936     134
[15] 2021.10.12 10:00:00   2053   2303    -250
...

```

When we learn how to [create indicators](/en/book/applications/indicators_make), we will be able to embed this algorithm into one of them (see IndDeltaVolume.mq5 in the section [Waiting for data and managing visibility](/en/book/applications/indicators_make/indicators_wait_none)) to visually display deltas directly on the chart.
