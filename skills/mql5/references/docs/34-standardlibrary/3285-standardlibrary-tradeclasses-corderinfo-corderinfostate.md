# State

Gets the order state.

```
ENUM_ORDER_STATE  State() const

```

Return Value

Order state from [ENUM_ORDER_STATE](/en/docs/constants/tradingconstants/orderproperties#enum_order_state) enumeration.

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
