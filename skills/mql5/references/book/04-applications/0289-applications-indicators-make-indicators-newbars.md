# Tracking bar formation

The IndUnityPercent.mq5 indicator discussed in the previous section is recalculated on the last bar on each tick since it uses Close prices. Some indicators and Experts Advisors are specially developed in a more economical style, with a single calculation on each bar. For example, we could calculate Unity's formula at open prices, and then it makes sense to skip ticks. There are several ways to detect a new bar:

- Remember the time of the current 0 bar (via the time parameter of the OnCalculate function — time[0] or, in general, iTime(symbol, period, 0)) and wait for it to change
- Memorize the number of bars rates_total (or iBars(symbol, period)) and respond to an increase by 1 (a change to a different amount in one direction or another is suspicious and may indicate a history modification)
- Wait for a bar with a tick volume equal to 1 (the first tick on the bar)

However, with the multicurrency nature of the indicator, the very concept of the formation of a new bar becomes not so unambiguous.

On each symbol, the next bar appears upon the arrival of its own ticks, and they usually have different arrival times. In this case, the indicator developer must determine how to act: whether to wait for the appearance of bars with the same time on all symbols or to recalculate the indicator on the last bars several times after the appearance of a new bar on any of the symbols.

In this section, we will introduce a simple class MultiSymbolMonitor (see fileMultiSymbolMonitor.mqh) to track the formation of new bars according to a given list of symbols.

The required timeframe can be passed to the class constructor. By default, it tracks the timeframe of the current chart, on which the program is running.

```
class MultiSymbolMonitor
{
protected:
   ENUM_TIMEFRAMES period;
   
public:
   MultiSymbolMonitor(): period(_Period) {}
   MultiSymbolMonitor(const ENUM_TIMEFRAMES p): period(p) {}
   ...

```

To store the list of tracked symbols, we will use an auxiliary class MapArray from the previous section. In this array, we will write pairs [symbol name;timestamp of the last bar], that is, template types <string,datetime>. The attach method populates the array.

```
protected:
   MapArray<string,datetime> lastTime;
...
public:
   void attach(const string symbol)
   {
      lastTime.put(symbol, NULL);
   }

```

For a given array, the class can update and check timestamps in the check method by calling the iTime function in a loop over symbols.

```
   ulong check(const bool refresh = false)
   {
      ulong flags = 0;
      for(int i = 0; i < lastTime.getSize(); i++)
      {
         const string symbol = lastTime.getKey(i);
         const datetime dt = iTime(symbol, period, 0);
        
         if(dt != lastTime[symbol]) // are there any changes?
         {
            flags |= 1 << i;
         }
         
         if(refresh) // update timestamp
         {
            lastTime.put(symbol, dt);
         }
      }
      return flags;
   }

```

The calling code should call check at its own discretion, which is usually upon the arrival of ticks, or on a timer. Strictly speaking, both of these options do not provide an instant reaction to the appearance of ticks (and new bars) on other instruments since the OnCalculate event appears only on the ticks of the working symbol of the chart, and if there was a tick of some other symbol between them, we will not know about it until the next "own" tick.

We will consider real-time monitoring of ticks from several instruments in the chapter on interactive chart events (see spy indicator EventTickSpy.mq5 in the section [Generation of custom events](/en/book/applications/events/events_custom)).

For now, we'll check bars with available accuracy. So, let's proceed with the check method.

Each point in time is characterized by its own state of the timestamps set for all symbols in the array. For example, a new bar may form at 12:00 only for the most liquid instrument, and for several other instruments, ticks will appear in a few milliseconds or even seconds. During this interval, one element will be updated in the array, and the rest will be old. Then gradually all symbols will get 12:00 bars.

For all symbols for which the opening time of the last bar is not equal to the saved one, the method sets the bit with the symbol number, thus forming a bit mask with changes. The list must not contain more than 64 symbols.

If the return value is zero, no changes have been registered.

The refresh parameter specifies whether the check method will only register changes (false), or will update the status according to the current market situation (true).

The describe method allows you to get a list of changed symbols by a bitmask.

```
   string describe(ulong flags = 0)
   {
      string message = "";
      if(flags == 0) flags = check();
      for(int i = 0; i < lastTime.getSize(); i++)
      {
         if((flags & (1 << i)) != 0)
         {
            message += lastTime.getKey(i) + "\t";
         }
      }
      return message;
   }

```

Next, we will use the inSync to determine if all symbols in the array have the same last bar time. It makes sense to use it only for a set of currencies with the same trading sessions.

```
   bool inSync() const
   {
      if(lastTime.getSize() == 0) return false;
      const datetime first = lastTime[0];
      for(int i = 1; i < lastTime.getSize(); i++)
      {
         if(first != lastTime[i]) return false;
      }
      return true;
   }

```

Using the described class, we implement a simple multicurrency indicator IndMultiSymbolMonitor.mq5, whose only task will be to detect new bars for a list of symbols.

Since no drawing is provided for the indicator, the number of buffers and charts is 0.

```
#property indicator_chart_window
#property indicator_buffers 0
#property indicator_plots   0

```

The list of instruments is specified in the corresponding input variable and then converted to an array registered in the monitor object.

```
input string Instruments = "EURUSD,GBPUSD,USDCHF,USDJPY,AUDUSD,USDCAD,NZDUSD";
   
#include <MQL5Book/MultiSymbolMonitor.mqh>
   
MultiSymbolMonitor monitor;
   
void OnInit()
{
   string symbols[];
   const int n = StringSplit(Instruments, ',', symbols);
   for(int i = 0; i < n; ++i)
   {
      monitor.attach(symbols[i]);
   }
}

```

The OnCalculate handler calls the monitor on ticks and outputs state changes to the log.

```
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const int begin,
                const double &price[])
{
   const ulong changes = monitor.check(true);
   if(changes != 0)
   {
      Print("New bar(s) on: ", monitor.describe(changes),
         ", in-sync:", monitor.inSync());
   }
   return rates_total;
}

```

To check this indicator, we would need to spend a lot of time online in the terminal. However, MetaTrader 5 allows you to do this much easier — with the help of a tester. We will do this in the next section.
