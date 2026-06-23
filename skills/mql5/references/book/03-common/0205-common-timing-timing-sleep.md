# Pausing a Program

As we saw earlier in the examples, programs sometimes need to repeat certain actions periodically, either on a simple schedule or after previous attempts have failed. When this is done in a loop, it is recommended to pause the program regularly to prevent too frequent requests and unnecessary load on the CPU, as well as to allow time for external "players" to do their work (for example, if we are waiting for data from another program, loading the history of quotes, etc.).

For this purpose, MQL5 provides the Sleep function. This section gives its formal description, and an example will be given in the next section, along with the functions for [time interval measurements](/en/book/common/timing/timing_count).

void Sleep(int milliseconds)

The function pauses the execution of the MQL program for the specified number of milliseconds. After their expiration, the instructions following the Sleep call will continue to be executed.

It makes sense to use the function in the first place in [scripts](/en/book/applications/script_service/scripts) and [services](/en/book/applications/script_service/services) because these types of programs have no other way to wait.

In Expert Advisors and indicators, it is recommended to use [timers](/en/book/applications/timer) and the [OnTimer](/en/book/applications/timer/timer_ontimer) event. In this scheme, the MQL program returns control to the terminal and will be called after a specified interval.

Moreover, the Sleep function cannot be called from indicators, since they are executed in terminal interface threads, the suspension of which will affect the rendering of charts.

If the user interrupts the MQL program from the terminal interface while it is waiting for the call to complete Sleep, the exit from the function occurs immediately (within 100ms), i.e., the pause ends ahead of schedule. This will set the stop flag _StopFlag (also available via the function [IsStopped](/en/book/common/environment/env_stop)), and the program should stop execution as quickly and correctly as possible.
