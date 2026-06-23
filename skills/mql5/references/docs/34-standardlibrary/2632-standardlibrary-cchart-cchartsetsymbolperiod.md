# SetSymbolPeriod

Changes symbol and period of the chart assigned to the class instance.

```
bool  SetSymbolPeriod(
   const string     symbol_name,     // symbol
   ENUM_TIMEFRAMES  timeframe        // period
   )

```

Parameters

symbol_name

[in]  New chart symbol. [NULL](/en/docs/basis/types/void) means the symbol of the current chart (to which an expert is attached).

timeframe

[in]  New chart timeframe (from [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration). 0 means the current chart timeframe.

Return Value

true - successful, false - cannot change the property.
