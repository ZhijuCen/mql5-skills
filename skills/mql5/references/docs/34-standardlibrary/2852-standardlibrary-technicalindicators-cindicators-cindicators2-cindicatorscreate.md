# Create

Creates the indicator of the specified type with the specified parameters.

```
CIndicator*  Create(
   const string           symbol,     // symbol name
   const ENUM_TIMEFRAMES  period,     // period
   const ENUM_INDICATOR   type,       // type
   const int              count,      // number of parameters
   const MqlParam&        params      // parameters array
   )

```

Parameters

symbol

[in]  Indicator symbol name.

period

[in]  Indicator timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

type

[in]  Indicator type ([ENUM_INDICATOR](/en/docs/constants/indicatorconstants/enum_indicator) enumeration value).

count

[in]  Number of parameters for the indicator.

params

[in]  Reference to the parameters array for the indicator.

Return Value

Reference to the created indicator - successful, [NULL](/en/docs/basis/types/void) - cannot create the indicator.
