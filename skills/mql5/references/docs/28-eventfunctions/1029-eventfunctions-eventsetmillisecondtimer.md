# EventSetMillisecondTimer

The function indicates to the client terminal that [timer](/en/docs/runtime/event_fire#timer) events should be generated at intervals less than one second for this Expert Advisor or indicator.

```
bool  EventSetMillisecondTimer(
   int  milliseconds      // number of milliseconds
   );

```

Parameters

milliseconds

[in]  Number of milliseconds defining the frequency of timer events.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

This feature is designed for the cases when high-resolution timer is required. In other words, timer events should be received more frequently than once per second. If a conventional timer with the period of more than one second is enough for you, use [EventSetTimer()](/en/docs/eventfunctions/eventsettimer).

In general, when the timer period is reduced, the testing time is increased, as the handler of timer events is called more often. When working in real-time mode, timer events are generated no more than 1 time in 10-16 milliseconds due to hardware limitations.

Usually, this function should be called from [OnInit()](/en/docs/event_handlers/oninit) function or in class [constructor](/en/docs/basis/types/classes#constructor). To handle events coming from the timer, an Expert Advisor or an indicator should have [OnTimer()](/en/docs/event_handlers/ontimer) function.

Each Expert Advisor and each indicator work with its own timer receiving events solely from this timer. During mql5 application shutdown, the timer is forcibly destroyed in case it has been created but has not been disabled by [EventKillTimer()](/en/docs/eventfunctions/eventkilltimer) function.

Only one timer can be launched for each program. Each mql5 application and chart have their own queue of events where all newly arrived events are placed. If the queue already contains [Timer](/en/docs/runtime/event_fire#timer) event or this event is in the processing stage, then the new Timer event is not added to mql5 application queue.
