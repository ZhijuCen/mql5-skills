# The main function of scripts and services: OnStart

Utility programs — scripts and services — are executed in the terminal by calling their single event handling function OnStart.

void OnStart()

The function has no parameters and does not return any value. It only serves as an entry point to the application program from the terminal side.

Scripts are intended, as a rule, for one-time actions performed on a chart (later we will study all the possibilities provided by the chart API). For example, a script can be used to set up a grid of orders or, conversely, to close all profitable open positions, to automatically apply markup with graphical objects, or to temporarily hide all objects.

In scripts, you can use constant actions wrapped in an infinite loop, in which, as mentioned earlier, you should always check the stop sign ([_StopFlag](/en/book/common/environment/env_stop)) and periodically release the processor ([Sleep](/en/book/common/timing/timing_sleep)). It should be remembered here that when you turn off and on the terminal, the script will have to be run again.

Therefore, for such constant activity, if it is not directly related to the schedule, it is better to use the service. The standard technique in the implementation of the service is just an "infinite" loop.

In the previous parts of the book, almost all examples were implemented as scripts. An example of a service is the program GlobalsWithCondition.mq5 from the section [Synchronizing programs using global variables](/en/book/common/globals/globals_condition). We will see another example in the next section about stopping Expert Advisors and scripts using the ExpertRemove function.
