# OrderSendAsync

The OrderSendAsync() function is used for conducting asynchronous [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions) without waiting for the trade server's response to a sent [request](/en/docs/constants/structures/mqltraderequest). The function is designed for high-frequency trading, when under the terms of the trading algorithm it is unacceptable to waste time waiting for a response from the server.

```
bool  OrderSendAsync(
   MqlTradeRequest&  request,      // Request structure
   MqlTradeResult&   result        // Response structure
   );

```

Parameters

request

[in]  A pointer to a structure of the [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type that describes the trade action of the client.

result

[in,out]  A pointer to a structure of the [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) type that describes the result of a trade operation in case of successful execution of the function (if true is returned).

Return Value

Returns true if the request is sent to a trade server. In case the request is not sent, it returns false. In case the request is sent, in the result variable the response code contains [TRADE_RETCODE_PLACED](/en/docs/constants/errorswarnings/enum_trade_return_codes) value (code 10008) – "order placed". Successful execution means only the fact of sending, but does not give any guarantee that the request has reached the trade server and has been accepted for processing. When processing the received request, a trade server sends a reply to a client terminal notifying of change in the current state of positions, orders and deals, which leads to the generation of the [Trade](/en/docs/runtime/event_fire#trade) event.

The result of executing the trade request on a server sent by OrderSendAsync() function can be tracked by [OnTradeTransaction](/en/docs/event_handlers/ontradetransaction) handler. It should be noted that OnTradeTransaction handler will be called several times when executing one trade request.

For example, when sending a market buy order, it is handled, an appropriate buy order is created for the account, the order is then executed and removed from the list of the open ones, then it is added to the orders history, an appropriate deal is added to the history and a new position is created. OnTradeTransaction function will be called for each of these events. To get such a data, the function parameters should be analyzed:

- trans - this parameter gets [MqlTradeTransaction](/en/docs/constants/structures/mqltradetransaction) structure describing a trade transaction applied to a trade account;
- request - this parameter gets [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) structure describing the trade request resulted in a trade transaction;
- result - this parameter gets [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) structure describing a trade request execution result.

Note

In terms of purposes and parameters, the function is similar to [OrderSend()](/en/docs/trading/ordersend), but unlike it, it is asynchronous, i.e. does not hold the program operation while waiting for the function execution result. You can compare the rate of trade operations of these two functions using the sample Expert Advisor.

Example:

```
#property description "Expert Advisor for sending trade requests "
                      " using OrderSendAsync() function.\r\n"
#property description "Handling trading events using"
                      " OnTrade() and OnTradeTransaction() handler functions is displayed\r\n"
#property description "Expert Advisor parameters allow setting Magic Number"
                      " (unique ID) "
#property description "and the mode of displaying messages in Experts log. All details are displayed by default.\r\n"
//--- input parameters
input int  MagicNumber=1234567;      // Expert Advisor ID
input bool DescriptionModeFull=true; // Detailed output mode
//--- variable for using in HistorySelect() call
datetime history_start;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- check if autotrading is allowed
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
     {
      Alert("Autotrading in the terminal is disabled, Expert Advisor will be removed.");
      ExpertRemove();
      return(-1);
     }
//--- unable to trade on a real account
   if(AccountInfoInteger(ACCOUNT_TRADE_MODE)==ACCOUNT_TRADE_MODE_REAL)
     {
      Alert("Expert Advisor cannot trade on a real account!");
      ExpertRemove();
      return(-2);
     }
//--- check if it is possible to trade on this account (for example, trading is impossible when using an investor password)
   if(!AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
     {
      Alert("Trading on this account is disabled");
      ExpertRemove();
      return(-3);
     }
//--- save the time of launching the Expert Advisor for receiving trading history
   history_start=TimeCurrent();
//---
   CreateBuySellButtons();
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- delete all graphical objects
   ObjectDelete(0,"Buy");
   ObjectDelete(0,"Sell");
//---
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
  {
//--- heading named after trading event's handler function 
   Print("=> ",__FUNCTION__," at ",TimeToString(TimeCurrent(),TIME_SECONDS));
//--- receive transaction type as enumeration value 
   ENUM_TRADE_TRANSACTION_TYPE type=trans.type;
//--- if transaction is a result of request handling
   if(type==TRADE_TRANSACTION_REQUEST)
     {
      //--- display transaction name
      Print(EnumToString(type));
      //--- then display the string description of the handled request
      Print("------------RequestDescription\r\n",
            RequestDescription(request,DescriptionModeFull));
      //--- and show description of the request result
      Print("------------ ResultDescription\r\n",
            TradeResultDescription(result,DescriptionModeFull));
     }
   else // display full description of the transaction for transactions of another type
     {
      Print("------------ TransactionDescription\r\n",
            TransactionDescription(trans,DescriptionModeFull));
     }
//---     
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//--- static members for storing trading account status
   static int prev_positions=0,prev_orders=0,prev_deals=0,prev_history_orders=0;
//--- request trading history
   bool update=HistorySelect(history_start,TimeCurrent());
   PrintFormat("HistorySelect(%s , %s) = %s",
               TimeToString(history_start),TimeToString(TimeCurrent()),(string)update);
//--- heading named after trading event's handler function 
   Print("=> ",__FUNCTION__," at ",TimeToString(TimeCurrent(),TIME_SECONDS));
//--- display handler's name and the number of orders at the moment of handling
   int curr_positions=PositionsTotal();
   int curr_orders=OrdersTotal();
   int curr_deals=HistoryOrdersTotal();
   int curr_history_orders=HistoryDealsTotal();
//--- display the number of orders, positions, deals, as well as changes in parentheses 
   PrintFormat("PositionsTotal() = %d (%+d)",
               curr_positions,(curr_positions-prev_positions));
   PrintFormat("OrdersTotal() = %d (%+d)",
               curr_orders,curr_orders-prev_orders);
   PrintFormat("HistoryOrdersTotal() = %d (%+d)",
               curr_deals,curr_deals-prev_deals);
   PrintFormat("HistoryDealsTotal() = %d (%+d)",
               curr_history_orders,curr_history_orders-prev_history_orders);
//--- insert a string break to view the log more conveniently
   Print("");
//--- save the account status
   prev_positions=curr_positions;
   prev_orders=curr_orders;
   prev_deals=curr_deals;
   prev_history_orders=curr_history_orders;
//---
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//--- handling CHARTEVENT_CLICK event ("Clicking the chart")
   if(id==CHARTEVENT_OBJECT_CLICK)
     {
      Print("=> ",__FUNCTION__,": sparam = ",sparam);
      //--- minimum volume for a deal
      double volume_min=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN);
      //--- if "Buy" button is pressed, then buy
      if(sparam=="Buy")
        {
         PrintFormat("Buy %s %G lot",_Symbol,volume_min);
         BuyAsync(volume_min);
         //--- unpress the button
         ObjectSetInteger(0,"Buy",OBJPROP_STATE,false);
        }
      //--- if "Sell" button is pressed, then sell
      if(sparam=="Sell")
        {
         PrintFormat("Sell %s %G lot",_Symbol,volume_min);
         SellAsync(volume_min);
         //--- unpress the button
         ObjectSetInteger(0,"Sell",OBJPROP_STATE,false);
        }
      ChartRedraw();
     }
//---         
  }
//+------------------------------------------------------------------+
//| Returns the text description of a transaction                    |
//+------------------------------------------------------------------+
string TransactionDescription(const MqlTradeTransaction &trans,
                              const bool detailed=true)
  {
//--- prepare a string for returning from the function
   string desc=EnumToString(trans.type)+"\r\n";
//--- all possible data is added in detailed mode
   if(detailed)
     {
      desc+="Symbol: "+trans.symbol+"\r\n";
      desc+="Deal ticket: "+(string)trans.deal+"\r\n";
      desc+="Deal type: "+EnumToString(trans.deal_type)+"\r\n";
      desc+="Order ticket: "+(string)trans.order+"\r\n";
      desc+="Order type: "+EnumToString(trans.order_type)+"\r\n";
      desc+="Order state: "+EnumToString(trans.order_state)+"\r\n";
      desc+="Order time type: "+EnumToString(trans.time_type)+"\r\n";
      desc+="Order expiration: "+TimeToString(trans.time_expiration)+"\r\n";
      desc+="Price: "+StringFormat("%G",trans.price)+"\r\n";
      desc+="Price trigger: "+StringFormat("%G",trans.price_trigger)+"\r\n";
      desc+="Stop Loss: "+StringFormat("%G",trans.price_sl)+"\r\n";
      desc+="Take Profit: "+StringFormat("%G",trans.price_tp)+"\r\n";
      desc+="Volume: "+StringFormat("%G",trans.volume)+"\r\n";
     }
//--- return a received string
   return desc;
  }
//+------------------------------------------------------------------+
//| Returns the text description of the trade request                |
//+------------------------------------------------------------------+
string RequestDescription(const MqlTradeRequest &request,
                          const bool detailed=true)
  {
//--- prepare a string for returning from the function
   string desc=EnumToString(request.action)+"\r\n";
//--- add all available data in detailed mode
   if(detailed)
     {
      desc+="Symbol: "+request.symbol+"\r\n";
      desc+="Magic Number: "+StringFormat("%d",request.magic)+"\r\n";
      desc+="Order ticket: "+(string)request.order+"\r\n";
      desc+="Order type: "+EnumToString(request.type)+"\r\n";
      desc+="Order filling: "+EnumToString(request.type_filling)+"\r\n";
      desc+="Order time type: "+EnumToString(request.type_time)+"\r\n";
      desc+="Order expiration: "+TimeToString(request.expiration)+"\r\n";
      desc+="Price: "+StringFormat("%G",request.price)+"\r\n";
      desc+="Deviation points: "+StringFormat("%G",request.deviation)+"\r\n";
      desc+="Stop Loss: "+StringFormat("%G",request.sl)+"\r\n";
      desc+="Take Profit: "+StringFormat("%G",request.tp)+"\r\n";
      desc+="Stop Limit: "+StringFormat("%G",request.stoplimit)+"\r\n";
      desc+="Volume: "+StringFormat("%G",request.volume)+"\r\n";
      desc+="Comment: "+request.comment+"\r\n";
     }
//--- return the received string
   return desc;
  }
//+------------------------------------------------------------------+
//| Returns the text description of request handling result          |
//+------------------------------------------------------------------+
string TradeResultDescription(const MqlTradeResult &result,
                              const bool detailed=true)
  {
//--- prepare the string for returning from the function
   string desc="Retcode "+(string)result.retcode+"\r\n";
//--- add all available data in detailed mode
   if(detailed)
     {
      desc+="Request ID: "+StringFormat("%d",result.request_id)+"\r\n";
      desc+="Order ticket: "+(string)result.order+"\r\n";
      desc+="Deal ticket: "+(string)result.deal+"\r\n";
      desc+="Volume: "+StringFormat("%G",result.volume)+"\r\n";
      desc+="Price: "+StringFormat("%G",result.price)+"\r\n";
      desc+="Ask: "+StringFormat("%G",result.ask)+"\r\n";
      desc+="Bid: "+StringFormat("%G",result.bid)+"\r\n";
      desc+="Comment: "+result.comment+"\r\n";
     }
//--- return the received string
   return desc;
  }
//+------------------------------------------------------------------+
//| Create two buttons for buying and selling                        |
//+------------------------------------------------------------------+
void CreateBuySellButtons()
  {
//--- check the object named "Buy"
   if(ObjectFind(0,"Buy")>=0)
     {
      //--- if the found object is not a button, delete it
      if(ObjectGetInteger(0,"Buy",OBJPROP_TYPE)!=OBJ_BUTTON)
         ObjectDelete(0,"Buy");
     }
   else
      ObjectCreate(0,"Buy",OBJ_BUTTON,0,0,0); // create "Buy" button
//--- configure "Buy" button
   ObjectSetInteger(0,"Buy",OBJPROP_CORNER,CORNER_RIGHT_UPPER);
   ObjectSetInteger(0,"Buy",OBJPROP_XDISTANCE,100);
   ObjectSetInteger(0,"Buy",OBJPROP_YDISTANCE,50);
   ObjectSetInteger(0,"Buy",OBJPROP_XSIZE,70);
   ObjectSetInteger(0,"Buy",OBJPROP_YSIZE,30);
   ObjectSetString(0,"Buy",OBJPROP_TEXT,"Buy");
   ObjectSetInteger(0,"Buy",OBJPROP_COLOR,clrRed);
//--- check presence of the object named "Sell"
   if(ObjectFind(0,"Sell")>=0)
     {
      //--- if the found object is not a button, delete it
      if(ObjectGetInteger(0,"Sell",OBJPROP_TYPE)!=OBJ_BUTTON)
         ObjectDelete(0,"Sell");
     }
   else
      ObjectCreate(0,"Sell",OBJ_BUTTON,0,0,0); // create "Sell" button
//--- configure "Sell" button
   ObjectSetInteger(0,"Sell",OBJPROP_CORNER,CORNER_RIGHT_UPPER);
   ObjectSetInteger(0,"Sell",OBJPROP_XDISTANCE,100);
   ObjectSetInteger(0,"Sell",OBJPROP_YDISTANCE,100);
   ObjectSetInteger(0,"Sell",OBJPROP_XSIZE,70);
   ObjectSetInteger(0,"Sell",OBJPROP_YSIZE,30);
   ObjectSetString(0,"Sell",OBJPROP_TEXT,"Sell");
   ObjectSetInteger(0,"Sell",OBJPROP_COLOR,clrBlue);
//--- perform forced update of the chart to see the buttons immediately
   ChartRedraw();
//---
  }
//+------------------------------------------------------------------+
//| Buy using OrderSendAsync() asynchronous function                 |
//+------------------------------------------------------------------+
void BuyAsync(double volume)
  {
//--- prepare the request
   MqlTradeRequest req={};
   req.action      =TRADE_ACTION_DEAL;
   req.symbol      =_Symbol;
   req.magic       =MagicNumber;
   req.volume      =0.1;
   req.type        =ORDER_TYPE_BUY;
   req.price       =SymbolInfoDouble(req.symbol,SYMBOL_ASK);
   req.deviation   =10;
   req.comment     ="Buy using OrderSendAsync()";
   MqlTradeResult  res={};
   if(!OrderSendAsync(req,res))
     {
      Print(__FUNCTION__,": error ",GetLastError(),", retcode = ",res.retcode);
     }
//---
  }
//+------------------------------------------------------------------+
//| Sell using OrderSendAsync() asynchronous function                |
//+------------------------------------------------------------------+
void SellAsync(double volume)
  {
//--- prepare the request
   MqlTradeRequest req={};
   req.action      =TRADE_ACTION_DEAL;
   req.symbol      =_Symbol;
   req.magic       =MagicNumber;
   req.volume      =0.1;
   req.type        =ORDER_TYPE_SELL;
   req.price       =SymbolInfoDouble(req.symbol,SYMBOL_BID);
   req.deviation   =10;
   req.comment     ="Sell using OrderSendAsync()";
   MqlTradeResult  res={};
   if(!OrderSendAsync(req,res))
     {
      Print(__FUNCTION__,": error ",GetLastError(),", retcode = ",res.retcode);
     }
//---
  }
//+------------------------------------------------------------------+

```

Example of displaying messages in "Experts" log:

```
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnChartEvent: sparam = Sell
 12:52:52   ExpertAdvisor (EURUSD,H1)   Sell EURUSD 0.01 lot
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTradeTransaction at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_TRANSACTION_REQUEST
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------RequestDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_ACTION_DEAL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Symbol: EURUSD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Magic Number: 1234567
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order type: ORDER_TYPE_SELL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order filling: ORDER_FILLING_FOK
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order time type: ORDER_TIME_GTC
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order expiration: 1970.01.01 00:00
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deviation points: 10
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Loss: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Take Profit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Limit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0.1
 12:52:52   ExpertAdvisor (EURUSD,H1)   Comment: Sell using OrderSendAsync()
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------ ResultDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   Retcode 10009
 12:52:52   ExpertAdvisor (EURUSD,H1)   Request ID: 2
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal ticket: 15048668
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0.1
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Ask: 1.29319
 12:52:52   ExpertAdvisor (EURUSD,H1)   Bid: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Comment: 
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistorySelect( 09:34 , 09:52) = true
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTrade at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   PositionsTotal() = 1 (+1)
 12:52:52   ExpertAdvisor (EURUSD,H1)   OrdersTotal() = 0 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryOrdersTotal() = 2 (+2)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryDealsTotal() = 2 (+2)
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTradeTransaction at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------ TransactionDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_TRANSACTION_ORDER_ADD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Symbol: EURUSD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal ticket: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal type: DEAL_TYPE_BUY
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order type: ORDER_TYPE_SELL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order state: ORDER_STATE_STARTED
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order time type: ORDER_TIME_GTC
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order expiration: 1970.01.01 00:00
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price trigger: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Loss: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Take Profit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0.1
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTradeTransaction at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------ TransactionDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_TRANSACTION_ORDER_DELETE
 12:52:52   ExpertAdvisor (EURUSD,H1)   Symbol: EURUSD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal ticket: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal type: DEAL_TYPE_BUY
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order type: ORDER_TYPE_SELL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order state: ORDER_STATE_STARTED
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order time type: ORDER_TIME_GTC
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order expiration: 1970.01.01 00:00
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price trigger: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Loss: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Take Profit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0.1
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistorySelect( 09:34 , 09:52) = true
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTrade at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   PositionsTotal() = 1 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   OrdersTotal() = 0 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryOrdersTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryDealsTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTradeTransaction at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------ TransactionDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_TRANSACTION_HISTORY_ADD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Symbol: EURUSD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal ticket: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal type: DEAL_TYPE_BUY
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order type: ORDER_TYPE_SELL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order state: ORDER_STATE_FILLED
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order time type: ORDER_TIME_GTC
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order expiration: 1970.01.01 00:00
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price trigger: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Loss: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Take Profit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistorySelect( 09:34 , 09:52) = true
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTrade at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   PositionsTotal() = 1 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   OrdersTotal() = 0 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryOrdersTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryDealsTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTradeTransaction at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   ------------ TransactionDescription
 12:52:52   ExpertAdvisor (EURUSD,H1)   TRADE_TRANSACTION_DEAL_ADD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Symbol: EURUSD
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal ticket: 15048668
 12:52:52   ExpertAdvisor (EURUSD,H1)   Deal type: DEAL_TYPE_SELL
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order ticket: 16361998
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order type: ORDER_TYPE_BUY
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order state: ORDER_STATE_STARTED
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order time type: ORDER_TIME_GTC
 12:52:52   ExpertAdvisor (EURUSD,H1)   Order expiration: 1970.01.01 00:00
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price: 1.29313
 12:52:52   ExpertAdvisor (EURUSD,H1)   Price trigger: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Stop Loss: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Take Profit: 0
 12:52:52   ExpertAdvisor (EURUSD,H1)   Volume: 0.1
 12:52:52   ExpertAdvisor (EURUSD,H1)   
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistorySelect( 09:34 , 09:52) = true
 12:52:52   ExpertAdvisor (EURUSD,H1)   => OnTrade at 09:52:53
 12:52:52   ExpertAdvisor (EURUSD,H1)   PositionsTotal() = 1 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   OrdersTotal() = 0 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryOrdersTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   HistoryDealsTotal() = 2 (+0)
 12:52:52   ExpertAdvisor (EURUSD,H1)   

```
