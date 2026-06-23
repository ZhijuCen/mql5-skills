# orders_total

Get the number of active orders.

```
orders_total()

```

Return Value

Integer value.

Note

The function is similar to [OrdersTotal](/en/docs/trading/orderstotal).

Example:

```
import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# check the presence of active orders
orders=mt5.orders_total()
if orders>0:
    print("Total orders=",orders)
else:
    print("Orders not found")
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

```

See also

[orders_get](/en/docs/python_metatrader5/mt5ordersget_py), [positions_total](/en/docs/python_metatrader5/mt5positionstotal_py)
