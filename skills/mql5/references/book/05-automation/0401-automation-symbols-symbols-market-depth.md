# Depth of Market

When it comes to exchange instruments, MetaTrader 5 allows you to get not only price and volume information packed in [ticks](/en/book/automation/symbols/symbols_tick), but also the Depth of Market (order book, level II prices), that is, the distribution of volumes in placed buy and sell orders at several nearest levels around the current price. One of the integer properties of the symbol SYMBOL_TICKS_BOOKDEPTH contains the maximum number of levels shown in the Depth of Market. This amount is allowed for each of the parties, that is, the total size of the order book can be two times larger (and this does not take into account price levels with zero volumes that are not broadcast).

Depending on the market situation, the actual size of the transmitted order book may become smaller than indicated in this property. For non-exchange instruments, this property is usually equal to 0, although some brokers can broadcast the order book for Forex symbols, limited only by the orders of their clients.

The order book itself and notifications about its update must be requested by the interested MQL program using a special API, which we will discuss in the [next chapter](/en/book/automation/marketbook).

It should be noted that due to the architectural features of the platform, this property is not directly related to the translation of the order book, that is, it is just a specification field filled in by the broker. In other words, a non-zero value of the property does not mean that the order book will necessarily arrive at the terminal in an open market. This depends on other server settings and whether it has an active connection to the data provider.

Let's try to get statistics on the depth of the market for all or selected symbols using the script SymbolFilterBookDepth.mq5.

```
input bool UseMarketWatch = false;
input int ShowSymbolsWithDepth = -1;

```

Parameter ShowSymbolsWithDepth, which is equal to -1 by default, instructs to collect statistics on different Depth of Market settings among all symbols. If you set the parameter to a different value, the program will try to find all symbols with the specified order book depth.

```
void OnStart()
{
   SymbolFilter f;                // filter object
   string symbols[];              // array for symbol names
   long depths[];                 // array of property values
   MapArray<long,int> stats;      // counters of occurrences of each depth
   
   if(ShowSymbolsWithDepth > -1)
   {
      f.let(SYMBOL_TICKS_BOOKDEPTH, ShowSymbolsWithDepth);
   }
   
   // apply filter and fill arrays
   f.select(UseMarketWatch, SYMBOL_TICKS_BOOKDEPTH, symbols, depths, true);
   const int n = ArraySize(symbols);
   
   PrintFormat("===== Book depths for %s symbols %s=====",
      (UseMarketWatch ? "Market Watch" : "all available"),
      (ShowSymbolsWithDepth > -1 ? "(filtered by depth="
      + (string)ShowSymbolsWithDepth + ") " : ""));
   PrintFormat("Total symbols: %d", n);
   ...

```

If a specific depth is given, we simply output an array of symbols (they all satisfy the filter condition), and exit.

```
   if(ShowSymbolsWithDepth > -1)
   {
      ArrayPrint(symbols);
      return;
   }
   ...

```

Otherwise, we calculate the statistics and display them.

```
   for(int i = 0; i < n; ++i)
   {
      stats.inc(depths[i]);
   }
   
   Print("Stats per depth:");
   stats.print();
   Print("Legend: key=depth, value=count");
}

```

With the default settings, we can get the following picture.

```
===== Book depths for all available symbols =====
Total symbols: 52357
Stats per depth:
    [key] [value]
[0]     0   52244
[1]     5       3
[2]    10      67
[3]    16       5
[4]    20      13
[5]    32      25
Legend: key=depth, value=count

```

If you set ShowSymbolsWithDepth to one of the detected values, for example, 32, we get a list of symbols with this order book depth.

```
===== Book depths for all available symbols (filtered by depth=32) =====
Total symbols: 25
[ 0] "USDCNH" "USDZAR" "USDHUF" "USDPLN" "EURHUF" "EURNOK" "EURPLN" "EURSEK" "EURZAR" "GBPNOK" "GBPPLN" "GBPSEK" "GBPZAR"
[13] "NZDCAD" "NZDCHF" "USDMXN" "EURMXN" "GBPMXN" "CADMXN" "CHFMXN" "MXNJPY" "NZDMXN" "USDCOP" "USDARS" "USDCLP"

```
