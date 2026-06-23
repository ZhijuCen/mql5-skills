# Terminal and program operating modes

The MetaTrader 5 environment provides a solution to various tasks at the intersection of trading and programming, which necessitates several modes of operation of both the terminal itself and a specific program.

Using the MQL5 API, you can distinguish between regular online activity and backtesting, between source code debugging (in order to identify potential errors) and performance analysis (search for bottlenecks in the code), as well as between a local copy of the terminal and the cloud one (MetaTrader VPS).

The modes are described by flags, each of which contains a value of a boolean type: true or false.

| Identifier | Description |
| --- | --- |
| MQL_DEBUG | The program is running in debug mode |
| MQL_PROFILER | The program works in code profiling mode |
| MQL_TESTER | The program works in the tester |
| MQL_FORWARD | The program is executed in the process of forward testing |
| MQL_OPTIMIZATION | The program is running in the optimization process |
| MQL_VISUAL_MODE | The program is running in visual testing mode |
| MQL_FRAME_MODE | The Expert Advisor is executed on the chart in the mode of collecting frames of optimization results |
| TERMINAL_VPS | The terminal works on a virtual server MetaTrader Virtual Hosting (MetaTrader VPS) |

The MQL_FORWARD, MQL_OPTIMIZATION, and MQL_VISUAL_MODE flags imply the presence of the MQL_TESTER flag set.

Some pairwise combinations of flags are mutually exclusive, i.e., such flags cannot be enabled at the same time.

In particular, the presence of MQL_FRAME_MODE excludes MQL_TESTER, and vice versa. MQL_OPTIMIZATION excludes MQL_VISUAL_MODE, and MQL_PROFILER excludes MQL_DEBUG.

We will study all the flags related to testing (MQL_TESTER, MQL_VISUAL_MODE) in the sections devoted to [Expert Advisors](/en/book/automation/tester/tester_debug_profile) and, in part, to [indicators](/en/book/applications/indicators_make/indicators_test). Everything related to Expert Advisor optimization (MQL_OPTIMIZATION, MQL_FORWARD, MQL_FRAME_MODE) will be covered in a [separate section](/en/book/automation/tester).

Now let's get acquainted with the principles of reading flags using the example of debugging (MQL_DEBUG) and profiling (MQL_PROFILER) modes. At the same time, let's recall how these modes are activated from the MetaEditor (for details, see the documentation, in sections [Debugging](https://www.metatrader5.com/en/metaeditor/help/development/debug) and [Profiling](https://www.metatrader5.com/en/metaeditor/help/development/profiling)).

We will use the EnvMode.mq5 script.

```
void OnStart()
{
   PRTF(MQLInfoInteger(MQL_TESTER));
   PRTF(MQLInfoInteger(MQL_DEBUG));
   PRTF(MQLInfoInteger(MQL_PROFILER));
   PRTF(MQLInfoInteger(MQL_VISUAL_MODE));
   PRTF(MQLInfoInteger(MQL_OPTIMIZATION));
   PRTF(MQLInfoInteger(MQL_FORWARD));
   PRTF(MQLInfoInteger(MQL_FRAME_MODE));
}

```

Before running the program, you should check the debugging/profiling settings. To do this, in MetaEditor, run the command Tools -> Options and check the field values in the Debugging/Profiling tab. If the option Use specified settings is enabled, then it is the values of the underlying fields that will affect the financial instrument chart and the timeframe on which the program will be launched. If the option is disabled, the first financial instrument in Market Watch and the H1 timeframe will be used.

At this stage, the choice of option is not critical.

After preparations, run the script using the command Debug -> Start on Real Data (F5). Since the script only prints the requested properties to the log (and we don't need breakpoints in it), its execution will be instantaneous. If step-by-step debugging is needed, we could put a breakpoint (F9) on any statement in the source code, and the script execution would freeze there for any period we need, making it possible to study the contents of all variables in MetaEditor, and also move line by line (F10) along the algorithm.

In the MetaTrader 5 log (Experts tab), we will see the following:

```
MQLInfoInteger(MQL_TESTER)=0 / ok
MQLInfoInteger(MQL_DEBUG)=1 / ok
MQLInfoInteger(MQL_PROFILER)=0 / ok
MQLInfoInteger(MQL_VISUAL_MODE)=0 / ok
MQLInfoInteger(MQL_OPTIMIZATION)=0 / ok
MQLInfoInteger(MQL_FORWARD)=0 / ok
MQLInfoInteger(MQL_FRAME_MODE)=0 / ok

```

Flags of all modes are reset, except for MQL_DEBUG.

Now let's run the same script from the Navigator in MetaTrader 5 (just drag it with the mouse to any chart). We will get an almost identical set of flags, but this time MQL_DEBUG will be equal to 0 (because the program was executed in a regular way, and not under a debugger).

Please note that the launch of the program with debugging is preceded by its recompilation in a special mode when service information permitting debugging is added to the executable file. Such binary file is larger and slower than usual. Therefore, after debugging is completed, before being used in real trading, transferred to the customer, or uploaded to the Market, the program should be recompiled with the File -> Compile (F7) command.  

   

The compilation method does not directly affect the MQL_DEBUG property. The debug version of the program, as we can see, can be launched in the terminal without a debugger, and MQL_DEBUG will be reset in this case. Two built-in macros allow you to determine the compilation method: _DEBUG and _RELEASE (see section [Predefined Constants](/en/book/basis/preprocessor/preprocessor_predefined)). They are constants, not functions, because this property is "hardwired" into the program at compile time, and cannot then be changed (unlike the runtime environment).

Now let's execute in MetaEditor the command Debug -> Start Profiling on Real Data. Of course, there is no particular point in profiling such a simple script, but our task now is to make sure that the appropriate flag is turned on in the environment properties. Indeed, opposite the MQL_PROFILER there is 1 now.

```
MQLInfoInteger(MQL_TESTER)=0 / ok
MQLInfoInteger(MQL_DEBUG)=0 / ok
MQLInfoInteger(MQL_PROFILER)=1 / ok
...

```

The launch of the program with profiling is also preceded by its recompilation in another special mode, which adds other service information to the binary file that is necessary to measure the speed of instruction execution. After analyzing the profiler report and fixing bottlenecks, you should recompile the program in the usual way.

In principle, debugging and profiling can be performed both online and in the tester (MQL_TESTER) on historical data, but the tester only supports Expert Advisors and indicators. Therefore, it is impossible to see the set MQL_TESTER or MQL_VISUAL_MODE flag in the script example.

As you know, MetaTrader 5 allows you to test trading programs in quick mode (without a chart) and in visual mode (on a separate chart). It is in the second case that the MQL_VISUAL_MODE properties will be enabled. It makes sense to check it, in particular, to disable manipulations with [graphic objects](/en/book/applications/objects) in the absence of visualization.

To debug in visual mode using history, you must first enable the option Use visual mode for debugging on history in the MetaEditor settings dialog. Analytical programs (indicators) are always tested in visual mode.

Keep in mind that online debugging is not safe for trading Expert Advisors.
