# Open

Opens chart with specified parameters and assigns it to the class instance.

```
long  Open(
   const string     symbol_name,     // symbol
   ENUM_TIMEFRAMES  timeframe        // period
   )

```

Parameters

symbol_name

[in]  Chart symbol. [NULL](/en/docs/basis/types/void) means the symbol of the current chart (to which an expert is attached).

timeframe

[in]  Chart timeframe (from [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration). 0 means the current timeframe.

Return Value

chart identifier.
