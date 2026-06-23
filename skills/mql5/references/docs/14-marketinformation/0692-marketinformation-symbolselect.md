# SymbolSelect

Selects a symbol in the Market Watch window or removes a symbol from the window.

```
bool  SymbolSelect(
   string  name,       // symbol name
   bool    select      // add or remove
   );

```

Parameters

name

[in] Symbol name.

select

[in] Switch. If the value is false, a symbol should be removed from MarketWatch, otherwise a symbol should be selected in this window. A symbol can't be removed if the symbol chart is open, or there are open positions for this symbol.

Return Value

In case of failure returns false.

Example:

```
#define SYMBOL_NAME "GBPHKD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- check for the presence of a symbol in the lists, if not found, report it and complete the work
   bool custom = false;
   if(!SymbolExist(SYMBOL_NAME, custom))
     {
      PrintFormat("'%s' symbol not found in the lists", SYMBOL_NAME);
      return;
     }
     
//--- add a symbol to the Market Watch window
   ResetLastError();
   if(!SymbolSelect(SYMBOL_NAME, true))
     {
      Print("SymbolSelect() failed. Error ", GetLastError());
      return;
     }
//--- if a symbol is successfully added to the list, get its index in the Market Watch window and send the result to the journal
   int index = SymbolIndex(SYMBOL_NAME);
   PrintFormat("The '%s' symbol has been added to the MarketWatch list. Symbol index in the list: %d", SYMBOL_NAME, index);
     
//--- now remove the symbol from the Market Watch window
   ResetLastError();
   if(!SymbolSelect(SYMBOL_NAME, false))
     {
      Print("SymbolSelect() failed. Error ", GetLastError());
      return;
     }
//--- if a symbol is successfully removed from the list, its index in the Market Watch window is -1, send the deletion result to the journal
   index = SymbolIndex(SYMBOL_NAME);
   PrintFormat("The '%s' symbol has been removed from the MarketWatch list. Symbol index in the list: %d", SYMBOL_NAME, index);
   
   /*
   result:
   The 'GBPHKD' symbol has been added to the MarketWatch list. Symbol index in the list: 12
   The 'GBPHKD' symbol has been removed from the MarketWatch list. Symbol index in the list: -1
   */
  }
//+------------------------------------------------------------------+
//| Return the symbol index in the Market Watch symbol list          |
//+------------------------------------------------------------------+
int SymbolIndex(const string symbol)
  {
   int total = SymbolsTotal(true);
   for(int i=0; i<total; i++)
     {
      string name = SymbolName(i, true);
      if(name == symbol)
         return i;
     }
   return(WRONG_VALUE);
  }

```
