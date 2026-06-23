# Checking and sending a trade order

If necessary, you can trade directly from a Python script. The pair of functions order_check and order_send allows you to pre-check and then execute a trading operation.

For both functions, the only parameter is the request structure TradeRequest (it can be initialized as a dictionary in Python, see an example). The structure fields are exactly the same as for [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest).

OrderCheckResult order_check(request)

The order_check function checks the correctness of trade request fields and the sufficiency of funds to complete the required trading operation.

The result of the function is returned as the OrderCheckResult structure. It repeats the structure of [MqlTradeCheckResult](/en/book/automation/experts/experts_mqltradecheckresult) but additionally contains the request field with a copy of the original request.

The order_check function is an analog of [OrderCheck](/en/book/automation/experts/experts_ordercheck).

Example (MQL5/Scripts/MQL5Book/python/ordercheck.py):

```
import MetaTrader5 as mt5
   
# let's establish a connection to the MetaTrader 5 terminal
...   
# get account currency for information
account_currency=mt5.account_info().currency
print("Account currency:", account_currency)
   
# get the necessary properties of the deal symbol
symbol = "USDJPY"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
   print(symbol, "not found, can not call order_check()")
   mt5.shutdown()
   quit()
   
point = mt5.symbol_info(symbol).point
# if the symbol is not available in the Market Watch, add it
if not symbol_info.visible:
   print(symbol, "is not visible, trying to switch on")
   if not mt5.symbol_select(symbol, True):
      print("symbol_select({}) failed, exit", symbol)
      mt5.shutdown()
      quit()
   
# prepare the query structure as a dictionary
request = \
{
   "action": mt5.TRADE_ACTION_DEAL,
   "symbol": symbol,
   "volume": 1.0,
   "type": mt5.ORDER_TYPE_BUY,
   "price": mt5.symbol_info_tick(symbol).ask,
   "sl": mt5.symbol_info_tick(symbol).ask - 100 * point,
   "tp": mt5.symbol_info_tick(symbol).ask + 100 * point,
   "deviation": 10,
   "magic": 234000,
   "comment": "python script",
   "type_time": mt5.ORDER_TIME_GTC,
   "type_filling": mt5.ORDER_FILLING_RETURN,
}
   
# run the test and display the result as is
result = mt5.order_check(request)
print(result)                       # [?this is not in the help log?]
   
# convert the result to a dictionary and output element by element
result_dict = result._asdict()
for field in result_dict.keys():
   print("   {}={}".format(field, result_dict[field]))
   # if this is the structure of a trade request, then output it element by element as well
   if field == "request":
      traderequest_dict = result_dict[field]._asdict()
      for tradereq_filed in traderequest_dict:
         print("       traderequest: {}={}".format(tradereq_filed,
         traderequest_dict[tradereq_filed]))
   
# terminate the connection to the terminal
mt5.shutdown()

```

Result:

```
Account currency: USD
OrderCheckResult(retcode=0, balance=10000.17, equity=10000.17, profit=0.0, margin=1000.0,...
   retcode=0
   balance=10000.17
   equity=10000.17
   profit=0.0
   margin=1000.0
   margin_free=9000.17
   margin_level=1000.017
   comment=Done
   request=TradeRequest(action=1, magic=234000, order=0, symbol='USDJPY', volume=1.0, price=144.128,...
       traderequest: action=1
       traderequest: magic=234000
       traderequest: order=0
       traderequest: symbol=USDJPY
       traderequest: volume=1.0
       traderequest: price=144.128
       traderequest: stoplimit=0.0
       traderequest: sl=144.028
       traderequest: tp=144.228
       traderequest: deviation=10
       traderequest: type=0
       traderequest: type_filling=2
       traderequest: type_time=0
       traderequest: expiration=0
       traderequest: comment=python script
       traderequest: position=0
       traderequest: position_by=0

```

OrderSendResult order_send(request)

The order_send function sends a request from the terminal to the trading server to make a trade operation.

The result of the function is returned as the OrderSendResult structure. It repeats the structure of [MqlTradeResult](/en/book/automation/experts/experts_mqltraderesult) but additionally contains the request field with a copy of the original request.

The function is an analog of [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync).

Example (MQL5/Scripts/MQL5Book/python/ordersend.py):

```
import time 
import MetaTrader5 as mt5 
   
# let's establish a connection to the MetaTrader 5 terminal
...   
# assign the properties of the working symbol
symbol = "USDJPY"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
   print(symbol, "not found, can not trade")
   mt5.shutdown()
   quit()
   
# if the symbol is not available in the Market Watch, add it
if not symbol_info.visible:
   print(symbol, "is not visible, trying to switch on")
   if not mt5.symbol_select(symbol, True):
      print("symbol_select({}) failed, exit", symbol)
      mt5.shutdown()
      quit()
   
# let's prepare the request structure for the purchase
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = \
{ 
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
   
# send a trade request to open a position
result = mt5.order_send(request)
# check the execution result
print("1. order_send(): by {} {} lots at {}".format(symbol, lot, price));
if result.retcode != mt5.TRADE_RETCODE_DONE:
   print("2. order_send failed, retcode={}".format(result.retcode))
   # request the result as a dictionary and display it element by element
   result_dict = result._asdict()
   for field in result_dict.keys():
      print("   {}={}".format(field, result_dict[field]))
      # if this is the structure of a trade request, then output it element by element as well
      if field == "request":
         traderequest_dict = result_dict[field]._asdict()
         for tradereq_filed in traderequest_dict: 
            print("       traderequest: {}={}".format(tradereq_filed,
            traderequest_dict[tradereq_filed]))
   print("shutdown() and quit")
   mt5.shutdown()
   quit()
   
print("2. order_send done, ", result)
print("   opened position with POSITION_TICKET={}".format(result.order))
print("   sleep 2 seconds before closing position #{}".format(result.order))
time.sleep(2)
# create a request to close 
position_id = result.order
price = mt5.symbol_info_tick(symbol).bid
request = \
{
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
# send a trade request to close the position
result = mt5.order_send(request)
# check the execution result
print("3. close position #{}: sell {} {} lots at {}".format(position_id,
symbol, lot, price));
if result.retcode != mt5.TRADE_RETCODE_DONE:
   print("4. order_send failed, retcode={}".format(result.retcode))
   print("   result", result)
else: 
   print("4. position #{} closed, {}".format(position_id, result))
   # request the result as a dictionary and display it element by element
   result_dict = result._asdict()
   for field in result_dict.keys():
      print("   {}={}".format(field, result_dict[field])) 
      # if this is the structure of a trade request, then output it element by element as well
      if field == "request": 
         traderequest_dict = result_dict[field]._asdict()
         for tradereq_filed in traderequest_dict:
            print("       traderequest: {}={}".format(tradereq_filed,
            traderequest_dict[tradereq_filed]))
   
# terminate the connection to the terminal
mt5.shutdown()

```

Result:

```
1. order_send(): by USDJPY 0.1 lots at 144.132
2. order_send done,  OrderSendResult(retcode=10009, deal=1445796125, order=1468026008, volume=0.1, price=144.132,...
   opened position with POSITION_TICKET=1468026008
   sleep 2 seconds before closing position #1468026008
3. close position #1468026008: sell USDJPY 0.1 lots at 144.124
4. position #1468026008 closed, OrderSendResult(retcode=10009, deal=1445796155, order=1468026041, volume=0.1, price=144.124,...
   retcode=10009
   deal=1445796155
   order=1468026041
   volume=0.1
   price=144.124
   bid=144.124
   ask=144.132
   comment=Request executed
   request_id=2
   retcode_external=0
   request=TradeRequest(action=1, magic=234000, order=0, symbol='USDJPY', volume=0.1, price=144.124, stoplimit=0.0,...
       traderequest: action=1
       traderequest: magic=234000
       traderequest: order=0
       traderequest: symbol=USDJPY
       traderequest: volume=0.1
       traderequest: price=144.124
       traderequest: stoplimit=0.0
       traderequest: sl=0.0
       traderequest: tp=0.0
       traderequest: deviation=20
       traderequest: type=1
       traderequest: type_filling=2
       traderequest: type_time=0
       traderequest: expiration=0
       traderequest: comment=python script close
       traderequest: position=1468026008
       traderequest: position_by=0

```
