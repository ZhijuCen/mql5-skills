# SetAsyncMode

Sets asynchronous mode for trade operations.

```
void  SetAsyncMode(
   bool  mode      // asynchronous mode flag
   )

```

Parameters

mode

[in]  Asynchronous mode flag.

Return Value

None.

Note

This mode is used for asynchronous (without waiting for the trade server's response to a sent request) trade operations (see [OrderSendAsync](/en/docs/trading/ordersendasync)).
