# Types of trading transactions

In addition to performing trading operations, MQL programs can respond to trading events. It is important to note that such events occur not only as a result of the actions of programs, but also for other reasons, for example, when manually managed by the user or performing automatic actions on the server (activation of a pending order, Stop Loss, Take Profit, Stop Out, position transfer to a new day, depositing or withdrawing funds from the account, and much more).

Regardless of the initiator of the actions, they result in the execution of trading transactions on the account. Trading transactions are indivisible steps that include:

- Processing a trade request
- Changing the list of active orders (including adding a new order, executing and deleting a triggered order)
- Changing the history of orders
- Changing the history of deals
- Changing positions

Depending on the nature of the operation, some steps may be optional. For example, modifying the protective levels of a position will miss three middle points. And when a buy order is sent, the market will go through a full cycle: the request is processed, a corresponding order is created for the account, the order is executed, it is removed from the active list, added to the order history, then the corresponding deal is added to the history and a new position is created. All these actions are trading transactions.

To receive notifications about such events, the special OnTradeTransaction handler function should be described in an Expert Advisor or an indicator. We will look at it in detail in the next section. The fact is that one of its parameters, the first and most important, has the type of a predefined structure MqlTradeTransaction. So let's first talk about transactions as such.

```
struct MqlTradeTransaction
{ 
   ulong                         deal;             // Deal ticket 
   ulong                         order;            // Order ticket 
   string                        symbol;           // Name of the trading instrument 
   ENUM_TRADE_TRANSACTION_TYPE   type;             // Trade transaction type 
   ENUM_ORDER_TYPE               order_type;       // Order type
   ENUM_ORDER_STATE              order_state;      // Order state 
   ENUM_DEAL_TYPE                deal_type;        // Deal type 
   ENUM_ORDER_TYPE_TIME          time_type;        // Order type by duration
   datetime                      time_expiration;  // Order expiration date 
   double                        price;            // Price 
   double                        price_trigger;    // Stop limit order trigger price 
   double                        price_sl;         // Stop Loss Level 
   double                        price_tp;         // Take Profit Level 
   double                        volume;           // Volume in lots 
   ulong                         position;         // Position ticket 
   ulong                         position_by;      // Opposite position ticket 
};

```

The following table describes each structure field.

| Field | Description |
| --- | --- |
| deal | Deal ticket |
| order | Order ticket |
| symbol | The name of the trading instrument on which the transaction was made |
| type | Trade transaction type ENUM_TRADE_TRANSACTION_TYPE (see below) |
| order_type | Order type  ENUM_ORDER_TYPE |
| order_state | Order status  ENUM_ORDER_STATE |
| deal_type | Deal type  ENUM_DEAL_TYPE |
| time_type | Order type by expiration  ENUM_ORDER_TYPE_TIME |
| time_expiration | Pending order expiration date |
| price | The price of an order, deal or position, depending on the transaction |
| price_trigger | Stop price (trigger price) of a stop limit order |
| price_sl | Stop Loss  price; it may refer to an order, deal, or position, depending on the transaction |
| price_tp | Take Profit  price; it may refer to an order, deal, or position, depending on the transaction |
| volume | Volume in lots; it may indicate the current volume of the order, deal, or position, depending on the transaction |
| position | Ticket of the position affected by the transaction |
| position_by | Opposite position ticket |

Some fields only make sense in certain cases. In particular, the time_expiration field is filled for orders with time_type equal to the ORDER_TIME_SPECIFIED or ORDER_TIME_SPECIFIED_DAY  expiration type. The price_trigger field is reserved for stop-limit orders only (ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT).

It is also obvious that position modifications operate on the position ticket (field position), but do not use order or deal tickets. In addition, the position_by field is reserved exclusively for closing a counter position, that is, the one opened for the same instrument but in the opposite direction.

The defining characteristic for the analysis of a transaction is its type (field type). To describe it, the MQL5 API introduces a special enumeration ENUM_TRADE_TRANSACTION_TYPE, which contains all possible types of transactions.

| Identifier | Description |
| --- | --- |
| TRADE_TRANSACTION_ORDER_ADD | Adding a new order |
| TRADE_TRANSACTION_ORDER_UPDATE | Changing an active order |
| TRADE_TRANSACTION_ORDER_DELETE | Deleting an active order |
| TRADE_TRANSACTION_DEAL_ADD | Adding a deal to history |
| TRADE_TRANSACTION_DEAL_UPDATE | Changing a deal in history |
| TRADE_TRANSACTION_DEAL_DELETE | Deleting a deal from history |
| TRADE_TRANSACTION_HISTORY_ADD | Adding an order to history as a result of execution or cancellation |
| TRADE_TRANSACTION_HISTORY_UPDATE | Changing an order in history |
| TRADE_TRANSACTION_HISTORY_DELETE | Deleting an order from history |
| TRADE_TRANSACTION_POSITION | Change a position |
| TRADE_TRANSACTION_REQUEST | Notification that a trade request has been processed by the server and the result of its processing has been received |

Let's provide some explanations.

In a transaction of the TRADE_TRANSACTION_ORDER_UPDATE type, order changes include not only explicit changes on the part of the client terminal or trade server but also changes in its state (for example, transition from the ORDER_STATE_STARTED state to ORDER_STATE_PLACED or from ORDER_STATE_PLACED to ORDER_STATE_PARTIAL, etc.).

During the TRADE_TRANSACTION_ORDER_DELETE transaction, an order can be deleted as a result of a corresponding explicit request or execution (fill) on the server. In both cases, it will be transferred to history and the transaction TRADE_TRANSACTION_HISTORY_ADD must also occur.

The TRADE_TRANSACTION_DEAL_ADD transaction is carried out not only as a result of order execution but also as a result of transactions with the account balance.

Some transactions, such as TRADE_TRANSACTION_DEAL_UPDATE, TRADE_TRANSACTION_DEAL_DELETE, TRADE_TRANSACTION_HISTORY_DELETE are quite rare because they describe situations when a deal or order in the history is changed or deleted on the server retroactively. This, as a rule, is a consequence of synchronization with an external trading system (exchange).

It is important to note that adding or liquidating a position does not entail the appearance of the TRADE_TRANSACTION_POSITION transaction. This type of transaction informs that the position has been changed on the side of the trade server, programmatically or manually by the user. In particular, a position can experience changes of the volume (partial opposite closing, reversal), opening price, as well as Stop Loss and Take Profit levels. Some actions, such as refills, do not trigger this event.

All trade requests issued by MQL programs are reflected in TRADE_TRANSACTION_REQUEST transactions, which allows analyzing their execution in a deferred way. This is especially important when using the function OrderSendAsync, which immediately returns control to the calling code, so the result is not known. At the same time, transactions are generated in the same way when using the synchronous OrderSend function.

In addition, using the TRADE_TRANSACTION_REQUEST transactions, you can analyze the user's trading actions from the terminal interface.
