# High-precision timer: EventSetMillisecondTimer

If your program requires the timer to trigger more frequently than 1 second, instead of EventSetTimer use the EventSetMillisecondTimer function.

Timers with different units cannot be started at the same time: either one function or the other must be used. The type of timer actually running is determined by which function was called later. All features inherent to [standard timer](/en/book/applications/timer/timer_event_set) remain valid for the high-precision timer.

bool EventSetMillisecondTimer(int milliseconds)

The function indicates to the client terminal that it is necessary to generate timer events for this Expert Advisor or indicator with a frequency of less than one second. The periodicity is set in milliseconds (parameter milliseconds).

The function returns a sign of success (true) or error (false).

When working in the strategy tester, keep in mind that the shorter the timer period, the longer the testing will take, as the number of calls to the timer event handler increases.

During normal operation, timer events are generated no more than once every 10-16 milliseconds, which is due to hardware limitations.

To demonstrate how to work with the millisecond timer, let's expand the indicator example MultipleTimers.mq5. Since the activation of the global timer is left to the application program, we can easily change the type of the timer, leaving the logical timer classes unchanged. The only difference will be that their multipliers will be applied to the base period in milliseconds that we will specify in the EventSetMillisecondTimer function.

To select the timer type, we will describe the enumeration and add a new input variable.

```
enum TIMER_TYPE
{
   Seconds,
   Milliseconds
};
   
input TIMER_TYPE TimerType = Seconds;

```

By default, we use a second timer. In OnInit, start the timer of the required type.

```
void OnInit()
{
   Print(__FUNCSIG__, " ", BaseTimerPeriod, " ", EnumToString(TimerType));
   if(TimerType == Seconds)
   {
      EventSetTimer(BaseTimerPeriod);
   }
   else
   {
      EventSetMillisecondTimer(BaseTimerPeriod);
   }
}

```

Let's see what will be displayed in the log when choosing a millisecond timer.

```
                                               // time ms
17:27:54.483  void OnInit() 1 Milliseconds        |             
17:27:54.514  void MyCountableTimer::notify()2 0    |           +31
17:27:54.545  bool OnTimer3()                        |          +31
17:27:54.561  void MyCountableTimer::notify()2 1      |         +16
17:27:54.561  void MyCountableTimer::notify()4 0      |
17:27:54.577  bool OnTimer5()                          |        +16
17:27:54.608  void MyCountableTimer::notify()2 2        |       +31
17:27:54.608  bool OnTimer3()                           |
17:27:54.608  void MySuspendedTimer::notify()1 0        |
17:27:54.623  void MySuspendedTimer::notify()1 1         |      +15
17:27:54.655  void MyCountableTimer::notify()2 3          |     +32
17:27:54.655  void MyCountableTimer::notify()4 1          |
17:27:54.655  void MySuspendedTimer::notify()1 2          |
17:27:54.670  bool OnTimer3()                              |    +15
17:27:54.670  void MySuspendedTimer::notify()1 3           |
17:27:54.686  void MyCountableTimer::notify()2 4            |   +16
17:27:54.686  void MySuspendedTimer::notify()1 4            |
17:27:54.686  Forcing all timers to stop                    |

```

The sequence of event generation is exactly the same as what we saw for the second timer, but everything happens much faster, almost instantly.

Due to the fact that the accuracy of the system timer is limited to a couple of tens of milliseconds, the real interval between events significantly exceeds the unattainable small 1 millisecond. In addition, there is a spread of the size of one "step". Thus, even when using a millisecond timer, it is desirable not to stick to periods less than a few tens of milliseconds.
