# EventKillTimer

Specifies the client terminal that is necessary to stop the generation of events from [Timer](/en/docs/runtime/event_fire#timer).

```
void  EventKillTimer();

```

Return Value

No return value.

Note

Typically, this function must be called from a function [OnDeinit()](/en/docs/event_handlers/ondeinit), if the [EventSetTimer()](/en/docs/eventfunctions/eventsettimer) function has been called from [OnInit()](/en/docs/event_handlers/oninit). This function can also be called form the class destructor, if the EventSetTimer() function has been called in the [constructor](/en/docs/basis/types/classes#destructor) of this class.

Every Expert Advisor, as well as every indicator works with its own timer and receives events only from it. As soon as a mql5 program stops operating, the timer is destroyed forcibly if it was created but hasn't been disabled by the [EventKillTimer()](/en/docs/eventfunctions/eventkilltimer) function
