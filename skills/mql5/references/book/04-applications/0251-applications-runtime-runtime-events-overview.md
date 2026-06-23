# Overview of event handling functions

The transfer of control to MQL programs, that is, their execution, occurs by calling special functions by the terminal or test agents, which the MQL developer defines in their application code to process predefined events. Such functions must have a specified prototype, including a name, a list of parameters (number, types, and order), and a return type.

The name of each function corresponds to the meaning of the event, with the addition of the prefix On. For example, OnStart is the main function for "starting" scripts and services; it is called by the terminal at the moment the script is placed on the chart or the service instance is launched.

For the purposes of this book, we will refer to an event and its corresponding handler by the same name.

![Mandatory handlers are marked with symbol '●', and optional handlers are marked with '+'.](pics/indicator_small.png)

| Program type 
 Event/Handler |  |  |  |  | Description |
| --- | --- | --- | --- | --- | --- |
| OnStart | - | - | ● | ● | Start/Execute |
| OnInit | + | + | - | - | Initialization after loading (see details in section  Features of starting and stopping programs of various types ) |
| OnDeinit | + | + | - | - | Deinitialization before stopping and unloading |
| OnTick | - | + | - | - | Getting a new price (tick) |
| OnCalculate | ● | - | - | - | Request to recalculate the indicator due to receiving a new price or synchronizing old prices |
| OnTimer | + | + | - | - | Timer activation with a specified frequency |
| OnTrade | - | + | - | - | Completion of a trading operation on the server |
| OnTradeTransaction | - | + | - | - | Changing the state of the trading account (orders, deals, positions) |
| OnBookEvent | + | + | - | - | Change in the order book |
| OnChartEvent | + | + | - | - | User or MQL program action on the chart |
| OnTester | - | + | - | - | End of a single tester pass |
| OnTesterInit | - | + | - | - | Initialization before optimization |
| OnTesterDeinit | - | + | - | - | Deinitialization after optimization |
| OnTesterPass | - | + | - | - | Receiving optimization data from the testing agent |

Mandatory handlers are marked with symbol '●', and optional handlers are marked with '+'.

Although handler functions are primarily intended to be called by the runtime, you can also call them from your own source code. For example, if an Expert Advisor needs to make some calculation based on the available quotes immediately after the start, and even in the absence of ticks (for example, on weekends), you can call OnTick before leaving OnInit. Alternatively, it would be logical to separate the calculation into a separate function and call it both from OnInit and from OnTick. However, it is desirable to perform the work of the initialization function quickly, and if the calculation is long, it should be performed on a [timer](/en/book/applications/timer).

All MQL programs (except libraries) must have at least one event handler. Otherwise, the compiler will generate an "event handling function not found" error.

The presence of some handler functions determines the type of the program in the absence of #property directives that set another type. For example, having the OnCalculate handler leads to the generation of the indicator (even if it is located in another folder, for example, scripts or Expert Advisors). The presence of the OnStart handler (if there is no OnCalculate) means creating a script. At the same time, if the indicator, in addition to OnCalculate, will face OnStart, we get a compiler warning "OnStart function defined in the non-script program".

The book includes two files: AllInOne.mq5 and AllInOne.mqh. The header file describes almost empty templates of all the main event handlers. They contain nothing except outputting the name of the handler to the log. We will consider the syntax and specifics of using each of the handlers in the sections on specific types of MQL programs. The meaning of this file is to provide a field for experiments with compiling different types of programs, depending on the presence of certain handlers and property directives (#property).

Some combinations may result in errors or warnings.

If the compilation was successful, then the resulting program type is automatically logged after it is loaded using the following line:

```
const string type = 
   PRTF(EnumToString((ENUM_PROGRAM_TYPE)MQLInfoInteger(MQL_PROGRAM_TYPE)));

```

We studied the enum ENUM_PROGRAM_TYPE and function MQLInfoInteger in the section [Program type and license](/en/book/common/environment/env_type_license).

The file AllInOne.mq5, which includes AllInOne.mqh, is initially located in the directory MQL5Book/Scripts/p5/, but it can be copied to any other folder, including neighboring Navigator branches (for example, to a folder of Expert Advisors or indicators). Inside the file, in the comments, options are left for connecting certain program assembly configurations. By default, if you do not edit the file, you will bet an Expert Advisor.

```
//+------------------------------------------------------------------+
//| Uncomment the following line to get the service                  |
//| NB: also activate #define _OnStart OnStart                       |
//+------------------------------------------------------------------+
//#property service
  
//+------------------------------------------------------------------+
//| Uncomment the following line to get a library                    |
//+------------------------------------------------------------------+
//#property library
  
//+------------------------------------------------------------------+
//| Uncomment the following line to get a script or                  |
//| service (#property service must be enabled)                      |
//+------------------------------------------------------------------+
//#define _OnStart OnStart
  
//+------------------------------------------------------------------+
//| Uncomment one of the following two lines for the indicator       |
//+------------------------------------------------------------------+
//#define _OnCalculate1 OnCalculate
//#define _OnCalculate2 OnCalculate
  
#include <MQL5Book/AllInOne.mqh>

```

If we attach the program to the chart, we will get an entry in the log:

```
EnumToString((ENUM_PROGRAM_TYPE)MQLInfoInteger(MQL_PROGRAM_TYPE))=PROGRAM_EXPERT / ok
OnInit
OnChartEvent
OnTick
OnTick
OnTick
...

```

Also, most likely, a stream of records will be generated from the OnTick handler if the market is open.

If you duplicate the mq5 file under a different name and, for example, uncomment the directive #property service, the compiler will generate the service but will return a few warnings.

```
no OnStart function defined in the script
OnInit function is useless for scripts
OnDeinit function is useless for scripts

```

The first of them, about the absence of the OnStart function, is actually significant, because when a service instance is created, no function will be called in it, but only global variables will be initialized. However, due to this, the journal (Experts tab in the terminal) will still print the PROGRAM_SERVICE type. But as a rule, in services, as well as in scripts, it is assumed that the OnStart function is present.

The other two warnings arise because our header file contains handlers for all occasions, and the compiler reminds us that OnInit and OnDeinit are pointless (will not be called by the terminal and will not even be included in the binary image of the program). Of course, in real programs there should be no such warnings, that is, all handlers should be involved, and everything superfluous should be removed from the source code, either physically or logically, using preprocessor directives for conditional compilation.

If you create another copy of AllInOne.mq5 and activate not only the #property service directive but also the #define _OnStart OnStart macro, you will get a fully working service as a result of its compilation. When launched, it will not only display the name of its type but also the name of the triggered handler OnStart.

The macro was required to be able to enable/disable the standard handler OnStart if they wish to. In the AllInOne.mqh text, this function is described as follows:

```
void _OnStart() // "extra" underline makes the function customized 
{
   Print(__FUNCTION__);
}

```

The name starting with an underscore makes it not a standard handler, but just a user-defined function with a similar prototype. When we include a macro, during compilation the compiler replaces _OnStart on OnStart, and the result is already a standard handler. If we explicitly named the OnStart function, then, according to the priorities of the characteristics that determine the type of the MQL program (see section [Features of MQL programs of various types](/en/book/applications/runtime/runtime_features_by_progtype)), it would not allow you to get an Expert Advisor template (because OnStart identifies the program as a script or service).

Similar custom compilation with macros _OnCalculate1 or _OnCalculate2 required to optionally "hide" the handler with a standard name OnCalculate: otherwise, if it was present, we would always get an indicator.

f in the next copy of the program you activate the macro #define _OnCalculate1 OnCalculate, you will get an example indicator (even though it is empty and does nothing). As we will see later, there are two different forms of the handler OnCalculate for indicators, in connection with which they are presented under numbered names (_OnCalculate1 and _OnCalculate2). If you run the indicator on the chart, you can see in the log the names of events OnCalculate (upon arrival of ticks) and OnChartEvent (for example, on a mouse click).

When compiling the indicator, the compiler will generate two warnings:

```
no indicator window property is defined, indicator_chart_window is applied
no indicator plot defined for indicator

```

This is because indicators, as data visualization tools, require some specific settings in their code that are not here. At this stage of superficial acquaintance with different types of programs, this is not important. But further on, we will learn how to describe their properties and arrays in indicators, which determine what and how should be visualized on the chart. Then these warnings will disappear.

Event queue

When a new event occurs, it must be delivered to all MQL programs running on the corresponding chart. Due to the single-threaded execution model of MQL programs (see section [Threads](/en/book/applications/runtime/runtime_threads)), it may happen that the next event arrives when the previous one is still being processed. For such cases, the terminal maintains an event queue for each interactive MQL program. All events in it are processed one after another in order of receipt.

Event queues have a limited size. Therefore, an irrationally written program can provoke an overflow of its queue due to slow actions. On overflow, new events are discarded without being queued.

Not processing events fast enough can negatively affect the user experience or data quality (imagine you record [Market Depth](/en/book/automation/marketbook) changes and skip a few messages). To solve this problem, you can look for more efficient algorithms or use the parallel operation of several interconnected MQL programs (for example, assign calculations to an indicator, and only read ready-made data in an Expert Advisor).

It should be borne in mind that the terminal does not place all events in the queue but operates selectively. Some types of events are processed according to the principle "no more than one event of this type in the queue". For example, if there is already the OnTick event in the queue, or it is being processed, then a new OnTick event is not queued. If there is already the OnTimer event or a chart change event in the queue, then new events of these types are also discarded (ignored). It is about a specific instance of the program. Other, less "busy" programs will receive this message.

We do not provide a complete list of such event types because this optimization by skipping "overlapping" events can be changed by the terminal developers.

The approach to organizing the work of programs in response to incoming events is called event-driven. It can also be called asynchronous because the queuing of an event in the program queue and its extraction (together with processing) occur at different moments (ideally, separated by a microscopic interval, but the ideal is not always achievable). However, of the four types of MQL programs, only indicators and Expert Advisors fully follow this approach. Scripts and services have, in fact, only the main function, which, when called, must either quickly perform the required action and complete or start an endless loop to maintain some activity (for example, reading data from the network) until the user stops. We have seen examples of such loops:

```
while(!IsStopped())
{
  useful code
   ...
   Sleep(...);
} 

```

In such loops, it is important not to forget to use Sleep with some period to share CPU resources with other programs. The value of the period is selected based on the estimated intensity of the activity being implemented.

This approach can be referred to as cyclic or synchronous, or even as real-time, since you can select the sleep period to provide a constant frequency of data handling, for example:

```
int rhythm = 100; // 100 ms, 10 times per sec
while(!IsStopped())
{
   const int start = (int)GetTickCount();
  useful code
   ...
   Sleep(rhythm - ((int)GetTickCount() - start));
} 

```

Of course, the "useful code" must fit in the allotted frame.

In contrast, with the event approach, it is not known in advance when the next time the piece of code (handler) will work. For example, in a fast market, during the news, ticks can come in batches, and at night they can be absent for whole seconds. In the limiting case, after the final tick on Friday evening, the next price change for some financial instrument can be broadcast only on Monday morning, and therefore the events OnTick will be absent for two days. In other words, in events (and moments of activation of event handlers) there is no regularity, no clear schedule.

But if necessary, you can combine both trips. In particular, the timer event ([OnTimer](/en/book/applications/timer/timer_ontimer)) provides regularity, and the developer can periodically generate [custom events](/en/book/applications/events/events_custom) for a chart inside a loop (for example, flashing a warning label).
