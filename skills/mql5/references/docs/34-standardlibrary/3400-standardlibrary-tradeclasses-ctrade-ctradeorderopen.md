# OrderOpen

Places the pending order with set parameters.

```
bool  OrderOpen(
   const string          symbol,          // symbol
   ENUM_ORDER_TYPE       order_type,      // order type
   double                volume,          // order volume
   double                limit_price,     // StopLimit price
   double                price,           // execution price
   double                sl,              // Stop Loss price
   double                tp,              // Take Profit price
   ENUM_ORDER_TYPE_TIME  type_time,       // type by expiration
   datetime              expiration,      // expiration
   const string          comment=""       // comment
   )

```

Parameters

symbol

[in] Name of trade instrument.

order_type

[in]  Type of order trade operation from [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration.

volume

[in] Requested order volume.

limit_price

[in] Price at which the StopLimit order will be placed.

price

[in] Price at which the order must be executed.

sl

[in] Price at which the Stop Loss will trigger.

tp

[in] Price at which the Take Profit will trigger.

type_time

[in]  Order type by execution from [ENUM_ORDER_TYPE_TIME](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time) enumeration.

expiration

[in] Expiration date of pending order.

comment=""

[in]  Order comment.

Return Value

true - successful check of the basic structures, otherwise - false.

Note

Successful completion of the OrderSend(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of a trade request (trade server return code) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode) and value returned by [ResultOrder()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultorder).
