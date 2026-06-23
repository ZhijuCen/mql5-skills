# Overview of functions for getting symbol properties

The complete specification of each symbol can be obtained by querying its properties: for this purpose, the MQL5 API provides three functions, namely SymbolInfoInteger, SymbolInfoDouble, and SymbolInfoString, each of which is responsible for the properties of a particular type. The properties are described as members of three enumerations: ENUM_SYMBOL_INFO_INTEGER, ENUM_SYMBOL_INFO_DOUBLE, and ENUM_SYMBOL_INFO_STRING, respectively. A similar technique is used in the chart and object APIs we already know.

The name of the symbol and the identifier of the requested property are passed to any of the functions.

Each of the functions is presented in two forms: abbreviated and full. The abbreviated version directly returns the requested property, while the full one writes it to the out parameter passed by reference. For example, for properties that are compatible with an integer type, the functions have prototypes like this:

long SymbolInfoInteger(const string symbol, ENUM_SYMBOL_INFO_INTEGER property)

bool SymbolInfoInteger(const string symbol, ENUM_SYMBOL_INFO_INTEGER property, long &value)

The second form returns a boolean indicator of success (true) or error (false). The most possible reasons why a function might return false include an invalid symbol name (MARKET_UNKNOWN_SYMBOL, 4301) or an invalid identifier for the requested property (MARKET_WRONG_PROPERTY, 4303). The details are provided in _LastError.

As before, the properties in the ENUM_SYMBOL_INFO_INTEGER enumeration are of various integer-compatible types: bool, int, long, color, datetime, and special enumerations (all of which will be discussed in separate sections).

For properties with a real number type, the following two forms of the SymbolInfoDouble function are defined.

double SymbolInfoDouble(const string symbol, ENUM_SYMBOL_INFO_DOUBLE property)

bool SymbolInfoDouble(const string symbol, ENUM_SYMBOL_INFO_DOUBLE property, double &value)

Finally, for string properties, similar functions look like this:

string SymbolInfoString(const string symbol, ENUM_SYMBOL_INFO_STRING property)

bool SymbolInfoString(const string symbol, ENUM_SYMBOL_INFO_STRING property, string &value)

The properties of various types which will be often used later when developing Expert Advisors are logically grouped in the descriptions of the following sections of this chapter.

Based on the above functions, we will create a universal class SymbolMonitor (fileSymbolMonitor.mqh) to get any symbol properties. It will be based on a set of overloaded get methods for three enumerations.

```
class SymbolMonitor
{
public:
   const string name;
   SymbolMonitor(): name(_Symbol) { }
   SymbolMonitor(const string s): name(s) { }
   
   long get(const ENUM_SYMBOL_INFO_INTEGER property) const
   {
      return SymbolInfoInteger(name, property);
   }
   
   double get(const ENUM_SYMBOL_INFO_DOUBLE property) const
   {
      return SymbolInfoDouble(name, property);
   }
   
   string get(const ENUM_SYMBOL_INFO_STRING property) const
   {
      return SymbolInfoString(name, property);
   }
   ...

```

The other three similar methods make it possible to eliminate the enumeration type in the first parameter and select the necessary overload by the compiler due to the second dummy parameter (its type here always matches the result type). We will use this in future template classes.

```
   long get(const int property, const long) const
   {
      return SymbolInfoInteger(name, (ENUM_SYMBOL_INFO_INTEGER)property);
   }
 
   double get(const int property, const double) const
   {
      return SymbolInfoDouble(name, (ENUM_SYMBOL_INFO_DOUBLE)property);
   }
 
   string get(const int property, const string) const
   {
      return SymbolInfoString(name, (ENUM_SYMBOL_INFO_STRING)property);
   }
   ...

```

Thus, by creating an object with the desired symbol name, you can uniformly query its properties of any type. To query and log all properties of the same type, we could implement something like this.

```
   // project (draft)
   template<typename E,typename R>
   void list2log()
   {
      E e = (E)0;
      int array[];
      const int n = EnumToArray(e, array, 0, USHORT_MAX);
      for(int i = 0; i < n; ++i)
      {
         e = (E)array[i];
         R r = get(e);
         PrintFormat("% 3d %s=%s", i, EnumToString(e), (string)r);
      }
   }

```

However, due to the fact that in properties of the type long values of other types are actually "hidden", which should be displayed in a specific way (for example, by calling EnumToString for enumerations, imeToString for date and time, etc.), it makes sense to define another three overloaded methods that would return a string representation of the property. Let's call them stringify. Then in the above list2log draft, it is possible to use stringify instead of casting values to (string), and the method itself will eliminate one template parameter.

```
   template<typename E>
   void list2log()
   {
      E e = (E)0;
      int array[];
      const int n = EnumToArray(e, array, 0, USHORT_MAX);
      for(int i = 0; i < n; ++i)
      {
         e = (E)array[i];
         PrintFormat("% 3d %s=%s", i, EnumToString(e), stringify(e));
      }
   }

```

For real and string types, the implementation of stringify looks pretty straightforward.

```
   string stringify(const ENUM_SYMBOL_INFO_DOUBLE property, const string format = NULL) const
   {
      if(format == NULL) return (string)SymbolInfoDouble(name, property);
      return StringFormat(format, SymbolInfoDouble(name, property));
   }
   
   string stringify(const ENUM_SYMBOL_INFO_STRING property) const
   {
      return SymbolInfoString(name, property);
   }

```

But for ENUM_SYMBOL_INFO_INTEGER, everything is a little more complicated. Of course, when the property is of type long or int, it is enough to cast it to (string). All other cases need to be individually analyzed and converted within the switch operator.

```
   string stringify(const ENUM_SYMBOL_INFO_INTEGER property) const
   {
      const long v = SymbolInfoInteger(name, property);
      switch(property)
      {
         ...
      }
      
      return (string)v;
   }

```

For example, if a property has a boolean type, it is convenient to represent it with the string "true" or "false" (thus it will be visually different from the simple numbers 1 and 0). Looking ahead, for the sake of giving an example, let's say that among the properties there is SYMBOL_EXIST, which is equivalent to the [SymbolExist](/en/book/automation/symbols/symbols_exist) function, that is, returning a boolean indication of whether the specified character exists. For its processing and other logical properties, it makes sense to implement an auxiliary method boolean.

```
   static string boolean(const long v)
   {
      return v ? "true" : "false";
   }
   
   string stringify(const ENUM_SYMBOL_INFO_INTEGER property) const
   {
      const long v = SymbolInfoInteger(name, property);
      switch(property)
      {
         case SYMBOL_EXIST:
            return boolean(v);
         ...
      }
      
      return (string)v;
   }

```

For properties that are enumerations, the most appropriate solution would be a template method using the EnumToString function.

```
   template<typename E>
   static string enumstr(const long v)
   {
      return EnumToString((E)v);
   }

```

For example, the SYMBOL_SWAP_ROLLOVER3DAYS property determines on which day of the week a triple swap is charged on open positions for a symbol, and this property has the type [ENUM_DAY_OF_WEEK](/en/book/basis/builtin_types/enums). So, to process it, we can write the following inside switch:

```
         case SYMBOL_SWAP_ROLLOVER3DAYS:
            return enumstr<ENUM_DAY_OF_WEEK>(v);

```

A special case is presented by properties whose values are combinations of bit flags. In particular, for each symbol, the broker sets permissions for orders of specific types, such as market, limit, stop loss, take profit, and others (we will consider these [permissions](/en/book/automation/symbols/symbols_trade_mode) separately). Each type of order is denoted by a constant with one bit enabled, so their superposition (combined by the bitwise OR operator '|') is stored in the SYMBOL_ORDER_MODE property, and in the absence of restrictions, all bits are enabled at the same time. For such properties, we will define our own enumerations in our header file, for example:

```
enum SYMBOL_ORDER
{
   _SYMBOL_ORDER_MARKET = 1,
   _SYMBOL_ORDER_LIMIT = 2,
   _SYMBOL_ORDER_STOP = 4,
   _SYMBOL_ORDER_STOP_LIMIT = 8,
   _SYMBOL_ORDER_SL = 16,
   _SYMBOL_ORDER_TP = 32,
   _SYMBOL_ORDER_CLOSEBY = 64,
};

```

Here, for each built-in constant, such as SYMBOL_ORDER_MARKET, a corresponding element is declared, whose identifier is the same as the constant but is preceded by an underscore to avoid naming conflicts.

To represent combinations of flags from such enumerations in the form of a string, we implement another template method, maskstr.

```
   template<typename E>
   static string maskstr(const long v)
   {
      string text = "";
      for(int i = 0; ; ++i)
      {
         ResetLastError();
         const string s = EnumToString((E)(1 << i));
         if(_LastError != 0)
         {
            break;
         }
         if((v & (1 << i)) != 0)
         {
            text += s + " ";
         }
      }
      return text;
   }

```

Its meaning is like enumstr, but the function EnumToString is called for each enabled bit in the property value, after which the resulting strings are "glued".

Now processing SYMBOL_ORDER_MODE in the statement switch is possible in a similar way:

```
         case SYMBOL_ORDER_MODE:
            return maskstr<SYMBOL_ORDER>(v);

```

Here is the full code of the stringify method for ENUM_SYMBOL_INFO_INTEGER. With all the properties and enumerations, we will gradually get acquainted in the following sections.

```
   string stringify(const ENUM_SYMBOL_INFO_INTEGER property) const
   {
      const long v = SymbolInfoInteger(name, property);
      switch(property)
      {
         case SYMBOL_SELECT:
         case SYMBOL_SPREAD_FLOAT:
         case SYMBOL_VISIBLE:
         case SYMBOL_CUSTOM:
         case SYMBOL_MARGIN_HEDGED_USE_LEG:
         case SYMBOL_EXIST:
            return boolean(v);
         case SYMBOL_TIME:
            return TimeToString(v, TIME_DATE|TIME_SECONDS);
         case SYMBOL_TRADE_CALC_MODE:   
            return enumstr<ENUM_SYMBOL_CALC_MODE>(v);
         case SYMBOL_TRADE_MODE:
            return enumstr<ENUM_SYMBOL_TRADE_MODE>(v);
         case SYMBOL_TRADE_EXEMODE:
            return enumstr<ENUM_SYMBOL_TRADE_EXECUTION>(v);
         case SYMBOL_SWAP_MODE:
            return enumstr<ENUM_SYMBOL_SWAP_MODE>(v);
         case SYMBOL_SWAP_ROLLOVER3DAYS:
            return enumstr<ENUM_DAY_OF_WEEK>(v);
         case SYMBOL_EXPIRATION_MODE:
            return maskstr<SYMBOL_EXPIRATION>(v);
         case SYMBOL_FILLING_MODE:
            return maskstr<SYMBOL_FILLING>(v);
         case SYMBOL_START_TIME:
         case SYMBOL_EXPIRATION_TIME:
            return TimeToString(v);
         case SYMBOL_ORDER_MODE:
            return maskstr<SYMBOL_ORDER>(v);
         case SYMBOL_OPTION_RIGHT:
            return enumstr<ENUM_SYMBOL_OPTION_RIGHT>(v);
         case SYMBOL_OPTION_MODE:
            return enumstr<ENUM_SYMBOL_OPTION_MODE>(v);
         case SYMBOL_CHART_MODE:
            return enumstr<ENUM_SYMBOL_CHART_MODE>(v);
         case SYMBOL_ORDER_GTC_MODE:
            return enumstr<ENUM_SYMBOL_ORDER_GTC_MODE>(v);
         case SYMBOL_SECTOR:
            return enumstr<ENUM_SYMBOL_SECTOR>(v);
         case SYMBOL_INDUSTRY:
            return enumstr<ENUM_SYMBOL_INDUSTRY>(v);
         case SYMBOL_BACKGROUND_COLOR: // Bytes: Transparency Blue Green Red
            return StringFormat("TBGR(0x%08X)", v);
      }
      
      return (string)v;
   }

```

To test the SymbolMonitor class, we have created a simple script SymbolMonitor.mq5. It logs all the properties of the working chart symbol.

```
#include <MQL5Book/SymbolMonitor.mqh>
   
void OnStart()
{
   SymbolMonitor m;
   m.list2log<ENUM_SYMBOL_INFO_INTEGER>();
   m.list2log<ENUM_SYMBOL_INFO_DOUBLE>();
   m.list2log<ENUM_SYMBOL_INFO_STRING>();
}

```

For example, if we run the script on the EURUSD chart, we can get the following records (given in a shortened form).

```
ENUM_SYMBOL_INFO_INTEGER Count=36
  0 SYMBOL_SELECT=true
  ...
  4 SYMBOL_TIME=2022.01.12 10:52:22
  5 SYMBOL_DIGITS=5
  6 SYMBOL_SPREAD=0
  7 SYMBOL_TICKS_BOOKDEPTH=10
  8 SYMBOL_TRADE_CALC_MODE=SYMBOL_CALC_MODE_FOREX
  9 SYMBOL_TRADE_MODE=SYMBOL_TRADE_MODE_FULL
 10 SYMBOL_TRADE_STOPS_LEVEL=0
 11 SYMBOL_TRADE_FREEZE_LEVEL=0
 12 SYMBOL_TRADE_EXEMODE=SYMBOL_TRADE_EXECUTION_INSTANT
 13 SYMBOL_SWAP_MODE=SYMBOL_SWAP_MODE_POINTS
 14 SYMBOL_SWAP_ROLLOVER3DAYS=WEDNESDAY
 15 SYMBOL_SPREAD_FLOAT=true
 16 SYMBOL_EXPIRATION_MODE=_SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY »
    _SYMBOL_EXPIRATION_SPECIFIED _SYMBOL_EXPIRATION_SPECIFIED_DAY
 17 SYMBOL_FILLING_MODE=_SYMBOL_FILLING_FOK
 ... 
 23 SYMBOL_ORDER_MODE=_SYMBOL_ORDER_MARKET _SYMBOL_ORDER_LIMIT _SYMBOL_ORDER_STOP »
    _SYMBOL_ORDER_STOP_LIMIT _SYMBOL_ORDER_SL _SYMBOL_ORDER_TP _SYMBOL_ORDER_CLOSEBY
 ... 
 26 SYMBOL_VISIBLE=true
 27 SYMBOL_CUSTOM=false
 28 SYMBOL_BACKGROUND_COLOR=TBGR(0xFF000000)
 29 SYMBOL_CHART_MODE=SYMBOL_CHART_MODE_BID
 30 SYMBOL_ORDER_GTC_MODE=SYMBOL_ORDERS_GTC
 31 SYMBOL_MARGIN_HEDGED_USE_LEG=false
 32 SYMBOL_EXIST=true
 33 SYMBOL_TIME_MSC=1641984742149
 34 SYMBOL_SECTOR=SECTOR_CURRENCY
 35 SYMBOL_INDUSTRY=INDUSTRY_UNDEFINED
ENUM_SYMBOL_INFO_DOUBLE Count=57
  0 SYMBOL_BID=1.13681
  1 SYMBOL_BIDHIGH=1.13781
  2 SYMBOL_BIDLOW=1.13552
  3 SYMBOL_ASK=1.13681
  4 SYMBOL_ASKHIGH=1.13781
  5 SYMBOL_ASKLOW=1.13552
 ...
 12 SYMBOL_POINT=1e-05
 13 SYMBOL_TRADE_TICK_VALUE=1.0
 14 SYMBOL_TRADE_TICK_SIZE=1e-05
 15 SYMBOL_TRADE_CONTRACT_SIZE=100000.0
 16 SYMBOL_VOLUME_MIN=0.01
 17 SYMBOL_VOLUME_MAX=500.0
 18 SYMBOL_VOLUME_STEP=0.01
 19 SYMBOL_SWAP_LONG=-0.7
 20 SYMBOL_SWAP_SHORT=-1.0
 21 SYMBOL_MARGIN_INITIAL=0.0
 22 SYMBOL_MARGIN_MAINTENANCE=0.0
 ...
 28 SYMBOL_TRADE_TICK_VALUE_PROFIT=1.0
 29 SYMBOL_TRADE_TICK_VALUE_LOSS=1.0
 ...
 43 SYMBOL_MARGIN_HEDGED=100000.0
 ...
 47 SYMBOL_PRICE_CHANGE=0.0132
ENUM_SYMBOL_INFO_STRING Count=15
  0 SYMBOL_BANK=
  1 SYMBOL_DESCRIPTION=Euro vs US Dollar
  2 SYMBOL_PATH=Forex\EURUSD
  3 SYMBOL_CURRENCY_BASE=EUR
  4 SYMBOL_CURRENCY_PROFIT=USD
  5 SYMBOL_CURRENCY_MARGIN=EUR
 ...
 13 SYMBOL_SECTOR_NAME=Currency

```

In particular, you can see that the symbol prices are broadcast with 5 digits (SYMBOL_DIGITS), the symbol does exist (SYMBOL_EXIST), the contract size is 100000.0 (SYMBOL_TRADE_CONTRACT_SIZE), etc. All information corresponds to the specification.
