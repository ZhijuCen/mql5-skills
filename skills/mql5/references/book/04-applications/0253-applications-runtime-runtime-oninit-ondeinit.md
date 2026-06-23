# Reference events of indicators and Expert Advisors: OnInit and OnDeinit

In interactive MQL programs — indicators and Expert Advisors — the environment generates two events to prepare for launch (OnInit) and stop (OnDeinit). There are no such events in scripts and services because they do not accept asynchronous events: after control is passed to their single event handler [OnStart](/en/book/applications/runtime/runtime_onstart) and until the end of the work, the execution context of the script/service thread is in the code of the MQL program. In contrast, for indicators and Expert Advisors, the normal course of work assumes that the environment will repeatedly call their specific event handling functions (we will discuss them in the sections on indicators and Expert Advisors), and each time, having taken the necessary actions, the programs will return control to the terminal for idle waiting for new events.

int OnInit()

Function OnInit is a handler of the event of the same name, which is generated after loading an Expert Advisor or an indicator. The function can only be defined as needed.

The function must return one of the ENUM_INIT_RETCODE enum values.

| Identifier | Description |
| --- | --- |
| INIT_SUCCEEDED | Successful initialization, program execution can be continued; corresponds to value 0 |
| INIT_FAILED | Unsuccessful initialization, execution cannot be continued due to fatal errors (for example, it was not possible to create a file or an auxiliary indicator); value 1 |
| INIT_PARAMETERS_INCORRECT | Incorrect set of input parameters, program execution is impossible |
| INIT_AGENT_NOT_SUITABLE | Specific code to work in  tester : for some reason, this agent is not suitable for testing (for example, not enough RAM, no OpenCL support, etc.) |

If OnInit returns any non-zero return code, this means unsuccessful initialization, and then the Deinit event is generated, with deinitialization reason code REASON_INITFAILED (see below).

The OnInit function can be declared with a result type void: in this case, initialization is always considered successful.

In the OnInit handler, it is important to check that all necessary environment information is present, and if it is not available, defer preparatory actions for the next tick or timer arrival events. The point is that when the terminal starts, the OnInit event often triggers before a connection to the server is established, and therefore many properties of financial instruments and a trading account are still unknown. In particular, the value of one pip of a particular symbol may be returned as zero.

void OnDeinit(const int reason)

The OnDeinit function (if it is defined) is called when the Expert Advisor or indicator is deinitialized. The function is optional.

The reason parameter contains the deinitialization reason code. Possible values are shown in the following table.

| Constant | Value | Description |
| --- | --- | --- |
| REASON_PROGRAM | 0 | Expert Advisor stopped operation by  ExpertRemove  function call |
| REASON_REMOVE | 1 | Program removed from the chart |
| REASON_RECOMPILE | 2 | Program recompiled |
| REASON_CHARTCHANGE | 3 | Chart symbol or period changed |
| REASON_CHARTCLOSE | 4 | Chart closed |
| REASON_PARAMETERS | 5 | Input parameters changed |
| REASON_ACCOUNT | 6 | Another account has been activated, or a reconnection to the trading server has occurred due to a change in the account settings |
| REASON_TEMPLATE | 7 | Different chart template applied |
| REASON_INITFAILED | 8 | OnInit  handler returned a non-null value |
| REASON_CLOSE | 9 | Terminal closed |

The same code can be obtained anywhere in the program using the [UninitializeReason](/en/book/common/environment/env_stop) function if the stop flag _StopFlag is set in the MQL program.

The AllInOne.mqh file has the Finalizer class which allows you to "hook" the deinitialization code in the destructor through the UninitializeReason call. We must get the same value in the OnDeinit handler.

```
class Finalizer
{
   static const Finalizer f;
public:
   ~Finalizer()
   {
      PRTF(EnumToString((ENUM_DEINIT_REASON)UninitializeReason()));
   }
};
 
static const Finalizer Finalizer::f;

```

For the convenience of translating codes into a string representation (names of reasons) using EnumToString, enumeration ENUM_DEINIT_REASON with constants from the above table is described in the Uninit.mqh file. The log will display entries like:

```
OnDeinit DEINIT_REASON_REMOVE
EnumToString((ENUM_DEINIT_REASON)UninitializeReason())=DEINIT_REASON_REMOVE / ok

```

When you change the symbol or timeframe of the chart on which the indicator is located, it is unloaded and loaded again. In this case, the sequence of triggering the event OnDeinit in the old copy and OnInit is not defined in the new copy. This is due to the specifics of asynchronous event processing by the terminal. In other words, it may not be entirely logical that a new copy will be loaded and initialized before the old one is completely unloaded. If the indicator performs some chart adjustment in OnInit (for example, creates a [graphic object](/en/book/applications/objects)), then without taking special measures, the unloaded copy can immediately "clean up" the chart (delete the object, considering it to be its own). In the specific case of graphical objects, there is a particular solution: objects can be given names that include symbol and timeframe prefixes (as well as the checksum of input variable values), but in the general case it will not work. For a universal solution to the problem, some kind of synchronization mechanism should be implemented, for example, on [global variables](/en/book/common/globals) or [resources](/en/book/advanced/resources).

When testing indicators in the tester, MetaTrader 5 developers decided not to generate the OnDeinit event. Their idea is that the indicator can create some graphical objects, which it usually removes in the OnDeinit handler, but the user would like to see them after the test is completed. In fact, the author of an MQL program can, if desired, provide similar behavior and leave objects with a positive check of the mode MQLInfoInteger(MQL_TESTER). This is strange since the OnDeinit handler is called after the Expert Advisor test, and the Expert Advisor can delete objects in the same way in OnDeinit. Now, only for indicators, it turns out that the regular behavior of the OnDeinit handler cannot be guaranteed in the tester. Moreover, other finalization is not performed, for example, destructors of global objects are not called.

Thus, if you need to perform a statistics calculation, file saving, or other action after the test run that was originally intended for the indicator's OnDeinit, you will have to transfer the indicator algorithms to the Expert Advisor.
