# OrderDelete

Deletes the pending order.

```
bool  OrderDelete(
   ulong  ticket      // order ticket
   )

```

Parameters

ticket

[in]  Order ticket.

Return Value

true - successful check of the basic structures, otherwise - false.

Note

Successful completion of the OrderDelete(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of trade request (trade server return code) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode).
