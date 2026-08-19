# CopyTicksRange

The function receives ticks in the [MqlTick](/en/docs/constants/structures/mqltick) format within the specified date range to ticks_array. Indexing goes from the past to the present meaning that a tick with the index 0 is the oldest one in the array. For tick analysis, check the flags field, which shows what exactly has changed.

```
int  CopyTicksRange(
   const string     symbol_name,           // symbol name
   MqlTick&         ticks_array[],         // tick receiving array
   uint             flags=COPY_TICKS_ALL,  // flag that defines the type of the ticks that are received
   ulong            from_msc=0,            // date, starting from which ticks are requested
   ulong            to_msc=0               // date, up to which ticks are requested
   );

```

Parameters

symbol_name

[in]  Symbol.

ticks_array

[out]  [MqlTick](/en/docs/constants/structures/mqltick) static or dynamic array for receiving ticks. If the static array cannot hold all the ticks from the requested time interval, the maximum possible amount of ticks is received. In this case, the function generates the error [ERR_HISTORY_SMALL_BUFFER](/en/docs/constants/errorswarnings/errorcodes) (4407) .

flags

[in]  A flag to define the type of the requested ticks. COPY_TICKS_INFO – ticks with Bid and/or Ask changes, COPY_TICKS_TRADE – ticks with changes in Last and Volume, COPY_TICKS_ALL – all ticks. For any type of request, the values of the previous tick are added to the remaining fields of the MqlTick structure.

from_msc

[in]   The date, from which you want to request ticks. In milliseconds since 1970.01.01. If the from_msc parameter is not specified, ticks from the beginning of the history are sent. Ticks with the time >= from_msc are sent.

to_msc

[in]   The date, up to which you want to request ticks. In milliseconds since 01.01.1970. Ticks with the time <= to_msc are sent. If the to_msc parameter is not specified, all ticks up to the end of the history are sent.

Return Value

The number of copied tick or -1 in case of an error. [GetLastError()](/en/docs/check/getlasterror) is able to return the following errors:

- ERR_HISTORY_TIMEOUT – ticks synchronization waiting time is up, the function has sent all it had.
- ERR_HISTORY_SMALL_BUFFER – static buffer is too small. Only the amount the array can store has been sent.
- ERR_NOT_ENOUGH_MEMORY – insufficient memory for receiving a history from the specified range to the dynamic tick array. Failed to allocate enough memory for the tick array.

Note

The CopyTicksRange() function is used for requesting ticks strictly from a specified range, for example, from a certain day in history. At the same time, CopyTicks() allows specifying only a start date, for example – receive all ticks from the beginning of the month till the current moment.

See also

[SymbolInfoTick](/en/docs/marketinformation/symbolinfotick), [Structure for Current Prices](/en/docs/constants/structures/mqltick), [OnTick](/en/docs/event_handlers/ontick), [CopyTicks](/en/docs/series/copyticks)
