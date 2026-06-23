# Multicurrency testing

As you know, the MetaTrader 5 tester allows you to test strategies that trade multiple financial instruments. Purely technically, subject to the computer hardware resources, it is possible to simulate simultaneous trading for all available instruments.

Testing such strategies imposes several additional technical requirements on the tester:

- Generation of tick sequences for all instruments
- Calculation of indicators for all instruments
- Calculation of margin requirements and emulation of other trading conditions for all instruments

The tester automatically downloads the history of required instruments from the terminal when accessing the history for the first time. If the terminal does not contain the required history, it will in turn request it from the trade server. Therefore, before testing a multicurrency Expert Advisor, it is recommended to select the required instruments in the terminal's Market Watch and download the desired amount of data.

The agent uploads the missing history with a small margin to provide the necessary data for calculating indicators or copying by the Expert Advisor at the time of testing. The minimum amount of history downloaded from the trading server depends on the timeframe. For example, for D1 timeframes and less, it is one year. In other words, the preliminary history is downloaded from the beginning of the previous year relative to the tester start date. This gives at least 1 year of history if testing is requested from January 1st and a maximum of almost two years if testing is ordered from December. For a weekly timeframe, a history of 100 bars is requested, that is, approximately two years (there are 52 weeks in a year). For testing on a monthly timeframe, the agent will request 100 months (equal to the history of about 8 years: 12 months * 8 years = 96). In any case, on timeframes lower than the working one, a proportionally larger number of bars will be available. If the existing data is not enough for the predefined depth of the preliminary history, this fact will be recorded in the test log.

You cannot configure (change) this behavior. Therefore, if you need to provide a specified number of historical bars of the current timeframe from the very beginning, you should set an earlier start date for the test and then "wait" in the Expert Advisor code for the required trading start date or a sufficient number of bars. Before that, you should skip all events.

The tester also emulates its own Market Watch, from which the program can obtain information on instruments. By default, at the beginning of testing, the tester Market Watch contains only one symbol: the symbol on which testing is started. All additional symbols are added to the tester Market Watch automatically when accessing them through the API functions. At the first access to a "third-party" symbol from an MQL program, the testing agent will synchronize the symbol data with the terminal.

The data of additional symbols can be accessed in the following cases:

- Using technical indicators, iCustom, or IndicatorCreate for the symbol/timeframe pair

- Querying another symbol's Market Watch:
SeriesInfoInteger
Bars
SymbolSelect
SymbolIsSynchronized
SymbolInfoDouble
SymbolInfoInteger
SymbolInfoString
SymbolInfoTick
SymbolInfoSessionQuote
SymbolInfoSessionTrade
MarketBookAdd
MarketBookGet

Querying the symbol/timeframe pair timeseries using the following functions:
CopyBuffer
CopyRates
CopyTime
CopyOpen
CopyHigh
CopyLow
CopyClose
CopyTickVolume
CopyRealVolume
CopySpread

In addition, you can explicitly request the history for the desired symbols by calling the SymbolSelect function in the OnInit handler. The history will be loaded in advance before the Expert Advisor testing starts.

At the moment when another symbol is accessed for the first time, the testing process stops and the symbol/period pair history is downloaded from the terminal into the testing agent. The tick sequence generation is also enabled at this moment.

Each instrument generates its own tick sequence according to the set tick generation mode.

Synchronization of bars of different symbols is of particular importance when implementing multicurrency Expert Advisors since the correctness of calculations depends on this. A state is considered synchronized when the last bars of all used symbols have the same opening time.

The tester generates and plays its tick sequence for each instrument. At the same time, a new bar on each instrument is opened regardless of how bars are opened on other instruments. This means that when testing a multicurrency Expert Advisor, a situation is possible (and most often it happens) when a new bar has already opened on one instrument, but not yet on another.

For example, if we are testing an Expert Advisor using EURUSD symbol data and a new hourly candlestick has opened for this symbol, we will receive the OnTick event. But at the same time, there is no guarantee that a new candlestick has opened on GBPUSD, which we might also be using.

Thus, the synchronization algorithm implies that you need to check the quotes of all instruments and wait for the equality of the opening times of the last bars.

This does not raise any questions for as long as the real tick, emulation of all ticks, or OHLC M1 testing modes are used. With these modes, a sufficient number of ticks are generated within one candlestick to wait for the moment of synchronization of bars from different symbols. Just complete the OnTick function and check the appearance of a new bar on GBPUSD on the next tick. But when testing in the "Open prices only" mode, there will be no other tick, since the Expert Advisor is called only once per bar, and it may seem that this mode is not suitable for testing multicurrency Expert Advisors. In fact, the tester allows you to detect the moment when a new bar opens on another symbol using the Sleep function (in a loop) or a timer.

First, let's consider an example of an Expert Advisor SyncBarsBySleep.mq5, which demonstrates the synchronization of bars through Sleep.

A pair of input parameters allows you to set the Pause size in seconds to wait for other symbol's bars, as well as the name of that other symbol (OtherSymbol), which must be different from the chart symbol.

```
input uint Pause = 1;                   // Pause (seconds)
input string OtherSymbol = "USDJPY";

```

To identify patterns in the delay of bar opening times, we describe a simple class BarTimeStatistics. It contains a field for counting the total number of bars (total) and the number of bars on which there was no synchronization initially (late), that is, the other symbol was late.

```
class BarTimeStatistics
{
public:
   int total;
   int late;
   
   BarTimeStatistics(): total(0), late(0) { }
   
   ~BarTimeStatistics()
   {
      PrintFormat("%d bars on %s was late among %d total bars on %s (%2.1f%%)",
         late, OtherSymbol, total, _Symbol, late * 100.0 / total);
   }
};

```

The object of this class prints the received statistics in its destructor. Since we are going to make this object static, the report will be printed at the very end of the test.

If the tick generation mode selected in the tester differs from the opening prices, we will detect this using the previously considered [getTickModel](/en/book/automation/tester/tester_ticks) function and will return a warning.

```
void OnTick()
{
   const TICK_MODEL model = getTickModel();
   if(model != TICK_MODEL_OPEN_PRICES)
   {
      static bool shownOnce = false;
      if(!shownOnce)
      {
         Print("This Expert Advisor is intended to run in \"Open Prices\" mode");
         shownOnce = true;
      }
   }

```

Next, OnTick provides the working synchronization algorithm.

```
   // time of the last known bar for _Symbol
   static datetime lastBarTime = 0;
   // attribute of synchronization
   static bool synchronized = false;
   // bar counters
   static BarTimeStatistics stats;
   
   const datetime currentTime = iTime(_Symbol, _Period, 0);
   
   // if it is executed for the first time or the bar has changed, save the bar
   if(lastBarTime != currentTime)
   {
      stats.total++;
      lastBarTime = currentTime;
      PrintFormat("Last bar on %s is %s", _Symbol, TimeToString(lastBarTime));
      synchronized = false;
   }
   
   // time of the last known bar for another symbol
   datetime otherTime;
   bool late = false;
   
   // wait until the times of two bars become the same
   while(currentTime != (otherTime = iTime(OtherSymbol, _Period, 0)))
   {
      late = true;
      PrintFormat("Wait %d seconds...", Pause);
      Sleep(Pause * 1000);
   }
   if(late) stats.late++;
   
   // here we are after synchronization, save the new status
   if(!synchronized)
   {
      // use TimeTradeServer() because TimeCurrent() does not change in the absence of ticks
      Print("Bars are in sync at ", TimeToString(TimeTradeServer(),
         TIME_DATE | TIME_SECONDS));
      // no longer print a message until the next out of sync
      synchronized = true;
   }
   // here is your synchronous algorithm
   // ...
}

```

Let's set up the tester to run the Expert Advisor on EURUSD, H1, which is the most liquid instrument. Let's use the default Expert Advisor parameters, that is, USDJPY will be the "other" symbol.

As a result of the test, the log will contain the following entries (we intentionally show the logs related to the downloading of the USDJPY history, which occurred during the first iTime call).

```
2022.04.15 00:00:00   Last bar on EURUSD is 2022.04.15 00:00
USDJPY: load 27 bytes of history data to synchronize in 0:00:00.001
USDJPY: history synchronized from 2020.01.02 to 2022.04.20
USDJPY,H1: history cache allocated for 8109 bars and contains 8006 bars from 2021.01.04 00:00 to 2022.04.14 23:00
USDJPY,H1: 1 bar from 2022.04.15 00:00 added
USDJPY,H1: history begins from 2021.01.04 00:00
2022.04.15 00:00:00   Bars are in sync at 2022.04.15 00:00:00
2022.04.15 01:00:00   Last bar on EURUSD is 2022.04.15 01:00
2022.04.15 01:00:00   Wait 1 seconds...
2022.04.15 01:00:01   Bars are in sync at 2022.04.15 01:00:01
2022.04.15 02:00:00   Last bar on EURUSD is 2022.04.15 02:00
2022.04.15 02:00:00   Wait 1 seconds...
2022.04.15 02:00:01   Bars are in sync at 2022.04.15 02:00:01
...
2022.04.20 23:59:59   95 bars on USDJPY was late among 96 total bars on EURUSD (99.0%)

```

You can see that the USDJPY bars are delayed regularly. If you select USDJPY, H1 in the tester settings and EURUSD in the Expert Advisor parameters, you will get the opposite picture.

```
2022.04.15 00:00:00   Last bar on USDJPY is 2022.04.15 00:00
EURUSD: load 27 bytes of history data to synchronize in 0:00:00.002
EURUSD: history synchronized from 2018.01.02 to 2022.04.20
EURUSD,H1: history cache allocated for 8109 bars and contains 8006 bars from 2021.01.04 00:00 to 2022.04.14 23:00
EURUSD,H1: 1 bar from 2022.04.15 00:00 added
EURUSD,H1: history begins from 2021.01.04 00:00
2022.04.15 00:00:00   Bars are in sync at 2022.04.15 00:00:00
2022.04.15 01:00:00   Last bar on USDJPY is 2022.04.15 01:00
2022.04.15 01:00:00   Wait 1 seconds...
2022.04.15 01:00:01   Bars are in sync at 2022.04.15 01:00:01
2022.04.15 02:00:00   Last bar on USDJPY is 2022.04.15 02:00
2022.04.15 02:00:00   Wait 1 seconds...
2022.04.15 02:00:01   Bars are in sync at 2022.04.15 02:00:01
...
2022.04.20 23:59:59   23 bars on EURUSD was late among 96 total bars on USDJPY (24.0%)

```

Here, in most cases, there was no need to wait: the EURUSD bars already existed at the time the USDJPY bar was formed.

There is another way to synchronize bars: using a timer. An example of such an Expert Advisor, SyncBarsByTimer.mq5, is included in the book. Please note that the timer events, as a rule, occur inside the bar (because the probability of hitting exactly the beginning is very low). Because of this, the bars are almost always synchronized.

We could also remind you about the possibility of synchronizing bars using the spy indicator [EventTickSpy.mq5](/en/book/applications/events/events_custom), but it's based on custom events that only work when testing visually. In addition, for such indicators that require a response to each tick, it is important to use the #property tester_everytick_calculate directive. We have already talked about it in the [Testing indicators](/en/book/applications/indicators_make/indicators_test) section, and we will remind you about it once again in the section on specific [tester directives](/en/book/automation/tester/tester_directives).
