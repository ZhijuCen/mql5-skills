# OrderProfitCheck

The function calculates the profit for the current account, based on the parameters passed. The function is used for pre-evaluation of the result of a trade operation. The value is returned in the account currency.

```
double  OrderProfitCheck(
   const string        symbol,              // symbol
   ENUM_ORDER_TYPE     trade_operation,     // order type (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
   double              volume,              // volume
   double              price_open,          // position open price
   double              price_close          // position close price
   ) const

```

Parameters

symbol

[in]  Symbol for trade operation.

trade_operation

[in] Type of trade operation from [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration.

volume

[in]  Volume of trade operation.

price_open

[in]  Open price.

price_close

[in]  Close price.

Return Value

If successful, it returns amount of profit or [EMPTY_VALUE](/en/docs/constants/namedconstants/typeconstants) in the case of error.
