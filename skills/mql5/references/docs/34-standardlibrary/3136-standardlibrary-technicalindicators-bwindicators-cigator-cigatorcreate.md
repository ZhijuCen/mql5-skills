# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,           // symbol
   ENUM_TIMEFRAMES  period,           // period
   int              jaw_period,       // jaws period
   int              jaw_shift,        // jaws shift
   int              teeth_period,     // teeth period
   int              teeth_shift,      // teeth shift
   int              lips_period,      // lips period
   int              lips_shift,       // lips shift
   ENUM_MA_METHOD   ma_method,        // averaging method
   int              applied           // price type, handle
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

jaw_period

[in]  Jaws averaging period.

jaw_shift

[in]  Jaws horizontal shift.

teeth_period

[in]  Teeth averaging period.

teeth_shift

[in]  Teeth horizontal shift.

lips_period

[in]  Lips averaging period.

lips_shift

[in]  Lips horizontal shift.

ma_method

[in]  Averaging method ([ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method) enumeration value).

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
