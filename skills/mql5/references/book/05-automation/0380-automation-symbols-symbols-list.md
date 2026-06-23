# Getting available symbols and Market Watch lists

The MQL5 API has several functions for operations with symbols. Using them, you can find the total number of available symbols, the number of symbols selected in Market Watch, as well as their names. As you know, the general list of symbols available in the terminal is indicated in the form of a hierarchical structure in the dialog Symbols, which the user can open with the command View -> Symbols, or from the Market Watch context menu. This list includes both the symbols provided by the broker and [custom symbols](/en/book/advanced/custom_symbols) created locally. You can use the SymbolsTotal function to find the total number of symbols.

int SymbolsTotal(bool selected)

The selected parameter specifies whether only symbols in Market Watch (true) or all available symbols (false) are requested.

The SymbolName function is often used along with SymbolsTotal. It returns the name of the symbol by its index (grouping the storage of symbols into logical folders is not taken into account here, see property [SYMBOL_PATH](/en/book/automation/symbols/symbols_description)).

string SymbolName(int index, bool selected)

The index parameter specifies the index of the requested symbol. Index value must be between 0 and the number of symbols, subject to the request context specified by the second parameter selected: true limits the enumeration to the symbols chosen in Market Watch, while false matches absolutely all symbols (by analogy with SymbolsTotal). Therefore, when calling SymbolName, set the selected parameter to the same value as in the previous SymbolsTotal call which is used to define the index range.

In case of an error, in particular, if the requested index is out of the list range, the function will return an empty string, and the error code will be written to the variable _LastError.

It is important to note that when the option selected is enabled, the pair of functions SymbolsTotal and SymbolName returns information for the list of symbols actually updated by the terminal, that is, symbols for which constant synchronization with the server is performed and for which the history of quotes is available for MQL programs. This list may be larger than the list visible in Market Watch, where elements are added explicitly: by the user or by an MQL program (to learn how to do this, see the section [Editing the list](/en/book/automation/symbols/symbols_select) in Market Watch). Such symbols, invisible in the window, are automatically connected by the terminal when they are needed for calculating cross-rates. Among the symbol properties, there are two that allow you to distinguish between explicit selection (SYMBOL_VISIBLE) and implicit selection (SYMBOL_SELECT); they will be discussed in the section on [symbol status check](/en/book/automation/symbols/symbols_state). Strictly speaking, for the SymbolsTotal and SymbolName functions, the setting of selected to true matches the extended symbols set with SYMBOL_SELECT cocked, not just those with SYMBOL_VISIBLE equal to true.

The order in which Market Watch symbols are returned corresponds to the terminal window (taking into account the possible rearrangement made by the user, and not taking into account sorting by any column, if it is enabled). Changing the order of symbols in Market Watch programmatically is not possible.

The order in the general list of Symbols is set by the terminal itself (content and sorting of Market Watch does not affect it).

As an example, let's look at the simple script SymbolList.mq5, which prints the available symbols to the log. The input parameter MarketWatchOnly allows the user to limit the list to the Market Watch symbols only (if the parameter is true) or to get the full list (false).

```
#property script_show_inputs
   
#include <MQL5Book/PRTF.mqh>
   
input bool MarketWatchOnly = true;
   
void OnStart()
{
   const int n = SymbolsTotal(MarketWatchOnly);
   Print("Total symbol count: ", n);
   // write a list of symbols in the Market Watch or all available
   for(int i = 0; i < n; ++i)
   {
      PrintFormat("%4d %s", i, SymbolName(i, MarketWatchOnly));
   }
   // intentionally asking for out-of-range to show an error
   PRTF(SymbolName(n, MarketWatchOnly)); // MARKET_UNKNOWN_SYMBOL(4301)
}

```

Below is an example log.

```
Total symbol count: 10
   0 EURUSD
   1 XAUUSD
   2 BTCUSD
   3 GBPUSD
   4 USDJPY
   5 USDCHF
   6 AUDUSD
   7 USDCAD
   8 NZDUSD
   9 USDRUB
SymbolName(n,MarketWatchOnly)= / MARKET_UNKNOWN_SYMBOL(4301)

```
