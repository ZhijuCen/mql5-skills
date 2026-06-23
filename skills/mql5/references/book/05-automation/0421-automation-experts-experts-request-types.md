# Types of trading operations

Trading in MQL5 is implemented by sending orders using the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function. We will study it in one of the following sections because its description requires you to first become familiar with several concepts.

The very first new concept will be the trading operation type. Each trade request contains an indication of the type of the requested trade and allows you to perform actions such as opening and closing positions, as well as placing, modifying, and deleting pending orders. All types of trading operations are described in the ENUM_TRADE_REQUEST_ACTIONS enumeration.

| Identifier | Description |
| --- | --- |
| TRADE_ACTION_DEAL | Place a trading order for an immediate trade with the specified parameters (place a market order) |
| TRADE_ACTION_PENDING | Place a trading order to execute a trade under the specified conditions (pending order) |
| TRADE_ACTION_SLTP | Change the  Stop Loss  and  Take Profit  values of an open position |
| TRADE_ACTION_MODIFY | Change the parameters of a previously placed order |
| TRADE_ACTION_REMOVE | Delete a previously placed pending order |
| TRADE_ACTION_CLOSE_BY | Close a position with an opposite one |

When requesting TRADE_ACTION_DEAL and TRADE_ACTION_PENDING, the program will need to specify a specific order type. This is another important concept that has its own reflection in the MQL5 API, and we will consider it in the next section.
