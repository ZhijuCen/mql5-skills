# OnTradeTransaction event

Expert Advisors and indicators can receive notifications about trading events if their code contains a special processing function OnTradeTransaction.

void OnTradeTransaction(const MqlTradeTransaction &trans,  

   const MqlTradeRequest &request, const MqlTradeResult &result)

The first parameter is the MqlTradeTransaction structure described in the [previous section](/en/book/automation/experts/experts_transaction_type). The second and third parameters are structures [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) and [MqlTradeResult](/en/book/automation/experts/experts_mqltraderesult), which were presented earlier in the relevant sections.

The MqlTradeTransaction structure that describes the trade transaction is filled in differently depending on the type of transaction specified in the type field. For example, for transactions of the TRADE_TRANSACTION_REQUEST type, all other fields are not important, and to obtain additional information, it is necessary to analyze the second and third parameters of the function (request and result). Conversely, for all other types of transactions, the last two parameters of the function should be ignored.

In case of TRADE_TRANSACTION_REQUEST, the request_id field in the result variable contains an identifier (through serial number), under which the trade request is registered in the terminal. This number has nothing to do with order and deal tickets, as well as position identifiers. During each session with the terminal, the numbering starts from the beginning (1). The presence of a request identifier allows you to associate the performed action (calling OrderSend or OrderSendAsync functions) with the result of this action passed to OnTradeTransaction. We'll look at examples later.

For trading transactions related to active orders (TRADE_TRANSACTION_ORDER_ADD, TRADE_TRANSACTION_ORDER_UPDATE and TRADE_TRANSACTION_ORDER_DELETE) and order history (TRADE_TRANSACTION_HISTORY_ADD, TRADE_TRANSACTION_HISTORY_UPDATE, TRADE_TRANSACTION_HISTORY_DELETE), the following fields are filled in the MqlTradeTransaction structure:

- order – order ticket
- symbol – name of the financial instrument in the order
- type – trade transaction type
- order_type – order type
- orders_state – current order state
- time_type – order expiration type
- time_expiration – order expiration time (for orders with ORDER_TIME_SPECIFIED and ORDER_TIME_SPECIFIED_DAY expiration types)
- price – order price specified by the client/program
- price_trigger – stop price for triggering a stop-limit order (only for ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT)
- price_sl – Stop Loss order price (filled if specified in the order)
- price_tp – Take Profit order price (filled if specified in the order)
- volume – current order volume (not executed), the initial order volume can be found from the order history
- position – ticket of an open, modified, or closed position
- position_by – opposite position ticket (only for orders to close with opposite position)

For trading transactions related to deals (TRADE_TRANSACTION_DEAL_ADD, TRADE_TRANSACTION_DEAL_UPDATE and TRADE_TRANSACTION_DEAL_DELETE), the following fields are filled in the MqlTradeTransaction structure:

- deal – deal ticket
- order – order ticket on the basis of which the deal was made
- symbol – name of the financial instrument in the deal
- type – trade transaction type
- deal_type – deal type
- price – deal price
- price_sl – Stop Loss price (filled if specified in the order on the basis of which the deal was made)
- price_tp – Take Profit price (filled if specified in the order on the basis of which the deal was made)
- volume – deal volume
- position – ticket of an open, modified, or closed position
- position_by – opposite position ticket (for deals to close with opposite position)

For trading transactions related to position changes (TRADE_TRANSACTION_POSITION), the following fields are filled in the MqlTradeTransaction structure:

- symbol – name of the financial instrument of the position
- type – trade transaction type
- deal_type – position type (DEAL_TYPE_BUY or DEAL_TYPE_SELL)
- price – weighted average position opening price
- price_sl – Stop Loss price
- price_tp – Take Profit price
- volume – position volume in lots
- position – position ticket

Not all available information on orders, deals and positions (for example, a comment) is transmitted in the description of a trading transaction. For more information use the relevant functions: OrderGet, HistoryOrderGet, HistoryDealGet and PositionGet.

One trade request sent from the terminal manually or through the trading functions OrderSend/OrderSendAsync can generate several consecutive trade transactions on the trade server. At the same time, the order in which notifications about these transactions arrive at the terminal is not guaranteed, so you cannot build your trading algorithm on waiting for some trading transactions after others.

Trading events are processed asynchronously, that is, delayed (in time) relative to the moment of generation. Each trade event is sent to the queue of the MQL program, and the program sequentially picks them up in the order of the queue.

When an Expert Advisor is processing trade transactions inside the OnTradeTransaction processor, the terminal continues to accept incoming trade transactions. Thus, the state of the trading account may change while OnTradeTransaction is running. In the future, the program will be notified of all these events in the order the appear.

The length of the transaction queue is 1024 elements. If OnTradeTransaction processes the next transaction for too long, old transactions in the queue may be ousted by newer ones.

Due to parallel multi-threaded operation of the terminal with trading objects, by the time the OnTradeTransaction handler is called, all the entities mentioned in it, including orders, deals, and positions, may already be in a different state than that specified in the transaction properties. To get their current state, you should select them in the current environment or in the history and request their properties using the appropriate MQL5 functions.

Let's start with a simple Expert Advisor example TradeTransactions.mq5, which logs all OnTradeTransaction trading events. Its only parameter DetailedLog allows you to optionally use classes OrderMonitor, DealMonitor, PositionMonitor to display all properties. By default, the Expert Advisor displays only the contents of the filled fields of the MqlTradeTransaction, MqlTradeRequest and MqlTradeResult structures, coming to the handler in the form of parameters; at the same time request and result are processed only for TRADE_TRANSACTION_REQUEST transactions.

```
input bool DetailedLog = false; // DetailedLog ('true' shows order/deal/position details)
   
void OnTradeTransaction(const MqlTradeTransaction &transaction,
   const MqlTradeRequest &request,
   const MqlTradeResult &result)
{
   static ulong count = 0;
   PrintFormat(">>>% 6d", ++count);
   Print(TU::StringOf(transaction));
   
   if(transaction.type == TRADE_TRANSACTION_REQUEST)
   {
      Print(TU::StringOf(request));
      Print(TU::StringOf(result));
   }
   
   if(DetailedLog)
   {
      if(transaction.order != 0)
      {
         OrderMonitor m(transaction.order);
         m.print();
      }
      if(transaction.deal != 0)
      {
         DealMonitor m(transaction.deal);
         m.print();
      }
      if(transaction.position != 0)
      {
         PositionMonitor m(transaction.position);
         m.print();
      }
   }
}

```

Let's run it on the EURUSD chart and perform several actions manually, and the corresponding entries will appear in the log (for the purity of the experiment, it is assumed that no one and nothing else performs operations on the trading account, in particular, no other Expert Advisors are running).

Let's open a long position with a minimum lot.

```
>>>      1
TRADE_TRANSACTION_ORDER_ADD, #=1296991463(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10947, V=0.01
>>>      2
TRADE_TRANSACTION_DEAL_ADD, D=1279627746(DEAL_TYPE_BUY), »
   » #=1296991463(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10947, V=0.01, P=1296991463
>>>      3
TRADE_TRANSACTION_ORDER_DELETE, #=1296991463(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10947, P=1296991463
>>>      4
TRADE_TRANSACTION_HISTORY_ADD, #=1296991463(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10947, P=1296991463
>>>      5
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10947, #=1296991463
DONE, D=1279627746, #=1296991463, V=0.01, @ 1.10947, Bid=1.10947, Ask=1.10947, Req=7

```

We will sell double the minimum lot.

```
>>>      6
TRADE_TRANSACTION_ORDER_ADD, #=1296992157(ORDER_TYPE_SELL/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10964, V=0.02
>>>      7
TRADE_TRANSACTION_DEAL_ADD, D=1279628463(DEAL_TYPE_SELL), »
   » #=1296992157(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10964, V=0.02, P=1296992157
>>>      8
TRADE_TRANSACTION_ORDER_DELETE, #=1296992157(ORDER_TYPE_SELL/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296992157
>>>      9
TRADE_TRANSACTION_HISTORY_ADD, #=1296992157(ORDER_TYPE_SELL/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296992157
>>>     10
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_SELL, V=0.02, ORDER_FILLING_FOK, @ 1.10964, #=1296992157
DONE, D=1279628463, #=1296992157, V=0.02, @ 1.10964, Bid=1.10964, Ask=1.10964, Req=8

```

Let's perform the counter closing operation.

```
>>>     11
TRADE_TRANSACTION_ORDER_ADD, #=1296992548(ORDER_TYPE_CLOSE_BY/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10964, V=0.01, P=1296991463, b=1296992157
>>>     12
TRADE_TRANSACTION_DEAL_ADD, D=1279628878(DEAL_TYPE_SELL), »
   » #=1296992548(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10964, V=0.01, P=1296991463
>>>     13
TRADE_TRANSACTION_POSITION, EURUSD, @ 1.10947, P=1296991463
>>>     14
TRADE_TRANSACTION_DEAL_ADD, D=1279628879(DEAL_TYPE_BUY), »
   » #=1296992548(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10947, V=0.01, P=1296992157
>>>     15
TRADE_TRANSACTION_ORDER_DELETE, #=1296992548(ORDER_TYPE_CLOSE_BY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296991463, b=1296992157
>>>     16
TRADE_TRANSACTION_HISTORY_ADD, #=1296992548(ORDER_TYPE_CLOSE_BY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296991463, b=1296992157
>>>     17
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_CLOSE_BY, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, #=1296992548, »
   » P=1296991463, b=1296992157
DONE, D=1279628878, #=1296992548, V=0.01, @ 1.10964, Bid=1.10961, Ask=1.10965, Req=9

```

We still have a short position of the minimum lot. Let's close it.

```
>>>     18
TRADE_TRANSACTION_ORDER_ADD, #=1297002683(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10964, V=0.01, P=1296992157
>>>     19
TRADE_TRANSACTION_ORDER_DELETE, #=1297002683(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296992157
>>>     20
TRADE_TRANSACTION_HISTORY_ADD, #=1297002683(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10964, P=1296992157
>>>     21
TRADE_TRANSACTION_DEAL_ADD, D=1279639132(DEAL_TYPE_BUY), »
   » #=1297002683(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10964, V=0.01, P=1296992157
>>>     22
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10964, #=1297002683, »
   » P=1296992157
DONE, D=1279639132, #=1297002683, V=0.01, @ 1.10964, Bid=1.10964, Ask=1.10964, Req=10

```

If you wish, you can enable the DetailedLog option to log all properties of trading objects at the moment of event processing. In a detailed log, you can notice discrepancies between the state of objects stored in the transaction structure (at the time of its initiation) and the current state. For example, when adding an order to close a position (opposite or normal), a ticket is specified in the transaction, according to which the monitor object will no longer be able to read anything, since the position has been deleted. As a result, we will see lines like this in the log:

```
TRADE_TRANSACTION_ORDER_ADD, #=1297777749(ORDER_TYPE_CLOSE_BY/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10953, V=0.01, P=1297774881, b=1297776850
...
Error: PositionSelectByTicket(1297774881) failed: TRADE_POSITION_NOT_FOUND

```

Let's restart the Expert Advisor TradeTransaction.mq5 to reset the logged events for the next test. This time we will use default settings (no details).

Now let's try to perform trading actions programmatically in the new Expert Advisor OrderSendTransaction1.mq5, and at the same time describe our OnTradeTransaction handler in it (same as in the previous example).

This Expert Advisor allows you to select the trade direction and volume: if you leave it at zero, the minimum lot of the current symbol is used by default. Also in the parameters there is a distance to the protective levels in points. The market is entered with the specified parameters, there is a 5 second pause between the setting of Stop Loss and Take Profit, and then closing the position, so that the user can intervene (for example, edit the stop loss manually), although this is not necessary, since we have already made sure that manual operations are intercepted by the program.

```
enum ENUM_ORDER_TYPE_MARKET
{
   MARKET_BUY = ORDER_TYPE_BUY,    // ORDER_TYPE_BUY
   MARKET_SELL = ORDER_TYPE_SELL   // ORDER_TYPE_SELL
};
   
input ENUM_ORDER_TYPE_MARKET Type;
input double Volume;               // Volume (0 - minimal lot)
input uint Distance2SLTP = 1000;

```

The strategy is launched once, for which a 1-second timer is used, which is turned off in its own handler.

```
int OnInit()
{
   EventSetTimer(1);
   return INIT_SUCCEEDED;
}
   
void OnTimer()
{
   EventKillTimer();
   ...

```

All actions are performed through an already familiar MqlTradeRequestSync structure with advanced features (MqlTradeSync.mqh): implicit initialization of fields with correct values, buy/sell methods for market orders, adjust for protective levels, and close for closing the position.

Step 1:

```
   MqlTradeRequestSync request;
   
   const double volume = Volume == 0 ?
      SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN) : Volume;
   
   Print("Start trade");
   const ulong order = (Type == MARKET_BUY ? request.buy(volume) : request.sell(volume));
   if(order == 0 || !request.completed())
   {
      Print("Failed Open");
      return;
   }
   
   Print("OK Open");

```

Step 2:

```
   Sleep(5000); // wait 5 seconds (user can edit position)
   Print("SL/TP modification");
   const double price = PositionGetDouble(POSITION_PRICE_OPEN);
   const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   TU::TradeDirection dir((ENUM_ORDER_TYPE)Type);
   const double SL = dir.negative(price, Distance2SLTP * point);
   const double TP = dir.positive(price, Distance2SLTP * point);
   if(request.adjust(SL, TP) && request.completed())
   {
      Print("OK Adjust");
   }
   else
   {
      Print("Failed Adjust");
   }

```

Step 3:

```
   Sleep(5000); // wait another 5 seconds
   Print("Close down");
   if(request.close(request.result.position) && request.completed())
   {
      Print("Finish");
   }
   else
   {
      Print("Failed Close");
   }
}

```

Intermediate waits not only make it possible to have time to consider the process, but also demonstrate an important aspect of MQL5 programming, which is single-threading. While our trading Expert Advisor is inside OnTimer, trading events generated by the terminal are accumulated in its queue and will be forwarded to the internal OnTradeTransaction handler in a deferred style, only after the exit from OnTimer.

At the same time, the TradeTransactions Expert Advisor running in parallel is not busy with any calculations and will receive trading events as quickly as possible.

The result of the execution of two Expert Advisors is presented in the following log with timing (for brevity OrderSendTransaction1 tagged as OS1, and Trade Transactions tagged as TTs).

```
19:09:08.078  OS1  Start trade
19:09:08.109  TTs  >>>     1
19:09:08.125  TTs  TRADE_TRANSACTION_ORDER_ADD, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_STARTED), »
                   EURUSD, @ 1.10913, V=0.01
19:09:08.125  TTs  >>>     2
19:09:08.125  TTs  TRADE_TRANSACTION_DEAL_ADD, D=1280661362(DEAL_TYPE_BUY), »
                   #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10913, V=0.01, »
                   P=1298021794
19:09:08.125  TTs  >>>     3
19:09:08.125  TTs  TRADE_TRANSACTION_ORDER_DELETE, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10913, P=1298021794
19:09:08.125  TTs  >>>     4
19:09:08.125  TTs  TRADE_TRANSACTION_HISTORY_ADD, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10913, P=1298021794
19:09:08.125  TTs  >>>     5
19:09:08.125  TTs  TRADE_TRANSACTION_REQUEST
19:09:08.125  TTs  TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10913, »
                   D=10, #=1298021794, M=1234567890
19:09:08.125  TTs  DONE, D=1280661362, #=1298021794, V=0.01, @ 1.10913, Bid=1.10913, Ask=1.10913, »
                   Req=9
19:09:08.125  OS1  Waiting for position for deal D=1280661362
19:09:08.125  OS1  OK Open
19:09:13.133  OS1  SL/TP modification
19:09:13.164  TTs  >>>     6
19:09:13.164  TTs  TRADE_TRANSACTION_POSITION, EURUSD, @ 1.10913, SL=1.09913, TP=1.11913, V=0.01, »
                   P=1298021794
19:09:13.164  OS1  OK Adjust
19:09:13.164  TTs  >>>     7
19:09:13.164  TTs  TRADE_TRANSACTION_REQUEST
19:09:13.164  TTs  TRADE_ACTION_SLTP, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, SL=1.09913, »
                   TP=1.11913, D=10, P=1298021794, M=1234567890
19:09:13.164  TTs  DONE, Req=10
19:09:18.171  OS1  Close down
19:09:18.187  OS1  Finish
19:09:18.218  TTs  >>>     8
19:09:18.218  TTs  TRADE_TRANSACTION_ORDER_ADD, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_STARTED), »
                   EURUSD, @ 1.10901, V=0.01, P=1298021794
19:09:18.218  TTs  >>>     9
19:09:18.218  TTs  TRADE_TRANSACTION_DEAL_ADD, D=1280661967(DEAL_TYPE_SELL), »
                   #=1298022443(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10901, »
                   SL=1.09913, TP=1.11913, V=0.01, P=1298021794
19:09:18.218  TTs  >>>    10
19:09:18.218  TTs  TRADE_TRANSACTION_ORDER_DELETE, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10901, P=1298021794
19:09:18.218  TTs  >>>    11
19:09:18.218  TTs  TRADE_TRANSACTION_HISTORY_ADD, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10901, P=1298021794
19:09:18.218  TTs  >>>    12
19:09:18.218  TTs  TRADE_TRANSACTION_REQUEST
19:09:18.218  TTs  TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_SELL, V=0.01, ORDER_FILLING_FOK, @ 1.10901, »
                   D=10, #=1298022443, P=1298021794, M=1234567890
19:09:18.218  TTs  DONE, D=1280661967, #=1298022443, V=0.01, @ 1.10901, Bid=1.10901, Ask=1.10901, »
                   Req=11
19:09:18.218  OS1  >>>     1
19:09:18.218  OS1  TRADE_TRANSACTION_ORDER_ADD, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_STARTED), »
                   EURUSD, @ 1.10913, V=0.01
19:09:18.218  OS1  >>>     2
19:09:18.218  OS1  TRADE_TRANSACTION_DEAL_ADD, D=1280661362(DEAL_TYPE_BUY), »
                   #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, »
                   @ 1.10913, V=0.01, P=1298021794
19:09:18.218  OS1  >>>     3
19:09:18.218  OS1  TRADE_TRANSACTION_ORDER_DELETE, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10913, P=1298021794
19:09:18.218  OS1  >>>     4
19:09:18.218  OS1  TRADE_TRANSACTION_HISTORY_ADD, #=1298021794(ORDER_TYPE_BUY/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10913, P=1298021794
19:09:18.218  OS1  >>>     5
19:09:18.218  OS1  TRADE_TRANSACTION_REQUEST
19:09:18.218  OS1  TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10913, »
                   D=10, #=1298021794, M=1234567890
19:09:18.218  OS1  DONE, D=1280661362, #=1298021794, V=0.01, @ 1.10913, Bid=1.10913, Ask=1.10913, »
                   Req=9
19:09:18.218  OS1  >>>     6
19:09:18.218  OS1  TRADE_TRANSACTION_POSITION, EURUSD, @ 1.10913, SL=1.09913, TP=1.11913, V=0.01, »
                   P=1298021794
19:09:18.218  OS1  >>>     7
19:09:18.218  OS1  TRADE_TRANSACTION_REQUEST
19:09:18.218  OS1  TRADE_ACTION_SLTP, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, »
                   SL=1.09913, TP=1.11913, D=10, P=1298021794, M=1234567890
19:09:18.218  OS1  DONE, Req=10
19:09:18.218  OS1  >>>     8
19:09:18.218  OS1  TRADE_TRANSACTION_ORDER_ADD, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_STARTED), »
                   EURUSD, @ 1.10901, V=0.01, P=1298021794
19:09:18.218  OS1  >>>     9
19:09:18.218  OS1  TRADE_TRANSACTION_DEAL_ADD, D=1280661967(DEAL_TYPE_SELL), »
                   #=1298022443(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10901, »
                   SL=1.09913, TP=1.11913, V=0.01, P=1298021794
19:09:18.218  OS1  >>>    10
19:09:18.218  OS1  TRADE_TRANSACTION_ORDER_DELETE, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10901, P=1298021794
19:09:18.218  OS1  >>>    11
19:09:18.218  OS1  TRADE_TRANSACTION_HISTORY_ADD, #=1298022443(ORDER_TYPE_SELL/ORDER_STATE_FILLED), »
                   EURUSD, @ 1.10901, P=1298021794
19:09:18.218  OS1  >>>    12
19:09:18.218  OS1  TRADE_TRANSACTION_REQUEST
19:09:18.218  OS1  TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_SELL, V=0.01, ORDER_FILLING_FOK, @ 1.10901, »
                   D=10, #=1298022443, P=1298021794, M=1234567890
19:09:18.218  OS1  DONE, D=1280661967, #=1298022443, V=0.01, @ 1.10901, Bid=1.10901, Ask=1.10901, »
                   Req=11

```

The numbering of events in the programs is the same (provided that they are started cleanly, as recommended). Note that the same event is printed first from TTs immediately after the request is executed, and the second time only at the end of the test, where, in fact, all events are output from the queue to the OS1.

If we remove artificial delays, the script will, of course, run faster, but still the OnTradeTransaction handler will receive notifications (multiple times) after all three steps, not after each respective request. How critical it is?

Now the examples use our modification of the structure MqlTradeRequestSync, purposefully using the synchronous option OrderSend, which also implements a universal completed method which checks if the request completed successfully. With this control, we can set protective levels for a position, because we know how to wait for its ticket to appear. Within the framework of such a synchronous concept (adopted for the sake of convenience), we do not need to analyze query results in OnTradeTransaction. However, this is not always the case.

When an Expert Advisor needs to send many requests at once, as in the case of the example with setting a grid of orders PendingOrderGrid2.mq5 discussed in the section on [position properties](/en/book/automation/experts/experts_positionget_funcs), waiting for each position or order to be "ready" may reduce the overall performance of the Expert Advisor. In such cases, it is recommended to use the OrderSendAsync function. But if successful, it fills only the request_id field in the MqlTradeResult, with which you then need to track the appearance of orders, deals and positions in OnTradeTransaction.

One of the most obvious but not particularly elegant tricks for implementing this scheme is to store the identifiers of requests or entire structures of the requests being sent in an array, in the global context. These identifiers can then be looked up in incoming transactions in OnTradeTransaction, the tickets can be found in the MqlTradeResult parameter and further actions can be taken. As a result, the trading logic is separated into different functions. For example, in the context of the last Expert Advisor OrderSendTransaction1.mq5 this "diversification" lies in the fact that after sending the first order, the code fragments must be transferred to OnTradeTransaction and checked for the following:

- transaction type in MqlTradeTransaction (transaction type);
- request type in MqlTradeRequest (request action);
- request id in MqlTradeResult (result.request_id);

All this should be supplemented with specific applied logic (for example, checking for the existence of a position), which provides branching by trading strategy states. A little later we will make a similar modification of the OrderSendTransaction Expert Advisor under a different number to visually show the amount of additional source code. And then we will offer a way to organize the program more linearly, but without abandoning transactional events.

For now, we only note that the developer should choose whether to build an algorithm around OnTradeTransaction or without it. In many cases, when bulk sending of orders is not needed, it is possible to stay in the synchronous programming paradigm. However, OnTradeTransaction is the most practical way to control the triggering of pending orders and protective levels, as well as other events generated by the server. After a little preparation, we will present two relevant examples: the final modification of the grid Expert Advvisor and the implementation of the popular setup of two OCO (One Cancels Other) orders (see the section [On Trade](/en/book/automation/experts/experts_ontrade)).

An alternative to application of OnTradeTransaction consists in periodic analysis of the trading environment, that is, in fact, in remembering the number of orders and positions and looking for changes among them. This approach is suitable for strategies based on schedules or allowing certain time delays.

We emphasize again that the use of OnTradeTransaction does not mean that the program must necessarily switch from OrderSend on OrderSendAsync: You can use either variety or both. Recall that the OrderSend function is also not quite synchronous, as it returns, at best, the ticket of the order and the deal but not the position. Soon we will be able to measure the execution time of a batch of orders within the same grid strategy using both variants of the function: OrderSend and OrderSendAsync.

To unify the development of synchronous and asynchronous programs, it would be great to support OrderSendAsync in our structure MqlTradeRequestSync (despite its name). This can be done with just a couple of corrections. First, you need to replace all currently existing calls OrderSend to your own method orderSend, and in it switch the call to OrderSend or OrderSendAsync depending on a flag.

```
struct MqlTradeRequestSync: public MqlTradeRequest
{
   ...
   static bool AsyncEnabled;
   ...
private:
   bool orderSend(const MqlTradeRequest &req, MqlTradeResult &res)
   {
      return AsyncEnabled ? ::OrderSendAsync(req, res) : ::OrderSend(req, res);
   }
};

```

By setting the AsyncEnabled public variable to true or false, you can switch from one mode to another, for example, in the code fragment where mass orders are sent.

Second, those methods of the structure that returned a ticket (for example, for entering the market) you should return the request_id field instead of order. For example, inside the methods _pending and _market we had the following operator:

```
if(OrderSend(this, result)) return result.order;

```

Now it is replaced by:

```
if(orderSend(this, result)) return result.order ? result.order :
   (result.retcode == TRADE_RETCODE_PLACED ? result.request_id : 0);

```

Of course, when asynchronous mode is enabled, we can no longer use the completed method to wait for the query results to be ready immediately after it is sent. But this method is, basically, optional: you can just drop it even when working through OrderSend.

So, taking into account the new modification of the MqlTradeSync.mqh file, let's create OrderSendTransaction2.mq5.

This Expert Advisor will send the initial request as before from OnTimer, while setting protective levels and closing a position in OnTradeTransaction step by step. Although we will not have an artificial delay between the stages this time, the sequence of states itself is standard for many Expert Advisors: opened a position, modified, closed (if certain market conditions are met, which are left behind the scenes here).

Two global variables will allow you to track the state: RequestID with the id of the last request sent (the result of which we expect) and Position Ticket with an open position ticket. When there the position did not appear yet, or no longer exists, the ticket is equal to 0.

```
uint RequestID = 0;
ulong PositionTicket = 0;

```

Asynchronous mode is enabled in the OnInit handler.

```
int OnInit()
{
   ...
   MqlTradeRequestSync::AsyncEnabled = true;
   ...
}

```

The OnTimer function is now much shorter.

```
void OnTimer()
{
   ...
   // send a request TRADE_ACTION_DEAL (asynchronously!)
   const ulong order = (Type == MARKET_BUY ? request.buy(volume) : request.sell(volume));
   if(order) // in asynchronous mode this is now request_id
   {
      Print("OK Open?");
      RequestID = request.result.request_id; // same as order
   }
   else
   {
      Print("Failed Open");
   }
}

```

On successful completion of the request, we get only request_id and store it in the RequestID variable. The status print now contains a question mark, like "OK Open?", because the actual result is not yet known.

OnTradeTransaction became significantly more complicated due to the verification of the results and the execution of subsequent trading orders according to the conditions. Let's consider it gradually.

In this case, the entire trading logic has moved into the branch for transactions of the TRADE_TRANSACTION_REQUEST type. Of course, the developer can use other types if desired, but we use this one because it contains information in the form of a familiar structure MqlTradeResult, i.e., this sort of represents a delayed ending of an asynchronous call OrderSendAsync.

```
void OnTradeTransaction(const MqlTradeTransaction &transaction,
   const MqlTradeRequest &request,
   const MqlTradeResult &result)
{
   static ulong count = 0;
   PrintFormat(">>>% 6d", ++count);
   Print(TU::StringOf(transaction));
   
   if(transaction.type == TRADE_TRANSACTION_REQUEST)
   {
      Print(TU::StringOf(request));
      Print(TU::StringOf(result));
      
      ...
      // here is the whole algorithm
   }
}

```

We should only be interested in requests with the ID we expect. So the next statement will be nested if. In its block, we describe the MqlTradeRequestSync object in advance, because it will be necessary to send regular trade requests according to the plan.

```
      if(result.request_id == RequestID)
      {
         MqlTradeRequestSync next;
         next.magic = Magic;
         next.deviation = Deviation;
         ...
      }

```

We have only two working request types, so we add one more nested if one for them.

```
         if(request.action == TRADE_ACTION_DEAL)
         {
            ... // here is the reaction to opening and closing a position
         }
         else if(request.action == TRADE_ACTION_SLTP)
         {
            ... // here is the reaction to setting SLTP for an open position
         }

```

Please note that TRADE_ACTION_DEAL is used for both opening and closing a position, and therefore one more if is required, in which we will distinguish between these two states depending on the value of the PositionTicket variable.

```
            if(PositionTicket == 0)
            {
               ... // there is no position, so this is an opening notification 
            }
            else
            {
               ... // there is a position, so this is a closure
            }

```

There are no position increases (for netting) or multiple positions (for hedging) in the trading strategy under consideration, which is why this part is logically simple. Real Expert Advisors will require much more different estimates of intermediate states.

In the case of a position opening notification, the block of code looks like this:

```
            if(PositionTicket == 0)
            {
               // trying to get results from the transaction: select an order by ticket
               if(!HistoryOrderSelect(result.order))
               {
                  Print("Can't select order in history");
                  RequestID = 0;
                  return;
               }
               // get position ID and ticket
               const ulong posid = HistoryOrderGetInteger(result.order, ORDER_POSITION_ID);
               PositionTicket = TU::PositionSelectById(posid);
               ...

```

For simplicity, we have omitted error and requote checking here. You can see an example of their handling in the attached source code. Recall that all these checks have already been implemented in the methods of the MqlTradeRequestSync structure, but they only work in synchronous mode, and therefore we have to repeat them explicitly.

The next code fragment for setting protective levels has not changed much.

```
            if(PositionTicket == 0)
            {
               ...
               const double price = PositionGetDouble(POSITION_PRICE_OPEN);
               const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
               TU::TradeDirection dir((ENUM_ORDER_TYPE)Type);
               const double SL = dir.negative(price, Distance2SLTP * point);
               const double TP = dir.positive(price, Distance2SLTP * point);
               // sending TRADE_ACTION_SLTP request (asynchronously!)
               if(next.adjust(PositionTicket, SL, TP))
               {
                  Print("OK Adjust?");
                  RequestID = next.result.request_id;
               }
               else
               {
                  Print("Failed Adjust");
                  RequestID = 0;
               }
            }

```

The only difference here is: we fill the RequestID variable with ID of the new TRADE_ACTION_SLTP request.

Receiving a notification about a deal with a non-zero PositionTicket implies that the position has been closed.

```
            if(PositionTicket == 0)
            {
               ... // see above
            }
            else
            {
               if(!PositionSelectByTicket(PositionTicket))
               {
                  Print("Finish");
                  RequestID = 0;
                  PositionTicket = 0;
               }
            }

```

In case of successful deletion, the position cannot be selected using PositionSelectByTicket, so we reset RequestID and PositionTicket. The Expert Advisor then returns to its initial state and is ready to make the next buy/sell-modify-close cycle.

It remains for us to consider sending a request to close the position. In our simplified to a minimum strategy, this happens immediately after the successful modification of the protective levels.

```
         if(request.action == TRADE_ACTION_DEAL)
         {
            ... // see above
         }
         else if(request.action == TRADE_ACTION_SLTP)
         {
            // send a TRADE_ACTION_DEAL request to close (asynchronously!)
            if(next.close(PositionTicket))
            {
               Print("OK Close?");
               RequestID = next.result.request_id;
            }
            else
            {
               PrintFormat("Failed Close %lld", PositionTicket);
            }
         }

```

That's the whole function OnTradeTransaction. The Expert Advisor is ready.

Let's run OrderSendTransaction2.mq5 with default settings on EURUSD. Below is an example log.

```
Start trade
OK Open?
>>>     1
TRADE_TRANSACTION_ORDER_ADD, #=1299508203(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10640, V=0.01
>>>     2
TRADE_TRANSACTION_DEAL_ADD, D=1282135720(DEAL_TYPE_BUY), »
   » #=1299508203(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10640, V=0.01, P=1299508203
>>>     3
TRADE_TRANSACTION_ORDER_DELETE, #=1299508203(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10640, P=1299508203
>>>     4
TRADE_TRANSACTION_HISTORY_ADD, #=1299508203(ORDER_TYPE_BUY/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10640, P=1299508203
>>>     5
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10640, D=10, »
   » #=1299508203, M=1234567890
DONE, D=1282135720, #=1299508203, V=0.01, @ 1.1064, Bid=1.1064, Ask=1.1064, Req=7
OK Adjust?
>>>     6
TRADE_TRANSACTION_POSITION, EURUSD, @ 1.10640, SL=1.09640, TP=1.11640, V=0.01, P=1299508203
>>>     7
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_SLTP, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, SL=1.09640, TP=1.11640, »
   » D=10, P=1299508203, M=1234567890
DONE, Req=8
OK Close?
>>>     8
TRADE_TRANSACTION_ORDER_ADD, #=1299508215(ORDER_TYPE_SELL/ORDER_STATE_STARTED), EURUSD, »
   » @ 1.10638, V=0.01, P=1299508203
>>>     9
TRADE_TRANSACTION_ORDER_DELETE, #=1299508215(ORDER_TYPE_SELL/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10638, P=1299508203
>>>    10
TRADE_TRANSACTION_HISTORY_ADD, #=1299508215(ORDER_TYPE_SELL/ORDER_STATE_FILLED), EURUSD, »
   » @ 1.10638, P=1299508203
>>>    11
TRADE_TRANSACTION_DEAL_ADD, D=1282135730(DEAL_TYPE_SELL), »
   » #=1299508215(ORDER_TYPE_BUY/ORDER_STATE_STARTED), EURUSD, @ 1.10638, »
   » SL=1.09640, TP=1.11640, V=0.01, P=1299508203
>>>    12
TRADE_TRANSACTION_REQUEST
TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_SELL, V=0.01, ORDER_FILLING_FOK, @ 1.10638, D=10, »
   » #=1299508215, P=1299508203, M=1234567890
DONE, D=1282135730, #=1299508215, V=0.01, @ 1.10638, Bid=1.10638, Ask=1.10638, Req=9
Finish

```

The trading logic is working as expected, and transaction events arrive strictly after each next order is sent. If we now run our new Expert Advisor and the transactions interceptor TradeTransactions.mq5 in parallel, log messages from two Expert Advisors will appear synchronously.

However, a remake from the first straight version OrderSendTransaction1.mq5 to an asynchronous second version OrderSendTransaction2.mq5 required significantly more sophisticated code. The question arises: is it possible to somehow combine the principles of sequential description of trading logic (code transparency) and parallel processing (speed)?

In theory, this is possible, but it will require at some point to spend time to work on creating some kind of auxiliary mechanism.
