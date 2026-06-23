# Structure of a Trade Transaction (MqlTradeTransaction)

When performing some definite actions on a trade account, its state changes. Such actions include:

- Sending a trade request from any MQL5 application in the client terminal using [OrderSend](/en/docs/trading/ordersend) and [OrderSendAsync](/en/docs/trading/ordersendasync) functions and its further execution;
- Sending a trade request via the terminal graphical interface and its further execution;

- Pending orders and stop orders activation on the server;
- Performing operations on a trade server side.

The following trade transactions are performed as a result of these actions:

- handling a trade request;
- changing open orders;
- changing orders history;
- changing deals history;
- changing positions.

For example, when sending a market buy order, it is handled, an appropriate buy order is created for the account, the order is then executed and removed from the list of the open ones, then it is added to the orders history, an appropriate deal is added to the history and a new position is created. All these actions are trade transactions.

Special [OnTradeTransaction()](/en/docs/event_handlers/ontradetransaction) handler is provided in MQL5 to get trade transactions applied to an account. The first parameter of the handler gets MqlTradeTransaction structure describing [trade transactions](/en/docs/constants/tradingconstants/enum_trade_transaction_type).

```
struct MqlTradeTransaction
  {
   ulong                         deal;             // Deal ticket
   ulong                         order;            // Order ticket
   string                        symbol;           // Trade symbol name
   ENUM_TRADE_TRANSACTION_TYPE   type;             // Trade transaction type
   ENUM_ORDER_TYPE               order_type;       // Order type
   ENUM_ORDER_STATE              order_state;      // Order state
   ENUM_DEAL_TYPE                deal_type;        // Deal type
   ENUM_ORDER_TYPE_TIME          time_type;        // Order type by action period
   datetime                      time_expiration;  // Order expiration time
   double                        price;            // Price 
   double                        price_trigger;    // Stop limit order activation price
   double                        price_sl;         // Stop Loss level
   double                        price_tp;         // Take Profit level
   double                        volume;           // Volume in lots
   ulong                         position;         // Position ticket
   ulong                         position_by;      // Ticket of an opposite position
  };

```

Fields Description

| Field | Description |
| --- | --- |
| deal | Deal ticket. |
| order | Order ticket. |
| symbol | The name of the trading symbol, for which transaction is performed. |
| type | Trade transaction type. The value can be one of  ENUM_TRADE_TRANSACTION_TYPE  enumeration values. |
| order_type | Trade order type. The value can be one of  ENUM_ORDER_TYPE  enumeration values. |
| order_state | Trade order state. The value can be one of  ENUM_ORDER_STATE  enumeration values. |
| deal_type | Deal type. The value can be one of  ENUM_DEAL_TYPE  enumeration values. |
| time_type | Order type upon expiration. The value can be one of  ENUM_ORDER_TYPE_TIME  values. |
| time_expiration | Pending order expiration term (for orders of  ORDER_TIME_SPECIFIED  and  ORDER_TIME_SPECIFIED_DAY  types). |
| price | Price. Depending on a trade transaction type, it may be a price of an order, a deal or a position. |
| price_trigger | Stop limit order stop (activation) price ( ORDER_TYPE_BUY_STOP_LIMIT  and  ORDER_TYPE_SELL_STOP_LIMIT ). |
| price_sl | Stop Loss price. Depending on a trade transaction type, it may relate to an order, a deal or a position. |
| price_tp | Take Profit price. Depending on a trade transaction type, it may relate to an order, a deal or a position. |
| volume | Volume in lots. Depending on a trade transaction type, it may indicate the current volume of an order, a deal or a position. |
| position | The ticket of the position affected by the transaction. |
| position_by | The ticket of the opposite position. Used when closing a position by an opposite one, i.e. by a position of the same symbol that was opened in the opposite direction. |

The essential parameter for received transaction analysis is its type specified in type field. For example, if a transaction is of [TRADE_TRANSACTION_REQUEST](/en/docs/constants/tradingconstants/enum_trade_transaction_type) type (a result of handling a trade request by the server has been received), the structure has only only one field that is filled completely - type. Other fields are not analyzed. In this case, we may analyze two additional request and result parameters submitted to OnTradeTransaction() handler, as shown below.

Having data on a trading operation type, you can decide on the analysis of the current state of orders, positions and deals on a trading account. Remember that one trade request sent to the server from the terminal can generate several new transactions. The priority of their arrival at the terminal is not guaranteed.

MqlTradeTransaction structure is filled in different ways depending on a trade transaction type ([ENUM_TRADE_TRANSACTION_TYPE](/en/docs/constants/tradingconstants/enum_trade_transaction_type)):

TRADE_TRANSACTION_ORDER_* and TRADE_TRANSACTION_HISTORY_*

The following fields in MqlTradeTransaction structure are filled for trade transactions related to open orders handling (TRADE_TRANSACTION_ORDER_ADD, TRADE_TRANSACTION_ORDER_UPDATE and TRADE_TRANSACTION_ORDER_DELETE) and orders history (TRADE_TRANSACTION_HISTORY_ADD, TRADE_TRANSACTION_HISTORY_UPDATE, TRADE_TRANSACTION_HISTORY_DELETE):

- order - order ticket;
- symbol - order symbol name;
- type - trade transaction type;
- order_type - order type;
- orders_state - order current state;
- time_type - order expiration type;
- time_expiration - order expiration time (for orders having [ORDER_TIME_SPECIFIED](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time) and [ORDER_TIME_SPECIFIED_DAY](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time) expiration types);
- price - order price specified by a client;
- price_trigger - stop limit order stop price (only for [ORDER_TYPE_BUY_STOP_LIMIT](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) and [ORDER_TYPE_SELL_STOP_LIMIT](/en/docs/constants/tradingconstants/orderproperties#enum_order_type));
- price_sl - Stop Loss order price (filled, if specified in the order);
- price_tp - Take Profit order price (filled, if specified in the order);
- volume - order current volume (unfilled). Initial order volume can be found in the orders history using [HistoryOrders*](/en/docs/trading/historyordergetticket) function.
- position - the ticket of the position that was opened, modified or closed as a result of order execution. It is only filled for market orders, not filled for TRADE_TRANSACTION_ORDER_ADD.
- position_by - the ticket of the opposite position. It is only filled for the close by orders (to close a position by an opposite one).

TRADE_TRANSACTION_DEAL_*

The following fields in MqlTradeTransaction structure are filled for trade transactions related to deals handling (TRADE_TRANSACTION_DEAL_ADD, TRADE_TRANSACTION_DEAL_UPDATE and TRADE_TRANSACTION_DEAL_DELETE):

- deal - deal ticket;
- order - order ticket, based on which a deal has been performed;
- symbol - deal symbol name;
- type - trade transaction type;
- deal_type - deal type;
- price - deal price;
- price_sl - Stop Loss price (filled, if specified in the order, based on which a deal has been performed);
- price_tp - Take Profit price (filled, if specified in the order, based on which a deal has been performed);
- volume - deal volume in lots.
- position - the ticket of the position that was opened, modified or closed as a result of deal execution.
- position_by - the ticket of the opposite position. It is only filled for the out by deals (closing a position by an opposite one).

TRADE_TRANSACTION_POSITION

The following fields in MqlTradeTransaction structure are filled for trade transactions related to changing the positions not connected with deals execution (TRADE_TRANSACTION_POSITION):

- symbol - position symbol name;
- type - trade transaction type;
- deal_type - position type ([DEAL_TYPE_BUY](/en/docs/constants/tradingconstants/dealproperties#enum_deal_type) or [DEAL_TYPE_SELL](/en/docs/constants/tradingconstants/dealproperties#enum_deal_type));
- price - weighted average position open price;
- price_sl - Stop Loss price;
- price_tp - Take Profit price;
- volume - position volume in lots, if it has been changed.

```
Position change (adding, changing or closing), as a result of a deal execution, does not lead to the occurrence of TRADE_TRANSACTION_POSITION transaction.

```

TRADE_TRANSACTION_REQUEST

Only one field in MqlTradeTransaction structure is filled for trade transactions describing the fact that a trade request has been processed by a server and processing result has been received (TRADE_TRANSACTION_REQUEST):

- type - trade transaction type;

```
Only type field (trade transaction type) must be analyzed for such transactions. The second and third parameters of OnTradeTransaction function (request and result) must be analyzed for additional data.

```

Example:

```
input int MagicNumber=1234567;
 
//--- enable CTrade trading class and declare the variable of this class
#include <Trade\Trade.mqh>
CTrade trade;
//--- flags for installing and deleting the pending order
bool pending_done=false;
bool pending_deleted=false;
//--- pending order ticket will be stored here
ulong order_ticket;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- set MagicNumber to mark all our orders
   trade.SetExpertMagicNumber(MagicNumber);
//--- trade requests will be sent in asynchronous mode using OrderSendAsync() function
   trade.SetAsyncMode(true);
//--- initialize the variable by zero
   order_ticket=0;
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---installing a pending order
   if(!pending_done)
     {
      double ask=SymbolInfoDouble(_Symbol,SYMBOL_ASK);
      double buy_stop_price=NormalizeDouble(ask+1000*_Point,(int)SymbolInfoInteger(_Symbol,SYMBOL_DIGITS));
      bool res=trade.BuyStop(0.1,buy_stop_price,_Symbol);
      //--- if BuyStop() function performed successfully 
      if(res)
        {
         pending_done=true;
         //--- get a result of the request sending from ctrade
         MqlTradeResult trade_result;
         trade.Result(trade_result);
         //--- get request_id for the sent request
         uint request_id=trade_result.request_id;
         Print("Request has been sent to set a pending order. Request_ID=",request_id);
         //--- storing the order ticket (will be zero if using the asynchronous mode of sending to CTrade)
         order_ticket=trade_result.order;
         //--- all is done, early exit from OnTick() handler
         return;
        }
     }
//--- delete the pending order
   if(!pending_deleted)
      //--- additional check
      if(pending_done && (order_ticket!=0))
        {
         //--- trying to delete the pending order
         bool res=trade.OrderDelete(order_ticket);
         Print("OrderDelete=",res);
         //--- when delete request is sent successfully
         if(res)
           {
            pending_deleted=true;
            //--- get the request execution result
            MqlTradeResult trade_result;
            trade.Result(trade_result);
            //--- take request ID from the result
            uint request_id=trade_result.request_id;
            //--- display in Journal
            Print("The request has been sent to delete a pending order #",order_ticket,
                  ". Request_ID=",request_id,
                  "\r\n");
            //--- fix the order ticket from the request result
            order_ticket=trade_result.order;
           }
        }
//---        
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
  {
//--- get transaction type as enumeration value 
   ENUM_TRADE_TRANSACTION_TYPE type=(ENUM_TRADE_TRANSACTION_TYPE)trans.type;
//--- if the transaction is the request handling result, only its name is displayed
   if(type==TRADE_TRANSACTION_REQUEST)
     {
      Print(EnumToString(type));
      //--- display the handled request string name
      Print("------------RequestDescription\r\n",RequestDescription(request));
      //--- display request result description
      Print("------------ResultDescription\r\n",TradeResultDescription(result));
      //--- store the order ticket for its deletion at the next handling in OnTick()
      if(result.order!=0)
        {
         //--- delete this order by its ticket at the next OnTick() call
         order_ticket=result.order;
         Print(" Pending order ticket ",order_ticket,"\r\n");
        }
     }
   else // display the full description for transactions of another type
//--- display description of the received transaction in the Journal
      Print("------------TransactionDescription\r\n",TransactionDescription(trans));
 
//---     
  }
//+------------------------------------------------------------------+
//| Returns transaction textual description                          |
//+------------------------------------------------------------------+
string TransactionDescription(const MqlTradeTransaction &trans)
  {
//--- 
   string desc=EnumToString(trans.type)+"\r\n";
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
   desc+="Position: "+(string)trans.position+"\r\n";
   desc+="Position by: "+(string)trans.position_by+"\r\n";
//--- return the obtained string
   return desc;
  }
//+------------------------------------------------------------------+
//| Returns the trade request textual description                    |
//+------------------------------------------------------------------+
string RequestDescription(const MqlTradeRequest &request)
  {
//---
   string desc=EnumToString(request.action)+"\r\n";
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
//--- return the obtained string
   return desc;
  }
//+------------------------------------------------------------------+
//| Returns the textual description of the request handling result   |
//+------------------------------------------------------------------+
string TradeResultDescription(const MqlTradeResult &result)
  {
//---
   string desc="Retcode "+(string)result.retcode+"\r\n";
   desc+="Request ID: "+StringFormat("%d",result.request_id)+"\r\n";
   desc+="Order ticket: "+(string)result.order+"\r\n";
   desc+="Deal ticket: "+(string)result.deal+"\r\n";
   desc+="Volume: "+StringFormat("%G",result.volume)+"\r\n";
   desc+="Price: "+StringFormat("%G",result.price)+"\r\n";
   desc+="Ask: "+StringFormat("%G",result.ask)+"\r\n";
   desc+="Bid: "+StringFormat("%G",result.bid)+"\r\n";
   desc+="Comment: "+result.comment+"\r\n";
//--- return the obtained string
   return desc;
  }

```

See also

[Trade Transaction Types](/en/docs/constants/tradingconstants/enum_trade_transaction_type), [OnTradeTransaction()](/en/docs/event_handlers/ontradetransaction)
