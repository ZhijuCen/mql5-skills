# TypeFilling

Gets the type of order execution by remainder.

```
ENUM_ORDER_TYPE_FILLING  TypeFilling() const

```

Return Value

Type of order execution by remainder from [ENUM_ORDER_TYPE_FILLING](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling) enumeration.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
