# OrderSend

The OrderSend() function is used for executing [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions) by sending [requests](/en/docs/constants/structures/mqltraderequest) to a trade server.

```
bool  OrderSend(
   MqlTradeRequest&  request,      // query structure
   MqlTradeResult&   result        // structure of the answer
   );

```

Parameters

request

[in]  Pointer to a structure of [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type describing the trade activity of the client.

result

[in,out]  Pointer to a structure of [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) type describing the result of trade operation in case of a successful completion (if true is returned).

Return Value

In case of a successful basic check of structures (index checking) returns true. However, this is not a sign of successful execution of a trade operation. For a more detailed description of the function execution result, analyze the fields of result structure.

Note

The trade requests go through several stages of checking on a trade server. First of all, it checks if all the required fields of the request parameter are filled out correctly. If there are no errors, the server accepts the order for further processing. If the order is successfully accepted by the trade server, the OrderSend() function returns true.

It is recommended to check the request before sending it to a trade server. To check requests, use the [OrderCheck()](/en/docs/trading/ordercheck) function. It checks if there are enough funds to execute the trade operation, and returns many useful parameters in the [results of trade request checking](/en/docs/constants/structures/mqltradecheckresult):

- [return code](/en/docs/constants/errorswarnings/enum_trade_return_codes) containing information about errors in the checked request;
- balance value that will appear after the trade operation is executed;
- equity value that will appear after the trade operation is executed;
- floating point value that will appear after the trade operation is executed;
- margin required for the trade operation;
- amount of free equity that will remain after the execution of the trade operation;
- the margin level that will be set after the trade operation is executed;
- comment to the reply code, error description.

When sending a market order (MqlTradeRequest.action=[TRADE_ACTION_DEAL](/en/docs/constants/tradingconstants/enum_trade_request_actions)), the successful result of the OrderSend() function does not mean that the order has been executed (appropriate trades have been performed). In this case, 'true' means only that the order has been successfully placed in the trading system for further execution. The trade server can fill in the deal or order field values in the returned [result structure](/en/docs/constants/structures/mqltraderesult), if it is aware of these data when forming a response to an OrderSend() call. Generally, event(s) of executing trades corresponding to an order may happen after sending a response to the OrderSend() call. Therefore, for any type of a trade request, when receiving the OrderSend() execution result, we should first check the retcode trade server response code and the retcode_external external system response code (if necessary) available in the obtained [result structure](/en/docs/constants/structures/mqltraderesult).

Each accepted order is stored on the trade server awaiting processing until one of the conditions for its execution occurs:

- expiration,
- appearance of an opposite request,
- order execution when the execution price appears,
- a request to cancel the order is received.

At the moment of the order processing, the trade server sends to the terminal a message about the occurrence of the [Trade](/en/docs/runtime/event_fire#trade) event, which can be processed by the [OnTrade()](/en/docs/event_handlers/ontrade) function.

The result of executing the trade request on a server sent by OrderSend() function can be tracked by [OnTradeTransaction](/en/docs/event_handlers/ontradetransaction) handler. It should be noted that OnTradeTransaction handler will be called several times when executing one trade request.

For example, when sending a market buy order, it is handled, an appropriate buy order is created for the account, the order is then executed and removed from the list of the open ones, then it is added to the orders history, an appropriate deal is added to the history and a new position is created. OnTradeTransaction function will be called for each of these events.

Example:

```
//--- value for ORDER_MAGIC
input long order_magic=55555;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- make sure that the account is demo
   if(AccountInfoInteger(ACCOUNT_TRADE_MODE)==ACCOUNT_TRADE_MODE_REAL)
     {
      Alert("Script operation is not allowed on a live account!");
      return;
     }
//--- place or delete order
   if(GetOrdersTotalByMagic(order_magic)==0) 
     {
      //--- no current orders - place an order
      uint res=SendRandomPendingOrder(order_magic);
      Print("Return code of the trade server ",res);
     }
   else // there are orders - delete orders
     {
      DeleteAllOrdersByMagic(order_magic);
     }
//---
  }
//+------------------------------------------------------------------+
//| Receives the current number of orders with specified ORDER_MAGIC |
//+------------------------------------------------------------------+
int GetOrdersTotalByMagic(long const magic_number)
  {
   ulong order_ticket;
   int total=0;
//--- go through all pending orders
   for(int i=0;i<OrdersTotal();i++)
      if((order_ticket=OrderGetTicket(i))>0)
         if(magic_number==OrderGetInteger(ORDER_MAGIC)) total++;
//---
   return(total);
  }
//+------------------------------------------------------------------+
//| Deletes all pending orders with specified ORDER_MAGIC            |
//+------------------------------------------------------------------+
void DeleteAllOrdersByMagic(long const magic_number)
  {
   ulong order_ticket;
//--- go through all pending orders
   for(int i=OrdersTotal()-1;i>=0;i--)
      if((order_ticket=OrderGetTicket(i))>0)
         //--- order with appropriate ORDER_MAGIC
         if(magic_number==OrderGetInteger(ORDER_MAGIC))
           {
            MqlTradeResult result={};
            MqlTradeRequest request={};
            request.order=order_ticket;
            request.action=TRADE_ACTION_REMOVE;
            OrderSend(request,result);
            //--- write the server reply to log
            Print(__FUNCTION__,": ",result.comment," reply code ",result.retcode);
           }
//---
  }
//+------------------------------------------------------------------+
//| Sets a pending order in a random way                             |
//+------------------------------------------------------------------+
uint SendRandomPendingOrder(long const magic_number)
  {
//--- prepare a request
   MqlTradeRequest request={};
   request.action=TRADE_ACTION_PENDING;         // setting a pending order
   request.magic=magic_number;                  // ORDER_MAGIC
   request.symbol=_Symbol;                      // symbol
   request.volume=0.1;                          // volume in 0.1 lots
   request.sl=0;                                // Stop Loss is not specified
   request.tp=0;                                // Take Profit is not specified     
//--- form the order type
   request.type=GetRandomType();                // order type
//--- form the price for the pending order
   request.price=GetRandomPrice(request.type);  // open price
//--- send a trade request
   MqlTradeResult result={};
   OrderSend(request,result);
//--- write the server reply to log  
   Print(__FUNCTION__,":",result.comment);
   if(result.retcode==10016) Print(result.bid,result.ask,result.price);
//--- return code of the trade server reply
   return result.retcode;
  }
//+------------------------------------------------------------------+
//| Returns type of a pending order in a random way                  |
//+------------------------------------------------------------------+
ENUM_ORDER_TYPE GetRandomType()
  {
   int t=MathRand()%4;
//---   0<=t<4
   switch(t)
     {
      case(0):return(ORDER_TYPE_BUY_LIMIT);
      case(1):return(ORDER_TYPE_SELL_LIMIT);
      case(2):return(ORDER_TYPE_BUY_STOP);
      case(3):return(ORDER_TYPE_SELL_STOP);
     }
//--- incorrect value
   return(WRONG_VALUE);
  }
//+------------------------------------------------------------------+
//| Returns price in a random way                                    |
//+------------------------------------------------------------------+
double GetRandomPrice(ENUM_ORDER_TYPE type)
  {
   int t=(int)type;
//--- stop levels for the symbol
   int distance=(int)SymbolInfoInteger(_Symbol,SYMBOL_TRADE_STOPS_LEVEL);
//--- receive data of the last tick
   MqlTick last_tick={};
   SymbolInfoTick(_Symbol,last_tick);
//--- calculate price according to the type
   double price;
   if(t==2 || t==5) // ORDER_TYPE_BUY_LIMIT or ORDER_TYPE_SELL_STOP
     {
      price=last_tick.bid; // depart from price Bid
      price=price-(distance+(MathRand()%10)*5)*_Point;
     }
   else             // ORDER_TYPE_SELL_LIMIT or ORDER_TYPE_BUY_STOP
     {
      price=last_tick.ask; // depart from price Ask
      price=price+(distance+(MathRand()%10)*5)*_Point;
     }
//---
   return(price);
  }

```

See also

[Trade Operation Types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Trade Request Structure](/en/docs/constants/structures/mqltraderequest), [Structure of Request Check Results](/en/docs/constants/structures/mqltradecheckresult), [Structure of a Trade Request Result](/en/docs/constants/structures/mqltraderesult)
