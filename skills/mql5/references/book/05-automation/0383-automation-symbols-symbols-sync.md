# Checking the symbol data relevance

Due to the distributed client-server architecture, client and server data may occasionally be different. For example, this can happen immediately after the start of the terminal session, when the connection is lost, or when the computer resources are heavily loaded. Also, the symbol will most likely remain out of sync for some time immediately after it is added to the Market Watch. The MQL5 API allows you to check the relevance of quote data for a particular symbol using the SymbolIsSynchronized function.

bool SymbolIsSynchronized(const string name)

The function returns true if the local data on the symbol named name is synchronized with the data on the trade server.

The section [Obtaining characteristics of price arrays](/en/book/applications/timeseries/timeseries_properties), among other timeseries properties, introduced the SERIES_SYNCHRONIZED property which returns an attribute of synchronization that is narrower in its meaning: it applies to a specific combination of a symbol and a timeframe. In contrast to this property, the SymbolIsSynchronized function returns an attribute of synchronization of the general history for a symbol.

The construction of all timeframes starts only after the completion of the history download. Due to the multi-threaded architecture and parallel computing in the terminal, it might happen that SymbolIsSynchronized will return true, and for a timeframe on the same symbol, the SERIES_SYNCHRONIZED property will be temporarily equal to false.

Let's see how the new function works in the SymbolListSync.mq5 indicator. It is designed to periodically check all symbols from Market Watch for synchronization. The check period is set by the user in seconds in the SyncCheckupPeriod parameter. It causes the timer to start in OnInit.

```
#property indicator_chart_window
#property indicator_plots 0
   
input int SyncCheckupPeriod = 1; // SyncCheckupPeriod (seconds)
   
void OnInit()
{
   EventSetTimer(SyncCheckupPeriod);
}

```

In the OnTimer handler, in a loop, we call SymbolIsSynchronized and collect all unsynchronized symbols into a common string, after which they are displayed in the comment and the log.

```
void OnTimer()
{
   string unsynced;
   const int n = SymbolsTotal(true);
   // check all symbols in the Market Watch
   for(int i = 0; i < n; ++i)
   {
      const string s = SymbolName(i, true);
      if(!SymbolIsSynchronized(s))
      {
         unsynced += s + "\n";
      }
   }
      
   if(StringLen(unsynced) > 0)
   {
      Comment("Unsynced symbols:\n" + unsynced);
      Print("Unsynced symbols:\n" + unsynced);
   }
   else
   {
      Comment("All Market Watch is in sync");
   }
}

```

For example, if we add some previously missing symbol (Brent) to the Market Watch, we get an entry like this:

```
Unsynced symbols:
Brent

```

Under normal conditions, most of the time (while the indicator is running) there should be no such messages in the log. However, a flood of alerts may be generated during communication problems.
