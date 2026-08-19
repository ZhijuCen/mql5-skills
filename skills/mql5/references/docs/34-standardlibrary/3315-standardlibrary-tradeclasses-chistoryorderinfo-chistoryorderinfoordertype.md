# OrderType

Gets the order type.

```
ENUM_ORDER_TYPE  OrderType() const

```

Return Value

Order type from [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
