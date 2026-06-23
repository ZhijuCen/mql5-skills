# CustomTicksReplace

Fully replaces the price history of the custom symbol within the specified time interval with the data from the [MqlTick](/en/docs/constants/structures/mqltick) type array.

```
int  CustomTicksReplace(
   const string     symbol,            // symbol name
   long             from_msc,          // start date
   long             to_msc,            // end date
   const MqlTick&   ticks[],           // array for the data to be applied to a custom symbol
   uint             count=WHOLE_ARRAY  // number of the ticks[] array elements to be used
   );

```

Parameters

symbol

[in]  Custom symbol name.

from_msc

[in]  Time of the first tick in the price history within the specified range to be removed. Time in milliseconds since 01.01.1970.

to_msc

[in]  Time of the last tick in the price history within the specified range to be removed. Time in milliseconds since 01.01.1970.

ticks[]

[in]   Array of the [MqlTick](/en/docs/constants/structures/mqltick) type tick data ordered in time in ascending order.

count=WHOLE_ARRAY

[in]  Number of the ticks[] array elements to be used for replacement in the specified time interval. [WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants) means that all ticks[] array elements should be used.

Return Value

Number of updated ticks or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Since several ticks may often have the same time up to a millisecond in a stream of quotes (accurate tick time is stored in the time_msc field of the [MqlTick](/en/docs/constants/structures/mqltick) structure), the CustomTicksReplace function does not automatically sort out the ticks[] array elements by time. Therefore, the array of ticks must be pre-arranged in time ascending order.

The ticks are replaced consecutively, day after day, until the time specified in to_msc or until an error occurs. The first day from the specified range is processed followed by the next one, etc.  As soon as the mismatch between the tick time and the ascending (non-descending) order is detected, the tick replacement stops on the current day. All ticks from the previous days are successfully replaced, while the current day (at the moment of a wrong tick) and all the remaining days in the specified interval remain unchanged.

If the ticks[] array contains no tick data for any day (generally, any time interval), a "hole" corresponding to the missing data appears in the custom symbol history after the tick data from ticks[] are applied. In other words, the call of CustomTicksReplace with missing ticks is equivalent to deleting part of the tick history, as if [CustomTicksDelete](/en/docs/customsymbols/customticksdelete) with the "hole" interval is called.

If the tick database has no data for the specified time interval, CustomTicksReplace will add to the database ticks form the ticks[] array.

The CustomTicksReplace function works directly with the tick database.

Example:

```
//+------------------------------------------------------------------+
//|                                           CustomTicksReplace.mq5 |
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
 
//--- now change Ask and Bid tick values in the array using the equation Ask(Symbol) = 1.0 / Ask(Symbol), Bid(Symbol) = 1.0 / Bid(Symbol)
   for(int i=0; i<total; i++)
     {
      array[i].ask = (array[i].ask !=0 ? 1.0 / array[i].ask : array[i].ask);
      array[i].bid = (array[i].bid !=0 ? 1.0 / array[i].bid : array[i].bid);
     }
   Print("\nNow the ticks are changed");
 
//--- replace the tick history of the custom symbol with data from the modified array of ticks
   Print("...");
   start=GetTickCount();
   PrintFormat("Start replacing %u changed ticks in the history of the custom symbol '%s'", array.Size(), CUSTOM_SYMBOL_NAME);
   int replaced=CustomTicksReplace(CUSTOM_SYMBOL_NAME, array[0].time_msc, array[total-1].time_msc, array);
   PrintFormat("Replaced %u ticks in the history of the custom symbol '%s' in %u ms", replaced, CUSTOM_SYMBOL_NAME, GetTickCount()-start);
   
//--- get the newly replaced custom symbol tick data to the MqlTick array
   Print("...");
   if(!GetTicksToArray(CUSTOM_SYMBOL_NAME, array.Size(), array))
      return;
   
//--- print the time of the first and last received modified ticks of the custom symbol
   total=(int)array.Size();
   PrintFormat("First changed tick time: %s.%03u, Last changed tick time: %s.%03u",
               TimeToString(array[0].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[0].time_msc%1000,
               TimeToString(array[total-1].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[total-1].time_msc%1000);
               
//--- print DATATICKS_TO_PRINT last modified ticks of the custom symbol in the journal
   PrintFormat("\nThe last %d changed ticks for the custom symbol '%s':", DATATICKS_TO_PRINT, CUSTOM_SYMBOL_NAME);
   for(int i=total-DATATICKS_TO_PRINT; i<total; i++)
     {
      if(i<0)
         continue;
      PrintFormat("  %dth Changed tick: %s", i, GetTickDescription(array[i]));
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
   The tick history for the 'EURUSD' symbol is received in the amount of 351195822 ticks in 55735 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.21 08:39:03.113
   
   The last 20 ticks for the standard symbol 'EURUSD':
     351195802th Tick: 2024.06.21 08:38:10.076 Ask=1.07194 (Info tick)
     351195803th Tick: 2024.06.21 08:38:13.162 Ask=1.07195 (Info tick)
     351195804th Tick: 2024.06.21 08:38:13.872 Bid=1.07195 (Info tick)
     351195805th Tick: 2024.06.21 08:38:14.866 Ask=1.07194 Bid=1.07194 (Info tick)
     351195806th Tick: 2024.06.21 08:38:17.374 Bid=1.07194 (Info tick)
     351195807th Tick: 2024.06.21 08:38:18.883 Bid=1.07194 (Info tick)
     351195808th Tick: 2024.06.21 08:38:19.771 Bid=1.07194 (Info tick)
     351195809th Tick: 2024.06.21 08:38:20.873 Ask=1.07195 Bid=1.07195 (Info tick)
     351195810th Tick: 2024.06.21 08:38:22.278 Ask=1.07196 Bid=1.07196 (Info tick)
     351195811th Tick: 2024.06.21 08:38:22.775 Bid=1.07196 (Info tick)
     351195812th Tick: 2024.06.21 08:38:23.477 Bid=1.07196 (Info tick)
     351195813th Tick: 2024.06.21 08:38:38.194 Ask=1.07197 (Info tick)
     351195814th Tick: 2024.06.21 08:38:38.789 Ask=1.07196 (Info tick)
     351195815th Tick: 2024.06.21 08:38:39.290 Ask=1.07197 (Info tick)
     351195816th Tick: 2024.06.21 08:38:43.695 Ask=1.07196 (Info tick)
     351195817th Tick: 2024.06.21 08:38:52.203 Ask=1.07195 Bid=1.07195 (Info tick)
     351195818th Tick: 2024.06.21 08:38:55.105 Ask=1.07196 Bid=1.07196 (Info tick)
     351195819th Tick: 2024.06.21 08:38:57.607 Ask=1.07195 Bid=1.07195 (Info tick)
     351195820th Tick: 2024.06.21 08:39:00.512 Ask=1.07196 Bid=1.07196 (Info tick)
     351195821th Tick: 2024.06.21 08:39:03.113 Ask=1.07195 Bid=1.07195 (Info tick)
   ...
   Start of adding 351195822 ticks to the history of the custom symbol 'EURUSD.C'
   Added 351195822 ticks to the history of the custom symbol 'EURUSD.C' in 349407 ms
   ...
   Requested 351195822 ticks to get tick history for the symbol 'EURUSD.C'
   The tick history for the 'EURUSD.C' symbol is received in the amount of 351195822 ticks in 190203 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.21 08:39:03.113
   
   The last 20 ticks for the custom symbol 'EURUSD.C':
     351195802th Tick: 2024.06.21 08:38:10.076 Ask=1.07194 Bid=1.07194 (Info tick)
     351195803th Tick: 2024.06.21 08:38:13.162 Ask=1.07195 Bid=1.07195 (Info tick)
     351195804th Tick: 2024.06.21 08:38:13.872 Ask=1.07195 Bid=1.07195 (Info tick)
     351195805th Tick: 2024.06.21 08:38:14.866 Ask=1.07194 Bid=1.07194 (Info tick)
     351195806th Tick: 2024.06.21 08:38:17.374 Ask=1.07194 Bid=1.07194 (Info tick)
     351195807th Tick: 2024.06.21 08:38:18.883 Ask=1.07194 Bid=1.07194 (Info tick)
     351195808th Tick: 2024.06.21 08:38:19.771 Ask=1.07194 Bid=1.07194 (Info tick)
     351195809th Tick: 2024.06.21 08:38:20.873 Ask=1.07195 Bid=1.07195 (Info tick)
     351195810th Tick: 2024.06.21 08:38:22.278 Ask=1.07196 Bid=1.07196 (Info tick)
     351195811th Tick: 2024.06.21 08:38:22.775 Ask=1.07196 Bid=1.07196 (Info tick)
     351195812th Tick: 2024.06.21 08:38:23.477 Ask=1.07196 Bid=1.07196 (Info tick)
     351195813th Tick: 2024.06.21 08:38:38.194 Ask=1.07197 Bid=1.07197 (Info tick)
     351195814th Tick: 2024.06.21 08:38:38.789 Ask=1.07196 Bid=1.07196 (Info tick)
     351195815th Tick: 2024.06.21 08:38:39.290 Ask=1.07197 Bid=1.07197 (Info tick)
     351195816th Tick: 2024.06.21 08:38:43.695 Ask=1.07196 Bid=1.07196 (Info tick)
     351195817th Tick: 2024.06.21 08:38:52.203 Ask=1.07195 Bid=1.07195 (Info tick)
     351195818th Tick: 2024.06.21 08:38:55.105 Ask=1.07196 Bid=1.07196 (Info tick)
     351195819th Tick: 2024.06.21 08:38:57.607 Ask=1.07195 Bid=1.07195 (Info tick)
     351195820th Tick: 2024.06.21 08:39:00.512 Ask=1.07196 Bid=1.07196 (Info tick)
     351195821th Tick: 2024.06.21 08:39:03.113 Ask=1.07195 Bid=1.07195 (Info tick)
   
   Now the ticks are changed
   ...
   Start replacing 351195822 changed ticks in the history of the custom symbol 'EURUSD.C'
   Replaced 351195822 ticks in the history of the custom symbol 'EURUSD.C' in 452266 ms
   ...
   Requested 351195822 ticks to get tick history for the symbol 'EURUSD.C'
   The tick history for the 'EURUSD.C' symbol is received in the amount of 351195822 ticks in 199812 ms
   First changed tick time: 2011.12.19 00:00:08.000, Last changed tick time: 2024.06.21 08:39:03.113
   
   The last 20 changed ticks for the custom symbol 'EURUSD.C':
     351195802th Changed tick: 2024.06.21 08:38:10.076 Ask=0.93289 Bid=0.93289 (Info tick)
     351195803th Changed tick: 2024.06.21 08:38:13.162 Ask=0.93288 Bid=0.93288 (Info tick)
     351195804th Changed tick: 2024.06.21 08:38:13.872 Ask=0.93288 Bid=0.93288 (Info tick)
     351195805th Changed tick: 2024.06.21 08:38:14.866 Ask=0.93289 Bid=0.93289 (Info tick)
     351195806th Changed tick: 2024.06.21 08:38:17.374 Ask=0.93289 Bid=0.93289 (Info tick)
     351195807th Changed tick: 2024.06.21 08:38:18.883 Ask=0.93289 Bid=0.93289 (Info tick)
     351195808th Changed tick: 2024.06.21 08:38:19.771 Ask=0.93289 Bid=0.93289 (Info tick)
     351195809th Changed tick: 2024.06.21 08:38:20.873 Ask=0.93288 Bid=0.93288 (Info tick)
     351195810th Changed tick: 2024.06.21 08:38:22.278 Ask=0.93287 Bid=0.93287 (Info tick)
     351195811th Changed tick: 2024.06.21 08:38:22.775 Ask=0.93287 Bid=0.93287 (Info tick)
     351195812th Changed tick: 2024.06.21 08:38:23.477 Ask=0.93287 Bid=0.93287 (Info tick)
     351195813th Changed tick: 2024.06.21 08:38:38.194 Ask=0.93286 Bid=0.93286 (Info tick)
     351195814th Changed tick: 2024.06.21 08:38:38.789 Ask=0.93287 Bid=0.93287 (Info tick)
     351195815th Changed tick: 2024.06.21 08:38:39.290 Ask=0.93286 Bid=0.93286 (Info tick)
     351195816th Changed tick: 2024.06.21 08:38:43.695 Ask=0.93287 Bid=0.93287 (Info tick)
     351195817th Changed tick: 2024.06.21 08:38:52.203 Ask=0.93288 Bid=0.93288 (Info tick)
     351195818th Changed tick: 2024.06.21 08:38:55.105 Ask=0.93287 Bid=0.93287 (Info tick)
     351195819th Changed tick: 2024.06.21 08:38:57.607 Ask=0.93288 Bid=0.93288 (Info tick)
     351195820th Changed tick: 2024.06.21 08:39:00.512 Ask=0.93287 Bid=0.93287 (Info tick)
     351195821th Changed tick: 2024.06.21 08:39:03.113 Ask=0.93288 Bid=0.93288 (Info tick)
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

[CustomRatesDelete](/en/docs/customsymbols/customratesdelete), [CustomRatesUpdate](/en/docs/customsymbols/customratesupdate), [CustomTicksDelete](/en/docs/customsymbols/customticksdelete), [CopyTicks](/en/docs/series/copyticks), [CopyTicksRange](/en/docs/series/copyticksrange)
