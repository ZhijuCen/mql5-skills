# SymbolsTotal

Returns the number of available (selected in Market Watch or all) symbols.

```
int  SymbolsTotal(
   bool  selected      // True - only symbols in MarketWatch
   );

```

Parameters

selected

[in] Request mode. Can be true or false.

Return Value

If the 'selected' parameter is true, the function returns the number of symbols selected in MarketWatch. If the value is false, it returns the total number of all symbols.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the number of available symbols
   int total    = SymbolsTotal(false);       // all symbols on the server
   int selected = SymbolsTotal(true);        // all symbols added to the Market Watch window
 
//--- send the obtained data to the journal
   PrintFormat("Number of available symbols on the server: %d\n"+
               "Number of available symbols selected in MarketWatch: %d", total, selected);
   /*
   result:
   Number of available symbols on the server: 140
   Number of available symbols selected in MarketWatch: 11
   */
  }

```
