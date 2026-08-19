# SetTypeFillingBySymbol

Sets [filling](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling) type of the order according to the specified symbol settings.

```
bool  SetTypeFillingBySymbol(
   const string   symbol      // symbol name
   )

```

Parameters

symbol

[in]  Name of the symbol, in which [SYMBOL_FILLING_MODE](/en/docs/constants/environment_state/marketinfoconstants#symbol_filling_mode) contains allowed order filling policies.

Return Value

true – successful execution, false – failed to define the filling policy.

Note

If [SYMBOL_FILLING_FOK](/en/docs/constants/environment_state/marketinfoconstants#symbol_filling_mode) and [SYMBOL_FILLING_IOC](/en/docs/constants/environment_state/marketinfoconstants#symbol_filling_mode) filling policies are allowed for a symbol simultaneously, the [ORDER_FILLING_FOK](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling) value is set for the order.
