# Request sending result: MqlTradeResult structure

In response to a trade request executed by the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) or [OrderSendAsync](/en/book/automation/experts/experts_ordersend_ordersendasync) functions, which we'll cover in the next section, the server returns the request processing results. For this purpose, a special predefined structure is used MqlTradeResult.

```
struct MqlTradeResult 
{ 
   uint     retcode;          // Operation result code 
   ulong    deal;             // Transaction ticket, if it is completed 
   ulong    order;            // Order ticket, if it is placed 
   double   volume;           // Trade volume confirmed by the broker 
   double   price;            // Trade price confirmed by the broker 
   double   bid;              // Current market bid price 
   double   ask;              // Current market offer price 
   string   comment;          // Broker's comment on the operation 
   uint     request_id;       // Request identifier, set by the terminal when sending  
   uint     retcode_external; // Response code of the external trading system 
};

```

The following table describes its fields.

| Field | Description |
| --- | --- |
| retcode | Trade server return code |
| deal | Deal ticket if it is performed (during the  TRADE_ACTION_DEAL  trading operation) |
| order | Order ticket if it is placed (during the  TRADE_ACTION_PENDING  trading operation) |
| volume | Trade volume confirmed by the broker (depends on the order  execution modes ) |
| price | The price in the deal confirmed by the broker (depends on the  deviation  field in the  trade request ,  execution mode , and the trading operation) |
| bid | Current market bid price |
| ask | Current market ask price |
| comment | Broker's comment on the trade (by default, it is filled in with the decryption of the trade server return code) |
| request_id | Request ID which is set by the terminal when sending it to the trade server |
| retcode_external | Error code returned by the external trading system |

As we will see below when conducting trading operations, a variable of type MqlTradeResult is passed as the second parameter by reference in the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) or [OrderSendAsync](/en/book/automation/experts/experts_ordersend_ordersendasync) function. It returns the result.

When sending a trade request to the server, the terminal sets the request_id identifier to a unique value. This is necessary for the analysis of subsequent trading events, which is required if an asynchronous function OrderSendAsync is used. This identifier allows you to associate the sent request with the result of its processing passed to the [OnTradeTransaction](/en/book/automation/experts/experts_ontradetransaction) event handler.

The presence and types of errors in the retcode_external field depend on the broker and the external trading system into which trading operations are forwarded.

Request results are analyzed in different ways, depending on the trading operations and the way they are sent. We will deal with this in subsequent sections on specific actions: market buy and sell, placing and deleting pending orders, and modifying and closing positions.
