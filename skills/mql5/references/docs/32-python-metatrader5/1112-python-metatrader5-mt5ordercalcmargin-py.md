# order_calc_margin

Return margin in the account currency to perform a specified trading operation.

```
order_calc_margin(
   action,      // order type (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
   symbol,      // symbol name
   volume,      // volume
   price        // open price
   )

```

Parameters

action

[in]  Order type taking values from the [ORDER_TYPE](/en/docs/python_metatrader5/mt5ordercalcmargin_py#order_type) enumeration. Required unnamed parameter.

symbol

[in]  Financial instrument name. Required unnamed parameter.

volume

[in]  Trading operation volume. Required unnamed parameter.

price

[in]  Open price. Required unnamed parameter.

Return Value

Real value if successful, otherwise None. The error info can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

The function allows estimating the margin necessary for a specified order type on the current account and in the current market environment without considering the current pending orders and open positions. The function is similar to [OrderCalcMargin](/en/docs/trading/ordercalcmargin).

ORDER_TYPE

| ID | Description |
| --- | --- |
| ORDER_TYPE_BUY | Market buy order |
| ORDER_TYPE_SELL | Market sell order |
| ORDER_TYPE_BUY_LIMIT | Buy Limit pending order |
| ORDER_TYPE_SELL_LIMIT | Sell Limit pending order |
| ORDER_TYPE_BUY_STOP | Buy Stop pending order |
| ORDER_TYPE_SELL_STOP | Sell Stop pending order |
| ORDER_TYPE_BUY_STOP_LIMIT | Upon reaching the order price, Buy Limit pending order is placed at StopLimit price |
| ORDER_TYPE_SELL_STOP_LIMIT | Upon reaching the order price, Sell Limit pending order is placed at StopLimit price |
| ORDER_TYPE_CLOSE_BY | Order for closing a position by an opposite one |

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
 
# get account currency
account_currency=mt5.account_info().currency
print("Account currency:",account_currency)
 
# arrange the symbol list
symbols=("EURUSD","GBPUSD","USDJPY", "USDCHF","EURJPY","GBPJPY")
print("Symbols to check margin:", symbols)
action=mt5.ORDER_TYPE_BUY
lot=0.1
for symbol in symbols:
    symbol_info=mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol,"not found, skipped")
        continue
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, skipped",symbol)
            continue
    ask=mt5.symbol_info_tick(symbol).ask
    margin=mt5.order_calc_margin(action,symbol,lot,ask)
    if margin != None:
        print("   {} buy {} lot margin: {} {}".format(symbol,lot,margin,account_currency));
    else:
        print("order_calc_margin failed: , error code =", mt5.last_error())
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
 
Account currency: USD
 
Symbols to check margin: ('EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'EURJPY', 'GBPJPY')
   EURUSD buy 0.1 lot margin: 109.91 USD
   GBPUSD buy 0.1 lot margin: 122.73 USD
   USDJPY buy 0.1 lot margin: 100.0 USD
   USDCHF buy 0.1 lot margin: 100.0 USD
   EURJPY buy 0.1 lot margin: 109.91 USD
   GBPJPY buy 0.1 lot margin: 122.73 USD

```

See also

[order_calc_profit](/en/docs/python_metatrader5/mt5ordercalcprofit_py), [order_check](/en/docs/python_metatrader5/mt5ordercheck_py)
