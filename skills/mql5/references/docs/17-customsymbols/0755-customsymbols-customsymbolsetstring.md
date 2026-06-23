# CustomSymbolSetString

Sets the string type property value for a custom symbol.

```
bool  CustomSymbolSetString(
   const string              symbol_name,      // symbol name
   ENUM_SYMBOL_INFO_STRING   property_id,      // property ID
   string                    property_value    // property value
   );

```

Parameters

symbol_name

[in]  Custom symbol name.

property_id

[in]  Symbol property ID. The value can be one of the values of the [ENUM_SYMBOL_INFO_STRING](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_string) enumeration.

property_value

[in]  A string type variable containing the property value.

Return Value

true – success, otherwise – false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The minute and tick history of the custom symbol is completely removed if the SYMBOL_FORMULA property (setting the equation for the custom symbol price construction) is changed in the symbol specification. After deleting the custom symbol history, the terminal attempts to create a new history using the new equation. The same happens when the custom symbol equation is changed manually.

Example:

```
//+------------------------------------------------------------------+
//|                                        CustomSymbolSetString.mq5 |
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
//--- (minimum volume, maximum volume, minimum volume change step for deal execution)
   string origin_basis    = SymbolInfoString(CUSTOM_SYMBOL_ORIGIN, SYMBOL_BASIS);
   string origin_category = SymbolInfoString(CUSTOM_SYMBOL_ORIGIN, SYMBOL_CATEGORY);
   string origin_formula  = SymbolInfoString(CUSTOM_SYMBOL_ORIGIN, SYMBOL_FORMULA);
   
   PrintFormat("The '%s' symbol from which the custom '%s' was created:\n"+
               "  Basis: %s\n  Category: %s\n  Formula: %s",
               CUSTOM_SYMBOL_ORIGIN, CUSTOM_SYMBOL_NAME,
               origin_basis, origin_category, origin_formula);
   
//--- set other values for the custom symbol properties
   ResetLastError();
   bool res=true;
   res &=CustomSymbolSetString(CUSTOM_SYMBOL_NAME, SYMBOL_BASIS, CUSTOM_SYMBOL_ORIGIN);
   res &=CustomSymbolSetString(CUSTOM_SYMBOL_NAME, SYMBOL_CATEGORY, "FX");
   res &=CustomSymbolSetString(CUSTOM_SYMBOL_NAME, SYMBOL_FORMULA, ("1.0 / "+CUSTOM_SYMBOL_ORIGIN));
 
//--- if there was an error when setting any of the properties, display an appropriate message in the journal
   if(!res)
      Print("CustomSymbolSetString() failed. Error ", GetLastError());
   
//--- get and print in the journal the modified custom symbol properties
//--- (minimum volume, maximum volume, minimum volume change step for deal execution)
   string custom_basis    = SymbolInfoString(CUSTOM_SYMBOL_NAME, SYMBOL_BASIS);
   string custom_category = SymbolInfoString(CUSTOM_SYMBOL_NAME, SYMBOL_CATEGORY);
   string custom_formula  = SymbolInfoString(CUSTOM_SYMBOL_NAME, SYMBOL_FORMULA);
   
   PrintFormat("Custom symbol '%s' based on '%s':\n"+
               "  Basis: %s\n  Category: %s\n  Formula: %s",
               CUSTOM_SYMBOL_ORIGIN, CUSTOM_SYMBOL_NAME,
               custom_basis, custom_category, custom_formula);
   
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
     Basis: 
     Category: 
     Formula: 
   Custom symbol 'EURUSD' based on 'EURUSD.C':
     Basis: EURUSD
     Category: FX
     Formula: 1.0 / EURUSD
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

[SymbolInfoString](/en/docs/marketinformation/symbolinfostring)
