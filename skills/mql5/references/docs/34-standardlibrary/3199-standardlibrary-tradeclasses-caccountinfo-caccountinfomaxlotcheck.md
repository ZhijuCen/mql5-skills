# MaxLotCheck

Gets the maximum possible volume of trade operation.

```
double  MaxLotCheck(
   const string        symbol,              // symbol
   ENUM_ORDER_TYPE     trade_operation,     // order type (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
   double              price,               // price
   double              percent=100          // percent of available margin (default is 100%)
   ) const

```

Parameters

symbol

[in]  Symbol for trade operation.

trade_operation

[in]  Type of trade operation from [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration.

price

[in]  Price of trade operation.

percent=100

[in]  Percent of available margin (in %) to be used for trade operation.

Return Value

Maximum possible volume of trade operation.
