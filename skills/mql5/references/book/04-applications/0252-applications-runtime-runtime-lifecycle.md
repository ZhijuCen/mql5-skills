# Features of starting and stopping programs of various types

In programming, the term initialization is used in many different contexts. In MQL5, there is also some ambiguity. In the [Initialization](/en/book/basis/variables/initialization) section, we have already used this word to mean setting the initial values of variables. Then we discussed the initialization event OnInit in indicators and Expert Advisors. Although the meaning of both initializations is similar (bring the program to a working state), they actually mean different stages of preparing an MQL program for launch: system and application.

The life cycle of a finished MQL program can be represented by the following major steps:

1. Loading — reading a program from a file into the terminal's memory: this includes instructions, predefined data (literals), [resources](/en/book/advanced/resources), and [libraries](/en/book/advanced/libraries). This is where #property directives come into play.
2. Allocating memory for global variables and setting their initial values — it is system initialization performed by the runtime. Recall that in the section [Initialization](/en/book/basis/variables/initialization), while studying the start of the program under the debugger step by step, we saw that the @global_initializations entry was on the stack. This was the code block for this item, which was created implicitly by the compiler. If the program uses global objects of classes/structures, their [constructors](/en/book/oop/classes_and_interfaces/classes_ctors) will be called at this stage.
3. Calling the OnInit event handler (if it exists): it carries out a higher-level, applied initialization, and thus each program performs it independently, as necessary. For example, it can be dynamic memory allocation for arrays of objects, for which, for one reason or another, you need to use parametric constructors instead of default constructors. As we know, automatic memory allocation for arrays uses only default constructors, and therefore they cannot be initialized within the previous step (2). It can also be opening files, calling built-in API functions to enable the necessary chart modes, etc.
4. A loop until the user closes the program or terminal or performs any other action that requires reinitialization (see further):
calling other handlers as appropriate events occur.

Calling the OnDeinit event handler (if it exists) upon detection of an attempt to close the program by the user or programmatically (the corresponding function [ExpertRemove](/en/book/applications/runtime/runtime_remove) is available only in Expert Advisors and scripts).
Finalization: freeing allocated memory and other resources that the programmer did not consider as necessary to free in OnDeinit. If the program uses OOP, the destructors of global and static objects are called here.
Downloading the program.

Scripts and services a priori do not have OnInit and OnDeinit handlers, and therefore steps 3 and 5 are absent for them, and step 4 degenerates into a single OnStart call.

System initialization (step 2) is inseparable from loading, that is, it always follows it. Finalization always precedes unloading. However, indicators and Expert Advisors go through the stages of loading and unloading differently in different situations. Therefore, OnInit and OnDeinit calls (steps 3 and 5) are the reference points at which it is possible to provide consistent applied initialization and deinitialization of Expert Advisors and indicators.

Loading of indicators and Expert Advisors is performed in the following cases:

| Case |  |  |
| --- | --- | --- |
| The user launches the program on the chart | + | + |
| Launching the terminal (if the program was running on the chart before the previous closing of the terminal) | + | + |
| Loading a template (if the template contains a program attached to the chart) | + | + |
| Profile change (if the program is attached to one of the profile charts) | + | + |
| After successful recompilation, if the program was attached to the chart | + | + |
| Changing the active account | + | + |
| - | - | - |
| Change the symbol or period of the chart to which the indicator is attached | + | - |
| Changing the input parameters of the indicator | + | - |
| - | - | - |
| Connecting to the account (authorization), even if the account number has not changed | - | + |

In a more compact form, the following rule can be formulated: Expert Advisors do not go through the full life cycle, that is, they do not reload when the symbol/timeframe of the chart changes, as well as when the input parameters change.

Therefore, a similar asymmetry can be observed when unloading programs. The reasons for unloading indicators and Expert Advisors are:

| Case |  |  |
| --- | --- | --- |
| Removing the program from the chart | + | + |
| Closing the terminal (when the program is attached to the chart) | + | + |
| Loading a template on the chart on which the program is running | + | + |
| Closing the chart on which the program is running | + | + |
| Changing the profile if the program is attached to one of the charts of the profile | + | + |
| Changing the account to which the terminal is connected | + | + |
| - | - | - |
| Changing the symbol and/or period of the chart to which the indicator is attached | + | - |
| Changing the input parameters of the indicator | + | - |
| - | - | - |
| Attaching another or the same EA to the chart where the current EA is already running | - | + |
| Calling the  ExpertRemove  function | - | + |

The reason for deinitialization can be found in the program using the function UninitializeReason or flag _UninitReason (cm. section [Checking the status and reason for stopping an MQL program](/en/book/common/environment/env_stop)).

Please note that when you change the symbol or timeframe of the chart, as well as when you change the input parameters, the Expert Advisor remains in memory, that is, steps 6-7 (finalization and unloading) and steps 1-2 (loading and primary memory allocation) are not executed, therefore values of global and static variables are not reset. In this case, the OnDeinit and OnInit handlers are called sequentially on the old and on the new symbol/timeframe respectively (or at the old and new settings).

A consequence of global variables not being cleared in Expert Advisors is that the deinitialization code _UninitReason remains unchanged for analysis in the OnInit handler. The new code will be written to the variable only in case of the next event, just before the OnDeinit call.

All events received for the Expert Advisor before the end of the OnInit function, are skipped.

When the MQL program is launched for the first time, the settings dialog is displayed between steps 1 and 2. When changing the input parameters, the settings dialog is wedged into the general loop in different ways depending on the type of program: for indicators, it still appears before step 2, and for Expert Advisors – before step 3.  

   

The book is accompanied by an indicator and Expert Advisor template entitled LifeCycle.mq5. It logs global initialization/finalization steps in OnInit/OnDeinit handlers. Place programs on the chart and see what events occur in response to various user actions: loading/unloading, changing parameters, switching symbols/timeframes.

The script is loaded only when it is added to the chart. If a script is running in a loop, recompiling it does not result in a restart.

The service is loaded and unloaded using the context menu commands in the terminal interface. When a service that is already running is recompiled, it is restarted. Recall that active instances of services are automatically loaded when the terminal starts and unloaded when closes.

In the next two sections, we will consider the features of launching different MQL programs at the level of event handlers.
