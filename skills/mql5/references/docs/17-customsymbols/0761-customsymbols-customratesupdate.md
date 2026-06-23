# CustomRatesUpdate

Adds missing bars to the custom symbol history and replaces existing data with  the ones from the [MqlRates](/en/docs/constants/structures/mqlrates) type array.

```
int  CustomRatesUpdate(
   const string     symbol,             // custom symbol name
   const MqlRates&  rates[],            // array for the data to be applied to a custom symbol
   uint             count=WHOLE_ARRAY   // number of the rates[] array elements to be used
   );

```

Parameters

symbol

[in]  Custom symbol name.

rates[]

[in]  Array of the [MqlRates](/en/docs/constants/structures/mqlrates) type history data for M1.

count=WHOLE_ARRAY

[in]  Number of the rates[] array elements to be used for update. [WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants) means that all rates[] array elements should be used.

Return Value

Number of updated bars or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If there is no bar from the rates[] array in the current custom symbol history, it is added.  If such a bar already exists, it is replaced. All other bars in the current price history remain unchanged. The rates[] array data should be correct regarding OHLC prices, while the bars opening time should correspond to the M1 [timeframe](/en/docs/constants/chartconstants/enum_timeframes).

Example:

```
//+------------------------------------------------------------------+
//|                                            CustomRatesUpdate.mq5 |
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
 
//--- get and print in the journal the number of standard symbol bars
   int bars_origin=Bars(CUSTOM_SYMBOL_ORIGIN, PERIOD_M1);
   PrintFormat("The symbol '%s' from which the custom '%s' was created has %d bars of minute history.", CUSTOM_SYMBOL_ORIGIN, CUSTOM_SYMBOL_NAME, bars_origin);
      
//--- get and print in the journal the number of custom symbol bars
   int bars_custom=Bars(CUSTOM_SYMBOL_NAME, PERIOD_M1);
   PrintFormat("Custom symbol '%s' created from symbol '%s' has %d bars of minute history", CUSTOM_SYMBOL_NAME, CUSTOM_SYMBOL_ORIGIN, bars_custom);
      
//--- get the data of all bars of the standard symbol minute timeframe into the MqlRates array
   MqlRates rates[]={};
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_ORIGIN, PERIOD_M1, 0, bars_origin, rates)!=bars_origin)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_ORIGIN, bars_origin, GetLastError());
      return;
     }
 
//--- set the copied data to the minute history of the custom symbol
   ResetLastError();
   int updated=CustomRatesUpdate(CUSTOM_SYMBOL_NAME, rates);
   if(updated<0)
     {
      PrintFormat("CustomRatesUpdate(%s) failed. Error %d", CUSTOM_SYMBOL_NAME, GetLastError());
      return;
     }
 
//--- get and print in the journal the number of custom symbol bars after adding history
   bars_custom=Bars(CUSTOM_SYMBOL_NAME, PERIOD_M1);
   PrintFormat("\nAfter CustomRatesUpdate(), the custom symbol '%s' has %d bars of minute history", CUSTOM_SYMBOL_NAME, bars_custom);
 
//--- get the data of all bars of the custom symbol minute timeframe into the MqlRates array
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_NAME, PERIOD_M1, 0, bars_custom, rates)!=bars_custom)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_NAME, bars_custom, GetLastError());
      return;
     }
 
//--- print the last four bars of the custom symbol minute history in the journal
   int digits=(int)SymbolInfoInteger(CUSTOM_SYMBOL_NAME, SYMBOL_DIGITS);
   PrintFormat("Last %d bars of the custom symbol's minute history:", DATARATES_COUNT);
   ArrayPrint(rates, digits, NULL, bars_custom-DATARATES_COUNT, DATARATES_COUNT);
   
//--- replace the data in the MqlRates array with the one calculated using the equation 1.0 / SymbolName
   for(int i=0; i<bars_custom; i++)
     {
      rates[i].open  =(rates[i].open !=0  ? 1.0 / rates[i].open  : rates[i].open);
      rates[i].high  =(rates[i].high !=0  ? 1.0 / rates[i].high  : rates[i].high);
      rates[i].low   =(rates[i].low  !=0  ? 1.0 / rates[i].low   : rates[i].low);
      rates[i].close =(rates[i].close!=0  ? 1.0 / rates[i].close : rates[i].close);
     }
 
//--- set the modified data to the minute history of the custom symbol
   ResetLastError();
   updated=CustomRatesUpdate(CUSTOM_SYMBOL_NAME, rates);
   if(updated<0)
     {
      PrintFormat("CustomRatesUpdate(%s) failed. Error %d", CUSTOM_SYMBOL_NAME, GetLastError());
      return;
     }
 
//--- get the data of all bars of the custom symbol minute timeframe into the MqlRates array again
   ResetLastError();
   if(CopyRates(CUSTOM_SYMBOL_NAME, PERIOD_M1, 0, bars_custom, rates)!=bars_custom)
     {
      PrintFormat("CopyRates(%s, PERIOD_M1, 0, %d) failed. Error %d", CUSTOM_SYMBOL_NAME, bars_custom, GetLastError());
      return;
     }
 
//--- print the last four bars of the updated custom symbol minute history in the journal
   Print("\nLast %d bars after changing the custom symbol calculation formula:", DATARATES_COUNT);
   ArrayPrint(rates, digits, NULL, bars_custom-DATARATES_COUNT, DATARATES_COUNT);
   
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
   The symbol 'EURUSD' from which the custom 'EURUSD.C' was created has 250488 bars of minute history.
   Custom symbol 'EURUSD.C' created from symbol 'EURUSD' has 0 bars of minute history
   
   After CustomRatesUpdate(), the custom symbol 'EURUSD.C' has 250488 bars of minute history
   Last 4 bars of the custom symbol's minute history:
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2024.06.18 11:14:00 1.07235 1.07239 1.07232 1.07239            24        0             0
   [1] 2024.06.18 11:15:00 1.07238 1.07239 1.07232 1.07235            44        0             0
   [2] 2024.06.18 11:16:00 1.07234 1.07238 1.07227 1.07234            37        0             0
   [3] 2024.06.18 11:17:00 1.07234 1.07234 1.07217 1.07225            41        0             0
   
   Last 4 bars after changing the custom symbol calculation formula:
                    [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
   [0] 2024.06.18 11:14:00 0.93253 0.93250 0.93256 0.93250            24        0             0
   [1] 2024.06.18 11:15:00 0.93251 0.93250 0.93256 0.93253            44        0             0
   [2] 2024.06.18 11:16:00 0.93254 0.93251 0.93260 0.93254            37        0             0
   [3] 2024.06.18 11:17:00 0.93254 0.93254 0.93269 0.93262            41        0             0
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

[CustomRatesReplace](/en/docs/customsymbols/customratesreplace), [CustomRatesDelete](/en/docs/customsymbols/customratesdelete), [CopyRates](/en/docs/series/copyrates)
