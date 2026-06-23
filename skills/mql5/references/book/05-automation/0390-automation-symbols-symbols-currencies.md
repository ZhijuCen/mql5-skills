# Base, quote, and margin currencies of the instrument

One of the most important properties of each financial instrument is its working currencies:

- The base currency in which the purchased or sold asset is expressed (for Forex instruments)
- The profit calculation (quotation) currency
- The margin calculation currency

An MQL program can get the names of these currencies using the SymbolInfoString function and three properties from the following table.

| Identifier | Description |
| --- | --- |
| SYMBOL_CURRENCY_BASE | Base currency |
| SYMBOL_CURRENCY_PROFIT | Profit currency |
| SYMBOL_CURRENCY_MARGIN | Margin currency |

These properties help to analyze Forex instruments, in the names of which many brokers add various prefixes and suffixes, as well as exchange instruments. In particular, the algorithm will be able to find a symbol to obtain a cross rate of two given currencies or select a portfolio of indexes with a given common quote currency.

Since searching for tools according to certain requirements is a very common task, let's create a class SymbolFilter (SymbolFilter.mqh) to build a list of suitable symbols and their selected properties. In the future, we will use this class not only to analyze currencies but also other characteristics.

First, we will consider a simplified version and then supplement it with convenient functionality.

In development, we will use ready-made auxiliary tools: an associative map array ([MapArray.mqh](/en/book/applications/indicators_make/indicators_multisymbol)) to store key-value pairs of selected types and a symbol property monitor ([SymbolMonitor.mqh](/en/book/automation/symbols/symbols_info)).

```
#include <MQL5Book/MapArray.mqh>
#include <MQL5Book/SymbolMonitor.mqh>

```

To simplify the statements for accumulating the results of work in arrays, we use an improved version of the PUSH macro, which we have already seen in previous examples, as well as its EXPAND version for multidimensional arrays (simple assignment is impossible in this case).

```
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1, ArraySize(A) * 2) - 1] = V)
#define EXPAND(A) (ArrayResize(A, ArrayRange(A, 0) + 1, ArrayRange(A, 0) * 2) - 1)

```

An object of the SymbolFilter class must have a storage for the property values which will be used to filter symbols. Therefore, we will describe three MapArray arrays in the class for integer, real, and string properties.

```
class SymbolFilter
{
   MapArray<ENUM_SYMBOL_INFO_INTEGER,long> longs;
   MapArray<ENUM_SYMBOL_INFO_DOUBLE,double> doubles;
   MapArray<ENUM_SYMBOL_INFO_STRING,string> strings;
   ...

```

Setting the required filter properties is done using overloaded the let methods.

```
public:
   SymbolFilter *let(const ENUM_SYMBOL_INFO_INTEGER property, const long value)
   {
      longs.put(property, value);
      return &this;
   }
   
   SymbolFilter *let(const ENUM_SYMBOL_INFO_DOUBLE property, const double value)
   {
      doubles.put(property, value);
      return &this;
   }
   
   SymbolFilter *let(const ENUM_SYMBOL_INFO_STRING property, const string value)
   {
      strings.put(property, value);
      return &this;
   }
   ...

```

Please note that the methods return a pointer to the filter, which allows you to write conditions as a chain: for example, if earlier in the code an object f of type SymbolFilter was described, then you can impose two conditions on the price type and the name of the profit currency as follows:

```
f.let(SYMBOL_CHART_MODE, SYMBOL_CHART_MODE_LAST).let(SYMBOL_CURRENCY_PROFIT, "USD");

```

The formation of an array of symbols that satisfy the conditions is performed by the filter object in several variants of the select method, the simplest of which is presented below (other options will be discussed later).

The watch parameter defines the search context for symbols: among those selected in Market Watch (true) or all available (false). The output array symbols will be filled with the names of matching symbols. We already know the code structure inside the method: it has a loop through the symbols for each of which a monitor object m is created.

```
   void select(const bool watch, string &symbols[]) const
   {
      const int n = SymbolsTotal(watch);
      for(int i = 0; i < n; ++i)
      {
         const string s = SymbolName(i, watch);
         SymbolMonitor m(s);
         if(match<ENUM_SYMBOL_INFO_INTEGER,long>(m, longs)
         && match<ENUM_SYMBOL_INFO_DOUBLE,double>(m, doubles)
         && match<ENUM_SYMBOL_INFO_STRING,string>(m, strings))
         {
            PUSH(symbols, s);
         }
      }
   }

```

It is with the help of the monitor that we can get the value of any property in a unified way. Checking if the properties of the current symbol match the stored set of conditions in longs, doubles, and strings arrays is implemented by a helper method match. Only of all requested properties match, the symbol name will be saved in the symbols output array.

In the simplest case, the implementation of the match method is as follows (subsequently it will be changed).

```
protected:
   template<typename K,typename V>
   bool match(const SymbolMonitor &m, const MapArray<K,V> &data) const
   {
      for(int i = 0; i < data.getSize(); ++i)
      {
         const K key = data.getKey(i);
         if(!equal(m.get(key), data.getValue(i)))
         {
            return false;
         }
      }
      return true;
   }

```

If at least one of the values in the data array does not match the corresponding character property, the method returns false. If all properties match (or there are no conditions for properties of this type), the method returns true.

The comparison of two values is performed using the equal. Given the fact that among the properties there may be properties of type double, the implementation is not as simple as one might think.

```
   template<typename V>
   static bool equal(const V v1, const V v2)
   {
      return v1 == v2 || eps(v1, v2);
   }

```

For type double, the expression v1 == v2 may not work for close numbers, and therefore the precision of the real DBL_EPSILON type should be taken into account. This is done in a separate method eps, overloaded separately for type double and all other types due to the template.

```
   static bool eps(const double v1, const double v2)
   {
      return fabs(v1 - v2) < DBL_EPSILON * fmax(v1, v2);
   }
   
   template<typename V>
   static bool eps(const V v1, const V v2)
   {
      return false;
   }

```

When values of any type except double are equal, the template method eps just won't be called, and in all other cases (including when values differ), it returns false as required (thus, only the condition v1 == v2).

The filter option described above only allows you to check properties for equality. However, in practice, it is often required to analyze conditions for inequality, as well as for greater/less. For this reason, the SymbolFilter class has the IS enumeration with basic comparison operations (if desired, it can be supplemented).

```
class SymbolFilter
{
   ...
   enum IS
   {
      EQUAL,
      GREATER,
      NOT_EQUAL,
      LESS
   };
   ...

```

For each property from the ENUM_SYMBOL_INFO_INTEGER, ENUM_SYMBOL_INFO_DOUBLE, and ENUM_SYMBOL_INFO_STRING enumerations, it is required to save not only the desired property value (recall about associative arrays longs, doubles, strings), but also the comparing method from the new IS enumeration.

Since the elements of standard enumerations have non-overlapping values (there is one exception related to [volumes](/en/book/automation/symbols/symbols_tick_parts) but it is not critical), it makes sense to reserve one common map array conditions for the comparison method. This raises the question of which type to choose for the map key in order to technically "combine" different enumerations. To do this, we had to describe the dummy enumeration ENUM_ANY which only denotes a certain type of generic enumeration. Recall that all enumerations have an internal representation equivalent to an integer int, and therefore can be reduced to one another.

```
   enum ENUM_ANY
   {
   };
   
   MapArray<ENUM_ANY,IS> conditions;
   MapArray<ENUM_ANY,long> longs;
   MapArray<ENUM_ANY,double> doubles;
   MapArray<ENUM_ANY,string> strings;
   ...

```

Now we can complete all let methods which set the desired value of the property by adding the cmp input parameter that specifies the comparison method. By default, it sets the check for equality (EQUAL).

```
   SymbolFilter *let(const ENUM_SYMBOL_INFO_INTEGER property, const long value,
      const IS cmp = EQUAL)
   {
      longs.put((ENUM_ANY)property, value);
      conditions.put((ENUM_ANY)property, cmp);
      return &this;
   }

```

Here's a variant for integer properties. The other two overloads change in the same way.

Taking into account new information about different ways of comparing and simultaneously eliminating different types of keys in map arrays, we modify the match method. In it, for each specified property, we retrieve a condition from the conditions array based on the key in the data map array, and appropriate checks are performed using the switch operator.

```
   template<typename V>
   bool match(const SymbolMonitor &m, const MapArray<ENUM_ANY,V> &data) const
   {
      // dummy variable to select m.get method overload below
      static const V type = (V)NULL;
      // cycle by conditions imposed on the properties of the symbol
      for(int i = 0; i < data.getSize(); ++i)
      {
         const ENUM_ANY key = data.getKey(i);
         // choice of comparison method in the condition
         switch(conditions[key])
         {
         case EQUAL:
            if(!equal(m.get(key, type), data.getValue(i))) return false;
            break;
         case NOT_EQUAL:
            if(equal(m.get(key, type), data.getValue(i))) return false;
            break;
         case GREATER:
            if(!greater(m.get(key, type), data.getValue(i))) return false;
            break;
         case LESS:
            if(greater(m.get(key, type), data.getValue(i))) return false;
            break;
         }
      }
      return true;
   }

```

The new template greater method is implemented simplistically.

```
   template<typename V>
   static bool greater(const V v1, const V v2)
   {
      return v1 > v2;
   }

```

Now the match method call can be written in a shorter form since the only remaining type of the template V is automatically determined by the passed data argument (and this is one of the arrays longs, doubles, or strings).

```
   void select(const bool watch, string &symbols[]) const
   {
      const int n = SymbolsTotal(watch);
      for(int i = 0; i < n; ++i)
      {
         const string s = SymbolName(i, watch);
         SymbolMonitor m(s);
         if(match(m, longs)
            && match(m, doubles)
            && match(m, strings))
         {
            PUSH(symbols, s);
         }
      }
   }

```

This is not the final version of the SymbolFilter class yet, but we can already test it in action.

Let's create a script SymbolFilterCurrency.mq5 that can filter symbols based on the properties of the base currency and profit currency; in this case, it is USD. The MarketWatchOnly parameter only searches in the Market Watch by default.

```
#include <MQL5Book/SymbolFilter.mqh>
   
input bool MarketWatchOnly = true;
   
void OnStart()
{
   SymbolFilter f;   // filter object
   string symbols[]; // array for results
   ...

```

Let's say that we want to find Forex instruments that have direct quotes, that is, "USD" appears in their names at the beginning. In order not to depend on the specifics of the formation of names for a particular broker, we will use the SYMBOL_CURRENCY_BASE property, which contains the first currency.

Let's write down the condition that the base currency of the symbol is equal to USD and apply the filter.

```
   f.let(SYMBOL_CURRENCY_BASE, "USD")
   .select(MarketWatchOnly, symbols);
   Print("===== Base is USD =====");
   ArrayPrint(symbols);
   ...

```

The resulting array is output to the log.

```
===== Base is USD =====
"USDCHF" "USDJPY" "USDCNH" "USDRUB" "USDCAD" "USDSEK" "SP500m" "Brent" 

```

As you can see, the array includes not only Forex symbols with USD at the beginning of the ticker but also the S&P500 index and the commodity (oil). The last two symbols are quoted in dollars, but they also have the same base currency. At the same time, the quote currency of Forex symbols (it is also the profit currency) is second and differs from USD. This allows you to supplement the filter in such a way that non-Forex symbols no longer match it.

Let's clear the array, add a condition that the profit currency is not equal to "USD", and again request suitable symbols (the previous condition was saved in the f object).

```
   ...
   ArrayResize(symbols, 0);
   
   f.let(SYMBOL_CURRENCY_PROFIT, "USD", SymbolFilter::IS::NOT_EQUAL)
   .select(MarketWatchOnly, symbols);
   Print("===== Base is USD and Profit is not USD =====");
   ArrayPrint(symbols);
}

```

This time, only the symbols you are looking for are actually displayed in the log.

```
===== Base is USD and Profit is not USD =====
"USDCHF" "USDJPY" "USDCNH" "USDRUB" "USDCAD" "USDSEK"

```
