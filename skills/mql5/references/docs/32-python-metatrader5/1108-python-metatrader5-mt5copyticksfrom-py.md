# copy_ticks_from

Get ticks from the MetaTrader 5 terminal starting from the specified date.

```
copy_ticks_from(
   symbol,       // symbol name
   date_from,    // date the ticks are requested from
   count,        // number of requested ticks
   flags         // combination of flags defining the type of requested ticks
   )

```

Parameters

symbol

[in]  Financial instrument name, for example, "EURUSD". Required unnamed parameter.

from

[in]  Date the ticks are requested from. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Required unnamed parameter.

count

[in]  Number of ticks to receive. Required unnamed parameter.

flags

[in]  A flag to define the type of the requested ticks. COPY_TICKS_INFO – ticks with Bid and/or Ask changes, COPY_TICKS_TRADE – ticks with changes in Last and Volume, COPY_TICKS_ALL – all ticks. Flag values are described in the [COPY_TICKS](/en/docs/python_metatrader5/mt5copyticksfrom_py#copy_ticks) enumeration. Required unnamed parameter.

Return Value

Returns ticks as the numpy array with the named time, bid, ask, last and flags columns. The 'flags' value can be a combination of flags from the [TICK_FLAG](/en/docs/python_metatrader5/mt5copyticksfrom_py#tick_flag) enumeration. Return None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

See the [CopyTicks](/en/docs/series/copyticks) function for more information.

When creating the 'datetime' object, Python uses the local time zone, while MetaTrader 5 stores tick and bar open time in UTC time zone (without the shift). Therefore, 'datetime' should be created in UTC time for executing functions that use time. Data received from the MetaTrader 5 terminal has UTC time.

COPY_TICKS defines the types of ticks that can be requested using the [copy_ticks_from()](/en/docs/python_metatrader5/mt5copyticksfrom_py) and [copy_ticks_range()](/en/docs/python_metatrader5/mt5copyticksrange_py) functions.

| ID | Description |
| --- | --- |
| COPY_TICKS_ALL | all ticks |
| COPY_TICKS_INFO | ticks containing Bid and/or Ask price changes |
| COPY_TICKS_TRADE | ticks containing Last and/or Volume price changes |

TICK_FLAG defines possible flags for ticks. These flags are used to describe ticks obtained by the [copy_ticks_from()](/en/docs/python_metatrader5/mt5copyticksfrom_py) and [copy_ticks_range()](/en/docs/python_metatrader5/mt5copyticksrange_py) functions.

| ID | Description |
| --- | --- |
| TICK_FLAG_BID | Bid price changed |
| TICK_FLAG_ASK | Ask price changed |
| TICK_FLAG_LAST | Last price changed |
| TICK_FLAG_VOLUME | Volume changed |
| TICK_FLAG_BUY | last Buy price changed |
| TICK_FLAG_SELL | last Sell price changed |

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
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
# request 100 000 EURUSD ticks starting from 10.01.2019 in UTC time zone
ticks = mt5.copy_ticks_from("EURUSD", utc_from, 100000, mt5.COPY_TICKS_ALL)
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
 
Ticks received: 100000
Display obtained ticks 'as is'
(1578614400, 1.11051, 1.11069, 0., 0, 1578614400987, 134, 0.)
(1578614402, 1.11049, 1.11067, 0., 0, 1578614402025, 134, 0.)
(1578614404, 1.1105, 1.11066, 0., 0, 1578614404057, 134, 0.)
(1578614404, 1.11049, 1.11067, 0., 0, 1578614404344, 134, 0.)
(1578614412, 1.11052, 1.11064, 0., 0, 1578614412106, 134, 0.)
(1578614418, 1.11039, 1.11051, 0., 0, 1578614418265, 134, 0.)
(1578614418, 1.1104, 1.1105, 0., 0, 1578614418905, 134, 0.)
(1578614419, 1.11039, 1.11051, 0., 0, 1578614419519, 134, 0.)
(1578614456, 1.11037, 1.11065, 0., 0, 1578614456011, 134, 0.)
(1578614456, 1.11039, 1.11051, 0., 0, 1578614456015, 134, 0.)
 
Display dataframe with ticks
                 time      bid      ask  last  volume       time_msc  flags  volume_real
0 2020-01-10 00:00:00  1.11051  1.11069   0.0       0  1578614400987    134          0.0
1 2020-01-10 00:00:02  1.11049  1.11067   0.0       0  1578614402025    134          0.0
2 2020-01-10 00:00:04  1.11050  1.11066   0.0       0  1578614404057    134          0.0
3 2020-01-10 00:00:04  1.11049  1.11067   0.0       0  1578614404344    134          0.0
4 2020-01-10 00:00:12  1.11052  1.11064   0.0       0  1578614412106    134          0.0
5 2020-01-10 00:00:18  1.11039  1.11051   0.0       0  1578614418265    134          0.0
6 2020-01-10 00:00:18  1.11040  1.11050   0.0       0  1578614418905    134          0.0
7 2020-01-10 00:00:19  1.11039  1.11051   0.0       0  1578614419519    134          0.0
8 2020-01-10 00:00:56  1.11037  1.11065   0.0       0  1578614456011    134          0.0
9 2020-01-10 00:00:56  1.11039  1.11051   0.0       0  1578614456015    134          0.0

```

See also

[CopyRates](/en/docs/series/copyrates), [copy_rates_from_pos](/en/docs/python_metatrader5/mt5copyratesfrompos_py), [copy_rates_range](/en/docs/python_metatrader5/mt5copyratesrange_py), [copy_ticks_from](/en/docs/python_metatrader5/mt5copyticksfrom_py), [copy_ticks_range](/en/docs/python_metatrader5/mt5copyticksrange_py)
