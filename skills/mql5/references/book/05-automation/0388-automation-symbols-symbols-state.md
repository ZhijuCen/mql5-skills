# Checking symbol status

Earlier we looked at several functions related to the status of a symbol. Recall that [SymbolExist](/en/book/automation/symbols/symbols_exist) is used to check for the existence of a symbol, and [SymbolSelect](/en/book/automation/symbols/symbols_select) is used to check for inclusion or exclusion from the Market Watch list. Among the properties of the symbol, there are several flags similar in purpose, the use of which has both pluses and minuses compared to the above functions.

In particular, the SYMBOL_SELECT property allows you to find out if the specified symbol is selected in Market Watch, while the SymbolSelect function changes this property.

The SymbolExist function, unlike the similar SYMBOL_EXIST property, additionally populates the output variable with an indication that the symbol is a user-defined one. When querying properties, it would be necessary to analyze these two attributes separately, since the attribute of the custom symbol is stored in another property, [SYMBOL_CUSTOM](/en/book/automation/symbols/symbols_custom). However, in some cases, the program may need only one property, and then the possibility of a separate query becomes a plus.

All flags are boolean values obtained through the SymbolInfoInteger function.

| Identifier | Description |
| --- | --- |
| SYMBOL_EXIST | Indicates that a symbol with the given name exists |
| SYMBOL_SELECT | Indicates that the symbol is selected in  Market Watch |
| SYMBOL_VISIBLE | Indicates that the specified symbol is displayed in  Market Watch |

Of particular interest is SYMBOL_VISIBLE. The fact is that some symbols (as a rule, these are cross rates that are necessary for calculating margin requirements and profit in the deposit currency) are selected in Market Watch automatically and are not displayed in the list visible to the user. Such symbols must be explicitly chosen (by the user or programmatically) to be displayed. Thus, it is the SYMBOL_VISIBLE property that allows you to determine whether a symbol is visible in the window: it can be equal to false for some elements of the [list](/en/book/automation/symbols/symbols_list), obtained using a pair of functions SymbolsTotal and SymbolName with the selected parameter equal to true.

Consider a simple script (SymbolInvisible.mq5), which searches the terminal for implicitly selected symbols, that is, those that are not displayed in the Market Watch (SYMBOL_VISIBLE is reset) while SYMBOL_SELECT for them is equal to true.

```
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1) - 1] = V)
   
void OnStart()
{
   const int n = SymbolsTotal(false);
   int selected = 0;
   string invisible[];
   // loop through all available symbols 
   for(int i = 0; i < n; ++i)
   {
      const string s = SymbolName(i, false);
      if(SymbolInfoInteger(s, SYMBOL_SELECT))
      {
         selected++;
         if(!SymbolInfoInteger(s, SYMBOL_VISIBLE))
         {
            // collect selected but invisible symbols into an array 
            PUSH(invisible, s);
         }
      }
   }
   PrintFormat("Symbols: total=%d, selected=%d, implicit=%d",
      n, selected, ArraySize(invisible));
   if(ArraySize(invisible))
   {
      ArrayPrint(invisible);
   }
}

```

Try compiling and running the script on different accounts. The situation when a symbol is implicitly selected is not always encountered. For example, if in Market Watch tickers of Russian blue chips that are quoted in rubles are selected, and the trading account is in a different currency (for example, dollars or euros, but not rubles), then the USDRUB symbol will be automatically selected. Of course, this assumes that it has not been previously added to the Market Watch explicitly. Then we get the following result in the log:

```
Symbols: total=50681, selected=49, implicit=1
"USDRUB"

```
