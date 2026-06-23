# EventSetTimer

The function indicates to the client terminal, that for this indicator or Expert Advisor, events from the [timer](/en/docs/runtime/event_fire#timer) must be generated with the specified periodicity.

```
bool  EventSetTimer(
   int  seconds      // number of seconds
   );

```

Parameters

seconds

[in] Number of seconds that determine the frequency of the timer event occurrence.

Return Value

In case of success returns true, otherwise false. In order to get an [error code](/en/docs/constants/errorswarnings/errorcodes), the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

Normally, this function must be called from the [OnInit()](/en/docs/event_handlers/oninit) function or from a class [constructor](/en/docs/basis/types/classes#constructor). In order to handle events coming from the timer, the Expert Advisor must have the [OnTimer()](/en/docs/event_handlers/ontimer) function.

Every Expert Advisor, as well as every indicator works with its own timer and receives events only from it. As soon as a mql5 program stops operating, the timer is destroyed forcibly if it was created but hasn't been disabled by the [EventKillTimer()](/en/docs/eventfunctions/eventkilltimer) function.

For each program no more than one timer can be run. Each mql5 program and each chart has its own queue of events, in which all the newly received events are placed. If the [Timer](/en/docs/runtime/event_fire#timer) event is present in the queue or is being processed, the new Timer event will not be placed in the queue of the mql5 program.
