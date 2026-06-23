# SymbolInfoInteger

Returns the corresponding property of a specified symbol. There are 2 variants of the function.

1. Immediately returns the property value.

```
long  SymbolInfoInteger(
   string                    name,      // symbol
   ENUM_SYMBOL_INFO_INTEGER  prop_id    // identifier of a property
 
   );

```

2. Returns true or false depending on whether a function is successfully performed. In case of success, the value of the property is placed into a recipient variable, passed by reference by the last parameter.

```
bool  SymbolInfoInteger(
   string                    name,      // symbol
   ENUM_SYMBOL_INFO_INTEGER  prop_id,   // identifier of a property
   long&                     long_var   // here we accept the property value
   );

```

Parameters

name

[in] Symbol name.

prop_id

[in] Identifier of a symbol property. The value can be one of the values of the [ENUM_SYMBOL_INFO_INTEGER](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer) enumeration.

long_var

[out] Variable of the long type receiving the value of the requested property.

Return Value

The value of long type. In case of execution failure, information about the [error](/en/docs/constants/errorswarnings/errorcodes) can be obtained using [GetLastError()](/en/docs/check/getlasterror) function:

- 5040 – invalid string parameter for specifying a symbol name,
- 4301 – unknown symbol (financial instrument),
- 4302 – symbol is not selected in "Market Watch" (not found in the list of available ones),
- 4303 – invalid identifier of a symbol property.

Note

It is recommended to use [SymbolInfoTick()](/en/docs/marketinformation/symbolinfotick) if the function is used for getting information about the last tick. It may well be that not a single quote has appeared yet since the terminal is connected to a trading account. In such a case, the requested value will be indefinite.

In most cases, it is enough to use [SymbolInfoTick()](/en/docs/marketinformation/symbolinfotick) function allowing a user to receive the values of Ask, Bid, Last, Volume and the time of the last tick's arrival during a single call.

Example:

```
void OnTick()
  {
//--- obtain spread from the symbol properties
   bool spreadfloat=SymbolInfoInteger(Symbol(),SYMBOL_SPREAD_FLOAT);
   string comm=StringFormat("Spread %s = %I64d points\r\n",
                            spreadfloat?"floating":"fixed",
                            SymbolInfoInteger(Symbol(),SYMBOL_SPREAD));
//--- now let's calculate the spread by ourselves
   double ask=SymbolInfoDouble(Symbol(),SYMBOL_ASK);
   double bid=SymbolInfoDouble(Symbol(),SYMBOL_BID);
   double spread=ask-bid;
   int spread_points=(int)MathRound(spread/SymbolInfoDouble(Symbol(),SYMBOL_POINT));
   comm=comm+"Calculated spread = "+(string)spread_points+" points";
   Comment(comm);
  }

```
