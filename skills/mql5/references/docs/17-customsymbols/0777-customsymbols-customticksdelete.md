# CustomTicksDelete

Deletes all ticks from the price history of the custom symbol in the specified time interval.

```
int  CustomTicksDelete(
   const string     symbol,            // symbol name
   long             from_msc,          // start date
   long             to_msc             // end date
   );

```

Parameters

symbol

[in]  Custom symbol name.

from_msc

[in]  Time of the first tick in the price history within the specified range to be removed. Time in milliseconds since 01.01.1970.

to_msc

[in]  Time of the last tick in the price history within the specified range to be removed. Time in milliseconds since 01.01.1970.

Return Value

Number of deleted ticks or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Example:

```
//+------------------------------------------------------------------+
//|                                            CustomTicksDelete.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   CUSTOM_SYMBOL_NAME     Symbol()+".C"     // custom symbol name
#define   CUSTOM_SYMBOL_PATH     "Forex"           // name of the group, in which a symbol is to be created
#define   CUSTOM_SYMBOL_ORIGIN   Symbol()          // name of a symbol a custom one is to be based on
 
#define   DATATICKS_TO_COPY      UINT_MAX          // number of ticks copied
#define   DATATICKS_TO_DELETE    10                // number of deleted ticks
#define   DATATICKS_TO_PRINT     20                // number of ticks sent to the journal
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the error code when creating a custom symbol
   int create=CreateCustomSymbol(CUSTOM_SYMBOL_NAME, CUSTOM_SYMBOL_PATH, CUSTOM_SYMBOL_ORIGIN);
   
//--- if the error code is not 0 (successful symbol creation) and not 5304 (symbol has already been created) - leave
   if(create!=0 && create!=5304)
      return;
 
//--- get the standard symbol tick data to the MqlTick array
   MqlTick array[]={};
   if(!GetTicksToArray(CUSTOM_SYMBOL_ORIGIN, DATATICKS_TO_COPY, array))
      return;
   
//--- print the time of the first and last received ticks of the standard symbol
   int total=(int)array.Size();
   PrintFormat("First tick time: %s.%03u, Last tick time: %s.%03u",
               TimeToString(array[0].time,TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[0].time_msc%1000,
               TimeToString(array[total-1].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[total-1].time_msc%1000);
               
//--- print DATATICKS_TO_PRINT last ticks of the standard symbol in the journal
   PrintFormat("\nThe last %d ticks for the standard symbol '%s':", DATATICKS_TO_PRINT, CUSTOM_SYMBOL_ORIGIN);
   for(int i=total-DATATICKS_TO_PRINT; i<total; i++)
     {
      if(i<0)
         continue;
      PrintFormat("  %dth Tick: %s", i, GetTickDescription(array[i]));
     }
   
//--- add a custom symbol to the MarketWatch window
   ResetLastError();
   if(!SymbolSelect(CUSTOM_SYMBOL_NAME, true))
     {
      Print("SymbolSelect() failed. Error ", GetLastError());
      return;
     }
     
//--- add the tick array data to the custom symbol price history
   Print("...");
   uint start=GetTickCount();
   PrintFormat("Start of adding %u ticks to the history of the custom symbol '%s'", array.Size(), CUSTOM_SYMBOL_NAME);
   int added=CustomTicksAdd(CUSTOM_SYMBOL_NAME, array);
   PrintFormat("Added %u ticks to the history of the custom symbol '%s' in %u ms", added, CUSTOM_SYMBOL_NAME, GetTickCount()-start);
   
//--- get the newly added custom symbol tick data to the MqlTick array
   Print("...");
   if(!GetTicksToArray(CUSTOM_SYMBOL_NAME, array.Size(), array))
      return;
   
//--- print the time of the first and last received ticks of the custom symbol
   total=(int)array.Size();
   PrintFormat("First tick time: %s.%03u, Last tick time: %s.%03u",
               TimeToString(array[0].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[0].time_msc%1000,
               TimeToString(array[total-1].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[total-1].time_msc%1000);
               
//--- print DATATICKS_TO_PRINT last ticks of the custom symbol in the journal
   PrintFormat("\nThe last %d ticks for the custom symbol '%s':", DATATICKS_TO_PRINT, CUSTOM_SYMBOL_NAME);
   for(int i=total-DATATICKS_TO_PRINT; i<total; i++)
     {
      if(i<0)
         continue;
      PrintFormat("  %dth Tick: %s", i, GetTickDescription(array[i]));
     }
 
//--- get the tick time in milliseconds, from which we will delete the range of ticks, from history
   long time_from=array[total-DATATICKS_TO_DELETE-1].time_msc;
     
//--- delete DATATICKS_TO_DELETE the range of the last ticks of the custom symbol in the array
   Print("...");
   start=GetTickCount();
   PrintFormat("Start deleting %u ticks in the history of the custom symbol '%s'", DATATICKS_TO_DELETE, CUSTOM_SYMBOL_NAME);
   int deleted=CustomTicksDelete(CUSTOM_SYMBOL_NAME, time_from, array[total-2].time_msc);
   PrintFormat("Deleted %u ticks in the history of the custom symbol '%s' in %u ms", deleted, CUSTOM_SYMBOL_NAME, GetTickCount()-start);
   
//--- get the newly modified custom symbol tick data to the MqlTick array
   Print("...");
   if(!GetTicksToArray(CUSTOM_SYMBOL_NAME, array.Size(), array))
      return;
   
//--- print the time of the first and last ticks of a custom symbol with a removed tick range
   total=(int)array.Size();
   PrintFormat("Time of the first tick from the changed history: %s.%03u, Time of the last tick from the changed history: %s.%03u",
               TimeToString(array[0].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[0].time_msc%1000,
               TimeToString(array[total-1].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[total-1].time_msc%1000);
               
//--- print DATATICKS_TO_PRINT last ticks of the custom symbol in the journal
   PrintFormat("\nThe last %d ticks of custom symbol '%s' with modified history:", DATATICKS_TO_PRINT, CUSTOM_SYMBOL_NAME);
   for(int i=total-DATATICKS_TO_PRINT; i<total; i++)
     {
      if(i<0)
         continue;
      PrintFormat("  %dth Tick: %s", i, GetTickDescription(array[i]));
     }
 
//--- display a hint about the script termination keys on the chart comment
   Comment(StringFormat("Press 'Esc' to exit or 'Del' to delete the '%s' symbol and exit", CUSTOM_SYMBOL_NAME));
//--- wait for pressing the Esc or Del keys to exit in an endless loop
   while(!IsStopped() && TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE)==0)
     {
      Sleep(16);
      //--- when pressing Del, delete the created custom symbol and its data
      if(TerminalInfoInteger(TERMINAL_KEYSTATE_DELETE)<0)
        {
         //--- delete bar data
         int deleted=CustomRatesDelete(CUSTOM_SYMBOL_NAME, 0, LONG_MAX);
         if(deleted>0)
            PrintFormat("%d history bars of the custom symbol '%s' were successfully deleted", deleted, CUSTOM_SYMBOL_NAME);
         
         //--- delete tick data
         deleted=CustomTicksDelete(CUSTOM_SYMBOL_NAME, 0, LONG_MAX);
         if(deleted>0)
            PrintFormat("%d history ticks of the custom symbol '%s' were successfully deleted", deleted, CUSTOM_SYMBOL_NAME);
         
         //--- delete symbol
         if(DeleteCustomSymbol(CUSTOM_SYMBOL_NAME))
            PrintFormat("Custom symbol '%s' deleted successfully", CUSTOM_SYMBOL_NAME);
         break;
        }
     }
//--- clear the chart before exiting
   Comment("");
   /*
   result:
   Requested 4294967295 ticks to get tick history for the symbol 'EURUSD'
   The tick history for the 'EURUSD' symbol is received in the amount of 351199027 ticks in 55875 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.21 10:10:40.392
   
   The last 20 ticks for the standard symbol 'EURUSD':
     351199007th Tick: 2024.06.21 10:10:23.045 Bid=1.07032 (Info tick)
     351199008th Tick: 2024.06.21 10:10:24.045 Ask=1.07031 Bid=1.07031 (Info tick)
     351199009th Tick: 2024.06.21 10:10:24.545 Ask=1.07032 (Info tick)
     351199010th Tick: 2024.06.21 10:10:25.146 Bid=1.07032 (Info tick)
     351199011th Tick: 2024.06.21 10:10:25.649 Ask=1.07037 Bid=1.07037 (Info tick)
     351199012th Tick: 2024.06.21 10:10:27.050 Ask=1.07036 Bid=1.07036 (Info tick)
     351199013th Tick: 2024.06.21 10:10:28.153 Ask=1.07039 Bid=1.07039 (Info tick)
     351199014th Tick: 2024.06.21 10:10:29.157 Ask=1.07037 Bid=1.07037 (Info tick)
     351199015th Tick: 2024.06.21 10:10:29.658 Ask=1.07036 Bid=1.07036 (Info tick)
     351199016th Tick: 2024.06.21 10:10:30.258 Bid=1.07036 (Info tick)
     351199017th Tick: 2024.06.21 10:10:30.872 Ask=1.07035 Bid=1.07035 (Info tick)
     351199018th Tick: 2024.06.21 10:10:31.358 Ask=1.07036 (Info tick)
     351199019th Tick: 2024.06.21 10:10:31.859 Ask=1.07037 Bid=1.07037 (Info tick)
     351199020th Tick: 2024.06.21 10:10:32.377 Ask=1.07039 Bid=1.07039 (Info tick)
     351199021th Tick: 2024.06.21 10:10:32.962 Ask=1.0704 Bid=1.0704 (Info tick)
     351199022th Tick: 2024.06.21 10:10:33.961 Ask=1.07039 Bid=1.07039 (Info tick)
     351199023th Tick: 2024.06.21 10:10:34.667 Ask=1.0704 (Info tick)
     351199024th Tick: 2024.06.21 10:10:35.170 Bid=1.0704 (Info tick)
     351199025th Tick: 2024.06.21 10:10:38.266 Ask=1.07041 Bid=1.07041 (Info tick)
     351199026th Tick: 2024.06.21 10:10:40.392 Ask=1.07042 Bid=1.07042 (Info tick)
   ...
   Start of adding 351199027 ticks to the history of the custom symbol 'EURUSD.C'
   Added 351199027 ticks to the history of the custom symbol 'EURUSD.C' in 261594 ms
   ...
   Requested 351199027 ticks to get tick history for the symbol 'EURUSD.C'
   The tick history for the 'EURUSD.C' symbol is received in the amount of 351199027 ticks in 137156 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.21 10:10:40.392
   
   The last 20 ticks for the custom symbol 'EURUSD.C':
     351199007th Tick: 2024.06.21 10:10:23.045 Ask=1.07032 Bid=1.07032 (Info tick)
     351199008th Tick: 2024.06.21 10:10:24.045 Ask=1.07031 Bid=1.07031 (Info tick)
     351199009th Tick: 2024.06.21 10:10:24.545 Ask=1.07032 Bid=1.07032 (Info tick)
     351199010th Tick: 2024.06.21 10:10:25.146 Ask=1.07032 Bid=1.07032 (Info tick)
     351199011th Tick: 2024.06.21 10:10:25.649 Ask=1.07037 Bid=1.07037 (Info tick)
     351199012th Tick: 2024.06.21 10:10:27.050 Ask=1.07036 Bid=1.07036 (Info tick)
     351199013th Tick: 2024.06.21 10:10:28.153 Ask=1.07039 Bid=1.07039 (Info tick)
     351199014th Tick: 2024.06.21 10:10:29.157 Ask=1.07037 Bid=1.07037 (Info tick)
     351199015th Tick: 2024.06.21 10:10:29.658 Ask=1.07036 Bid=1.07036 (Info tick)
     351199016th Tick: 2024.06.21 10:10:30.258 Ask=1.07036 Bid=1.07036 (Info tick)
     351199017th Tick: 2024.06.21 10:10:30.872 Ask=1.07035 Bid=1.07035 (Info tick)
     351199018th Tick: 2024.06.21 10:10:31.358 Ask=1.07036 Bid=1.07036 (Info tick)
     351199019th Tick: 2024.06.21 10:10:31.859 Ask=1.07037 Bid=1.07037 (Info tick)
     351199020th Tick: 2024.06.21 10:10:32.377 Ask=1.07039 Bid=1.07039 (Info tick)
     351199021th Tick: 2024.06.21 10:10:32.962 Ask=1.0704 Bid=1.0704 (Info tick)
     351199022th Tick: 2024.06.21 10:10:33.961 Ask=1.07039 Bid=1.07039 (Info tick)
     351199023th Tick: 2024.06.21 10:10:34.667 Ask=1.0704 Bid=1.0704 (Info tick)
     351199024th Tick: 2024.06.21 10:10:35.170 Ask=1.0704 Bid=1.0704 (Info tick)
     351199025th Tick: 2024.06.21 10:10:38.266 Ask=1.07041 Bid=1.07041 (Info tick)
     351199026th Tick: 2024.06.21 10:10:40.392 Ask=1.07042 Bid=1.07042 (Info tick)
   ...
   Start deleting 10 ticks in the history of the custom symbol 'EURUSD.C'
   Deleted 10 ticks in the history of the custom symbol 'EURUSD.C' in 188 ms
   ...
   Requested 351199027 ticks to get tick history for the symbol 'EURUSD.C'
   The tick history for the 'EURUSD.C' symbol is received in the amount of 351199017 ticks in 138312 ms
   Time of the first tick from the changed history: 2011.12.19 00:00:08.000, Time of the last tick from the changed history: 2024.06.21 10:10:40.392
   
   The last 20 ticks of custom symbol 'EURUSD.C' with modified history:
     351198997th Tick: 2024.06.21 10:10:14.935 Ask=1.07036 Bid=1.07036 (Info tick)
     351198998th Tick: 2024.06.21 10:10:15.533 Ask=1.07035 Bid=1.07035 (Info tick)
     351198999th Tick: 2024.06.21 10:10:17.736 Ask=1.07036 Bid=1.07036 (Info tick)
     351199000th Tick: 2024.06.21 10:10:18.540 Ask=1.07037 Bid=1.07037 (Info tick)
     351199001th Tick: 2024.06.21 10:10:19.046 Ask=1.07038 Bid=1.07038 (Info tick)
     351199002th Tick: 2024.06.21 10:10:19.542 Ask=1.07036 Bid=1.07036 (Info tick)
     351199003th Tick: 2024.06.21 10:10:20.041 Ask=1.07035 Bid=1.07035 (Info tick)
     351199004th Tick: 2024.06.21 10:10:21.041 Ask=1.07035 Bid=1.07035 (Info tick)
     351199005th Tick: 2024.06.21 10:10:21.544 Ask=1.07032 Bid=1.07032 (Info tick)
     351199006th Tick: 2024.06.21 10:10:22.344 Ask=1.07032 Bid=1.07032 (Info tick)
     351199007th Tick: 2024.06.21 10:10:23.045 Ask=1.07032 Bid=1.07032 (Info tick)
     351199008th Tick: 2024.06.21 10:10:24.045 Ask=1.07031 Bid=1.07031 (Info tick)
     351199009th Tick: 2024.06.21 10:10:24.545 Ask=1.07032 Bid=1.07032 (Info tick)
     351199010th Tick: 2024.06.21 10:10:25.146 Ask=1.07032 Bid=1.07032 (Info tick)
     351199011th Tick: 2024.06.21 10:10:25.649 Ask=1.07037 Bid=1.07037 (Info tick)
     351199012th Tick: 2024.06.21 10:10:27.050 Ask=1.07036 Bid=1.07036 (Info tick)
     351199013th Tick: 2024.06.21 10:10:28.153 Ask=1.07039 Bid=1.07039 (Info tick)
     351199014th Tick: 2024.06.21 10:10:29.157 Ask=1.07037 Bid=1.07037 (Info tick)
     351199015th Tick: 2024.06.21 10:10:29.658 Ask=1.07036 Bid=1.07036 (Info tick)
     351199016th Tick: 2024.06.21 10:10:40.392 Ask=1.07042 Bid=1.07042 (Info tick)
   */
  }
//+------------------------------------------------------------------+
//| Create a custom symbol, return an error code                     |
//+------------------------------------------------------------------+
int CreateCustomSymbol(const string symbol_name, const string symbol_path, const string symbol_origin=NULL)
  {
//--- define the name of a symbol a custom one is to be based on
   string origin=(symbol_origin==NULL ? Symbol() : symbol_origin);
   
//--- if failed to create a custom symbol and this is not error 5304, report this in the journal
   ResetLastError();
   int error=0;
   if(!CustomSymbolCreate(symbol_name, symbol_path, origin))
     {
      error=GetLastError();
      if(error!=5304)
         PrintFormat("CustomSymbolCreate(%s, %s, %s) failed. Error %d", symbol_name, symbol_path, origin, error);
     }
//--- successful
   return(error);
  }
//+------------------------------------------------------------------+
//| Remove a custom symbol                                           |
//+------------------------------------------------------------------+
bool DeleteCustomSymbol(const string symbol_name)
  {
//--- hide the symbol from the Market Watch window
   ResetLastError();
   if(!SymbolSelect(symbol_name, false))
     {
      PrintFormat("SymbolSelect(%s, false) failed. Error %d", GetLastError());
      return(false);
     }
      
//--- if failed to delete a custom symbol, report this in the journal and return 'false'
   ResetLastError();
   if(!CustomSymbolDelete(symbol_name))
     {
      PrintFormat("CustomSymbolDelete(%s) failed. Error %d", symbol_name, GetLastError());
      return(false);
     }
//--- successful
   return(true);
  }
//+------------------------------------------------------------------+
//| Get the specified number of ticks in the array                   |
//+------------------------------------------------------------------+
bool GetTicksToArray(const string symbol, const uint count, MqlTick &array[])
  {
//--- notify of the start of loading historical data
   PrintFormat("Requested %u ticks to get tick history for the symbol '%s'", count, symbol);
   
//--- make 3 attempts to receive ticks 
   int attempts=0;
   while(attempts<3)
     {
      //--- measure the start time before receiving the ticks
      uint start=GetTickCount();
      
      //--- request the tick history since 1970.01.01 00:00.001 (parameter from=1 ms)
      int received=CopyTicks(symbol, array, COPY_TICKS_ALL, 1, count);
      if(received!=-1)
        {
         //--- display information about the number of ticks and spent time 
         PrintFormat("The tick history for the '%s' symbol is received in the amount of %u ticks in %d ms", symbol, received, GetTickCount()-start);
         
         //--- if the tick history is synchronized, the error code is equal to zero - return 'true'
         if(GetLastError()==0)
            return(true);
 
         PrintFormat("%s: Ticks are not synchronized yet, %d ticks received for %d ms. Error=%d", 
                     symbol, received, GetTickCount()-start, GetLastError());
        }
      //--- count attempts 
      attempts++; 
      //--- a one-second pause to wait for the end of synchronization of the tick database 
      Sleep(1000);
     }
//--- failed to copy ticks in 3 attempts
   return(false);
  }
//+------------------------------------------------------------------+ 
//| return the string description of a tick                          | 
//+------------------------------------------------------------------+ 
string GetTickDescription(MqlTick &tick) 
  { 
   string desc=StringFormat("%s.%03u ", TimeToString(tick.time, TIME_DATE|TIME_MINUTES|TIME_SECONDS),tick.time_msc%1000);
   
//--- check tick flags
   bool buy_tick   = ((tick.flags &TICK_FLAG_BUY)   == TICK_FLAG_BUY); 
   bool sell_tick  = ((tick.flags &TICK_FLAG_SELL)  == TICK_FLAG_SELL); 
   bool ask_tick   = ((tick.flags &TICK_FLAG_ASK)   == TICK_FLAG_ASK); 
   bool bid_tick   = ((tick.flags &TICK_FLAG_BID)   == TICK_FLAG_BID); 
   bool last_tick  = ((tick.flags &TICK_FLAG_LAST)  == TICK_FLAG_LAST); 
   bool volume_tick= ((tick.flags &TICK_FLAG_VOLUME)== TICK_FLAG_VOLUME); 
   
//--- check the tick for trading flags first (there are none for CustomTicksAdd())
   if(buy_tick || sell_tick) 
     { 
      //--- form an output for a trading tick 
      desc += (buy_tick ? StringFormat("Buy Tick: Last=%G Volume=%d ", tick.last, tick.volume)  : ""); 
      desc += (sell_tick? StringFormat("Sell Tick: Last=%G Volume=%d ",tick.last, tick.volume) : ""); 
      desc += (ask_tick ? StringFormat("Ask=%G ", tick.ask) : ""); 
      desc += (bid_tick ? StringFormat("Bid=%G ", tick.ask) : ""); 
      desc += "(Trade tick)"; 
     } 
   else 
     { 
      //--- form an output for an info tick a bit differently 
      desc += (ask_tick   ? StringFormat("Ask=%G ",  tick.ask)    : ""); 
      desc += (bid_tick   ? StringFormat("Bid=%G ",  tick.ask)    : ""); 
      desc += (last_tick  ? StringFormat("Last=%G ", tick.last)   : ""); 
      desc += (volume_tick? StringFormat("Volume=%d ",tick.volume): ""); 
      desc += "(Info tick)"; 
     } 
//--- return tick description 
   return(desc); 
  } 

```

See also

[CustomRatesDelete](/en/docs/customsymbols/customratesdelete), [CustomRatesUpdate](/en/docs/customsymbols/customratesupdate), [CustomTicksReplace](/en/docs/customsymbols/customticksreplace), [CopyTicks](/en/docs/series/copyticks), [CopyTicksRange](/en/docs/series/copyticksrange)
