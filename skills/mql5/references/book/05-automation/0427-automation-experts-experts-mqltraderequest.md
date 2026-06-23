# MqlTradeRequest structure

MQL5 API trading functions, in particular [OrderCheck](/en/book/automation/experts/experts_ordercheck) and [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync), operate on several built-in structures. Therefore, we will have to consider these structures before moving on to the functions themselves.

Let's start with the MqlTradeRequest structure which contains all the fields required for executing trades.

```
struct MqlTradeRequest 
{ 
   ENUM_TRADE_REQUEST_ACTIONS action;       // Type of action to perform 
   ulong                      magic;        // Unique Expert Advisor number 
   ulong                      order;        // Order ticket 
   string                     symbol;       // Name of the trading instrument 
   double                     volume;       // Requested trade volume in lots 
   double                     price;        // Price  
   double                     stoplimit;    // StopLimit order level 
   double                     sl;           // Stop Loss order level 
   double                     tp;           // Take Profit order level 
   ulong                      deviation;    // Maximum deviation from the given price
   ENUM_ORDER_TYPE            type;         // Order type 
   ENUM_ORDER_TYPE_FILLING    type_filling; // Order type by execution 
   ENUM_ORDER_TYPE_TIME       type_time;    // Order type by duration 
   datetime                   expiration;   // Order expiration date 
   string                     comment;      // Comment to the order 
   ulong                      position;     // Position ticket 
   ulong                      position_by;  // Opposite position ticket 
};

```

You should not be afraid of a large number of fields: the structure is designed to serve absolutely all possible types of trade requests, however, in each specific case, only a few fields are usually used.

Before filling in the fields, it is recommended to nullify the structure either by explicit initialization in its definition or by calling the [ZeroMemory](/en/book/common/arrays/zero_memory) function.

```
   MqlTradeRequest request = {};
   ...
   ZeroMemory(request);

```

This way it will avoid potential errors and side effects from passing random values to the API functions in those fields that were not explicitly assigned.

The following table provides a brief description of the fields. We will see how to fill them when describing trading operations.

| Field | Description |
| --- | --- |
| action | Trading operation type from  ENUM_TRADE_REQUEST_ACTIONS |
| magic | Expert ID (optional) |
| order | Pending order ticket for which modification is requested |
| symbol | Trading instrument name |
| volume | Requested trade volume in lots |
| price | The price at which the order must be executed |
| stoplimit | The price where a limit order will be placed when the ORDER_TYPE_BUY_STOP_LIMIT and ORDER_TYPE_SELL_STOP_LIMIT orders are activated |
| sl | Price at which  Stop Loss  order will be triggered when the price moves in an unfavorable direction |
| tp | Price at which  Take Profit  order will be triggered when the price moves in a favorable direction |
| deviation | Maximum acceptable deviation from the asked price, in points |
| type | Order type from  ENUM_ORDER_TYPE |
| type_filling | Order filling type from  ENUM_ORDER_TYPE_FILLING |
| type_time | Pending order expiration type from  ENUM_ORDER_TYPE_TIME |
| expiration | Pending order expiration date |
| comment | Comment to the order |
| position | Position ticket |
| position_by | Opposite position ticket for the TRADE_ACTION_CLOSE_BY operation |

To send orders for trading operations, it is necessary to fill in a different set of fields, depending on the nature of the operation. Some fields are required, and some are optional (can be omitted when filling out). Next, we'll take a closer look at the field requirements in the context of specific actions.

The program can check a formed MqlTradeRequest structure for correctness using the [OrderCheck](/en/book/automation/experts/experts_ordercheck) function or send it to the server using the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function. If successful, the requested operation will be performed.

The action field is the only one required for all trading activities.

A unique number in the magic field is usually indicated only for market buy/sell requests or when creating a new pending order. This leads to the subsequent marking of completed transactions and positions with this number, which allows for organizing the analytical processing of trading actions. When modifying the price levels of a position or pending orders, as well as deleting them, this field has no effect.

When manually performing trading operations from the MetaTrader 5 interface, the magic identifier cannot be set, and therefore it is equal to zero. This provides a popular but not entirely reliable way to distinguish between manual and automated trading when analyzing history. In fact, Expert Advisors can also use a zero identifier. Therefore, to find out who and how performed specific trading actions, use the corresponding properties of orders ([ORDER_REASON](/en/book/automation/experts/experts_order_properties)), deals ([DEAL_REASON](/en/book/automation/experts/experts_deal_properties)), and positions ([POSITION_REASON](/en/book/automation/experts/experts_position_properties)).

Each Expert Advisor can set its own unique ID or even use several IDs for different purposes (broken down by trading strategies, signals, etc.). The magic number of the position corresponds to the magic number of the last deal involved in the formation of the position.

Symbol name in the symbol field is important only for opening or increasing positions, as well as when placing pending orders. In cases of modifying and closing orders and positions, it will be ignored, but there is a small exception here. Since only one position can exist on netting accounts for each symbol, the symbol field can be used to identify a position in a request to change its protective price levels (Stop Loss and Take Profit).

The volume field is used in the same way: it is needed in immediate buy/sell orders or when creating pending orders. It should be taken into account that the actual volume in the operation will depend on the [execution mode](/en/book/automation/experts/experts_execution_filling) and may differ from what is requested.

The price field also has some limitations: when sending market orders (TRADE_ACTION_DEAL in the action) for instruments with execution mode SYMBOL_TRADE_EXECUTION_MARKET or SYMBOL_TRADE_EXECUTION_EXCHANGE, this field is ignored.

The stoplimit field makes sense only when setting stop-limit orders, i.e., when the type field contains ORDER_TYPE_BUY_STOP_LIMIT or ORDER_TYPE_SELL_STOP_LIMIT. It specifies the price at which a pending limit order will be placed when the price reaches the price value (this fact is tracked by the MetaTrader 5 server, and until this moment a pending order is not displayed in the trading system).

When placing pending orders, their expiration rules are set in a pair of fields: type_time and expiration. The latter contains a value of type datetime, which is taken into account only if type_time is equal to ORDER_TIME_SPECIFIED or ORDER_TIME_SPECIFIED_DAY.

Finally, the last couple of fields are related to the identification of positions in queries. Each new position created on the basis of orders (manually or programmatically) gets a ticket assigned by the system, a unique number. As a rule, it corresponds to the ticket of the order, as a result of which the position is opened, but may change subject to service operations on the server, for example, accrual of swaps by reopening a position.

We will talk about obtaining the properties of positions, deals, and orders in separate sections. Here, for now, it is important for us that the position field should be filled in when changing and closing a position in order to unambiguously identify it. In theory, on netting accounts, it is enough to indicate the position symbol in the symbol field, but for the unification of algorithms, it is better to leave the position field in work.

The position_by field is used for closing opposite positions (TRADE_ACTION_CLOSE_BY). It should indicate a position opened for the same symbol but in the opposite direction in relation to position (this is only possible on [hedging accounts](/en/book/automation/account/account_netting_hedge)).

The deviation field affects the execution of market orders only in the Instant Execution and Request Execution modes.

Examples of filling in the structure for trading operations of each type will be given in the relevant sections.
