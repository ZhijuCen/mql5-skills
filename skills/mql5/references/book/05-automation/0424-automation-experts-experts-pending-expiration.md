# Pending order expiration dates

For pending orders, an important characteristic is their expiration mode. In the MQL5 API, the order validity period can be set in the type_time field of the special [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure when sending a trade request via the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function. Acceptable values are described in the ENUM_ORDER_TYPE_TIME enumeration.

| Identifier (Value) | Description |
| --- | --- |
| ORDER_TIME_GTC (0) | The order will be in the queue until it is canceled |
| ORDER_TIME_DAY (1) | The order will be valid only during the current trading day |
| ORDER_TIME_SPECIFIED (2) | The order will be valid until the expiration date |
| ORDER_TIME_SPECIFIED_DAY (3) | The order will be valid until 23:59:59 of the specified day (if this time does not fall within the trading session, the expiration will occur at the nearest next trading time) |

It should be noted that each financial instrument has two properties SYMBOL_EXPIRATION_MODE and SYMBOL_ORDER_GTC_MODE, which determine [Pending order expiration rules](/en/book/automation/symbols/symbols_expiration) for this instrument. When forming an order, an MQL program can choose one of the allowed modes. We will consider an example after studying the OrderSend function.
