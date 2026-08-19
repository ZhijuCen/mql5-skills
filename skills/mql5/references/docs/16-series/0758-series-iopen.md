# iOpen

Returns the Open price of the bar (indicated by the 'shift' parameter) on the corresponding chart.

```
double  iOpen(
   const string        symbol,          // Symbol
   ENUM_TIMEFRAMES     timeframe,       // Period
   int                 shift            // Shift
   );

```

Parameters

symbol

[in]  The symbol name of the financial instrument. [NULL](/en/docs/constants/namedconstants/otherconstants) means the current symbol.

timeframe

[in]  Period. It can be one of the values of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration. 0 means the current chart period.

shift

[in]  The index of the received value from the timeseries (backward shift by specified number of bars relative to the current bar).

Return Value

The Open price of the bar (indicated by the 'shift' parameter) on the corresponding chart or 0 in case of an error. For [error](/en/docs/constants/errorswarnings/errorcodes) details, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function always returns actual data. For this purpose it performs a request to the timeseries for the specified symbol/period during each call. This means that if there is no ready data during the first function call, some time may be taken to prepare the result.

The function does not store previous calls results, and there is no local cache for quick value return.

Example:

```
input int shift=0;
//+------------------------------------------------------------------+
//| Function-event handler "tick"                                    |
//+------------------------------------------------------------------+
void OnTick()
  {
   datetime time  = iTime(Symbol(),Period(),shift);
   double   open  = iOpen(Symbol(),Period(),shift);
   double   high  = iHigh(Symbol(),Period(),shift);
   double   low   = iLow(Symbol(),Period(),shift);
   double   close = iClose(NULL,PERIOD_CURRENT,shift);
   long     volume= iVolume(Symbol(),0,shift);
   int      bars  = iBars(NULL,0);
 
   Comment(Symbol(),",",EnumToString(Period()),"\n",
           "Time: "  ,TimeToString(time,TIME_DATE|TIME_SECONDS),"\n",
           "Open: "  ,DoubleToString(open,Digits()),"\n",
           "High: "  ,DoubleToString(high,Digits()),"\n",
           "Low: "   ,DoubleToString(low,Digits()),"\n",
           "Close: " ,DoubleToString(close,Digits()),"\n",
           "Volume: ",IntegerToString(volume),"\n",
           "Bars: "  ,IntegerToString(bars),"\n"
           );
  }

```

See also

[CopyOpen](/en/docs/series/copyopen), [CopyRates](/en/docs/series/copyrates)
