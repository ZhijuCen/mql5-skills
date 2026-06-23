# history_deals_total

Get the number of deals in trading history within the specified interval.

```
history_deals_total(
   date_from,    // date the deals are requested from
   date_to       // date, up to which the deals are requested
   )

```

Parameters

date_from

[in]  Date the deals are requested from. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Required unnamed parameter.

date_to

[in]  Date, up to which the deals are requested. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Required unnamed parameter.

Return Value

Integer value.

Note

The function is similar to [HistoryDealsTotal](/en/docs/trading/historydealstotal).

Example:

```
from datetime import datetime
import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# get the number of deals in history
from_date=datetime(2020,1,1)
to_date=datetime.now()
deals=mt5.history_deals_total(from_date, to_date)
if deals>0:
    print("Total deals=",deals)
else:
    print("Deals not found in history")
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

```

See also

[history_deals_get](/en/docs/python_metatrader5/mt5historydealsget_py), [history_orders_total](/en/docs/python_metatrader5/mt5historyorderstotal_py)
