# TypeTime

Gets the type of order at the time of the expiration.

```
ENUM_ORDER_TYPE_TIME  TypeTime() const

```

Return Value

Type of order at the time of the expiration from [ENUM_ORDER_TYPE_TIME](/en/docs/constants/tradingconstants/orderproperties) enumeration.

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
