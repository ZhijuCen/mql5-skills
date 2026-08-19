# Getting Market Information

These are functions intended for receiving information about the market state.

| Function | Action |
| --- | --- |
| SymbolsTotal | Returns the number of available (selected in Market Watch or all) symbols |
| SymbolExist | Checks if a symbol with a specified name exists |
| SymbolName | Returns the name of a specified symbol |
| SymbolSelect | Selects a symbol in the Market Watch window or removes a symbol from the window |
| SymbolIsSynchronized | Checks whether data of a selected symbol in the terminal are  synchronized  with data on the trade server |
| SymbolInfoDouble | Returns the double value of the symbol for the corresponding property |
| SymbolInfoInteger | Returns a value of an integer type (long, datetime, int or bool) of a specified symbol for the corresponding property |
| SymbolInfoString | Returns a value of the string type of a specified symbol for the corresponding property |
| SymbolInfoMarginRate | Returns the margin rates depending on the order type and direction |
| SymbolInfoTick | Returns the current prices for the specified symbol in a variable of the  MqlTick  type |
| SymbolInfoSessionQuote | Allows receiving time of beginning and end of the specified quoting sessions for a specified symbol and day of week. |
| SymbolInfoSessionTrade | Allows receiving time of beginning and end of the specified trading sessions for a specified symbol and day of week. |
| MarketBookAdd | Provides opening of Depth of Market for a selected symbol, and subscribes for receiving notifications of the DOM changes |
| MarketBookRelease | Provides closing of Depth of Market for a selected symbol, and cancels the subscription for receiving notifications of the DOM changes |
| MarketBookGet | Returns a structure array  MqlBookInfo  containing records of the Depth of Market of a specified symbol |
