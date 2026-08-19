# SeriesInfoInteger

Returns information about the state of historical data. There are 2 variants of function calls.

Directly returns the property value.

```
long  SeriesInfoInteger(
   string                     symbol_name,     // symbol name
   ENUM_TIMEFRAMES            timeframe,       // period
   ENUM_SERIES_INFO_INTEGER   prop_id,         // property identifier
   );

```

Returns true or false depending on the success of the function run.

```
bool  SeriesInfoInteger(
   string                     symbol_name,     // symbol name
   ENUM_TIMEFRAMES            timeframe,       // period
   ENUM_SERIES_INFO_INTEGER   prop_id,         // property ID
   long&                      long_var         // variable for getting info
   );

```

Parameters

symbol_name

[in]  Symbol name.

timeframe

[in]  Period.

prop_id

[in]  Identifier of the requested property, value of the [ENUM_SERIES_INFO_INTEGER](/en/docs/constants/tradingconstants/enum_series_info_integer) enumeration.

long_var

[out]  Variable to which the value of the requested property is placed.

Return Value

In the first case, it returns value of the long type.

For the second case,  it returns true, if the specified property is available and its value has been placed into long_var variable, otherwise it returns false. For more details about an [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).

Example:

```
void OnStart()
  {
//---
   Print("Total number of bars for the symbol-period at this moment = ",
         SeriesInfoInteger(Symbol(),Period(),SERIES_BARS_COUNT));
 
   Print("The first date for the symbol-period at this moment = ",
         (datetime)SeriesInfoInteger(Symbol(),Period(),SERIES_FIRSTDATE));
 
   Print("The first date in the history for the symbol-period on the server = ",
         (datetime)SeriesInfoInteger(Symbol(),Period(),SERIES_SERVER_FIRSTDATE));
 
   Print("Symbol data are synchronized = ",
         (bool)SeriesInfoInteger(Symbol(),Period(),SERIES_SYNCHRONIZED));
  }

```
