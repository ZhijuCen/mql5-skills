# order_check

Check funds sufficiency for performing a required [trading operation](/en/docs/constants/tradingconstants/enum_trade_request_actions). Check result are returned as the [MqlTradeCheckResult](/en/docs/constants/structures/mqltradecheckresult) structure.

```
order_check(
   request      // request structure
   );

```

Parameters

request

[in]  [MqlTradeRequest](/en/docs/python_metatrader5/mt5ordersend_py#traderequest) type structure describing a required trading action. Required unnamed parameter. Example of filling in a request and the enumeration content are described below.

Return Value

Check result as the [MqlTradeCheckResult](/en/docs/constants/structures/mqltradecheckresult) structure. The request field in the answer contains the structure of a trading request passed to order_check().

Note

Successful sending of a request does not entail that the requested trading operation will be executed successfully. The order_check function is similar to [OrderCheck](/en/docs/trading/ordercheck).

TRADE_REQUEST_ACTIONS

| ID | Description |
| --- | --- |
| TRADE_ACTION_DEAL | Place an order for an instant deal with the specified parameters (set a market order) |
| TRADE_ACTION_PENDING | Place an order for performing a deal at specified conditions (pending order) |
| TRADE_ACTION_SLTP | Change open position Stop Loss and Take Profit |
| TRADE_ACTION_MODIFY | Change parameters of the previously placed trading order |
| TRADE_ACTION_REMOVE | Remove previously placed pending order |
| TRADE_ACTION_CLOSE_BY | Close a position by an opposite one |

ORDER_TYPE_FILLING

| ID | Description |
| --- | --- |
| ORDER_FILLING_FOK | This execution policy means that an order can be executed only in the specified volume. If the necessary amount of a financial instrument is currently unavailable in the market, the order will not be executed. The desired volume can be made up of several available offers. |
| ORDER_FILLING_IOC | An agreement to execute a deal at the maximum volume available in the market within the volume specified in the order. If the request cannot be filled completely, an order with the available volume will be executed, and the remaining volume will be canceled. |
| ORDER_FILLING_RETURN | This policy is used only for market ( ORDER_TYPE_BUY and   ORDER_TYPE_ SELL), limit and stop limit orders (ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT, ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT) and only for the symbols with Market or Exchange execution  modes . If filled partially, a market or limit order with the remaining volume is not canceled, and is processed further. 
 During activation of the ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT orders, an appropriate limit order ORDER_TYPE_BUY_LIMIT/ORDER_TYPE_SELL_LIMIT with the ORDER_FILLING_RETURN type is created. |

ORDER_TYPE_TIME

| ID | Description |
| --- | --- |
| ORDER_TIME_GTC | The order stays in the queue until it is manually canceled |
| ORDER_TIME_DAY | The order is active only during the current trading day |
| ORDER_TIME_SPECIFIED | The order is active until the specified date |
| ORDER_TIME_SPECIFIED_DAY | The order is active until 23:59:59 of the specified day. If this time appears to be out of a trading session, the expiration is processed at the nearest trading time. |

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
 
# prepare the request structure
symbol="USDJPY"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()
 
# if the symbol is unavailable in MarketWatch, add it
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol,True):
        print("symbol_select({}}) failed, exit",symbol)
        mt5.shutdown()
        quit()
 
# prepare the request
point=mt5.symbol_info(symbol).point
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 1.0,
    "type": mt5.ORDER_TYPE_BUY,
    "price": mt5.symbol_info_tick(symbol).ask,
    "sl": mt5.symbol_info_tick(symbol).ask-100*point,
    "tp": mt5.symbol_info_tick(symbol).ask+100*point,
    "deviation": 10,
    "magic": 234000,
    "comment": "python script",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
 
# perform the check and display the result 'as is'
result = mt5.order_check(request)
print(result);
# request the result as a dictionary and display it element by element
result_dict=result._asdict()
for field in result_dict.keys():
    print("   {}={}".format(field,result_dict[field]))
    # if this is a trading request structure, display it element by element as well
    if field=="request":
        traderequest_dict=result_dict[field]._asdict()
        for tradereq_filed in traderequest_dict:
            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
 
Account currecy: USD
   retcode=0
   balance=101300.53
   equity=68319.53
   profit=-32981.0
   margin=51193.67
   margin_free=17125.86
   margin_level=133.45308121101692
   comment=Done
   request=TradeRequest(action=1, magic=234000, order=0, symbol='USDJPY', volume=1.0, ...
       traderequest: action=1
       traderequest: magic=234000
       traderequest: order=0
       traderequest: symbol=USDJPY
       traderequest: volume=1.0
       traderequest: price=108.081
       traderequest: stoplimit=0.0
       traderequest: sl=107.98100000000001
       traderequest: tp=108.181
       traderequest: deviation=10
       traderequest: type=0
       traderequest: type_filling=2
       traderequest: type_time=0
       traderequest: expiration=0
       traderequest: comment=python script
       traderequest: position=0
       traderequest: position_by=0

```

See also

[order_send](/en/docs/python_metatrader5/mt5ordersend_py),[ OrderCheck](/en/docs/trading/ordercheck), [Trading operation types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Trading request structure](/en/docs/constants/structures/mqltraderequest), [Structure of the trading request check results](/en/docs/constants/structures/mqltradecheckresult), [Structure of the trading request result](/en/docs/constants/structures/mqltraderesult)
