# TypeTime

Gets the type of order at the time of the expiration.

```
ENUM_ORDER_TYPE_TIME  TypeTime() const

```

Return Value

Type of order at the time of the expiration from [ENUM_ORDER_TYPE_TIME](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_time) enumeration.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
