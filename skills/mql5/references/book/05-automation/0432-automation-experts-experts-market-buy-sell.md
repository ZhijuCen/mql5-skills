# Buying and selling operations

In this section, we finally begin to study the application of MQL5 functions for specific trading tasks. The purpose of these functions is to fill in the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure in a special way and call the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync)[ or ](/en/book/automation/experts/experts_ordersend_ordersendasync)[OrderSendAsync](/en/book/automation/experts/experts_ordersend_ordersendasync) function.

The first action we will learn is buying or selling a financial instrument at the current market price. The procedure for performing this action includes:

- Creating a market order based on a submitted order
- Executing a deal (one or several) under an order
- The result should be an open position

As we saw in the section on [types of trading operations](/en/book/automation/experts/experts_request_types), instant buy/sell corresponds to the TRADE_ACTION_DEAL element in the ENUM_TRADE_REQUEST_ACTIONS enumeration. Therefore, when filling the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure, write TRADE_ACTION_DEAL in the action field.

The trade direction is set using the type field which should contain one of the [order types](/en/book/automation/experts/experts_order_type): ORDER_TYPE_BUY or ORDER_TYPE_SELL.

Of course, to buy or sell, you need to specify the name of the symbol in the symbol field and its desired volume in the volume field.

The type_filling field must be filled with one of the fill policies from the enumeration [ENUM_ORDER_TYPE_FILLING](/en/book/automation/experts/experts_execution_filling), which is chosen based on the character property [SYMBOL_FILLING_MODE](/en/book/automation/symbols/symbols_execution_filling) with allowed policies.

Optionally, the program can fill in the fields with protective price levels (sl and tp), a comment (comment), and an Expert Advisor ID (magic).

The contents of other fields are set differently depending on the [price execution mode](/en/book/automation/experts/experts_execution_filling) for the selected symbol. In some modes, certain fields have no effect. For example, in the Request Execution and Instant Execution modes, the field with the price must be filled in with a suitable price (the last known Ask for buying and Bid for selling), and the deviation field may contain the maximum allowable deviation of the price from the set price for the successful execution of a deal. In Exchange Execution and Market Execution, these fields are ignored. In order to simplify the source code, you can fill in the price and slippage uniformly in all modes, but in the last two options, the price will still be selected and substituted by the trade server according to the rules of the modes.

Other fields of the MqlTradeRequest structure not mentioned here are not used for these trading operations.

The following table summarizes the rules for filling the fields for different execution modes. The required fields are marked with an asterisk, while optional fields are marked with a plus.

| Field | Request | Instant | Exchange | Market |
| --- | --- | --- | --- | --- |
| action | * | * | * | * |
| symbol | * | * | * | * |
| volume | * | * | * | * |
| type | * | * | * | * |
| type_filling | * | * | * | * |
| price | * | * |  |  |
| sl | + | + | + | + |
| tp | + | + | + | + |
| deviation | + | + |  |  |
| magic | + | + | + | + |
| comment | + | + | + | + |

Depending on server settings, it may be forbidden to fill in fields with protective sl and tp levels at the moment of opening a position. This is often the case for exchange execution or market execution modes, but the MQL5 API does not provide properties for clarifying this circumstance in advance. In such cases, Stop Loss and Take Profit should be set by [modifying](/en/book/automation/experts/experts_modify_position) an already open position. By the way, this method can be recommended for all execution modes, since it is the only one that allows you to accurately postpone the protective levels from the real position opening price. On the other hand, creating and setting up a position in two moves can lead to a situation where the position is open, but the second request to set protective levels failed for one reason or another.

Regardless of the trade direction (buy/sell), the Stop Loss order is always placed as a stop order (ORDER_TYPE_BUY_STOP or ORDER_TYPE_SELL_STOP), and the Take Profit order is placed as a limit order (ORDER_TYPE_BUY_LIMIT or ORDER_TYPE_SELL_LIMIT). Moreover, stop orders are always controlled by the MetaTrader 5 server and only when the price reaches the specified level, they are sent to the external trading system. In contrast, limit orders can be output directly to an external trading system. Specifically, this is usually the case for exchange-traded instruments.

In order to simplify the coding of trading operations, not only buying and selling but also all others, we will start from this section by developing classes, or rather structures that provide automatic and correct filling of fields for trade requests, as well as a truly synchronous waiting for the result. The latter is especially important, given that the OrderSend and OrderSendAsync functions return control to the calling code before the trading action is completed in full. In particular, for market buy and sell, the algorithm usually needs to know not the ticket number of the order created on the server, but whether the position is open or not. Depending on this, it can, for example, modify the position by setting Stop Loss and Take Profit if it has opened or repeat attempts to open it if the order was rejected.

A little later we will learn about the [OnTrade](/en/book/automation/experts/experts_ontrade) and [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) trading events, which inform the program about changes in the account state, including the status of orders, deals, and positions. However, dividing the algorithm into two fragments — separately generating orders according to certain signals or rules, and separately analyzing the situation in event handlers — makes the code less understandable and maintainable.

In theory, the asynchronous programming paradigm is not inferior to the synchronous one either in speed or in ease of coding. However, the ways of its implementation can be different, for example, based on direct pointers to callback functions (a basic technique in Java, JavaScript, and many other languages) or events (as in MQL5), which predetermines some features, which will be discussed in the [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) section. Asynchronous mode allows you to speed up the sending of requests due to deferred control over their execution. But this control will still need to be done sooner or later in the same thread, so the average performance of the circuits is the same.

All new structures will be placed in the MqlTradeSync.mqh file. In order not to "reinvent the wheel", let's take the built-in MQL5 structures as a starting point and describe our structures as child structures. For example, to get query results, let's define MqlTradeResultSync, which is derived from MqlTradeResult. Here we will add useful fields and methods, in particular, the position field to store an open position ticket as a result of a market buy or sell operation.

```
struct MqlTradeResultSync: public MqlTradeResult
{
   ulong position;
   ...
};

```

The second important improvement will be a constructor that resets all fields (this saves us from having to specify explicit initialization when describing variables of a structure type).

```
   MqlTradeResultSync()
   {
      ZeroMemory(this);
   }

```

Next, we will introduce a universal synchronization mechanism, i.e., waiting for the results of a request (each type of request will have its own rules for checking readiness).

Let's define the type of the condition callback function. A function of this type must take the MqlTradeResultSync structure parameter and return true if successful: the result of the operation is received.

```
   typedef bool (*condition)(MqlTradeResultSync &ref);

```

Functions like this are meant to be passed to the wait method, which implements a cyclic check for the readiness of the result during a predefined timeout in milliseconds.

```
   bool wait(condition p, const ulong msc = 1000)
   {
      const ulong start = GetTickCount64();
      bool success;
      while(!(success = p(this)) && GetTickCount64() - start < msc);
      return success;
   }

```

Let's clarify right away that the timeout is the maximum waiting time: even if it is set to a very large value, the loop will end immediately as soon as the result is received, which can happen instantly. Of course, a meaningful timeout should last no more than a few seconds.

Let's see an example of a method that will be used to synchronously wait for an order to appear on the server (it doesn't matter with what status: status analysis is the task of the calling code).

```
   static bool orderExist(MqlTradeResultSync &ref)
   {
      return OrderSelect(ref.order) || HistoryOrderSelect(ref.order);
   }

```

Two built-in MQL5 API functions are applied here, OrderSelect and HistoryOrderSelect: they search and logically select an order by its ticket in the internal trading environment of the terminal. First, this confirms the existence of an order (if one of the functions returned true), and second, it allows you to read its properties using other functions, which is not important to us yet. We will cover all these features in separate sections. The two functions are written in conjunction because a market order can be filled so quickly that its active phase (falling into OrderSelect) will immediately flow into history (HistoryOrderSelect).

Note that the method is declared static. This is due to the fact that MQL5 does not support pointers to object methods. If this were the case, we could declare the method non-static while using the prototype of the pointer to the condition callback functions without the parameter referencing to MqlTradeResultSync (since all fields are present inside the this object).

The waiting mechanism can be started as follows:

```
   if(wait(orderExist))
   {
      // there is an order
   }
   else
   {
      // timeout
   }

```

Of course, this fragment must be executed after we receive a result from the server with the status TRADE_RETCODE_DONE or TRADE_RETCODE_DONE_PARTIAL, and the order field in the MqlTradeResultSync structure is guaranteed to contain an order ticket. Please note that due to the system's distributed nature, an order from the server may not immediately be displayed in the terminal environment. That's why you need waiting time.

As long as the orderExist function returns false into the wait method, the wait loop inside runs until the timeout expires. Under normal circumstances, we will almost instantly find an order in the terminal environment, and the loop will end with a sign of success (true).

The positionExist function that checks the presence of an open position in a similar but a little more complicated way. Since the previous orderExist function has completed checking the order, its ticket contained in the field ref.order of the structure is confirmed as working.

```
   static bool positionExist(MqlTradeResultSync &ref)
   {
      ulong posid, ticket;
      if(HistoryOrderGetInteger(ref.order, ORDER_POSITION_ID, posid))
      {
         // in most cases, the position ID is equal to the ticket,
         // but not always: the full code implements getting a ticket by ID,
         // for which there are no built-in MQL5 tools
         ticket = posid;
         
         if(HistorySelectByPosition(posid))
         {
            ref.position = ticket;
            ...
            return true;
         }
      }
      return false;
   }

```

Using the built-in [HistoryOrderGetInteger](/en/book/automation/experts/experts_historyorderget_funcs) and [HistorySelectByPosition](/en/book/automation/experts/experts_history_select) functions, we get the ID and ticket of the position based on the order.

Later we will see the use of orderExist and positionExist when verifying a buy/sell request, but now let's turn to another structure: MqlTradeRequestSync. It is also inherited from the built-in one and contains additional fields, in particular, a structure with a result (so as not to describe it in the calling code) and a timeout for synchronous requests.

```
struct MqlTradeRequestSync: public MqlTradeRequest
{
   MqlTradeResultSync result;
   ulong timeout;
   ...

```

Since the inherited fields of the new structure are public, the MQL program can assign values to them explicitly, just as it was done with the standard MqlTradeRequest structure. The methods that we will add to perform trading operations will consider, check and, if necessary, correct these values for the valid ones.

In the constructor, we reset all fields and set the symbol to the default value if the parameter is omitted.

```
   MqlTradeRequestSync(const string s = NULL, const ulong t = 1000): timeout(t)
   {
      ZeroMemory(this);
      symbol = s == NULL ? _Symbol : s;
   }

```

In theory, due to the fact that all fields of the structure are public, they can technically be assigned directly, but this is not recommended for those fields that require validation and for which we implement setter methods: they will be called before performing trading operations. The first of these methods is setSymbol.

It fills the symbol field making sure the transmitted ticker exists and initiates the subsequent setting of the volume filling mode.

```
   bool setSymbol(const string s)
   {
      if(s == NULL)
      {
         if(symbol == NULL)
         {
            Print("symbol is NULL, defaults to " + _Symbol);
            symbol = _Symbol;
            setFilling();
         }
         else
         {
            Print("new symbol is NULL, current used " + symbol);
         }
      }
      else
      {
         if(SymbolInfoDouble(s, SYMBOL_POINT) == 0)
         {
            Print("incorrect symbol " + s);
            return false;
         }
         if(symbol != s)
         {
            symbol = s;
            setFilling();
         }
      }
      return true;
   }

```

So, changing the symbol with setSymbol will automatically pick up the correct filling mode via a nested call of setFilling.

The setFilling method provides the automatic specification of the volume filling method based on the SYMBOL_FILLING_MODE and SYMBOL_TRADE_EXEMODE symbol properties (see the section [Trading conditions and order execution modes](/en/book/automation/symbols/symbols_execution_filling)).

```
private:
   void setFilling()
   {
      const int filling = (int)SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE);
      const bool market = SymbolInfoInteger(symbol, SYMBOL_TRADE_EXEMODE)
         == SYMBOL_TRADE_EXECUTION_MARKET;
      
      // the field may already be filled
      // and bit match means a valid mode
      if(((type_filling + 1) & filling) != 0
         || (type_filling == ORDER_FILLING_RETURN && !market)) return;
      
      if((filling & SYMBOL_FILLING_FOK) != 0)
      {
         type_filling = ORDER_FILLING_FOK;
      }
      else if((filling & SYMBOL_FILLING_IOC) != 0)
      {
         type_filling = ORDER_FILLING_IOC;
      }
      else
      {
         type_filling = ORDER_FILLING_RETURN;
      }
   }

```

This method implicitly (without errors and messages) corrects the type_filling field if the Expert Advisor has set it incorrectly. If your algorithm requires a guaranteed specific fill method, without which trading is impossible, make appropriate edits to interrupt the process.

For the set of structures being developed, it is assumed that, in addition to the type_filling field, you can directly set only optional fields without specific requirements for their content, such as magic or comment.

In what follows, many of the methods are provided in a shorter form for the sake of simplicity. They have parts for the types of operations we'll look at later, as well as branched error checking.

For the buy and sell operations, we need the price and volume fields; both these values should be normalized and checked for the acceptable range. This is done by the setVolumePrices method.

```
   bool setVolumePrices(const double v, const double p,
      const double stop, const double take)
   {
      TU::SymbolMetrics sm(symbol);
      volume = sm.volume(v);
      
      if(p != 0) price = sm.price(p);
      else price = sm.price(TU::GetCurrentPrice(type, symbol));
      
      return setSLTP(stop, take);
   }

```

If the transaction price is not set (p == 0), the program will automatically take the current price of the correct type, depending on the direction, which is read from the type field.

Although the Stop Loss and Take Profit levels are not required, they should also be normalized if present, which is why they are added to the parameters of this method.

The abbreviation TU is already known to us. It stands for the namespace in the file [TradeUtilits.mqh](/en/book/automation/experts/experts_ordersend_ordersendasync) with a lot of useful functions, including those for the normalization of prices and volumes.

Processing of sl and tp fields is performed by the separate setSLTP method because this is needed not only in the buy and sell operations but also when [modifying an existing position](/en/book/automation/experts/experts_modify_position).

```
   bool setSLTP(const double stop, const double take)
   {
      TU::SymbolMetrics sm(symbol);
      TU::TradeDirection dir(type);
  
      if(stop != 0)
      {
         sl = sm.price(stop);
         if(!dir.worse(sl, price))
         {
            PrintFormat("wrong SL (%s) against price (%s)",
               TU::StringOf(sl), TU::StringOf(price));
            return false;
         }
      }
      else
      {
         sl = 0; // remove SL
      }
      
      if(take != 0)
      {
         tp = sm.price(take);
         if(!dir.better(tp, price))
         {
            PrintFormat("wrong TP (%s) against price (%s)",
               TU::StringOf(tp), TU::StringOf(price));
            return false;
         }
      }
      else
      {
         tp = 0; // remove TP
      }
      return true;
   }

```

In addition to normalizing and assigning values to sl and tp fields, this method checks the mutual correct location of the levels relative to the price. For this purpose, the TradeDirection class is described in the space TU.

Its constructors allow you to specify the analyzed direction of trade: buying or selling, in the context of which it is easy to identify a profitable or unprofitable mutual arrangement of two prices. With this class, the analysis is performed in a unified way and the checks in the code are reduced by 2 times since there is no need to separately process buy and sell operations. In particular, the worse method has two price parameters p1, p2, and returns true if the price p1 is placed worse, i.e., unprofitable, in relation to the price p2. A similar method better represents reverse logic: it will return true if the price p1 is better than price p2. For example, for a sale, the best price is placed lower because Take Profit is below the current price.

```
TU::TradeDirection dir(ORDER_TYPE_SELL);
Print(dir.better(100, 200)); // true

```

Now, if an order is placed incorrectly, the setSLTP function logs a warning and aborts the verification process without attempting to correct the values since the appropriate response may vary in different programs. For example, from the two passed stop and take levels only one can be wrong, and then it probably makes sense to use the second (correct) one.

You can change the behavior, for example, by skipping the assignment of invalid values (then the protection levels simply will not be changed) or adding a field with an error flag to the structure (for such a structure, an attempt to send a request should be suppressed so as not to load the server with obviously impossible requests). Sending an invalid request will end with the retcode error code equal to TRADE_RETCODE_INVALID_STOPS.

The setSLTP method also checks to make sure that the protective levels are not located closer to the current price than the number of points in the SYMBOL_TRADE_STOPS_LEVEL property of the symbol (if this property is set, i.e. greater than 0), and position modification is not requested when it is inside the SYMBOL_TRADE_FREEZE_LEVEL freeze area (if it is set). These nuances are not shown here: they can be found in the source code.

Now we are ready to implement a group of trading methods. For example, for buying and selling with the most complete set of fields, we define buy and sell methods.

```
public:
   ulong buy(const string name, const double lot, const double p = 0,
      const double stop = 0, const double take = 0)
   {
      type = ORDER_TYPE_BUY;
      return _market(name, lot, p, stop, take);
   }
   ulong sell(const string name, const double lot, const double p = 0,
      const double stop = 0, const double take = 0)
   {
      type = ORDER_TYPE_SELL;
      return _market(name, lot, p, stop, take);
   }

```

As already mentioned, to set optional fields like deviation, comment, and magic should do a direct assignment before calling buy/sell. This is all the more convenient since deviation and magic in most cases are set once, and used in subsequent queries.

The methods return an order ticket, but below we will show in action the mechanism of "synchronous" receipt of a position ticket, and this will be a ticket of a created or modified position (if position increase or partial closing was done).

Methods buy and sell differ only in the type field value, while everything else is the same. This is why the general part is framed as a separate method _market. This is where we set action in TRADE_ACTION_DEAL, and call setSymbol and setVolumePrices.

```
private:
   ulong _market(const string name, const double lot, const double p = 0,
      const double stop = 0, const double take = 0)
   {
      action = TRADE_ACTION_DEAL;
      if(!setSymbol(name)) return 0;
      if(!setVolumePrices(lot, p, stop, take)) return 0;
      ...

```

Next, we could just call OrderSend, but given the possibility of requotes (price updates on the server during the time the order was sent), let's wrap the call in a loop. Due to this, the method will be able to retry several times, but no more than the preset number of times MAX_REQUOTES (the macro is chosen to be 10 in the code).

```
      int count = 0;
      do
      {
         ZeroMemory(result);
         if(OrderSend(this, result)) return result.order;
         // automatic price selection means automatic processing of requotes
         if(result.retcode == TRADE_RETCODE_REQUOTE)
         {
            Print("Requote N" + (string)++count);
            if(p == 0)
            {
               price = TU::GetCurrentPrice(type, symbol);
            }
         }
      }
      while(p == 0 && result.retcode == TRADE_RETCODE_REQUOTE 
         && ++count < MAX_REQUOTES);
      return 0;
   }

```

Since the financial instrument is set in the structure constructor by default, we can provide a couple of simplified overloads of buy/sell methods without the symbol parameter.

```
public:
   ulong buy(const double lot, const double p = 0,
      const double stop = 0, const double take = 0)
   {
      return buy(symbol, lot, p, stop, take);
   }
   
   ulong sell(const double lot, const double p = 0,
      const double stop = 0, const double take = 0)
   {
      return sell(symbol, lot, p, stop, take);
   }

```

Thus, in a minimal configuration, it will be enough for the program to call request.buy(1.0) in order to make a one-lot buy operation.

Now let's get back to the problem of obtaining the final result of the request, which in the case of the operation TRADE_ACTION_DEAL means the position ticket. In the MqlTradeRequestSync structure, this problem is solved by the completed method: for each type of operation, it must ask for the nested MqlTradeResultSync structure to wait for its filling in accordance with the type of operation.

```
   bool completed()
   {
      if(action == TRADE_ACTION_DEAL)
      {
         const bool success = result.opened(timeout);
         if(success) position = result.position;
         return success;
      }
      ...
      return false;
   }

```

Position opening is controlled by the opened method. Inside we will find a couple of calls to the wait method described above: the first one is for orderExist, and the second one is for positionExist.

```
   bool opened(const ulong msc = 1000)
   {
      if(retcode != TRADE_RETCODE_DONE
         && retcode != TRADE_RETCODE_DONE_PARTIAL)
      {
         return false;
      }
      
      if(!wait(orderExist, msc))
      {
         Print("Waiting for order: #" + (string)order);
      }
      
      if(deal != 0)
      {
         if(HistoryDealGetInteger(deal, DEAL_POSITION_ID, position))
         {
            return true;
         }
         Print("Waiting for position for deal D=" + (string)deal);
      }
      
      if(!wait(positionExist, msc))
      {
         Print("Timeout");
         return false;
      }
      position = result.position;
      
      return true;
   }

```

Of course, it makes sense to wait for an order and a position to appear only if the status of the retcode indicates success. Other statuses refer to errors or cancellation of the operation, or to specific intermediate codes (TRADE_RETCODE_PLACED, TRADE_RETCODE_TIMEOUT) that are not accompanied by useful information in other fields. In both cases, this prevents further processing within this "synchronous" framework.

It is important to note that we are using OrderSync and therefore we rely on the obligatory presence of the order ticket in the structure received from the server.

In some cases, the system sends not only an order ticket but also a deal ticket at the same time. Then from the deal, you can find the position faster. But even if there is information about the deal, the trading environment of the terminal may temporarily not have information about the new position. That is why you should wait for it with wait(positionExist).

Let's sum up for the intermediate result. The created structures allow you to write the following code to buy 1 lot of the current symbol:

```
   MqlTradeRequestSync request;
   if(request.buy(1.0) && request.completed())
   {
      Print("OK Position: P=", request.result.position);
   }

```

We get inside the block of the conditional operator only with a guaranteed open position, and we know its ticket. If we used only buy/sell methods, they would receive an order ticket at their output and would have to check the execution themselves. In case of an error, we will not get inside the if block, and the server code will be contained in request.result.retcode.

When we implement methods for other trades in the following sections, they can be executed in a similar "blocking" mode, for example, to modify stop levels:

```
  if(request.adjust(SL, TP) && request.completed())
  {
     Print("OK Adjust")
  }

```

Of course, you are not required to call completed if you don't want to check the result of the operation in blocking mode. Instead, you can stick to the asynchronous paradigm and analyze the environment in [trading events](/en/book/automation/experts/experts_ontradetransaction) handlers. But even in this case, the MqlTradeRequestAsync structure can be useful for checking and normalizing operation parameters.

Let's write a test Expert Advisor MarketOrderSend.mq5 to put all this together. The input parameters will provide input of values for the main and some optional fields of the trade request.

```
enum ENUM_ORDER_TYPE_MARKET
{
   MARKET_BUY = ORDER_TYPE_BUY,  // ORDER_TYPE_BUY
   MARKET_SELL = ORDER_TYPE_SELL // ORDER_TYPE_SELL
};
   
input string Symbol;         // Symbol (empty = current _Symbol)
input double Volume;         // Volume (0 = minimal lot)
input double Price;          // Price (0 = current Ask)
input ENUM_ORDER_TYPE_MARKET Type;
input string Comment;
input ulong Magic;
input ulong Deviation;

```

The ENUM_ORDER_TYPE_MARKET enumeration is a subset of the standard [ENUM_ORDER_TYPE](/en/book/automation/experts/experts_order_type) and is introduced in order to limit the available types of operations to only two: market buy and sell.

The action will run once on a timer, in the same way as in the previous examples.

```
void OnInit()
{
   // scheduling a delayed start
   EventSetTimer(1);
}

```

In the timer handler, we disable the timer so that the request is executed only once. For the next launch, you will need to change the Expert Advisor parameters.

```
void OnTimer()
{
   EventKillTimer();
   ...

```

Let's describe a variable of type MqlTradeRequestSync and prepare the values for the main fields.

```
   const bool wantToBuy = Type == MARKET_BUY;
   const string symbol = StringLen(Symbol) == 0 ? _Symbol : Symbol;
   const double volume = Volume == 0 ?
      SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN) : Volume;
 
   MqlTradeRequestSync request(symbol);
   ...

```

Optional fields will be filled in directly.

```
   request.magic = Magic;
   request.deviation = Deviation;
   request.comment = Comment;
   ...

```

Among the optional fields, you can select the fill mode (type_filling). By default, MqlTradeRequestSync automatically writes to this field the first of the allowed modes [ENUM_ORDER_TYPE_FILLING](/en/book/automation/experts/experts_execution_filling). Recall that the structure has a special method setFilling for this.

Next, we call the buy or sell method with parameters, and if it returns an order ticket, we wait for an open position to appear.

```
   ResetLastError();
   const ulong order = (wantToBuy ?
      request.buy(volume, Price) :
      request.sell(volume, Price));
   if(order != 0)
   {
      Print("OK Order: #=", order);
      if(request.completed()) // waiting for an open position
      {
         Print("OK Position: P=", request.result.position);
      }
   }
   Print(TU::StringOf(request));
   Print(TU::StringOf(request.result));
}

```

At the end of the function, the query and result structures are logged for reference.

If we run the Expert Advisor with the default parameters (buying the current symbol with the minimum lot), we can get the following result for "XTIUSD".

```
OK Order: #=218966930
Waiting for position for deal D=215494463
OK Position: P=218966930
TRADE_ACTION_DEAL, XTIUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 109.340, P=218966930
DONE, D=215494463, #=218966930, V=0.01, @ 109.35, Request executed, Req=8

```

Pay attention to the warning about the temporary absence of a position: it will always appear due to the distributed processing of requests (the warnings themselves can be disabled by removing the SHOW_WARNINGS macro in the Expert Advisor code, but the situation will remain). But thanks to the developed new structures, the applied code is not diverted by these internal complexities and is written in the form of a sequence of simple steps, where each next one is "confident" in the success of the previous ones.

On a netting account, we can achieve an interesting effect of position reversal by subsequent selling with a doubled minimum lot (0.02 in this case).

```
OK Order: #=218966932
Waiting for position for deal D=215494468
Position ticket <> id: 218966932, 218966930
OK Position: P=218966932
TRADE_ACTION_DEAL, XTIUSD, ORDER_TYPE_SELL, V=0.02, ORDER_FILLING_FOK, @ 109.390, P=218966932
DONE, D=215494468, #=218966932, V=0.02, @ 109.39, Request executed, Req=9

```

It is important to note that after the reversal, the position ticket ceases to be equal to the position identifier: the identifier remains from the first order, and the ticket remains from the second. We deliberately bypassed the task of finding the position ticket by its identifier in order to simplify the presentation. In most cases, the ticket and ID are the same, but for precise control, use the TU::PositionSelectById function. Those interested can study the attached source code.

Identifiers are constant as long as the position exists (until it closes to zero in terms of volume) and are useful for analyzing the account history. Tickets describe positions while they are open (there is no concept of a position ticket in history) and are used in some types of requests, in particular, to modify protection levels or close with an opposite position. But there are nuances associated with pouring in parts. We'll talk more about position properties in a [separate section](/en/book/automation/experts/experts_position_properties).

When making a buy or sell operation, our buy/sell methods allow you to immediately set the Stop Loss and/or Take Profit levels. To do this, simply pass them as additional parameters obtained from input variables or calculated using some formulas. For example,

```
input double SL;
input double TP;
...
void OnTimer()
{
   ...
   const ulong order = (wantToBuy ?
      request.buy(symbol, volume, Price, SL, TP) :
      request.sell(symbol, volume, Price, SL, TP));
   ...

```

All methods of the new structures provide automatic normalization of the passed parameters, so there is no need to use NormalizeDouble or something else.

It has already been noted above that some server settings may prohibit the setting of protective levels at the position opening time. In this case, you should set the sl and tp fields via a separate request. Exactly the same request is also used in those cases when it is required to modify already set levels, in particular, to implement trailing stop or trailing profit.

In the next section, we will complete the current example with a delayed setting of sl and tp with the second request after the successful opening of a position.
