# CopyRates

Gets the historical series of the [MqlRates](/en/docs/constants/structures/mqlrates) structure of the specified symbol-period in the specified amount into a matrix or vector. Elements are counted down from the present to the past, which means that the starting position equal to 0 means the current bar.

The data is copied so that the oldest element is placed at the beginning of the matrix/vector. There are three function options.

Access by the initial position and the number of required elements

```
bool  matrix::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   ulong            start,        // index of the initial bar copying starts from 
   ulong            count         // how many to copy
   );

```

Access by the initial date and the number of required elements

```
bool  matrix::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   datetime         from,         // start date 
   ulong            count         // how many to copy
   );

```

Access by the initial and final dates of the required time interval

```
bool  matrix::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   datetime         from,         // start date 
   datetime         to            // end date
   );

```

Vector Methods

Access by the initial position and the number of required elements

```
bool  vector::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   ulong            start,        // index of the initial bar copying starts from 
   ulong            count         // how many to copy
   );

```

Access by the initial date and the number of required elements

```
bool  vector::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   datetime         from,         // start date 
   ulong            count         // how many to copy
   );

```

Access by the initial and final dates of the required time interval

```
bool  vector::CopyRates(
   string           symbol,       // symbol name
   ENUM_TIMEFRAMES  period,       // period
   ulong            rates_mask,   // combination of flags to specify the requested series
   datetime         from,         // start date 
   datetime         to            // end date
   );

```

Parameters

symbol

[in]  Symbol.

period

[in]  Period.

rates_mask

[in]  The ENUM_COPY_RATES enumeration combination of flags specifying the type of requested series.  When copying to a vector, only one value from the ENUM_COPY_RATES enumeration can be specified, otherwise an error occurs.

start

[in]  First copied element index.

count

[in]  Number of copied elements.

from

[in]  Bar time corresponding to the first element.

to

[in]  Bar time corresponding to the last element.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If the interval of the requested data is completely outside the available data on the server, then the function returns false. If the data outside [TERMINAL_MAXBARS](/en/docs/constants/environment_state/terminalstatus) (maximum number of bars on the chart) is requested, the function also returns false.

When requesting data from an EA or a script, [download from the server](/en/docs/series/timeseries_access#synchronized) is initiated if the terminal does not have the appropriate data locally, or construction of the necessary timeseries starts if the data can be constructed from the local history but they are not ready yet. The function returns the amount that will be ready by the time the timeout expires, however the history download continues, and the function returns more data during the next similar request.

When requesting data by the start date and the number of required items, only data whose date is less than (before) or equal to the specified one is returned. The interval is set and considered up to a second. In other words, the opening date of any bar the value is returned for (volume, spread, Open, High, Low, Close or Time) is always equal to or less than the specified one.

When requesting data in a given date range, only data that falls within the requested interval is returned. The interval is set and considered up to a second. In other words, the opening time of any bar the value is returned for (volume, spread, indicator buffer value, Open, High, Low, Close or Time) is always located in the requested interval.

For example, if the current day of the week is Saturday, the function returns 0 when attempting to copy data on the weekly timeframe by setting start_time=Last_Tuesday and stop_time=Last_Friday because the open time on the weekly timeframe always falls on Sunday, but not a single weekly bar falls within the specified range.

If you need to get the value corresponding to the current incomplete bar, then you can use the first call form indicating start_pos=0 and count=1.

ENUM_COPY_RATES

The ENUM_COPY_RATES enumeration contains the flags to specify the type of data to be passed to the matrix or array. The flag combination allows getting several series from the history in one request.  The order of the rows in the matrix will correspond to the order of the values in the ENUM_COPY_RATES enumeration. In other words, the row with High data will always be higher in the matrix than the row with Low data.

| ID | Value | Description |
| --- | --- | --- |
| COPY_RATES_OPEN | 1 | Open price series |
| COPY_RATES_HIGH | 2 | High price series |
| COPY_RATES_LOW | 4 | Low price series |
| COPY_RATES_CLOSE | 8 | Close price series |
| COPY_RATES_TIME | 16 | Time series (bar open time) 
   
 Getting time in  float  of the vector and the matrix (vectord and matrixf) causes losses of ~100 seconds since  float  accuracy is severely limited and integers greater than 1<<24 cannot be accurately represented in float. |
| COPY_RATES_VOLUME_TICK | 32 | Tick Volumes |
| COPY_RATES_VOLUME_REAL | 64 | Trade Volumes |
| COPY_RATES_SPREAD | 128 | Spreads |
| Combination |  |  |
| COPY_RATES_OHLC | 15 | Open, High, Low and Close series |
| COPY_RATES_OHLCT | 31 | Open, High, Low, Close and Time series |
| Data arrangement |  |  |
| COPY_RATES_VERTICAL | 32768 | Series are copied into the matrix along the vertical axis. The received series values will be arranged vertically in the matrix, i.e., the oldest data will be in the first row, while the most recent data will be in the last matrix row. 
   
 With default copying, series are added into a matrix along the horizontal axis. 
   
 The flag is only applicable when copying to a matrix. |

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- get quotes to the matrix
  matrix matrix_rates;
  if(matrix_rates.CopyRates(Symbol(), PERIOD_CURRENT, COPY_RATES_OHLCT, 1, 10))
    Print("matrix rates: \n", matrix_rates);
  else
    Print("matrix_rates.CopyRates failed. Error ", GetLastError());
//--- check
  MqlRates mql_rates[];
  if(CopyRates(Symbol(), PERIOD_CURRENT, 1, 10, mql_rates)>0)
   {
    Print("mql_rates array:");
    ArrayPrint(mql_rates);
   }
  else
    Print("CopyRates(Symbol(), PERIOD_CURRENT,1, 10, mql_rates). Error ", GetLastError());
//--- get quotes into the vector = invalid call
  vector vector_rates;
  if(vector_rates.CopyRates(Symbol(), PERIOD_CURRENT, COPY_RATES_OHLC, 1, 15))
    Print("vector_rates COPY_RATES_OHLC: \n", vector_rates);
  else
    Print("vector_rates.CopyRates COPY_RATES_OHLC failed. Error ", GetLastError());
//--- get close prices into the vector
  if(vector_rates.CopyRates(Symbol(), PERIOD_CURRENT, COPY_RATES_CLOSE, 1, 15))
    Print("vector_rates COPY_RATES_CLOSE: \n", vector_rates);
  else
    Print("vector_rates.CopyRates failed. Error ", GetLastError());
 };
/*
   matrix rates:
   [[0.99686,0.99638,0.99588,0.99441,0.99464,0.99594,0.99698,0.99758,0.99581,0.9952800000000001]
    [0.99708,0.99643,0.99591,0.9955000000000001,0.99652,0.99795,0.99865,0.99764,0.99604,0.9957]
    [0.9961100000000001,0.99491,0.99426,0.99441,0.99448,0.99494,0.9964499999999999,0.99472,0.9936,0.9922]
    [0.99641,0.99588,0.99441,0.99464,0.99594,0.99697,0.99758,0.99581,0.9952800000000001,0.99259]
    [1662436800,1662440400,1662444000,1662447600,1662451200,1662454800,1662458400,1662462000,1662465600,1662469200]]
   mql_rates array:
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2022.09.06 04:00:00 0.99686 0.99708 0.99611 0.99641          4463        0             0
   [1] 2022.09.06 05:00:00 0.99638 0.99643 0.99491 0.99588          4519        0             0
   [2] 2022.09.06 06:00:00 0.99588 0.99591 0.99426 0.99441          3060        0             0
   [3] 2022.09.06 07:00:00 0.99441 0.99550 0.99441 0.99464          3867        0             0
   [4] 2022.09.06 08:00:00 0.99464 0.99652 0.99448 0.99594          5280        0             0
   [5] 2022.09.06 09:00:00 0.99594 0.99795 0.99494 0.99697          7227        0             0
   [6] 2022.09.06 10:00:00 0.99698 0.99865 0.99645 0.99758         10130        0             0
   [7] 2022.09.06 11:00:00 0.99758 0.99764 0.99472 0.99581          7012        0             0
   [8] 2022.09.06 12:00:00 0.99581 0.99604 0.99360 0.99528          6166        0             0
   [9] 2022.09.06 13:00:00 0.99528 0.99570 0.99220 0.99259          6950        0             0
   vector_rates.CopyRates COPY_RATES_OHLC failed. Error 4003
   vector_rates COPY_RATES_CLOSE:
   [0.9931,0.99293,0.99417,0.99504,0.9968399999999999,0.99641,0.99588,0.99441,0.99464,0.99594,0.99697,0.99758,0.99581,0.9952800000000001,0.99259]
*/

```

See also

[Access to Timeseries and Indicators](/en/docs/series),  [CopyRates](/en/docs/series/copyrates)
