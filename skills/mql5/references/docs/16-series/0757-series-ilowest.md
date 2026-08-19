# iLowest

Returns the index of the smallest value found on the corresponding chart (shift relative to the current bar).

```
int  iLowest(
   const string        symbol,              // Symbol
   ENUM_TIMEFRAMES     timeframe,           // Period
   ENUM_SERIESMODE     type,                // Timeseries identifier
   int                 count=WHOLE_ARRAY,   // Number of elements
   int                 start=0              // Index
  );

```

Parameters

symbol

[in]  The symbol, on which the search will be performed. [NULL](/en/docs/constants/namedconstants/otherconstants) means the current symbol.

timeframe

[in]  Period. It can be one of the values of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration. 0 means the current chart period.

type

[in]  The identifier of the timeseries, in which the search will be performed. Can be equal to any value from [ENUM_SERIESMODE](/en/docs/constants/chartconstants/enum_timeframes#enum_seriesmode).

count=WHOLE_ARRAY

[in]  The number of elements in the timeseries (from the current bar towards index increasing direction), among which the search should be performed.

start=0

[in]  The index (shift relative to the current bar) of the initial bar, from which search for the lowest value begins. Negative values ​​are ignored and replaced with a zero value.

Return Value

The index of the lowest value found on the corresponding chart (shift relative to the current bar) or -1 in case of an error. For [error](/en/docs/constants/errorswarnings/errorcodes) details, call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
   double val;
//--- Search for a bar with the lowest value of the real volume among 15 consecutive bars
//--- From index 10 to index 24 inclusive, on the current timeframe
   int val_index=iLowest(NULL,0,MODE_REAL_VOLUME,15,10);
   if(val_index!=-1) 
      val=Low[val_index];
   else 
      PrintFormat("iLowest() call error. Error code=%d",GetLastError());

```
