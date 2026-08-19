# PositionCloseBy

Closes a position with the specified ticket by an opposite position.

```
bool  PositionCloseBy(
   const ulong   ticket,        // position ticket
   const ulong   ticket_by      // opposite position ticket
   )

```

Parameters

ticket

[in]  Ticket of the closed position.

ticket_by

[in]  Ticket of the opposite position used for closing.

Returned value

true - the basic check of structures is successful, otherwise - false.

Note

A successful completion of the PositionCloseBy(...) method does not always mean a successful execution of a trading operation. You should call the [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode) method to check the result of a trade request (trade server return code).
