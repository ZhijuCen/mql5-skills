# copy_ticks_range

Get ticks for the specified date range from the MetaTrader 5 terminal.

```
copy_ticks_range(
   symbol,       // symbol name
   date_from,    // date the ticks are requested from
   date_to,      // date, up to which the ticks are requested
   flags         // combination of flags defining the type of requested ticks
   )

```

Parameters

symbol

[in]  Financial instrument name, for example, "EURUSD". Required unnamed parameter.

date_from

[in]  Date the ticks are requested from. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Required unnamed parameter.

date_to

[in]  Date, up to which the ticks are requested. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Required unnamed parameter.

flags

[in]  A flag to define the type of the requested ticks. COPY_TICKS_INFO – ticks with Bid and/or Ask changes, COPY_TICKS_TRADE – ticks with changes in Last and Volume, COPY_TICKS_ALL – all ticks. Flag values are described in the [COPY_TICKS](/en/docs/python_metatrader5/mt5copyticksfrom_py#copy_ticks) enumeration. Required unnamed parameter.

Return Value

Returns ticks as the numpy array with the named time, bid, ask, last and flags columns. The 'flags' value can be a combination of flags from the [TICK_FLAG](/en/docs/python_metatrader5/mt5copyticksfrom_py#tick_flag) enumeration. Return None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

See the [CopyTicks](/en/docs/series/copyticks) function for more information.

When creating the 'datetime' object, Python uses the local time zone, while MetaTrader 5 stores tick and bar open time in UTC time zone (without the shift). Therefore, 'datetime' should be created in UTC time for executing functions that use time. The data obtained from MetaTrader 5 have UTC time, but Python applies the local time shift again when trying to print them. Thus, the obtained data should also be corrected for visual presentation.

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
utc_to = datetime(2020, 1, 11, tzinfo=timezone)
# request AUDUSD ticks within 11.01.2020 - 11.01.2020
ticks = mt5.copy_ticks_range("AUDUSD", utc_from, utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
# display data on each tick on a new line
print("Display obtained ticks 'as is'")
count = 0
for tick in ticks:
    count+=1
    print(tick)
    if count >= 10:
        break
 
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
 
# display data
print("\nDisplay dataframe with ticks")
print(ticks_frame.head(10)) 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
 
Ticks received: 37008
Display obtained ticks 'as is'
(1578614400, 0.68577, 0.68594, 0., 0, 1578614400820, 134, 0.)
(1578614401, 0.68578, 0.68594, 0., 0, 1578614401128, 130, 0.)
(1578614401, 0.68575, 0.68594, 0., 0, 1578614401128, 130, 0.)
(1578614411, 0.68576, 0.68594, 0., 0, 1578614411388, 130, 0.)
(1578614411, 0.68575, 0.68594, 0., 0, 1578614411560, 130, 0.)
(1578614414, 0.68576, 0.68595, 0., 0, 1578614414973, 134, 0.)
(1578614430, 0.68576, 0.68594, 0., 0, 1578614430188, 4, 0.)
(1578614450, 0.68576, 0.68595, 0., 0, 1578614450408, 4, 0.)
(1578614450, 0.68576, 0.68594, 0., 0, 1578614450519, 4, 0.)
(1578614456, 0.68575, 0.68594, 0., 0, 1578614456363, 130, 0.)
 
Display dataframe with ticks
                 time      bid      ask  last  volume       time_msc  flags  volume_real
0 2020-01-10 00:00:00  0.68577  0.68594   0.0       0  1578614400820    134          0.0
1 2020-01-10 00:00:01  0.68578  0.68594   0.0       0  1578614401128    130          0.0
2 2020-01-10 00:00:01  0.68575  0.68594   0.0       0  1578614401128    130          0.0
3 2020-01-10 00:00:11  0.68576  0.68594   0.0       0  1578614411388    130          0.0
4 2020-01-10 00:00:11  0.68575  0.68594   0.0       0  1578614411560    130          0.0
5 2020-01-10 00:00:14  0.68576  0.68595   0.0       0  1578614414973    134          0.0
6 2020-01-10 00:00:30  0.68576  0.68594   0.0       0  1578614430188      4          0.0
7 2020-01-10 00:00:50  0.68576  0.68595   0.0       0  1578614450408      4          0.0
8 2020-01-10 00:00:50  0.68576  0.68594   0.0       0  1578614450519      4          0.0
9 2020-01-10 00:00:56  0.68575  0.68594   0.0       0  1578614456363    130          0.0

```

See also

[CopyRates](/en/docs/series/copyrates), [copy_rates_from_pos](/en/docs/python_metatrader5/mt5copyratesfrompos_py), [copy_rates_range](/en/docs/python_metatrader5/mt5copyratesrange_py), [copy_ticks_from](/en/docs/python_metatrader5/mt5copyticksfrom_py), [copy_ticks_range](/en/docs/python_metatrader5/mt5copyticksrange_py)
