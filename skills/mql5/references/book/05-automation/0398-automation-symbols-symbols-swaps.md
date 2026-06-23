# Getting swap sizes

For the implementation of medium-term and long-term strategies, the swap sizes become important, since they can have a significant, usually negative, impact on the financial result. However, some readers are probably fans of the "Carry Trade" strategy, which was originally built on profiting from positive swaps. MQL5 has several symbol properties that provide access to specification strings that are associated with swaps.

| Identifier | Description |
| --- | --- |
| SYMBOL_SWAP_MODE | Swap calculation model ENUM_SYMBOL_SWAP_MODE |
| SYMBOL_SWAP_ROLLOVER3DAYS | Day of the week for triple swap credit  ENUM_DAY_OF_WEEK |
| SYMBOL_SWAP_LONG | Swap size for a long position |
| SYMBOL_SWAP_SHORT | Swap size for a short position |

The ENUM_SYMBOL_SWAP_MODE enumeration contains elements that specify options for units of measure and principles for calculating swaps. As well as SYMBOL_SWAP_ROLLOVER3DAYS, they refer to the integer properties of ENUM_SYMBOL_INFO_INTEGER.

The swap sizes are directly specified in the SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT properties as part of ENUM_SYMBOL_INFO_DOUBLE, that is, of type double.

Following are the elements of ENUM_SYMBOL_SWAP_MODE.

| Identifier | Description |
| --- | --- |
| SYMBOL_SWAP_MODE_DISABLED | no swaps |
| SYMBOL_SWAP_MODE_POINTS | points |
| SYMBOL_SWAP_MODE_CURRENCY_SYMBOL | the base currency of the symbol |
| SYMBOL_SWAP_MODE_CURRENCY_MARGIN | symbol margin currency |
| SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT | deposit currency |
| SYMBOL_SWAP_MODE_INTEREST_CURRENT | annual percentage of the price of the instrument at the time of swap calculation |
| SYMBOL_SWAP_MODE_INTEREST_OPEN | annual percentage of the symbol position opening price |
| SYMBOL_SWAP_MODE_REOPEN_CURRENT | points (with re-opening of the position at the closing price) |
| SYMBOL_SWAP_MODE_REOPEN_BID | points (with re-opening of the position at the Bid price of the new day). (in SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT parameters) |

For the SYMBOL_SWAP_MODE_INTEREST_CURRENT and SYMBOL_SWAP_MODE_INTEREST_OPEN options, there is assumed to be 360 banking days in a year.

For the SYMBOL_SWAP_MODE_REOPEN_CURRENT and SYMBOL_SWAP_MODE_REOPEN_BID options, the position is forcibly closed at the end of the trading day, and then their behavior is different.

With SYMBOL_SWAP_MODE_REOPEN_CURRENT, the position is reopened the next day at yesterday's closing price +/- the specified number of points. With SYMBOL_SWAP_MODE_REOPEN_BID, the position is reopened the next day at the current Bid price +/- the specified number of points. In both cases, the number of points is in the SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT parameters.

Let's check the operation of the properties using the script SymbolFilterSwap.mq5. In the input parameters, we provide the choice of the analysis context: Market Watch or all symbols depending on UseMarketWatch. When the ShowPerSymbolDetails parameter is false, we will calculate statistics, how many times one or another mode from ENUM_SYMBOL_SWAP_MODE is used in symbols. When the ShowPerSymbolDetails parameter is true, we will output an array of all symbols with the mode specified in mode, and sort the array in descending order of values in the fields SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT.

```
input bool UseMarketWatch = true;
input bool ShowPerSymbolDetails = false;
input ENUM_SYMBOL_SWAP_MODE Mode = SYMBOL_SWAP_MODE_POINTS;

```

For the elements of the combined array of swaps, we describe the SymbolSwap structure with the symbol name and swap value. The direction of the swap will be denoted by a prefix in the name field: "+" for swaps of long positions, "-" for swaps of short positions.

```
struct SymbolSwap
{
   string name;
   double value;
};

```

By tradition, we describe the filter object at the beginning of OnStart. However, the following code differs significantly depending on the value of the ShowPerSymbolDetails variable.

```
void OnStart()
{
   SymbolFilter f;                // filter object
   PrintFormat("===== Swap modes for %s symbols =====",
      (UseMarketWatch ? "Market Watch" : "all available"));
   
   if(ShowPerSymbolDetails)
   {
      // summary table of swaps of the selected Mode
      ...
   }
   else
   {
      // calculation of mode statistics
      ...
   }
}

```

Let's introduce the second branch first. Here we fill arrays with symbol names using the filter (symbols) and swap modes (values) that are taken from the SYMBOL_SWAP_MODE property. The resulting values are accumulated in an array map MapArray<ENUM_SYMBOL_SWAP_MODE,int> stats.

```
      // calculation of mode statistics
      string symbols[];
      long values[];
      MapArray<ENUM_SYMBOL_SWAP_MODE,int> stats; // counters for each mode
      // apply filter and collect mode values
      f.select(UseMarketWatch, SYMBOL_SWAP_MODE, symbols, values);
      const int n = ArraySize(symbols);
      for(int i = 0; i < n; ++i)
      {
         stats.inc((ENUM_SYMBOL_SWAP_MODE)values[i]);
      }
      ...

```

Next, we display the collected statistics.

```
      PrintFormat("Total symbols: %d", n);
      Print("Stats per swap mode:");
      stats.print();
      Print("Legend: key=swap mode, value=count");
      for(int i = 0; i < stats.getSize(); ++i)
      {
         PrintFormat("%d -> %s", stats.getKey(i), EnumToString(stats.getKey(i)));
      }

```

For the case of constructing a table with swap values, the algorithm is as follows. Swaps for long and short positions are requested separately, so we define paired arrays for names and values. Together they will be brought together in the swaps array of structures.

```
      // summary table of swaps of the selected Mode
      string buyers[], sellers[];    // arrays for names
      double longs[], shorts[];      // arrays for swap values
      SymbolSwap swaps[];            // total array to print

```

Set the condition for the selected swap mode in the filter. This is necessary to be able to compare and sort array elements.

```
      f.let(SYMBOL_SWAP_MODE, Mode);

```

Then we apply the filter twice for different properties (SYMBOL_SWAP_LONG, SYMBOL_SWAP_SHORT) and fill different arrays with their values (longs, shorts). Within each call, the arrays are sorted in ascending order.

```
      f.select(UseMarketWatch, SYMBOL_SWAP_LONG, buyers, longs, true);
      f.select(UseMarketWatch, SYMBOL_SWAP_SHORT, sellers, shorts, true);

```

In theory, the sizes of the arrays should be the same, since the filter condition is the same, but for clarity, let's allocate a variable for each size. Since each symbol will appear in the resulting table twice, for the long and short sides, we provide a double size for the swaps array.

```
      const int l = ArraySize(longs);
      const int s = ArraySize(shorts);
      const int n = ArrayResize(swaps, l + s); // should be l == s
      PrintFormat("Total symbols with %s: %d", EnumToString(Mode), l);

```

Next, we join the two arrays longs and shorts, processing them in reverse order, since we need to sort from positive to negative values.

```
      if(n > 0)
      {
         int i = l - 1, j = s - 1, k = 0;
         while(k < n)
         {
            const double swapLong = i >= 0 ? longs[i] : -DBL_MAX;
            const double swapShort = j >= 0 ? shorts[j] : -DBL_MAX;
            
            if(swapLong >= swapShort)
            {
               swaps[k].name = "+" + buyers[i];
               swaps[k].value = longs[i];
               --i;
               ++k;
            }
            else
            {
               swaps[k].name = "-" + sellers[j];
               swaps[k].value = shorts[j];
               --j;
               ++k;
            }
         }
         Print("Swaps per symbols (ordered):");
         ArrayPrint(swaps);
      }

```

It is interesting to run the script several times with different settings. For example, by default, we can get the following results.

```
===== Swap modes for Market Watch symbols =====
Total symbols: 13
Stats per swap mode:
    [key] [value]
[0]     1      10
[1]     0       2
[2]     2       1
Legend: key=swap mode, value=count
1 -> SYMBOL_SWAP_MODE_POINTS
0 -> SYMBOL_SWAP_MODE_DISABLED
2 -> SYMBOL_SWAP_MODE_CURRENCY_SYMBOL

```

These statistics show that 10 symbols have the swap mode SYMBOL_SWAP_MODE_POINTS, for two the swaps are disabled, SYMBOL_SWAP_MODE_DISABLED, and for one it is in the base currency SYMBOL_SWAP_MODE_CURRENCY_SYMBOL.

Let's find out what kind of symbols have SYMBOL_SWAP_MODE_POINTS and find out their swaps. For this, we will set ShowPerSymbolDetails to true (parameter mode already set to SYMBOL_SWAP_MODE_POINTS).

```
===== Swap modes for Market Watch symbols =====
Total symbols with SYMBOL_SWAP_MODE_POINTS: 10
Swaps per symbols (ordered):
        [name]   [value]
[ 0] "+AUDUSD"   6.30000
[ 1] "+NZDUSD"   2.80000
[ 2] "+USDCHF"   0.10000
[ 3] "+USDRUB"   0.00000
[ 4] "-USDRUB"   0.00000
[ 5] "+USDJPY"  -0.10000
[ 6] "+GBPUSD"  -0.20000
[ 7] "-USDCAD"  -0.40000
[ 8] "-USDJPY"  -0.60000
[ 9] "+EURUSD"  -0.70000
[10] "+USDCAD"  -0.80000
[11] "-EURUSD"  -1.00000
[12] "-USDCHF"  -1.00000
[13] "-GBPUSD"  -2.20000
[14] "+USDSEK"  -4.50000
[15] "-XAUUSD"  -4.60000
[16] "-USDSEK"  -4.90000
[17] "-NZDUSD"  -6.70000
[18] "+XAUUSD" -12.60000
[19] "-AUDUSD" -14.80000

```

You can compare the values with symbol specifications.

Finally, we change the Mode to SYMBOL_SWAP_MODE_CURRENCY_SYMBOL. In our case, we should get one symbol, but spaced into two lines: with a plus and a minus in the name.

```
===== Swap modes for Market Watch symbols =====
Total symbols with SYMBOL_SWAP_MODE_CURRENCY_SYMBOL: 1
Swaps per symbols (ordered):
       [name]   [value]
[0] "-SP500m" -35.00000
[1] "+SP500m" -41.41000

```

From the table, both swaps are negative.
