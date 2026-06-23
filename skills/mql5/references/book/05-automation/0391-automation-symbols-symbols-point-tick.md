# Price representation accuracy and change steps

Earlier, we have already met two interrelated properties of the working symbol of the chart: the minimum price change step ([Point](/en/book/applications/charts/charts_main_properties)) and the price presentation accuracy which is expressed in the number of decimal places ([Digits](/en/book/applications/charts/charts_main_properties)). They are also available in [Predefined variables](/en/book/common/environment/env_variables). To get similar properties of an arbitrary symbol, you should query the SYMBOL_POINT and SYMBOL_DIGITS properties, respectively. The SYMBOL_POINT property is closely related to the minimum price change (known to an MQL program as the SYMBOL_TRADE_TICK_SIZE property) and its value (SYMBOL_TRADE_TICK_VALUE), usually in the currency of the trading account (but some symbols can be configured to use the base currency; you may contact your broker for details if necessary). The table below shows the entire group of these properties.

| Identifier | Description |
| --- | --- |
| SYMBOL_DIGITS | The number of decimal places |
| SYMBOL_POINT | The value of one point in the quote currency |
| SYMBOL_TRADE_TICK_VALUE | SYMBOL_TRADE_TICK_VALUE_PROFIT value |
| SYMBOL_TRADE_TICK_VALUE_PROFIT | Current tick value for a profitable position |
| SYMBOL_TRADE_TICK_VALUE_LOSS | Current tick value for a losing position |
| SYMBOL_TRADE_TICK_SIZE | Minimum price change in the quote currency |

All properties except SYMBOL_DIGITS are real numbers and are requested using the SymbolInfoDouble function. The SYMBOL_DIGITS property is available via SymbolInfoInteger. To test the work with these properties, we will use ready-made classes [SymbolFilter](/en/book/automation/symbols/symbols_currencies) and [SymbolMonitor](/en/book/automation/symbols/symbols_info), which will automatically call the desired function for any property.

We will also improve the SymbolFilter class by adding a new overload of the select method, which will be able to fill not only an array with the names of suitable symbols but also another array with the values of their specific property.

In a more general case, we may be interested in several properties for each symbol at once, so it is advisable to use not one of the built-in data types for the output array but a special composite type with different fields.

In programming, such types are called tuples and are somewhat equivalent to MQL5 structures.

```
template<typename T1,typename T2,typename T3> // we can describe up to 64 fields
struct Tuple3                                 // MQL5 allows 64 template parameters
{
   T1 _1;
   T2 _2;
   T3 _3;
};

```

However, structures require a preliminary description with all fields, while we do not know in advance the number and list of requested symbol properties. Therefore, in order to simplify the code, we will represent our tuple as a vector in the second dimension of a dynamic array that receives the results of the query.

```
T array[][S];

```

As a data type T we can use any of the built-in types and enumerations used for properties. Size S must match the number of properties requested.

To tell the truth, such a simplification limits us in one query to values of the same types, that is, only integers, only reals, or only strings. However, filter conditions can include any properties. We will implement the approach with tuples a little later, using the example of filters of other trading entities: orders, deals, and [positions](/en/book/automation/experts/experts_positionget_funcs).

So the new version of the SymbolFilter::select method takes as an input a reference to the property array with property identifiers to read from the filtered symbols. The names of the symbols themselves and the values of these properties will be written to the symbols and data output arrays.

```
   template<typename E,typename V>
   bool select(const bool watch, const E &property[], string &symbols[],
      V &data[][], const bool sort = false) const
   {
      // the size of the array of requested properties must match the output tuple
      const int q = ArrayRange(data, 1);
      if(ArraySize(property) != q) return false;
      
      const int n = SymbolsTotal(watch);
      // iterate over characters
      for(int i = 0; i < n; ++i)
      {
         const string s = SymbolName(i, watch);
         // access to the symbol properties is provided by the monitor
         SymbolMonitor m(s);
         // check all filter conditions
         if(match(m, longs)
         && match(m, doubles)
         && match(m, strings))
         {
            // properties of a suitable symbol are written to arrays
            const int k = EXPAND(data);
            for(int j = 0; j < q; ++j)
            {
               data[k][j] = m.get(property[j]);
            }
            PUSH(symbols, s);
         }
      }
 
      if(sort)
      {
         ...
      }
      return true;
   }

```

Additionally, the new method can sort the output array by the first dimension (the first requested property): this functionality is left for independent study using source codes. To enable sorting, set the sort parameter to true. Arrays with symbol names and data are sorted consistently.

To avoid tuples in the calling code when only one property needs to be requested from the filtered characters, the following select option is implemented in SymbolFilter: inside it, we define intermediate arrays of properties (properties) and values (tuples) with size 1 in the second dimension, which are used to call the above full version of select.

```
   template<typename E,typename V>
   bool select(const bool watch, const E property, string &symbols[], V &data[],
      const bool sort = false) const
   {
      E properties[1] = {property};
      V tuples[][1];
      
      const bool result = select(watch, properties, symbols, tuples, sort);
      ArrayCopy(data, tuples);
      return result;
   }

```

Using the advanced filter, let's try to build a list of symbols sorted by tick value SYMBOL_TRADE_TICK_VALUE (see file SymbolFilterTickValue.mq5). Assuming that the deposit currency is USD, we should obtain a value equal to 1.0 for Forex instruments quoted in USD (of the type XXXUSD). For other assets, we will see non-trivial values.

```
#include <MQL5Book/SymbolFilter.mqh>
   
input bool MarketWatchOnly = true;
   
void OnStart()
{
   SymbolFilter f;      // filter object
   string symbols[];    // array with symbol names
   double tickValues[]; // array for results
   
   // apply the filter without conditions, fill and sort the array
   f.select(MarketWatchOnly, SYMBOL_TRADE_TICK_VALUE, symbols, tickValues, true);
   
   PrintFormat("===== Tick values of the symbols (%d) =====",
      ArraySize(tickValues));
   ArrayPrint(symbols);
   ArrayPrint(tickValues, 5);
}

```

Here is the result of running the script.

```
===== Tick values of the symbols (13) =====
"BTCUSD" "USDRUB" "XAUUSD" "USDSEK" "USDCNH" "USDCAD" "USDJPY" "NZDUSD" "AUDUSD" "EURUSD" "GBPUSD" "USDCHF" "SP500m"
 0.00100  0.01309  0.10000  0.10955  0.15744  0.80163  0.87319  1.00000  1.00000  1.00000  1.00000  1.09212 10.00000

```
