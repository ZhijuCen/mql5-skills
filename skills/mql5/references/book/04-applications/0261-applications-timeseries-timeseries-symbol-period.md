# Symbols and timeframes

Timeseries with quotes are identified by two parameters: symbol name (financial instrument) and timeframe (period).

The user can see the list of symbols in the Market Watch window and edit it based on the general list provided by the broker (dialog Symbols). For MQL programs, there is a set of functions that can be used to do the same: search in all symbols, find out their properties and add or remove symbols to/from Market Watch. These features will be the subject of a separate [chapter](/en/book/automation/symbols).

However, to request timeseries, it is enough to know the name of the symbol — this is a string containing the designation of an existing financial instrument. It, for example, can be set by the user in the input variable. In addition, the symbol of the current chart can be found from the built-in variable _Symbol (or the [Symbol](/en/book/applications/charts/charts_main_properties) function) but for our convenience, all timeseries functions support the convention that the NULL value also corresponds to the symbol of the current chart.

Now let's turn to timeframes. There are 21 standard timeframes defined in the system: each is specified by an element in the special enumeration ENUM_TIMEFRAMES.

| Identifier | Value (Hex) | Description |
| --- | --- | --- |
| PERIOD_CURRENT | 0 | Current chart period |
| PERIOD_M1 | 1 (0x1) | 1 minute |
| PERIOD_M2 | 2 (0x2) | 2 minutes |
| PERIOD_M3 | 3 (0x3) | 3 minutes |
| PERIOD_M4 | 4 (0x4) | 4 minutes |
| PERIOD_M5 | 5 (0x5) | 5 minutes |
| PERIOD_M6 | 6 (0x6) | 6 minutes |
| PERIOD_M10 | 10 (0xA) | 10 minutes |
| PERIOD_M12 | 12 (0xC) | 12 minutes |
| PERIOD_M15 | 15 (0xF) | 15 minutes |
| PERIOD_M20 | 20 (0x14) | 20 minutes |
| PERIOD_M30 | 30 (0x1E) | 30 minutes |
| PERIOD_H1 | 16385 (0x4001) | 1 hour |
| PERIOD_H2 | 16386 (0x4002) | 2 hours |
| PERIOD_H3 | 16387 (0x4003) | 3 hours |
| PERIOD_H4 | 16388 (0x4004) | 4 hours |
| PERIOD_H6 | 16390 (0x4006) | 6 hours |
| PERIOD_H8 | 16392 (0x4008) | 8 hours |
| PERIOD_H12 | 16396 (0x400C) | 12 hours |
| PERIOD_D1 | 16408 (0x4018) | 1 day |
| PERIOD_W1 | 32769 (0x8001) | 1 Week |
| PERIOD_MN1 | 49153 (0xC001) | 1 month |

As we saw in the section on [Predefined variables](/en/book/common/environment/env_variables), the program can learn the period of the current chart from the built-in variable _Period (or the [Period](/en/book/applications/charts/charts_main_properties) function). It is easy to see from the column of values that passing zero to the built-in functions that accept a timeframe will mean the period of the current chart.

The value for minute timeframes is the same as the number of minutes in them (for example, 30 means M30). For hourly timeframes, bit 0x4000 is set, and the lower byte contains the number of hours (for example, 0x4003 for H3). Day period D1 is encoded as 24 hours, that is 0x4018 (0x18 is equal to 24). Finally, the weekly and monthly timeframes have their own distinguishing bits 0x8000 and 0xC000, respectively, as unit indicators, and the count (in the low byte) is 1 in both cases.

For convenient conversion of enumeration elements into strings and back, a header file Periods.mqh is attached to the book (we have already used it in the example of working with files, and will use it in future examples). One of its functions, StringToPeriod, uses in its algorithm the above-described features of the internal bit representation of enumeration elements.

```
#define PERIOD_PREFIX_LENGTH 7 // StringLen("PERIOD_")
   
// getting the abbreviated name of the period without the "PERIOD_" prefix
string PeriodToString(const ENUM_TIMEFRAMES tf = PERIOD_CURRENT)
{
   const static int prefix = StringLen("PERIOD_");
   return StringSubstr(EnumToString(tf == PERIOD_CURRENT ? _Period : tf),
      PERIOD_PREFIX_LENGTH);
}
   
// get the period value by full (PERIOD_H4) or short (H4) name  
ENUM_TIMEFRAMES StringToPeriod(string name)
{
   if(StringLen(name) < 2) return 0;
   // converting full name "PERIOD_TN" to short "TN" if needed
   if(StringLen(name) > PERIOD_PREFIX_LENGTH)
   {
     name = StringSubstr(name, PERIOD_PREFIX_LENGTH);
   }
   // convert the digital ending "N" to a number, skip "T"
   const int count = (int)StringToInteger(StringSubstr(name, 1));
   // clear possible error WRONG_STRING_PARAMETER(5040)
   // for example, if the input string is "MN1", then N1 is not a number for StringToInteger
   ResetLastError();
   switch(name[0])
   {
      case 'M':
         if(!count) return PERIOD_MN1;
         return (ENUM_TIMEFRAMES)count;
      case 'H':
         return (ENUM_TIMEFRAMES)(0x4000 + count);
      case 'D':
         return PERIOD_D1;
      case 'W':
         return PERIOD_W1;
   }
   return 0;
}

```

Note that the _Symbol and _Period variables contain actual data only in the MQL programs that run on charts, including scripts, Expert Advisors, and indicators. In services, these variables are empty, and therefore, to access timeseries, you must explicitly set the symbol name and period or get them somehow from outside.

The defining property of a timeframe is its duration (bar duration). MQL5 allows you to get the number of seconds that form one bar of a specific timeframe using the PeriodSeconds function.

int PeriodSeconds(ENUM_TIMEFRAMES period = PERIOD_CURRENT)

The period parameter specifies the period as an element of the ENUM_TIMEFRAMES enumeration. If the parameter is not specified, then the number of seconds of the current chart period on which the program is running is returned.

We will consider examples of using the function in the indicator IndDeltaVolume.mq5 in the section [Waiting for data and managing visibility](/en/book/applications/indicators_make/indicators_wait_none), as well as in the indicator UseM1MA.mq5 in the section [Using built-in indicators](/en/book/applications/indicators_use/indicators_standard_use).

To generate timeframes of non-standard duration that are not included in the specified list, the MQL5 API provides [custom symbols](/en/book/advanced/custom_symbols), however, they do not allow you to trade like on standard charts without modifying Expert Advisors.

In addition, it is important to note that in MetaTrader 5 the duration of bars within a particular timeseries or on a chart is always the same. Therefore, to build charts in which bars are formed not according to time, but as other parameters accumulate, in particular, volumes (equivolume charts) or price movement in one direction in fixed steps (Renko), you can develop your own solutions based on indicators (for example, with the [DRAW_CANDLES or DRAW_BARS](/en/book/applications/indicators_make/indicators_multisymbol) render type) or using [custom symbols](/en/book/advanced/custom_symbols).
