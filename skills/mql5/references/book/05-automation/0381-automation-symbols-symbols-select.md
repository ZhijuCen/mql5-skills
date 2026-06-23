# Editing the Market Watch list

Using the SymbolSelect function, the MQL program developer can add a specific symbol to Market Watch or remove it from there.

bool SymbolSelect(const string name, bool select)

The name parameter contains the name of the symbol being affected by this operation. Depending on the value of the select parameter, a symbol is added to Market Watch (true) or removed from it. Symbol names are case-sensitive: for example, "EURUSD.m" is not equal to "EURUSD.M".

The function returns an indication of success (true) or error (false). The error code can be found in _LastError.

A symbol cannot be removed if there are open charts or open positions for this symbol. In addition, you cannot delete a symbol that is explicitly used in the formula for calculating a synthetic (custom) instrument added to Market Watch.

It should be kept in mind that even if there are no open charts and positions for a symbol, it can be indirectly used by MQL programs: for example, they can read its history of quotes or ticks. Removing such a symbol may cause problems in these programs.

The following script SymbolRemoveUnused.mq5 is able to hide all symbols that are not used explicitly, so it is recommended to check it on a demo account or save the current symbols set through the context menu first.

```
#include <MQL5Book/MqlError.mqh>
   
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1) - 1] = V)
   
void OnStart()
{
   // request user confirmation for deletion
   if(IDOK == MessageBox("This script will remove all unused symbols"
      " from the Market Watch. Proceed?", "Please, confirm", MB_OKCANCEL))
   {
      const int n = SymbolsTotal(true);
      ResetLastError();
      string removed[];
      // go through the symbols of the Market Watch in reverse order
      for(int i = n - 1; i >= 0; --i)
      {
         const string s = SymbolName(i, true);
         if(SymbolSelect(s, false))
         {
            // remember what was deleted
            PUSH(removed, s);
         }
         else
         {
            // in case of an error, display the reason
            PrintFormat("Can't remove '%s': %s (%d)", s, E2S(_LastError), _LastError);
         }
      }
      const int r = ArraySize(removed);
      PrintFormat("%d out of %d symbols removed", r, n);
      ArrayPrint(removed);
      ...

```

After the user confirms the analysis of the list of symbols, the program attempts to hide each symbol sequentially by calling SymbolSelect(s, false). This only works for instruments that are not used explicitly. The enumeration of symbols is performed in the reverse order so as not to violate the indexing. All successfully removed symbols are collected in the removed array. The log displays statistics and the array itself.

If Market Watch is changed, the user is then given the opportunity to restore all deleted symbols by calling SymbolSelect(removed[i], true) in a loop.

```
      if(r > 0)
      {
         // it is possible to return the deleted symbols back to the Market Watch
         // (at this point, the window displays a reduced list)
         if(IDOK == MessageBox("Do you want to restore removed symbols"
            " in the Market Watch?", "Please, confirm", MB_OKCANCEL))
         {
            int restored = 0;
            for(int i = r - 1; i >= 0; --i)
            {
               restored += SymbolSelect(removed[i], true);
            }
            PrintFormat("%d symbols restored", restored);
         }
      }
   }
}

```

Here's what the log output might look like.

```
Can't remove 'EURUSD': MARKET_SELECT_ERROR (4305)
Can't remove 'XAUUSD': MARKET_SELECT_ERROR (4305)
Can't remove 'BTCUSD': MARKET_SELECT_ERROR (4305)
Can't remove 'GBPUSD': MARKET_SELECT_ERROR (4305)
...
Can't remove 'USDRUB': MARKET_SELECT_ERROR (4305)
2 out of 10 symbols removed
"NZDUSD" "USDCAD"
2 symbols restored

```

Please note that although the symbols are restored in their original order, as they were in Market Watch relative to each other, the addition occurs at the end of the list, after the remaining symbols. Thus, all "busy" symbols will be at the beginning of the list, and all the restored will follow them. Such is the specific operation of SymbolSelect: a symbol is always added to the end of the list, that is, it is impossible to insert a symbol in a specific position. So, the rearrangement of the list elements is available only for manual editing.
