# Time management in the tester: timer, Sleep, GMT

When developing Expert Advisors, it should be taken into account that the tester has some specifics of simulating the passage of time based on [generated ticks](/en/book/automation/tester/tester_ticks) and operation of time-related functions.

When testing, the local time returned by the TimeLocal function is always equal to the server time according to TimeTradeServer. In turn, server time is always equal to GMT TimeGMT. Thus, all these functions, when tested, give the same time. This is a technical feature of the platform, which occurs because it was decided not to store information about the server time locally, but always take it from the server, with which there may be no connection at a particular moment.

This feature creates difficulties in the implementation of strategies related to global time, in particular, with reference to news releases. In such cases, it is necessary to specify the time zone of quotes in the settings of the Expert Advisor being tested or to invent methods for auto-detection of the time zone (see section [Daylight saving time](/en/book/common/timing/timing_daylight_saving)).

Let's turn now to other functions for working with time.

As we know, it is possible to process timer events in MQL5. The [OnTimer](/en/book/applications/timer/timer_ontimer) handler is called regardless of the testing mode. This means that if testing is launched in the "Open prices only" mode on the H4 period, and a timer is set inside the Expert Advisor with a call coming every second, then the OnTick handler will be called once at the opening of each H4 bar and then, within the bar, the OnTimer handler will be called 14400 times (3600 seconds * 4 hours). The extent to which the Expert Advisor testing time will increase in this case depends on its algorithm.

Another function that influences the course of time within a program is the [Sleep](/en/book/common/timing/timing_sleep) function. It allows you to suspend the execution of an Expert Advisor for some time. This may be necessary when requesting any data that is not yet ready at the time of the request, and it is necessary to wait until it is ready.

It is important to understand that Sleep affects only the program that calls it and does not delay the testing process. In fact, when calling Sleep, the generated ticks are "played" within the specified delay, as a result of which pending orders, stop levels, etc. can be triggered. After calling Sleep, the time simulated in the tester is increased by the interval specified in the function parameter.

Later, in the section on [testing multi-currency Expert Advisors](/en/book/automation/tester/tester_multicurrency_sync), we will show how you can use the timer and the Sleep function to synchronize bars.
