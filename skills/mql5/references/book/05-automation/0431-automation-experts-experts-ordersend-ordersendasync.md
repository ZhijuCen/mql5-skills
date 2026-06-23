# Sending a trade request: OrderSend and OrderSendAsync

To perform trading operations, the MQL5 API provides two functions: OrderSend and OrderSendAsync. Just like [OrderCheck](/en/book/automation/experts/experts_ordercheck), they perform a formal check of the request parameters passed in the form of the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure and then, if successful, send a request to the server.

The difference between the two functions is as follows. OrderSend expects for the order to be queued for processing on the server and receives meaningful data from it into the fields of the [MqlTradeResult](/en/book/automation/experts/experts_mqltraderesult) structure which is passed as the second function parameter. OrderSendAsync immediately returns control to the calling code regardless of how the server responds. At the same time, from all fields of the MqlTradeResult structure except retcode, important information is filled only into request_id. Using this request identifier, an MQL program can receive further information about the progress of processing this request in the [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) event. An alternative approach is to periodically analyze the lists of orders, deals, and positions. This can also be done in a loop, setting some timeout in case of communication problems.

It's important to note that despite the "Async" suffix in the second function's name, the first function without this suffix is also not fully synchronous. The fact is that the result of order processing by the server, in particular, the execution of a deal (or, probably, several deals based on one order) and the opening of a position, generally occurs asynchronously in an external trading system. So the OrderSend function also requires delayed collection and analysis of the consequences of request execution, which MQL programs must, if necessary, implement themselves. We'll look at an example of truly synchronous sending of a request and receiving all of its results later (see [MqlTradeSync.mqh](/en/book/automation/experts/experts_market_buy_sell)).

bool OrderSend(const MqlTradeRequest &request, MqlTradeResult &result)

The function returns true in case of a successful basic check of the request structure in the terminal and a few additional checks on the server. However, this only indicates the acceptance of the order by the server and does not guarantee a successful execution of the trade operation.

The trade server can fill the field deal or order values in the returned result structure if this data is known at the time the server formats an answer to the OrderSend call. However, in the general case, the events of deal execution or placing limit orders corresponding to an order can occur after the response is sent to the MQL program in the terminal. Therefore, for any type of trade request, when receiving the execution OrderSend result, it is necessary to check the trade server return code retcode and external trading system response code retcode_external (if necessary) which are available in the returned result structure. Based on them, you should decide whether to wait for pending actions on the server or take your own actions.

Each accepted order is stored on the trade server pending processing until any of the following events that affect its life cycle occurs:

- execution when a counter request appears
- triggered when the execution price arrives
- expiration date
- cancellation by the user or MQL program
- removal by the broker (for example, in case of clearing or shortage of funds, Stop Out)

The OrderSendAsync prototype completely repeats that of OrderSend.

bool OrderSendAsync(const MqlTradeRequest &request, MqlTradeResult &result)

The function is intended for high-frequency trading, when, according to the conditions of the algorithm, it is unacceptable to waste time waiting for a response from the server. The use of OrderSendAsync does not speed up request processing by the server or request sending to the external trading system.

Attention! In the tester, the OrderSendAsync function works like OrderSend. This makes it difficult to debug the pending processing of asynchronous requests.

The function returns true upon a successful sending of the request to the MetaTrader 5 server. However, this does not mean that the request reached the server and was accepted for processing. At the same time, the response code in the receiving result structure contains the TRADE_RETCODE_PLACED (10008) value, that is, "the order has been placed".

When processing the received request, the server will send a response message to the terminal about a change in the current state of positions, orders and deals, which leads to the generation of the [OnTrade](/en/book/automation/experts/experts_ontrade) event in an MQL program. There, the program can analyze the new trading environment and account history. We will look at relevant examples below.

Also, the details of the trader request execution on the server can be tracked using the [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) handler. At the same time, it should be considered that as a result of the execution of one trade request, the OnTradeTransaction handler will be called multiple times. For example, when sending a market buy request, it is accepted for processing by the server, a corresponding 'buy' order is created for the account, the order is executed and the trader is performed, as a result of which it is removed from the list of open orders and added to the history of orders. Then the trade is added to the history and a new position is created. For each of these events, the OnTradeTransaction function will be called.

Let's start with a simple Expert Advisor example CustomOrderSend.mq5. It allows you to set all fields of the request in the input parameters, which is similar to CustomOrderCheck.mq5, but further differs in that it sends a request to the server instead of a simple check in the terminal. Run the Expert Advisor on your demo account. After completing the experiments, don't forget to remove the Expert Advisor from the chart or close the chart so that you don't send a test request every next launch of the terminal.

The new example has several other improvements. First of all the input parameter Async is added.

```
input bool Async = false;

```

This option allows selecting the function that will send the request to the server. By default, the parameter equals to false and the OrderSend function is used. If you set it to true, OrderSendAsync will be called.

In addition, with this example, we will begin to describe and complete a special set of functions in the header file TradeUtils.mqh, which will come in handy to simplify the coding of robots. All functions are placed in the namespace TU (from "Trade Utilities"), and first, we introduce functions for convenient output to the structure log MqlTradeRequest and MqlTradeResult.

```
namespace TU
{
   string StringOf(const MqlTradeRequest &r)
   {
      SymbolMetrics p(r.symbol);
      
      // main block: action, type, symbol      
      string text = EnumToString(r.action);
      if(r.symbol != NULL) text += ", " + r.symbol;
      text += ", " + EnumToString(r.type);
      // volume block
      if(r.volume != 0) text += ", V=" + p.StringOf(r.volume, p.lotDigits);
      text += ", " + EnumToString(r.type_filling);
      // block of all prices 
      if(r.price != 0) text += ", @ " + p.StringOf(r.price);
      if(r.stoplimit != 0) text += ", X=" + p.StringOf(r.stoplimit);
      if(r.sl != 0) text += ", SL=" + p.StringOf(r.sl);
      if(r.tp != 0) text += ", TP=" + p.StringOf(r.tp);
      if(r.deviation != 0) text += ", D=" + (string)r.deviation;
      // pending orders expiration block
      if(IsPendingType(r.type)) text += ", " + EnumToString(r.type_time);
      if(r.expiration != 0) text += ", " + TimeToString(r.expiration);
      // modification block
      if(r.order != 0) text += ", #=" + (string)r.order;
      if(r.position != 0) text += ", #P=" + (string)r.position;
      if(r.position_by != 0) text += ", #b=" + (string)r.position_by;
      // auxiliary data
      if(r.magic != 0) text += ", M=" + (string)r.magic;
      if(StringLen(r.comment)) text += ", " + r.comment;
      
      return text;
   }
   
   string StringOf(const MqlTradeResult &r)
   {
      string text = TRCSTR(r.retcode);
      if(r.deal != 0) text += ", D=" + (string)r.deal;
      if(r.order != 0) text += ", #=" + (string)r.order;
      if(r.volume != 0) text += ", V=" + (string)r.volume;
      if(r.price != 0) text += ", @ " + (string)r.price; 
      if(r.bid != 0) text += ", Bid=" + (string)r.bid; 
      if(r.ask != 0) text += ", Ask=" + (string)r.ask; 
      if(StringLen(r.comment)) text += ", " + r.comment;
      if(r.request_id != 0) text += ", Req=" + (string)r.request_id;
      if(r.retcode_external != 0) text += ", Ext=" + (string)r.retcode_external;
      
      return text;
   }
   ...
};

```

The purpose of the functions is to provide all significant (non-empty) fields in a concise but convenient form: they are displayed in one line with a unique designation for each.

As you can see, the function uses the SymbolMetrics class for MqlTradeRequest. It facilitates the normalization of multiple prices or volumes for the same instrument. Don't forget that the normalization of prices and volumes is a prerequisite for preparing a correct trade request.

```
   class SymbolMetrics
   {
   public:
      const string symbol;
      const int digits;
      const int lotDigits;
      
      SymbolMetrics(const string s): symbol(s),
         digits((int)SymbolInfoInteger(s, SYMBOL_DIGITS)),
         lotDigits((int)MathLog10(1.0 / SymbolInfoDouble(s, SYMBOL_VOLUME_STEP)))
      { }
         
      double price(const double p)
      {
         return TU::NormalizePrice(p, symbol);
      }
      
      double volume(const double v)
      {
         return TU::NormalizeLot(v, symbol);
      }
   
      string StringOf(const double v, const int d = INT_MAX)
      {
         return DoubleToString(v, d == INT_MAX ? digits : d);
      }
   };

```

The direct normalization of values is entrusted to auxiliary functions NormalizePrice and NormalizeLot (the scheme of the latter is identical to what we saw in the file [LotMarginExposure.mqh](/en/book/automation/experts/experts_ordercalcmargin)).

```
   double NormalizePrice(const double price, const string symbol = NULL)
   {
      const double tick = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
      return MathRound(price / tick) * tick;
   }

```

If we connect TradeUtils.mqh, the example CustomOrderSend.mq5 has the following form (the omitted code fragments '...' remained unchanged from CustomOrderCheck.mq5).

```
void OnTimer()
{
   ...
   MqlTradeRequest request = {};
   MqlTradeCheckResult result = {};
   
   TU::SymbolMetrics sm(symbol);
   
   // fill in the request structure
   request.action = Action;
   request.magic = Magic;
   request.order = Order;
   request.symbol = symbol;
   request.volume = sm.volume(volume);
   request.price = sm.price(price);
   request.stoplimit = sm.price(StopLimit);
   request.sl = sm.price(SL);
   request.tp = sm.price(TP);
   request.deviation = Deviation;
   request.type = Type;
   request.type_filling = Filling;
   request.type_time = ExpirationType;
   request.expiration = ExpirationTime;
   request.comment = Comment;
   request.position = Position;
   request.position_by = PositionBy;
   
   // send the request and display the result
   ResetLastError();
   if(Async)
   {
      PRTF(OrderSendAsync(request, result));
   }
   else
   {
      PRTF(OrderSend(request, result));
   }
   Print(TU::StringOf(request));
   Print(TU::StringOf(result));
}

```

Due to the fact that prices and volume are now normalized, you can try to enter uneven values into the corresponding input parameters. They are often obtained in programs during calculations, and our code converts them according to the symbol specification.

With default settings, the Expert Advisor creates a request to buy the minimum lot of the current instrument by market and makes it using the OrderSend function.

```
OrderSend(request,result)=true / ok
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.12462
DONE, D=1250236209, #=1267684253, V=0.01, @ 1.12462, Bid=1.12456, Ask=1.12462, Request executed, Req=1

```

As a rule, with allowed trading, this operation should be completed successfully (status DONE, comment "Request executed"). In the result structure, we immediately received the deal number D.

If we open Expert Advisor settings and replace the value of the parameter Async with true, we will send a similar request but with the OrderSendAsync function.

```
OrderSendAsync(request,result)=true / ok
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.12449
PLACED, Order placed, Req=2

```

In this case, the status is PLACED, and the trade number at the time the function returns is not known. We only know the unique request ID Req=2. To get the deal and position number, you need to intercept the TRADE_TRANSACTION_REQUEST message with the same request ID in the [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) handler, where the filled structure will be received as a MqlTradeResult parameter.

From the user's point of view, both requests should be equally fast.

It will be possible to compare the performance of these two functions directly in the code of an MQL program using another example of an Expert Advisor (see the section on [synchronous and asynchronous requests](/en/book/automation/experts/experts_sync_vs_async)), which we will consider after studying the model of trading events.

It should be noted that trading events are sent to the OnTradeTransaction handler (if present in the code), regardless of which function is used to send requests, OrderSend or OrderSendAsync. The situation is as follows: in case of applying OrderSend some or all information about the execution of the order is immediately available in the receiving MqlTradeResult structure. However, in the general case, the result is distributed over time and volume, for example, when one order is "filled" into several deals. Then complete information can be obtained from trading events or by analyzing the history of transactions and orders.

If you try to send a deliberately incorrect request, for example, change the order type to a pending ORDER_TYPE_BUY_STOP, you will get an error message, because for such orders you should use the TRADE_ACTION_PENDING action. Furthermore, they should be located at a distance from the current price (we use the market price by default). Before this test, it is important not to forget to change the query mode back to synchronous (Async=false) to immediately see the error in the MqlTradeResult structure after ending the OrderSend call. Otherwise, OrderSendAsync would return true, but the order would still not be set, and the program could receive information about this only in OnTradeTransaction which we don't have yet.

```
OrderSend(request,result)=false / TRADE_SEND_FAILED(4756)
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY_STOP, V=0.01, ORDER_FILLING_FOK, @ 1.12452, ORDER_TIME_GTC
REQUOTE, Bid=1.12449, Ask=1.12452, Requote, Req=5

```

In this case, the error reports an invalid Requote price.

Examples of using functions to perform specific trading actions will be presented in the following sections.
