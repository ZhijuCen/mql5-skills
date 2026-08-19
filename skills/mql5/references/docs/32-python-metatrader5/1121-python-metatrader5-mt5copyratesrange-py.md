# copy_rates_range

Get bars in the specified date range from the MetaTrader 5 terminal.

```
copy_rates_range(
   symbol,       // symbol name
   timeframe,    // timeframe
   date_from,    // date the bars are requested from
   date_to       // date, up to which the bars are requested
   )

```

Parameters

symbol

[in]  Financial instrument name, for example, "EURUSD". Required unnamed parameter.

timeframe

[in]  Timeframe the bars are requested for. Set by a value from the [TIMEFRAME](/en/docs/python_metatrader5/mt5copyratesfrom_py#timeframe) enumeration. Required unnamed parameter.

date_from

[in]  Date the bars are requested from. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Bars with the open time >= date_from are returned. Required unnamed parameter.

date_to

[in]  Date, up to which the bars are requested. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Bars with the open time <= date_to are returned. Required unnamed parameter.

Return Value

Returns bars as the numpy array with the named time, open, high, low, close, tick_volume, spread and real_volume columns. Returns None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

See the [CopyRates()](/en/docs/series/copyrates) function for more information.

MetaTrader 5 terminal provides bars only within a history available to a user on charts. The number of bars available to users is set in the "[Max. bars in chart](https://www.metatrader5.com/en/terminal/help/startworking/settings#max_bars)" parameter.

When creating the 'datetime' object, Python uses the local time zone, while MetaTrader 5 stores tick and bar open time in UTC time zone (without the shift). Therefore, 'datetime' should be created in UTC time for executing functions that use time. Data received from the MetaTrader 5 terminal has UTC time.

Example:

```
from datetime import datetime
import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# import the 'pandas' module for displaying data obtained in the tabular form
import pandas as pd
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
# import pytz module for working with time zone
import pytz
 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)
# get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
rates = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_M5, utc_from, utc_to)
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
# display each element of obtained data in a new line
print("Display obtained data 'as is'")
counter=0
for rate in rates:
    counter+=1
    if counter<=10:
        print(rate)
 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the 'datetime' format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
 
# display data
print("\nDisplay dataframe with data")
print(rates_frame.head(10))
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
 
Display obtained data 'as is'
(1578614400, 109.513, 109.527, 109.505, 109.521, 43, 2, 0)
(1578614700, 109.521, 109.549, 109.518, 109.543, 215, 8, 0)
(1578615000, 109.543, 109.543, 109.466, 109.505, 98, 10, 0)
(1578615300, 109.504, 109.534, 109.502, 109.517, 155, 8, 0)
(1578615600, 109.517, 109.539, 109.513, 109.527, 71, 4, 0)
(1578615900, 109.526, 109.537, 109.484, 109.52, 106, 9, 0)
(1578616200, 109.52, 109.524, 109.508, 109.51, 205, 7, 0)
(1578616500, 109.51, 109.51, 109.491, 109.496, 44, 8, 0)
(1578616800, 109.496, 109.509, 109.487, 109.5, 85, 5, 0)
(1578617100, 109.5, 109.504, 109.487, 109.489, 82, 7, 0)
 
Display dataframe with data
                 time     open     high      low    close  tick_volume  spread  real_volume
0 2020-01-10 00:00:00  109.513  109.527  109.505  109.521           43       2            0
1 2020-01-10 00:05:00  109.521  109.549  109.518  109.543          215       8            0
2 2020-01-10 00:10:00  109.543  109.543  109.466  109.505           98      10            0
3 2020-01-10 00:15:00  109.504  109.534  109.502  109.517          155       8            0
4 2020-01-10 00:20:00  109.517  109.539  109.513  109.527           71       4            0
5 2020-01-10 00:25:00  109.526  109.537  109.484  109.520          106       9            0
6 2020-01-10 00:30:00  109.520  109.524  109.508  109.510          205       7            0
7 2020-01-10 00:35:00  109.510  109.510  109.491  109.496           44       8            0
8 2020-01-10 00:40:00  109.496  109.509  109.487  109.500           85       5            0
9 2020-01-10 00:45:00  109.500  109.504  109.487  109.489           82       7            0

```

See also

[CopyRates](/en/docs/series/copyrates), [copy_rates_from](/en/docs/python_metatrader5/mt5copyratesfrom_py), [copy_rates_range](/en/docs/python_metatrader5/mt5copyratesrange_py), [copy_ticks_from](/en/docs/python_metatrader5/mt5copyticksfrom_py), [copy_ticks_range](/en/docs/python_metatrader5/mt5copyticksrange_py)
