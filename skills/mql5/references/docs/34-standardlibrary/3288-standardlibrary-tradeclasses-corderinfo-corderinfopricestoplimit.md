# PriceStopLimit

Gets the price of a pending order.

```
double  PriceStopLimit() const

```

Return Value

Pending order price.

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
