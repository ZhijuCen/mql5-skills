# SignalSubscribe

Subscribes to the trading signal.

```
bool  SignalSubscribe(
   long     signal_id     // signal id 
   );

```

Parameters

signal_id

[in]  Signal identifier.

Return Value

Returns true if subscription was successful, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).
