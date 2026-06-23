# Turning timer on and off: EventSetTimer/EventKillTimer

MQL5 allows you to enable or disable the standard timer to perform any scheduled actions. There are two functions for this: EventSetTimer and EventKillTimer.

bool EventSetTimer(int seconds)

The function indicates to the client terminal that for this Expert Advisor or indicator it is necessary to generate events from the timer with the specified frequency, which is set in seconds (parameter seconds).

The function returns a sign of success (true) or error (false). The error code can be obtained from _LastError.

In order to process timer events, an Expert Advisor or an indicator must have the [OnTimer](/en/book/applications/timer/timer_ontimer) function in its code. The first timer event will not occur immediately after the call of EventSetTimer, but after seconds seconds.

For each Expert Advisor or indicator that calls the EventSetTimer function, it creates its own, dedicated timer. The program will receive events only from it. Timers in different programs work independently.

Each interactive MQL program placed on a chart has a separate event queue where the events received for it are added. If there is already an event in the queue OnTimer or it is in processing state, then the new OnTimer event is not queued.

If the timer is no longer needed, it should be disabled with the EventKillTimer function.

void EventKillTimer(void)

The function stops the timer that was enabled before by the EventSetTimer function (or by [EventSetMillisecondTimer](/en/book/applications/timer/timer_event_set_millisecond), which we will discuss next). The function can also be called from the OnTimer handler. Thus, in particular, it is possible to perform a delayed single action.

The call of EventKillTimer in indicators does not clear the queue, so after it you can get the last residual OnTimer event.

When the MQL program terminates, the timer is forcibly destroyed if it was created but not disabled by the EventKillTimer function.

Each program can only set one timer. Therefore, if you want to call different parts of the algorithm at different intervals, you should enable a timer with a period that is the least common divisor of the required periods (in the limiting case, with a minimum period of 1 second), and in the OnTimer handler independently track larger periods. We'll look at an example of this approach in the next section.

MQL5 also allows to create timers with a period of less than 1 second: there is a function for this, [EventSetMillisecondTimer](/en/book/applications/timer/timer_event_set_millisecond).
