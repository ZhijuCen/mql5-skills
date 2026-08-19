# Init

Initializes the object.

```
bool  Init(
   CSymbolInfo      symbol,   // symbol
   ENUM_TIMEFRAMES  period,   // timeframe
   double           point     // point
   )

```

Parameters

symbol

[in]  Pointer to the object of [CSymbolInfo](/en/docs/standardlibrary/tradeclasses/csymbolinfo) type for access to symbol information.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration).

point

[in]  The "weight" of 2/4-digit point.

Return Value

true - successful completion, otherwise - false.
