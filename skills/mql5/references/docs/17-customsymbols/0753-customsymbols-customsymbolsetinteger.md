# CustomSymbolSetInteger

Sets the integer type property value for a custom symbol.

```
bool  CustomSymbolSetInteger(
   const string              symbol_name,      // symbol name
   ENUM_SYMBOL_INFO_INTEGER  property_id,      // property ID
   long                      property_value    // property value
   );

```

Parameters

symbol_name

[in]  Custom symbol name.

property_id

[in]  Symbol property ID. The value can be one of the values of the [ENUM_SYMBOL_INFO_INTEGER](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer) enumeration.

property_value

[in]  A long type variable containing the property value.

Return Value

true – success, otherwise – false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The minute and tick history of the custom symbol is completely removed if any of these properties is changed in the symbol specification:

- SYMBOL_CHART_MODE – price type for constructing bars (Bid or Last)
- SYMBOL_DIGITS – number of digits after the decimal point to display the price

After deleting the custom symbol history, the terminal attempts to create a new history using the updated properties. The same happens when the custom symbol properties are changed manually.

Example:

```
//+------------------------------------------------------------------+
//|                                       CustomSymbolSetInteger.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   CUSTOM_SYMBOL_NAME     Symbol()+".C"  // custom symbol name
#define   CUSTOM_SYMBOL_PATH     "Forex"        // name of the group, in which a symbol is to be created
#define   CUSTOM_SYMBOL_ORIGIN   Symbol()       // name of a symbol a custom one is to be based on
 
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
      
//--- get and print in the journal the properties of the symbol the custom one is based on
//--- (trading mode, Stop order installation level and trading operations freezing distance)
   ENUM_SYMBOL_TRADE_EXECUTION origin_exe_mode = (ENUM_SYMBOL_TRADE_EXECUTION)SymbolInfoInteger(CUSTOM_SYMBOL_ORIGIN, SYMBOL_TRADE_EXEMODE);
   int origin_stops_level = (int)SymbolInfoInteger(CUSTOM_SYMBOL_ORIGIN, SYMBOL_TRADE_STOPS_LEVEL);
   int origin_freeze_level= (int)SymbolInfoInteger(CUSTOM_SYMBOL_ORIGIN, SYMBOL_TRADE_FREEZE_LEVEL);
   
   PrintFormat("The '%s' symbol from which the custom '%s' was created:\n"+
               "  Deal execution mode: %s\n  Stops Level: %d\n  Freeze Level: %d",
               CUSTOM_SYMBOL_ORIGIN, CUSTOM_SYMBOL_NAME,
               StringSubstr(EnumToString(origin_exe_mode), 23), origin_stops_level, origin_freeze_level);
   
//--- set other values for the custom symbol properties
   ResetLastError();
   bool res=true;
   res &=CustomSymbolSetInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_EXEMODE, SYMBOL_TRADE_EXECUTION_MARKET);
   res &=CustomSymbolSetInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_STOPS_LEVEL, 10);
   res &=CustomSymbolSetInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_FREEZE_LEVEL, 3);
 
//--- if there was an error when setting any of the properties, display an appropriate message in the journal
   if(!res)
      Print("CustomSymbolSetInteger() failed. Error ", GetLastError());
   
//--- get and print in the journal the modified custom symbol properties
//--- (trading mode, Stop order installation level and trading operations freezing distance)
   ENUM_SYMBOL_TRADE_EXECUTION custom_exe_mode = (ENUM_SYMBOL_TRADE_EXECUTION)SymbolInfoInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_EXEMODE);
   int custom_stops_level = (int)SymbolInfoInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_STOPS_LEVEL);
   int custom_freeze_level= (int)SymbolInfoInteger(CUSTOM_SYMBOL_NAME, SYMBOL_TRADE_FREEZE_LEVEL);
   
   PrintFormat("Custom symbol '%s' based on '%s':\n"+
               "  Deal execution mode: %s\n  Stops Level: %d\n  Freeze Level: %d",
               CUSTOM_SYMBOL_NAME, CUSTOM_SYMBOL_ORIGIN, 
               StringSubstr(EnumToString(custom_exe_mode), 23), custom_stops_level, custom_freeze_level);
   
//--- display a hint about the script termination keys on the chart comment
   Comment(StringFormat("Press 'Esc' to exit or 'Del' to delete the '%s' symbol and exit", CUSTOM_SYMBOL_NAME));
 
//--- wait for pressing the Esc or Del keys to exit in an endless loop
   while(!IsStopped() && TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE)==0)
     {
      Sleep(16);
      //--- when pressing Del, delete the created custom symbol
      if(TerminalInfoInteger(TERMINAL_KEYSTATE_DELETE)<0)
        {
         if(DeleteCustomSymbol(CUSTOM_SYMBOL_NAME))
            PrintFormat("Custom symbol '%s' deleted successfully", CUSTOM_SYMBOL_NAME);
         break;
        }
     }
//--- clear the chart before exiting
   Comment("");
   /*
   result:
   The 'EURUSD' symbol from which the custom 'EURUSD.C' was created:
     Deal execution mode: INSTANT
     Stops Level: 0
     Freeze Level: 0
   Custom symbol 'EURUSD.C' based on 'EURUSD':
     Deal execution mode: MARKET
     Stops Level: 10
     Freeze Level: 3
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

[SymbolInfoInteger](/en/docs/marketinformation/symbolinfointeger)
