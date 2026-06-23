# Create

Creates the indicator of the specified type with the specified parameters.

```
bool  Create(
   const string           symbol,         // symbol
   const ENUM_TIMEFRAMES  period,         // period
   const ENUM_INDICATOR   type,           // type
   const int              num_params,     // number of parameters
   const MqlParam&        params[]        // array of parameters
   )

```

Parameters

symbol

[in]  Indicator symbol.

period

[in]  Indicator timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration).

type

[in]  Indicator type ([ENUM_INDICATOR](/en/docs/constants/indicatorconstants/enum_indicator) enumeration).

num_params

[in]  Number of indicator's parameters.

params

[in]  Reference to the parameters array for the indicator.

Return Value

true - successful, false - cannot create the indicator.
