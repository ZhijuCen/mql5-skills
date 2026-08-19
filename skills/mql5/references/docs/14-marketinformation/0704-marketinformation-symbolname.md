# SymbolName

Returns the name of a symbol.

```
string  SymbolName(
   int   pos,          // number in the list
   bool  selected      // true - only symbols in MarketWatch
   );

```

Parameters

pos

[in] Order number of a symbol.

selected

[in] Request mode. If the value is true, the symbol is taken from the list of symbols selected in MarketWatch. If the value is false, the symbol is taken from the general list.

Return Value

Value of string type with the symbol name.

Example:

```
#define SYMBOL_NAME "GBPHKD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the flag of the server symbol search result
   bool found = false;
   
//--- find the 'SYMBOL_NAME' symbol in the list of all server symbols
   int total = SymbolsTotal(false);
   for(int i=0; i<total; i++)
     {
      //--- get a symbol name in the list by loop index
      string name = SymbolName(i, false);
      
      //--- if this is the desired symbol, send its name and position in the list to the journal and exit the loop
      if(name == SYMBOL_NAME)
        {
         PrintFormat("The '%s' symbol was found in the list of server symbols at index %d", name, i);
         found = true;
         break;
        }
     }
     
//--- if a symbol is not found on the server, report this before shutting down
   if(!found)
      PrintFormat("The '%s' symbol was not found on the server.", SYMBOL_NAME);
  }

```
