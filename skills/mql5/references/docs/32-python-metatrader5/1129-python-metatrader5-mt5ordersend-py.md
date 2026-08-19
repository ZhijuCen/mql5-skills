# order_send

Send a [request](/en/docs/constants/structures/mqltraderequest) to perform a [trading operation](/en/docs/constants/tradingconstants/enum_trade_request_actions) from the terminal to the trade server. The function is similar to [OrderSend](/en/docs/trading/ordersend).

```
order_send(
   request      // request structure
   );

```

Parameters

request

[in]  [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type structure describing a required trading action. Required unnamed parameter. Example of filling in a request and the enumeration content are described below.

Return Value

Execution result as the [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) structure. The request field in the answer contains the structure of a trading request passed to order_send(). The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

The [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) trading request structure

| Field | Description |
| --- | --- |
| action | Trading operation type. The value can be one of the values of the  TRADE_REQUEST_ACTIONS  enumeration |
| magic | EA ID. Allows arranging the analytical handling of trading orders. Each EA can set a unique ID when sending a trading request |
| order | Order ticket. Required for modifying pending orders |
| symbol | The name of the trading instrument, for which the order is placed. Not required when modifying orders and closing positions |
| volume | Requested volume of a deal in lots. A real volume when making a deal depends on an  order execution type . |
| price | Price at which an order should be executed. The price is not set in case of market orders for instruments of the "Market Execution" ( SYMBOL_TRADE_EXECUTION_MARKET ) type having the  TRADE_ACTION_DEAL  type |
| stoplimit | A price a pending Limit order is set at when the price reaches the 'price' value (this condition is mandatory). The pending order is not passed to the trading system until that moment |
| sl | A price a Stop Loss order is activated at when the price moves in an unfavorable direction |
| tp | A price a Take Profit order is activated at when the price moves in a favorable direction |
| deviation | Maximum acceptable deviation from the requested price, specified in  points |
| type | Order type. The value can be one of the values of the  ORDER_TYPE  enumeration |
| type_filling | Order filling type. The value can be one of the  ORDER_TYPE_FILLING  values |
| type_time | Order type by expiration. The value can be one of the  ORDER_TYPE_TIME  values |
| expiration | Pending order expiration time (for  TIME_SPECIFIED  type orders) |
| comment | Comment to an order |
| position | Position ticket. Fill it when changing and closing a position for its clear identification. Usually, it is the same as the ticket of the order that opened the position. |
| position_by | Opposite position ticket. It is used when closing a position by an opposite one (opened at the same symbol but in the opposite direction). |

Note

A trading request passes several verification stages on the trade server. First, the validity of all the necessary request fields is checked. If there are no errors, the server accepts the order for further handling. See the [OrderSend](/en/docs/trading/ordersend) function description for the details about executing trading operations.

Example:

```
import time
import MetaTrader5 as mt5
 
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# prepare the buy request structure
symbol = "USDJPY"
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
 
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
 
# send a trading request
result = mt5.order_send(request)
# check the execution result
print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    print("shutdown() and quit")
    mt5.shutdown()
    quit()
 
print("2. order_send done, ", result)
print("   opened position with POSITION_TICKET={}".format(result.order))
print("   sleep 2 seconds before closing position #{}".format(result.order))
time.sleep(2)
# create a close request
position_id=result.order
price=mt5.symbol_info_tick(symbol).bid
deviation=20
request={
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "position": position_id,
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
# send a trading request
result=mt5.order_send(request)
# check the execution result
print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("4. order_send failed, retcode={}".format(result.retcode))
    print("   result",result)
else:
    print("4. position #{} closed, {}".format(position_id,result))
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
 
Result
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
1. order_send(): by USDJPY 0.1 lots at 108.023 with deviation=20 points
2. order_send done,  OrderSendResult(retcode=10009, deal=535084512, order=557416535, volume=0.1, price=108.023, ...
   opened position with POSITION_TICKET=557416535
   sleep 2 seconds before closing position #557416535
3. close position #557416535: sell USDJPY 0.1 lots at 108.018 with deviation=20 points
4. position #557416535 closed, OrderSendResult(retcode=10009, deal=535084631, order=557416654, volume=0.1, price=...
   retcode=10009
   deal=535084631
   order=557416654
   volume=0.1
   price=108.015
   bid=108.015
   ask=108.02
   comment=Request executed
   request_id=55
   retcode_external=0
   request=TradeRequest(action=1, magic=234000, order=0, symbol='USDJPY', volume=0.1, price=108.018, stoplimit=0.0, ...
       traderequest: action=1
       traderequest: magic=234000
       traderequest: order=0
       traderequest: symbol=USDJPY
       traderequest: volume=0.1
       traderequest: price=108.018
       traderequest: stoplimit=0.0
       traderequest: sl=0.0
       traderequest: tp=0.0
       traderequest: deviation=20
       traderequest: type=1
       traderequest: type_filling=2
       traderequest: type_time=0
       traderequest: expiration=0
       traderequest: comment=python script close
       traderequest: position=557416535
       traderequest: position_by=0

```

See also

[order_check](/en/docs/python_metatrader5/mt5ordercheck_py), [OrderSend](/en/docs/trading/ordersend),[Trading operation types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Trading request structure](/en/docs/constants/structures/mqltraderequest), [Structure of the trading request check results](/en/docs/constants/structures/mqltradecheckresult), [Structure of the trading request result](/en/docs/constants/structures/mqltraderesult)
