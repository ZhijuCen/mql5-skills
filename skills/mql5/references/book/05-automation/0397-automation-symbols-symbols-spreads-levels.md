# Spreads and order distance from the current price

For many trading strategies, especially those based on short-term trades, information about the spread and the distance from the current price, allowing the installation or modification of orders, is important. All of these properties are part of the ENUM_SYMBOL_INFO_INTEGER enumeration and are available through the [SymbolInfoInteger](/en/book/automation/symbols/symbols_info) function.

| Identifier | Description |
| --- | --- |
| SYMBOL_SPREAD | Spread size (in points) |
| SYMBOL_SPREAD_FLOAT | Boolean sign of a floating spread |
| SYMBOL_TRADE_STOPS_LEVEL | Minimum allowed distance from the current price (in points) for setting Stop Loss, Take Profit, and pending orders |
| SYMBOL_TRADE_FREEZE_LEVEL | Distance from the current price (in points) to freeze orders and positions |

In the table above, the current price refers to the Ask or Bid price, depending on the nature of the operation being performed.

Protective Stop Loss and Take Profit levels indicate that a position should be closed. This is performed by an operation opposite to the opening. Therefore, for buy orders opened at the Ask price, protective levels indicate Bid, and for sell orders opened at Bid, protective levels indicate Ask. When placing pending orders, the open price type is selected in the standard way: buy orders (Buy Stop, Buy Limit, Buy Stop Limit) are based on Ask and sell orders (Sell Stop, Sell Limit, Sell Stop Limit) are based on Bid. Taking into account such types of prices in the context of the mentioned trading operations, the distance in points is calculated for the SYMBOL_TRADE_STOPS_LEVEL and SYMBOL_TRADE_FREEZE_LEVEL properties.

The SYMBOL_TRADE_STOPS_LEVEL property, if it is non-zero, disables modification of Stop Loss and Take Profit levels for an open position if the new level would be closer to the current price than the specified distance. Similarly, it is impossible to move the opening price of a pending order closer than SYMBOL_TRADE_STOPS_LEVEL points from the current price.

The SYMBOL_TRADE_FREEZE_LEVEL property, if it is non-zero, restricts any trading operations for a pending order or an open position within the specified distance from the current price. For a pending order, freezing occurs when the specified open price is at a distance less than SYMBOL_TRADE_FREEZE_LEVEL points from the current price (again, the type of the current price is Ask or Bid, depending on whether it is buying or selling). For a position, freezing occurs for Stop Loss and Take Profit levels, which happened to be near the current price, and therefore the measurement for them is performed for "opposite" price types.

If the SYMBOL_SPREAD_FLOAT property is true, the SYMBOL_SPREAD property is not part of the symbol specification but contains the actual spread, dynamically changing with each call according to market conditions. It can also be found as the difference between Ask and Bid prices in the MqlTick structure by calling [SymbolInfoTick](/en/book/automation/symbols/symbols_tick).

The script SymbolFilterSpread.mq5 will allow you to analyze the specified properties. It defines a custom enumeration ENUM_SYMBOL_INFO_INTEGER_PART, which includes only the properties of interest to us in this context from ENUM_SYMBOL_INFO_INTEGER.

```
enum ENUM_SYMBOL_INFO_INTEGER_PART
{
   SPREAD_FIXED = SYMBOL_SPREAD,
   SPREAD_FLOAT = SYMBOL_SPREAD_FLOAT,
   STOPS_LEVEL = SYMBOL_TRADE_STOPS_LEVEL,
   FREEZE_LEVEL = SYMBOL_TRADE_FREEZE_LEVEL
};

```

The new enumeration defines the Property input parameter, which specifies which of the four properties will be analyzed. Parameters UseMarketWatch and ShowPerSymbolDetails control the process in the already known way, as in the previous test scripts.

```
input bool UseMarketWatch = true;
input ENUM_SYMBOL_INFO_INTEGER_PART Property = SPREAD_FIXED;
input bool ShowPerSymbolDetails = true;

```

For the convenient display of information for each symbol (property name and value in each line) using the ArrayPrint function, an auxiliary structure SymbolDistance is defined (used only when ShowPerSymbolDetails equals true).

```
struct SymbolDistance
{
   string name;
   int value;
};

```

In the OnStart handler, we describe the necessary objects and arrays.

```
void OnStart()
{
   SymbolFilter f;                // filter object
   string symbols[];              // receiving array for names
   long values[];                 // receiving array for values
   SymbolDistance distances[];    // array to print
   MapArray<long,int> stats;      // counters of specific values of the selected property
   ...

```

Then we apply the filter and fill the receiving arrays with the values of the specified Property while also applying sorting.

```
   f.select(UseMarketWatch, (ENUM_SYMBOL_INFO_INTEGER)Property, symbols, values, true);
   const int n = ArraySize(symbols);
   if(ShowPerSymbolDetails) ArrayResize(distances, n);
   ...

```

In a loop, we count the statistics and fill in the SymbolDistance structures, if it is needed.

```
   for(int i = 0; i < n; ++i)
   {
      stats.inc(values[i]);
      if(ShowPerSymbolDetails)
      {
         distances[i].name = symbols[i];
         distances[i].value = (int)values[i];
      }
   }
   ...

```

Finally, we output the results to the log.

```
   PrintFormat("===== Distances for %s symbols =====",
      (UseMarketWatch ? "Market Watch" : "all available"));
   PrintFormat("Total symbols: %d", n);
   
   PrintFormat("Stats per %s:", EnumToString((ENUM_SYMBOL_INFO_INTEGER)Property));
   stats.print();
   
   if(ShowPerSymbolDetails)
   {
      Print("Details per symbol:");
      ArrayPrint(distances);
   }
}

```

Here's what you get when you run the script with default settings, which is consistent with spread analysis.

```
===== Distances for Market Watch symbols =====
Total symbols: 13
Stats per SYMBOL_SPREAD:
    [key] [value]
[0]     0       2
[1]     2       3
[2]     3       1
[3]     6       1
[4]     7       1
[5]     9       1
[6]   151       1
[7]   319       1
[8]  3356       1
[9]  3400       1
Details per symbol:
       [name] [value]
[ 0] "USDJPY"       0
[ 1] "EURUSD"       0
[ 2] "USDCHF"       2
[ 3] "USDCAD"       2
[ 4] "GBPUSD"       2
[ 5] "AUDUSD"       3
[ 6] "XAUUSD"       6
[ 7] "SP500m"       7
[ 8] "NZDUSD"       9
[ 9] "USDCNH"     151
[10] "USDSEK"     319
[11] "BTCUSD"    3356
[12] "USDRUB"    3400

```

To understand whether the spreads are floating (changing dynamically) or fixed, let's run the script with different settings: Property = SPREAD_FLOAT, ShowPerSymbolDetails = false.

```
===== Distances for Market Watch symbols =====
Total symbols: 13
Stats per SYMBOL_SPREAD_FLOAT:
    [key] [value]
[0]     1      13

```

According to this data, all symbols in the market watch have a floating spread (value 1 in the key  key is true in SYMBOL_SPREAD_FLOAT). Therefore, if we run the script again and again with the default settings, we will receive new values (with an open market).
