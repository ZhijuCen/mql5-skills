# Debugging and profiling

The MetaTrader 5 tester is useful not only for testing the profitability of trading strategies but also for debugging MQL programs. Error detection is primarily associated with the ability to reproduce the problem situation. If we could only run MQL programs online, debugging and analyzing source code execution would require an unrealistic amount of effort. However, the tester allows you to "run" programs on arbitrary sections of history, change account settings and trading symbols.

Recall that in MetaEditor there are 2 commands in the Debug menu:

- Start/Continue on real data (F5)
- Start/Continue on historical data (Ctrl-F5)

In both cases, the program is promptly recompiled in a special way with additional debugging information in the ex5 file and then launched directly in the terminal (first option) or in the tester (second option).

When debugging in the tester, you can use both quick (background) mode and visual mode. This setting is provided in the Setting dialog on the Debug/Profile tab: enable or disable the flag Use visual mode for debugging on history. The environment and settings of the program being debugged can be taken directly from the tester (as they were last set for this program) or in the same dialog in the input fields under the flag Use specified settings (for them to work, the flag must be enabled).

You can pre-set breakpoints (F9) on operators in the part where something is supposedly starting to work wrong. The tester will pause the process when it reaches the specified location in the source code.

Please note that in the tester, the number of history bars loaded at startup depends on different factors (including timeframe, day number within a year, etc.) and can vary significantly. If necessary, move the start time of the test back in time.

In addition to obvious bugs that cause the program to stop or explicitly malfunction, there is a class of subtle bugs that negatively affect performance. As a rule, they are not so obvious, but turn into problems as the amount of data processed increases, for example, on trading accounts with a very long history, or on charts with a large number of markup objects.

To find "bottlenecks" in terms of performance, the debugger provides a source code profiling mechanism. It can also be performed online or in the tester, and the latter is especially valuable, as it allows you to significantly compress the time. The corresponding commands are also available in the debug menu.

- Start profiling on real data
- Start profiling on historical data

For profiling, the program is also pre-compiled with special settings, so don't forget to compile the program again in normal mode after debugging or profiling is complete (especially if you plan to send it to a client or upload it to the MQL5 Market).

As a result of profiling in MetaEditor, you will receive time statistics of your code execution, broken down by lines and functions (methods). As a result, it will become clear what exactly slows down the program. The next stage of development is usually source code refactoring, i.e., its rewriting using improved algorithms, data structures, or other principles of the constructive organization of modules (components). Unfortunately, a significant part of the time in programming is spent on rewriting existing code, finding and fixing errors.

The program itself can, if necessary, find out its mode of operation and adapt its behavior to the environment (for example, when run in the tester, it will not try to download data from the Internet, since this feature is disabled, but will read them from a certain file).

At the compilation stage, the debug and production versions of the program can be formed differently due to preprocessor macros [_DEBUG and _RELEASE](/en/book/basis/preprocessor/preprocessor_predefined).

At the program execution stage, its modes can be distinguished using the [MQLInfoInteger](/en/book/common/environment/env_mode) function options.

The following table summarizes all available combinations that affect runtime specifics.

| Runtime\ flags | MQL_DEBUG | MQL_PROFILER | Normal(release) |
| --- | --- | --- | --- |
| Online | + | + | + |
| Tester 
 (MQL_TESTER) | + | + | + |
| Tester 
 ( MQL_TESTER+MQL_VISUAL_MODE ) | + | - | + |

Profiling in the tester is only possible without the visual mode, so you should measure operations with charts and objects online.

Debugging is not allowed during the optimization process, including special handlers OnTesterInit, OnTesterDeinit, and OnTesterPass. If you need to check their performance, consider calling their code under other conditions.
