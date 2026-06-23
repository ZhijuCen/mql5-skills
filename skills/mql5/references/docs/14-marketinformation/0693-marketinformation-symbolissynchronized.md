# SymbolIsSynchronized

The function checks whether data of a selected symbol in the terminal are synchronized with data on the trade server.

```
bool  SymbolIsSynchronized(
   string  name,       // symbol name
   );

```

Parameters

name

[in]  Symbol name.

Return value

If data are [synchronized](/en/docs/series/timeseries_access#synchronized), returns 'true'; otherwise returns 'false'.

Example:

```
#define SYMBOL_NAME "EURUSD"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the flag for synchronizing data in the terminal using the 'SYMBOL_NAME' symbol with the server data
   bool   sync = SymbolIsSynchronized(SYMBOL_NAME);
   
//--- create a message depending on the synchronization flag
   string text = StringFormat("The data on the '%s' symbol in the terminal is synchronized with the data on the trading server.", SYMBOL_NAME);
   if(!sync)
      text = StringFormat("The data for the '%s' symbol in the terminal is not synchronized with the data on the trading server.", SYMBOL_NAME);
   
//--- send the obtained result to the journal
   Print(text);
   
   /*
   result for synchronized data:
   The data on the 'EURUSD' symbol in the terminal is synchronized with the data on the trading server.
   
   result for data not yet synchronized:
   The data for the 'GBPHKD' symbol in the terminal is not synchronized with the data on the trading server.
   */
  }

```

See also

[SymbolInfoInteger](/en/docs/marketinformation/symbolinfointeger), [Organizing Data Access](/en/docs/series/timeseries_access)
