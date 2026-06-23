# Permitted volumes of trading operations

In later chapters, where we will learn how to program Expert Advisors, we will need to control many of the symbol characteristics that determine the success of sending trading orders. In particular, this applies to the part of the symbol specification that specifies the allowed scope of operations. The corresponding properties are also available in MQL5. All of them are of type double and are requested by the SymbolInfoDouble function.

| Identifier | Description |
| --- | --- |
| SYMBOL_VOLUME_MIN | Minimum deal volume in lots |
| SYMBOL_VOLUME_MAX | Maximum deal volume in lots |
| SYMBOL_VOLUME_STEP | Minimum step for changing the deal volume in lots |
| SYMBOL_VOLUME_LIMIT | Maximum allowable total volume of an open position and pending orders in one direction (buy or sell) |
| SYMBOL_TRADE_CONTRACT_SIZE | Trading contract size = 1 lot |

Attempts to buy or sell a financial instrument with a volume less than the minimum, more than the maximum, or not a multiple of a step will result in an error. In the chapter related to [trading APIs](/en/book/automation/experts), we will implement a code to unify the necessary checks and normalize volumes before calling the MQL5 API trading functions.

Among other things, the MQL program should also check SYMBOL_VOLUME_LIMIT. For example, with a limit of 5 lots, you can have an open buy position with a volume of 5 lots and place a pending order Sell Limit with a volume of 5 lots. However, you cannot place a pending Buy Limit order (because the cumulative volume in one direction will exceed the limit) or set Sell Limit of more than 5 lots.

As an introductory example, consider the script SymbolFilterVolumes.mq5 which logs the values of the above properties for the selected symbols. Let's add the MinimalContractSize variable to the input parameters to be able to filter symbols by the SYMBOL_TRADE_CONTRACT_SIZE property: we display only those which contract size is greater than the specified one (by default, 0, that is, all symbols satisfy the condition).

```
#include <MQL5Book/SymbolFilter.mqh>
   
input bool MarketWatchOnly = true;
input double MinimalContractSize = 0;

```

At the beginning of OnStart, let's define a filter object and output arrays to get lists of property names and values as vectors double for four fields. The list of the four required properties is indicated in the volumeIds array.

```
void OnStart()
{
   SymbolFilter f;                      // filter object
   string symbols[];                    // receiving array with names
   double volumeLimits[][4];            // receiving array with data vectors
   
   // requested symbol properties
   ENUM_SYMBOL_INFO_DOUBLE volumeIds[] =
   {
      SYMBOL_VOLUME_MIN,
      SYMBOL_VOLUME_STEP,
      SYMBOL_VOLUME_MAX,
      SYMBOL_VOLUME_LIMIT
   };
   ...

```

Next, we apply a filter by contract size (should be greater than the specified one) and get the specification fields associated with volumes for matching symbols.

```
   f.let(SYMBOL_TRADE_CONTRACT_SIZE, MinimalContractSize, SymbolFilter::IS::GREATER)
   .select(MarketWatchOnly, volumeIds, symbols, volumeLimits);
   
   const int n = ArraySize(volumeLimits);
   PrintFormat("===== Volume limits of the symbols (%d) =====", n);
   string title = "";
   for(int i = 0; i < ArraySize(volumeIds); ++i)
   {
      title += "\t" + EnumToString(volumeIds[i]);
   }
   Print(title);
   for(int i = 0; i < n; ++i)
   {
      Print(symbols[i]);
      ArrayPrint(volumeLimits, 3, NULL, i, 1, 0);
   }
}

```

For default settings, the script might show results like the following (with abbreviations).

```
===== Volume limits of the symbols (13) =====
SYMBOL_VOLUME_MIN SYMBOL_VOLUME_STEP SYMBOL_VOLUME_MAX SYMBOL_VOLUME_LIMIT
EURUSD
  0.010   0.010 500.000   0.000
GBPUSD
  0.010   0.010 500.000   0.000
USDCHF
  0.010   0.010 500.000   0.000
USDJPY
  0.010   0.010 500.000   0.000
USDCNH
   0.010    0.010 1000.000    0.000
USDRUB
   0.010    0.010 1000.000    0.000
...
XAUUSD
  0.010   0.010 100.000   0.000
BTCUSD
   0.010    0.010 1000.000    0.000
SP500m
 0.100  0.100  5.000 15.000

```

Some symbols may not be limited by SYMBOL_VOLUME_LIMIT (value is 0). You can compare the results against the symbol specifications: they must match.
