# CustomRatesDelete

Deletes all bars from the price history of the custom symbol in the specified time interval.

```
int  CustomRatesDelete(
   const string     symbol,       // symbol name
   datetime         from,         // start date
   datetime         to            // end date
   );

```

Parameters

symbol

[in]  Custom symbol name.

from

[in]  Time of the first bar in the price history within the specified range to be removed.

to

[in]  Time of the last bar in the price history within the specified range to be removed.

Return Value

Number of deleted bars or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Example:

```
//+------------------------------------------------------------------+
//|                                            CustomRatesDelete.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   CUSTOM_SYMBOL_NAME     Symbol()+".C"     // custom symbol name
#define   CUSTOM_SYMBOL_PATH     "Forex"           // name of the group, in which a symbol is to be created
#define   CUSTOM_SYMBOL_ORIGIN   Symbol()          // name of a symbol a custom one is to be based on
 
#define   DATARATES_COUNT        4                 // number of bars sent to the journal
 
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
 
//--- get the number of standard symbol bars
   int bars=Bars(CUSTOM_SYMBOL_ORIGIN, PERIOD_M1);
      
//--- get the data of all bars of the standard symbol minute timeframe into the MqlRates array
   MqlRates rates[]={};
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_ORIGIN, PERIOD_M1, 0, bars, rates)!=bars)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_ORIGIN, bars, GetLastError());
      return;
     }
 
//--- set the copied data to the minute history of the custom symbol
   ResetLastError();
   if(CustomRatesUpdate(CUSTOM_SYMBOL_NAME, rates)<0)
     {
      PrintFormat("CustomRatesUpdate(%s) failed. Error %d", CUSTOM_SYMBOL_NAME, GetLastError());
      return;
     }
     
//--- after updating the historical data, get the number of custom symbol bars
   bars=Bars(CUSTOM_SYMBOL_NAME, PERIOD_M1);
   
//--- get the data of all bars of the custom symbol minute timeframe into the MqlRates array
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_NAME, PERIOD_M1, 0, bars, rates)!=bars)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_NAME, bars, GetLastError());
      return;
     }
 
//--- print the last DATARATES_COUNT bars of the custom symbol minute history in the journal
   int digits=(int)SymbolInfoInteger(CUSTOM_SYMBOL_NAME, SYMBOL_DIGITS);
   PrintFormat("Last %d bars of the custom symbol's minute history:", DATARATES_COUNT);
   ArrayPrint(rates, digits, NULL, bars-DATARATES_COUNT, DATARATES_COUNT);
   
//--- delete the two penultimate data bars in the custom symbol minute history
   datetime time_from= rates[bars-3].time;
   datetime time_to  = rates[bars-2].time;
   ResetLastError();
   int deleted=CustomRatesDelete(CUSTOM_SYMBOL_NAME, time_from, time_to);
   if(deleted<0)
     {
      PrintFormat("CustomRatesDelete(%s) failed. Error %d", CUSTOM_SYMBOL_NAME, GetLastError());
      return;
     }
     
//--- after deleting two bars of historical data, get the number of custom symbol bars again
   bars=Bars(CUSTOM_SYMBOL_NAME, PERIOD_M1);
   
//--- get the data of all remaining bars of the custom symbol minute timeframe again
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_NAME, PERIOD_M1, 0, bars, rates)!=bars)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_NAME, bars, GetLastError());
      return;
     }
 
//--- print the last DATARATES_COUNT bars of the updated custom symbol minute history in the journal
   PrintFormat("\nLast %d bars after applying CustomRatesDelete() with %d deleted bars:", DATARATES_COUNT, deleted);
   ArrayPrint(rates, digits, NULL, bars-DATARATES_COUNT, DATARATES_COUNT);
     
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
   Last 4 bars of the custom symbol's minute history:
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2024.06.18 20:53:00 1.07341 1.07347 1.07336 1.07343            38        0             0
   [1] 2024.06.18 20:54:00 1.07344 1.07354 1.07344 1.07353            21        0             0
   [2] 2024.06.18 20:55:00 1.07353 1.07362 1.07351 1.07356            32        0             0
   [3] 2024.06.18 20:56:00 1.07356 1.07358 1.07352 1.07354            24        0             0
   
   Last 4 bars after applying CustomRatesDelete() with 2 deleted bars:
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2024.06.18 20:51:00 1.07357 1.07358 1.07347 1.07349            25        0             0
   [1] 2024.06.18 20:52:00 1.07349 1.07350 1.07336 1.07341            31        0             0
   [2] 2024.06.18 20:53:00 1.07341 1.07347 1.07336 1.07343            38        0             0
   [3] 2024.06.18 20:56:00 1.07356 1.07358 1.07352 1.07354            24        0             0
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

```

See also

[CustomRatesReplace](/en/docs/customsymbols/customratesreplace), [CustomRatesUpdate](/en/docs/customsymbols/customratesupdate), [CopyRates](/en/docs/series/copyrates)
