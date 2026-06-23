# CustomTicksAdd

Adds data from an array of the [MqlTick](/en/docs/constants/structures/mqltick) type to the price history of a custom symbol. The custom symbol must be [selected](/en/docs/marketinformation/symbolselect) in the Market Watch window.

```
int  CustomTicksAdd(
   const string     symbol,             // Symbol name
   const MqlTick&   ticks[],            // The array with tick data that should be applied to the custom symbol
   uint             count=WHOLE_ARRAY   // number of the ticks[] array elements to be used
   );

```

Parameters

symbol

[in]  The name of the custom symbol.

ticks[]

[in]   An array of tick data of the [MqlTick](/en/docs/constants/structures/mqltick) type arranged in order of time from earlier data to more recent ones, i.e. ticks[k].time_msc <= ticks[n].time_msc, if k<n.

count=WHOLE_ARRAY

[in]  Number of the ticks[] array elements to be used for adding. [WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants) means that all ticks[] array elements should be used.

Return Value

The number of added ticks or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Further Note

The CustomTicksAdd function only works for custom symbols opened in the Market Watch window. If the symbol is not selected in Market Watch, then you should add ticks using [CustomTicksReplace](/en/docs/customsymbols/customticksreplace).

The CustomTicksAdd function allows transmitting ticks as if they are delivered from the broker's server. Data are sent to the Market Watch window instead of being written directly to the tick database. The terminal then saves ticks from the Market Watch to a database. If the amount of data transmitted during one function call is large, the behavior of the function changes in order to reduce resource usage. If more than 256 ticks are passed, data is divided into two parts. The first, i.e. the larger part is written directly to the tick database (as it is done in [CustomTicksReplace](/en/docs/customsymbols/customticksreplace)). The second part containing 128 ticks is passed to the Market Watch window, from which the terminal saves the ticks to a database.

The [MqlTick](/en/docs/constants/structures/mqltick) structure has two fields with the time value: time (the tick time in seconds) and  time_msc (the tick time in milliseconds), which are counted from January 1, 1970. These fields in the added ticks are processed in the following order:

1. If ticks[k].time_msc!=0, we use it to fill the ticks[k].time field, i.e. ticks[k].time=ticks[k].time_msc/1000 (integer division) is set for the tick
2. If ticks[k].time_msc==0 and ticks[k].time!=0, time in milliseconds is obtained by multiplying by 1000, i.e. ticks[k].time_msc=ticks[k].time*1000
3. If ticks[k].time_msc==0 and ticks[k].time==0, the current [trade server time](/en/docs/dateandtime/timetradeserver) up to a millisecond as of the moment of CustomTicksAdd call is written to these fields.

If the value of ticks[k].bid, ticks[k].ask, ticks[k].last or ticks[k].volume is greater than zero, a combination of appropriate flags is written to the ticks[k].flags field:

- TICK_FLAG_BID – the tick has changed the bid price
- TICK_FLAG_ASK  – the tick has changed the ask price
- TICK_FLAG_LAST – the tick has changed the last deal price
- TICK_FLAG_VOLUME – the tick has changed the volume

If the value of a field is less than or equal to zero, the corresponding flag is not written to the ticks[k].flags field.

Flags TICK_FLAG_BUY and TICK_FLAG_SELL are not added to the history of a custom symbol.

Example:

```
//+------------------------------------------------------------------+
//|                                               CustomTicksAdd.mq5 |
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
               TimeToString(array[0].time, TIME_DATE|TIME_MINUTES|TIME_SECONDS), array[0].time_msc%1000,
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
   
//--- get the custom symbol tick data to the MqlTick array
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
   Requested 4294967295 ticks to download tick history for the symbol 'EURUSD'
   The tick history for the 'EURUSD' symbol is received in the amount of 351183943 ticks in 56454 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.20 21:18:12.010
   
   The last 20 ticks for the standard symbol 'EURUSD':
     351183923th Tick: 2024.06.20 21:17:46.380 Bid=1.07124 (Info tick)
     351183924th Tick: 2024.06.20 21:17:47.779 Ask=1.07125 Bid=1.07125 (Info tick)
     351183925th Tick: 2024.06.20 21:17:48.584 Ask=1.07124 Bid=1.07124 (Info tick)
     351183926th Tick: 2024.06.20 21:17:49.481 Ask=1.07125 (Info tick)
     351183927th Tick: 2024.06.20 21:17:49.985 Ask=1.07122 Bid=1.07122 (Info tick)
     351183928th Tick: 2024.06.20 21:17:50.482 Ask=1.07124 Bid=1.07124 (Info tick)
     351183929th Tick: 2024.06.20 21:17:51.584 Ask=1.07123 Bid=1.07123 (Info tick)
     351183930th Tick: 2024.06.20 21:17:52.786 Ask=1.07124 Bid=1.07124 (Info tick)
     351183931th Tick: 2024.06.20 21:17:53.487 Ask=1.07125 Bid=1.07125 (Info tick)
     351183932th Tick: 2024.06.20 21:17:53.989 Ask=1.07126 Bid=1.07126 (Info tick)
     351183933th Tick: 2024.06.20 21:17:55.789 Ask=1.07125 Bid=1.07125 (Info tick)
     351183934th Tick: 2024.06.20 21:17:58.495 Ask=1.07126 Bid=1.07126 (Info tick)
     351183935th Tick: 2024.06.20 21:18:00.102 Bid=1.07126 (Info tick)
     351183936th Tick: 2024.06.20 21:18:00.698 Ask=1.07129 Bid=1.07129 (Info tick)
     351183937th Tick: 2024.06.20 21:18:03.699 Bid=1.07129 (Info tick)
     351183938th Tick: 2024.06.20 21:18:04.699 Ask=1.07128 Bid=1.07128 (Info tick)
     351183939th Tick: 2024.06.20 21:18:05.901 Ask=1.07129 Bid=1.07129 (Info tick)
     351183940th Tick: 2024.06.20 21:18:07.606 Ask=1.07128 Bid=1.07128 (Info tick)
     351183941th Tick: 2024.06.20 21:18:11.512 Ask=1.07127 Bid=1.07127 (Info tick)
     351183942th Tick: 2024.06.20 21:18:12.010 Ask=1.07126 Bid=1.07126 (Info tick)
   ...
   Start of adding 351183943 ticks to the history of the custom symbol 'EURUSD.C'
   Added 351183943 ticks to the history of the custom symbol 'EURUSD.C' in 269890 ms
   ...
   Requested 351183943 ticks to download tick history for the symbol 'EURUSD.C'
   The tick history for the 'EURUSD.C' symbol is received in the amount of 351183943 ticks in 116407 ms
   First tick time: 2011.12.19 00:00:08.000, Last tick time: 2024.06.20 21:18:12.010
   
   The last 20 ticks for the custom symbol 'EURUSD.C':
     351183923th Tick: 2024.06.20 21:17:46.380 Ask=1.07124 Bid=1.07124 (Info tick)
     351183924th Tick: 2024.06.20 21:17:47.779 Ask=1.07125 Bid=1.07125 (Info tick)
     351183925th Tick: 2024.06.20 21:17:48.584 Ask=1.07124 Bid=1.07124 (Info tick)
     351183926th Tick: 2024.06.20 21:17:49.481 Ask=1.07125 Bid=1.07125 (Info tick)
     351183927th Tick: 2024.06.20 21:17:49.985 Ask=1.07122 Bid=1.07122 (Info tick)
     351183928th Tick: 2024.06.20 21:17:50.482 Ask=1.07124 Bid=1.07124 (Info tick)
     351183929th Tick: 2024.06.20 21:17:51.584 Ask=1.07123 Bid=1.07123 (Info tick)
     351183930th Tick: 2024.06.20 21:17:52.786 Ask=1.07124 Bid=1.07124 (Info tick)
     351183931th Tick: 2024.06.20 21:17:53.487 Ask=1.07125 Bid=1.07125 (Info tick)
     351183932th Tick: 2024.06.20 21:17:53.989 Ask=1.07126 Bid=1.07126 (Info tick)
     351183933th Tick: 2024.06.20 21:17:55.789 Ask=1.07125 Bid=1.07125 (Info tick)
     351183934th Tick: 2024.06.20 21:17:58.495 Ask=1.07126 Bid=1.07126 (Info tick)
     351183935th Tick: 2024.06.20 21:18:00.102 Ask=1.07126 Bid=1.07126 (Info tick)
     351183936th Tick: 2024.06.20 21:18:00.698 Ask=1.07129 Bid=1.07129 (Info tick)
     351183937th Tick: 2024.06.20 21:18:03.699 Ask=1.07129 Bid=1.07129 (Info tick)
     351183938th Tick: 2024.06.20 21:18:04.699 Ask=1.07128 Bid=1.07128 (Info tick)
     351183939th Tick: 2024.06.20 21:18:05.901 Ask=1.07129 Bid=1.07129 (Info tick)
     351183940th Tick: 2024.06.20 21:18:07.606 Ask=1.07128 Bid=1.07128 (Info tick)
     351183941th Tick: 2024.06.20 21:18:11.512 Ask=1.07127 Bid=1.07127 (Info tick)
     351183942th Tick: 2024.06.20 21:18:12.010 Ask=1.07126 Bid=1.07126 (Info tick)
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
