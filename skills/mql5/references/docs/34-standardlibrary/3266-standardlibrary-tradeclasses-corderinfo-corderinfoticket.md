# Ticket

Gets the ticket of an order.

```
ulong  Ticket() const

```

Return Value

Order ticket if successful, otherwise - [ULONG_MAX](/en/docs/constants/namedconstants/typeconstants).

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
