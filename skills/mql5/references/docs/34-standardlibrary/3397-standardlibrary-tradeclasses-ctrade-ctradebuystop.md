# BuyStop

Places the pending order of Buy Stop type (buy at the price higher than current market price) with specified parameters.

```
bool  BuyStop(
   double                volume,                       // order volume
   double                price,                        // order price
   const string          symbol=NULL,                  // symbol
   double                sl=0.0,                       // stop loss price
   double                tp=0.0,                       // take profit price
   ENUM_ORDER_TYPE_TIME  type_time=ORDER_TIME_GTC,     // order lifetime
   datetime              expiration=0,                 // order expiration time
   const string          comment=""                    // comment
   )

```

Parameters

volume

[in]  Requested order volume.

price

[in]  Order price.

symbol=[NULL](/en/docs/basis/types/void)

[in]  Order symbol. If the symbol isn't specified, the current symbol will be used.

sl=0.0

[in]  Stop Loss price.

tp=0.0

[in]  Take Profit price.

type_time=[ORDER_TIME_GTC](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time)

[in]  Order lifetime from [ENUM_ORDER_TYPE_TIME](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time) enumeration.

expiration=0

[in]  Order expiration time (used only if type_time=[ORDER_TIME_SPECIFIED](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time)).

comment=""

[in]  Order comment.

Return Value

true - successful check of the structures, otherwise - false.

Note

Successful completion of the BuyStop(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of trade request (trade server [return code](/en/docs/constants/errorswarnings/enum_trade_return_codes)) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode) and value returned by [ResultOrder()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultorder).
