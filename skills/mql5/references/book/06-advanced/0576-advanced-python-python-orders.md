# Getting the number and list of active orders

The Python API provides the following functions for working with active orders.

int orders_total()

The orders_total function returns the number of active orders.

The function is an analog of [Orders Total](/en/book/automation/experts/experts_order_list).

Detailed information about each order can be obtained using the orders_get function, which has several options with the ability to filter by symbol or ticket. Either way, the function returns the array of named tuples TradeOrder (field names match [ENUM_ORDER_PROPERTY_enumerations](/en/book/automation/experts/experts_order_properties) without the "ORDER_" prefix and reduced to lowercase). In case of an error, the result is None.

namedtuple[] orders_get()

namedtuple[] orders_get(symbol = <"SYMBOL">)

namedtuple[] orders_get(group = <"PATTERN">)

namedtuple[] orders_get(ticket = <TICKET>)

The orders_get function without parameters returns orders for all symbols.

The optional named parameter symbol makes it possible to specify a specific symbol name for order selection.

The optional named parameter group is intended for specifying a search pattern using the wildcard character '*' (as a substitute for an arbitrary number of any characters, including zero characters in the given place of the pattern) and the condition logical negation character '!'. The filter template operation principle was described in the section [Getting information about financial instruments](/en/book/advanced/python/python_symbols).

If the ticket parameter is specified, a certain order is searched.

In one function call, you can get all active orders. It is an analog of the combined use of [OrdersTotal](/en/book/automation/experts/experts_order_list), [OrderSelect](/en/book/automation/experts/experts_order_list), and [OrderGet](/en/book/automation/experts/experts_orderget_funcs)[ functions](/en/book/automation/experts/experts_orderget_funcs).

In the next example (MQL5/Scripts/MQL5Book/Python/ordersget.py), we request information about orders using different ways.

```
import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # how many columns to show
pd.set_option('display.width', 1500)      # max. table width to display
   
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize(): 
   print("initialize() failed, error code =", mt5.last_error())
   quit()
   
# display information about active orders on the GBPUSD symbol
orders = mt5.orders_get(symbol = "GBPUSD")
if orders is None:
   print("No orders on GBPUSD, error code={}".format(mt5.last_error()))
else:
   print("Total orders on GBPUSD:", len(orders))
   # display all active orders
   for order in orders:
      print(order)
print()
   
# getting a list of orders on symbols whose names contain "*GBP*"
gbp_orders = mt5.orders_get(group="*GBP*")
if gbp_orders is None: 
   print("No orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
else: 
   print("orders_get(group=\"*GBP*\")={}".format(len(gbp_orders)))
   # display orders as a table using pandas.DataFrame
   df = pd.DataFrame(list(gbp_orders), columns = gbp_orders[0]._asdict().keys())
   df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id',
   'reason', 'volume_initial', 'price_stoplimit'], axis = 1, inplace = True)
   df['time_setup'] = pd.to_datetime(df['time_setup'], unit = 's')
   print(df)
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

The sample result is below:

```
Total orders on GBPUSD: 2 
TradeOrder(ticket=554733548, time_setup=1585153667, time_setup_msc=1585153667718, time_done=0, time_done_msc=0, time_expiration=0, type=3, type_time=0, ... 
TradeOrder(ticket=554733621, time_setup=1585153671, time_setup_msc=1585153671419, time_done=0, time_done_msc=0, time_expiration=0, type=2, type_time=0, ... 
  
orders_get(group="*GBP*")=4 
      ticket          time_setup  time_setup_msc  type ... volume_current  price_open   sl   tp  price_current  symbol comment external_id 
0  554733548 2020-03-25 16:27:47   1585153667718     3 ...            0.2     1.25379  0.0  0.0        1.16803  GBPUSD                     
1  554733621 2020-03-25 16:27:51   1585153671419     2 ...            0.2     1.14370  0.0  0.0        1.16815  GBPUSD                     
2  554746664 2020-03-25 16:38:14   1585154294401     3 ...            0.2     0.93851  0.0  0.0        0.92428  EURGBP                     
3  554746710 2020-03-25 16:38:17   1585154297022     2 ...            0.2     0.90527  0.0  0.0        0.92449  EURGBP    

```
