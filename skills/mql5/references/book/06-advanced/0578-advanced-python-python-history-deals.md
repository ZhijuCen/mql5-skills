# Reading the history of orders and deals

Working with orders and deals in the account history using Python scripts is also possible. For these purposes, there are functions history_orders_total, history_orders_get, history_deals_total, and history_deals_get.

int history_orders_total(date_from, date_to)

The history_orders_total function returns the number of orders in the trading history in the specified time interval. Each of the parameters is set by the datetime object or as the number of seconds since 1970.01.01.

The function is an analog of [HistoryOrdersTotal](/en/book/automation/experts/experts_history_select).

The history_orders_get function is available in several versions and supports order filtering by substring in symbol name, ticket, or position ID. All variants return an array of named tuples TradeOrder (field names match [ENUM_ORDER_PROPERTY_enumerations](/en/book/automation/experts/experts_order_properties) without the "ORDER_" prefix and in lowercase). If there are no matching orders, the array will be empty. In case of an error, the function will return None.

namedtuple[] history_orders_get(date_from, date_to, group = <"PATTERN">)

namedtuple[] history_orders_get(ticket = <ORDER_TICKET>)

namedtuple[] history_orders_get(position = <POSITION_ID>)

The first version selects orders within the specified time range (similar to history_orders_total). In the optional named parameter group, you can specify a search pattern for a substring of the symbol name (you can use the wildcard characters '*' and negation '!' in it, see the section [Getting information about financial instruments](/en/book/advanced/python/python_symbols)).

The second version is designed to search for a specific order by its ticket.

The last version selects orders by position ID (ORDER_POSITION_ID property).

Either option is equivalent to calling several MQL5 functions: [HistoryOrdersTotal](/en/book/automation/experts/experts_history_select), [HistoryOrderSelect](/en/book/automation/experts/experts_history_select), and [HistoryOrderGet](/en/book/automation/experts/experts_history_select)[-functions](/en/book/automation/experts/experts_history_select).

Let's see on an example of the script historyordersget.py how to get the number and list of historical orders for different conditions.

```
from datetime import datetime 
import MetaTrader5 as mt5 
import pandas as pd 
pd.set_option('display.max_columns', 500) # how many columns to show 
pd.set_option('display.width', 1500)      # max. table width for display
...   
# get the number of orders in the history for the period (total and *GBP*)
from_date = datetime(2022, 9, 1)
to_date = datetime.now()
total = mt5.history_orders_total(from_date, to_date)
history_orders=mt5.history_orders_get(from_date, to_date, group="*GBP*")
# print(history_orders)
if history_orders == None: 
   print("No history orders with group=\"*GBP*\", error code={}".format(mt5.last_error())) 
else :
   print("history_orders_get({}, {}, group=\"*GBP*\")={} of total {}".format(from_date,
   to_date, len(history_orders), total))
   
# display all canceled historical orders for ticket position 0
position_id = 0
position_history_orders = mt5.history_orders_get(position = position_id)
if position_history_orders == None:
   print("No orders with position #{}".format(position_id))
   print("error code =", mt5.last_error())
elif len(position_history_orders) > 0:
   print("Total history orders on position #{}: {}".format(position_id,
   len(position_history_orders)))
   # display received orders as is
   for position_order in position_history_orders:
      print(position_order)
   # display these orders as a table using pandas.DataFrame
   df = pd.DataFrame(list(position_history_orders),
   columns = position_history_orders[0]._asdict().keys())
   df.drop(['time_expiration', 'type_time', 'state', 'position_by_id', 'reason', 'volume_current',
   'price_stoplimit','sl','tp', 'time_setup_msc', 'time_done_msc', 'type_filling', 'external_id'],
   axis = 1, inplace = True)
   df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
   df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
   print(df)
...

```

The result of the script (given with abbreviations):

```
history_orders_get(2022-09-01 00:00:00, 2022-09-26 21:50:04, group="*GBP*")=15 of total 44
   
Total history orders on position #0: 14
TradeOrder(ticket=1437318706, time_setup=1661348065, time_setup_msc=1661348065049, time_done=1661348083,
   time_done_msc=1661348083632, time_expiration=0, type=2, type_time=0, type_filling=2, state=2, magic=0,
   position_id=0, position_by_id=0, reason=3, volume_initial=0.01, volume_current=0.01, price_open=0.99301,
   sl=0.0, tp=0.0, price_current=0.99311, price_stoplimit=0.0, symbol='EURUSD', comment='', external_id='')
TradeOrder(ticket=1437331579, time_setup=1661348545, time_setup_msc=1661348545750, time_done=1661348551,
   time_done_msc=1661348551354, time_expiration=0, type=2, type_time=0, type_filling=2, state=2, magic=0,
   position_id=0, position_by_id=0, reason=3, volume_initial=0.01, volume_current=0.01, price_open=0.99281,
   sl=0.0, tp=0.0, price_current=0.99284, price_stoplimit=0.0, symbol='EURUSD', comment='', external_id='')
TradeOrder(ticket=1437331739, time_setup=1661348553, time_setup_msc=1661348553935, time_done=1661348563,
   time_done_msc=1661348563412, time_expiration=0, type=2, type_time=0, type_filling=2, state=2, magic=0,
   position_id=0, position_by_id=0, reason=3, volume_initial=0.01, volume_current=0.01, price_open=0.99285,
   sl=0.0, tp=0.0, price_current=0.99286, price_stoplimit=0.0, symbol='EURUSD', comment='', external_id='')
...
   
        ticket          time_setup           time_done  type  ... _initial  price_open  price_current  symbol comment
0   1437318706 2022-08-24 13:34:25 2022-08-24 13:34:43     2          0.01     0.99301        0.99311  EURUSD        
1   1437331579 2022-08-24 13:42:25 2022-08-24 13:42:31     2          0.01     0.99281        0.99284  EURUSD        
2   1437331739 2022-08-24 13:42:33 2022-08-24 13:42:43     2          0.01     0.99285        0.99286  EURUSD
...

```

We can see that in September, there were only 44 orders, 15 of which included the GBP currency (an odd number due to the open position). The history contains 14 canceled orders.

int history_deals_total(date_from, date_to)

The history_deals_total function returns the number of deals in history for the specified period.

The function is an analog of [HistoryDealsTotal](/en/book/automation/experts/experts_history_select).

The history_deals_get function has several forms and is designed to select trades with the ability to filter by order ticket or position ID. All forms of the function return an array of named tuples TradeDeal, with fields reflecting properties from the [ENUM_DEAL_PROPERTY_enumerations](/en/book/automation/experts/experts_deal_properties) (the prefix "DEAL_" has been removed from the field names and lowercase has been applied). In case of an error, we get None.

namedtuple[] history_deals_get(date_from, date_to, group = <"PATTERN">)

namedtuple[] history_deals_get(ticket = <ORDER_TICKET>)

namedtuple[] history_deals_get(position = <POSITION_ID>)

The first form of the function is similar to requesting historical orders using history_orders_get.

The second form allows the selection of deals generated by a specific order by its ticket (the DEAL_ORDER property).

Finally, the third form requests deals that have formed a position with a given ID (the DEAL_POSITION_ID property).

The function allows you to get all transactions together with their properties in one call, which is analogous to the bunch of [HistoryDealsTotal](/en/book/automation/experts/experts_history_select), [HistoryDealSelect](/en/book/automation/experts/experts_history_select), and [HistoryDealGet](/en/book/automation/experts/experts_historydealget_funcs)[-functions](/en/book/automation/experts/experts_historydealget_funcs).

Here is the main part of the test script historydealsget.py.

```
# set the time range
from_date = datetime(2020, 1, 1)
to_date = datetime.now() 
   
# get trades for symbols whose names do not contain either "EUR" or "GBP"
deals = mt5.history_deals_get(from_date, to_date, group="*,!*EUR*,!*GBP*") 
if deals == None: 
   print("No deals, error code={}".format(mt5.last_error()))
elif len(deals) > 0: 
   print("history_deals_get(from_date, to_date, group=\"*,!*EUR*,!*GBP*\") =",
   len(deals)) 
   # display all received deals as they are
   for deal in deals: 
      print("  ",deal) 
   # display these trades as a table using pandas.DataFrame
   df = pd.DataFrame(list(deals), columns = deals[0]._asdict().keys()) 
   df['time'] = pd.to_datetime(df['time'], unit='s')
   df.drop(['time_msc','commission','fee'], axis = 1, inplace = True)
   print(df) 

```

An example of result:

```
history_deals_get(from_date, to_date, group="*,!*EUR*,!*GBP*") = 12
   TradeDeal(ticket=1109160642, order=0, time=1632188460, time_msc=1632188460852, type=2, entry=0, magic=0, position_id=0, reason=0, volume=0.0, price=0.0, commission=0.0, swap=0.0, profit=10000.0, fee=0.0, symbol='', comment='', external_id='')
   TradeDeal(ticket=1250629232, order=1268074569, time=1645709385, time_msc=1645709385815, type=0, entry=0, magic=0, position_id=1268074569, reason=0, volume=0.01, price=1970.98, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250639814, order=1268085019, time=1645709950, time_msc=1645709950618, type=1, entry=1, magic=0, position_id=1268074569, reason=0, volume=0.01, price=1970.09, commission=0.0, swap=0.0, profit=-0.89, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250639928, order=1268085129, time=1645709955, time_msc=1645709955502, type=1, entry=0, magic=0, position_id=1268085129, reason=0, volume=0.01, price=1969.98, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250640111, order=1268085315, time=1645709965, time_msc=1645709965148, type=0, entry=1, magic=0, position_id=1268085129, reason=0, volume=0.01, price=1970.17, commission=0.0, swap=0.0, profit=-0.19, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250640309, order=1268085512, time=1645709973, time_msc=1645709973623, type=1, entry=0, magic=0, position_id=1268085512, reason=0, volume=0.1, price=1970.09, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250640400, order=1268085611, time=1645709978, time_msc=1645709978701, type=0, entry=1, magic=0, position_id=1268085512, reason=0, volume=0.1, price=1970.22, commission=0.0, swap=0.0, profit=-1.3, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250640616, order=1268085826, time=1645709988, time_msc=1645709988277, type=1, entry=0, magic=0, position_id=1268085826, reason=0, volume=1.1, price=1969.95, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1250640810, order=1268086019, time=1645709996, time_msc=1645709996990, type=0, entry=1, magic=0, position_id=1268085826, reason=0, volume=1.1, price=1969.88, commission=0.0, swap=0.0, profit=7.7, fee=0.0, symbol='XAUUSD', comment='', external_id='')
   TradeDeal(ticket=1445796125, order=1468026008, time=1664199450, time_msc=1664199450488, type=0, entry=0, magic=234000, position_id=1468026008, reason=3, volume=0.1, price=144.132, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='USDJPY', comment='python script op', external_id='')
   TradeDeal(ticket=1445796155, order=1468026041, time=1664199452, time_msc=1664199452567, type=1, entry=1, magic=234000, position_id=1468026008, reason=3, volume=0.1, price=144.124, commission=0.0, swap=0.0, profit=-0.56, fee=0.0, symbol='USDJPY', comment='python script cl', external_id='')
   TradeDeal(ticket=1446217804, order=1468454363, time=1664217233, time_msc=1664217233239, type=1, entry=0, magic=0, position_id=1468454363, reason=0, volume=0.01, price=0.99145, commission=0.0, swap=0.0, profit=0.0, fee=0.0, symbol='USDCHF', comment='', external_id='')
   
        ticket       order                time t  e   position_id  volume       price    profit  symbol  comment external_id
0   1109160642           0 2021-09-21 01:41:00  2   0              0    0.00     0.00000  10000.00                             
1   1250629232  1268074569 2022-02-24 13:29:45  0   0     1268074569    0.01  1970.98000      0.00  XAUUSD                     
2   1250639814  1268085019 2022-02-24 13:39:10  1   1     1268074569    0.01  1970.09000     -0.89  XAUUSD                     
3   1250639928  1268085129 2022-02-24 13:39:15  1   0     1268085129    0.01  1969.98000      0.00  XAUUSD                     
4   1250640111  1268085315 2022-02-24 13:39:25  0   1     1268085129    0.01  1970.17000     -0.19  XAUUSD                     
5   1250640309  1268085512 2022-02-24 13:39:33  1   0     1268085512    0.10  1970.09000      0.00  XAUUSD                     
6   1250640400  1268085611 2022-02-24 13:39:38  0   1     1268085512    0.10  1970.22000     -1.30  XAUUSD                     
7   1250640616  1268085826 2022-02-24 13:39:48  1   0     1268085826    1.10  1969.95000      0.00  XAUUSD                     
8   1250640810  1268086019 2022-02-24 13:39:56  0   1     1268085826    1.10  1969.88000      7.70  XAUUSD                     
9   1445796125  1468026008 2022-09-26 13:37:30  0   0     1468026008    0.10   144.13200      0.00  USDJPY  python script op   
10  1445796155  1468026041 2022-09-26 13:37:32  1   1     1468026008    0.10   144.12400     -0.56  USDJPY  python script cl   
11  1446217804  1468454363 2022-09-26 18:33:53  1   0     1468454363    0.01     0.99145      0.00  USDCHF                     
 

```
