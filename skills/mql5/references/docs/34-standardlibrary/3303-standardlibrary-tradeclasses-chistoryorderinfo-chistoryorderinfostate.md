# State

Gets the order state.

```
ENUM_ORDER_STATE  State() const

```

Return Value

Order state from [ENUM_ORDER_STATE](/en/docs/constants/tradingconstants/orderproperties#enum_order_state) enumeration.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
