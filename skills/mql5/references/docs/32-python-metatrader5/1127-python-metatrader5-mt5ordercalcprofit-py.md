# order_calc_profit

Return profit in the account currency for a specified trading operation.

```
order_calc_profit(
   action,          // order type (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
   symbol,          // symbol name
   volume,          // volume
   price_open,      // open price
   price_close      // close price
   );

```

Parameters

action

[in]  Order type may take one of the two [ORDER_TYPE](/en/docs/python_metatrader5/mt5ordercalcmargin_py#order_type) enumeration values: ORDER_TYPE_BUY or ORDER_TYPE_SELL. Required unnamed parameter.

symbol

[in]  Financial instrument name. Required unnamed parameter.

volume

[in]  Trading operation volume. Required unnamed parameter.

price_open

[in]  Open price. Required unnamed parameter.

price_close

[in]  Close price. Required unnamed parameter.

Return Value

Real value if successful, otherwise None. The error info can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

The function allows estimating a trading operation result on the current account and in the current trading environment. The function is similar to [OrderCalcProfit](/en/docs/trading/ordercalcprofit).

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
symbols = ("EURUSD","GBPUSD","USDJPY")
print("Symbols to check margin:", symbols)
# estimate profit for buying and selling
lot=1.0
distance=300
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
    point=mt5.symbol_info(symbol).point
    symbol_tick=mt5.symbol_info_tick(symbol)
    ask=symbol_tick.ask
    bid=symbol_tick.bid
    buy_profit=mt5.order_calc_profit(mt5.ORDER_TYPE_BUY,symbol,lot,ask,ask+distance*point)
    if buy_profit!=None:
        print("   buy {} {} lot: profit on {} points => {} {}".format(symbol,lot,distance,buy_profit,account_currency));
    else:
        print("order_calc_profit(ORDER_TYPE_BUY) failed, error code =",mt5.last_error())
    sell_profit=mt5.order_calc_profit(mt5.ORDER_TYPE_SELL,symbol,lot,bid,bid-distance*point)
    if sell_profit!=None:
        print("   sell {} {} lots: profit on {} points => {} {}".format(symbol,lot,distance,sell_profit,account_currency));
    else:
        print("order_calc_profit(ORDER_TYPE_SELL) failed, error code =",mt5.last_error())
    print()
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
 
Account currency: USD
Symbols to check margin: ('EURUSD', 'GBPUSD', 'USDJPY')
   buy EURUSD 1.0 lot: profit on 300 points => 300.0 USD
   sell EURUSD 1.0 lot: profit on 300 points => 300.0 USD
 
   buy GBPUSD 1.0 lot: profit on 300 points => 300.0 USD
   sell GBPUSD 1.0 lot: profit on 300 points => 300.0 USD
 
   buy USDJPY 1.0 lot: profit on 300 points => 276.54 USD
   sell USDJPY 1.0 lot: profit on 300 points => 278.09 USD

```

See also

[order_calc_margin](/en/docs/python_metatrader5/mt5ordercalcmargin_py), [order_check](/en/docs/python_metatrader5/mt5ordercheck_py)
