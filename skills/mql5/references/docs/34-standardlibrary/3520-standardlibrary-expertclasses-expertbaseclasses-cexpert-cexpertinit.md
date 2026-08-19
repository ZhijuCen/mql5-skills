# Init

Class instance initialization method.

```
bool  Init(
   string             symbol,        // symbol
   ENUM_TIMEFRAMES    period,        // timeframe
   bool               every_tick,    // flag
   ulong              magic          // Expert Advisor identifier
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe from [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration.

every_tick

[in]  Flag.

magic

[in]  Expert Advisor ID (Magic number).

Return Value

None.

Note

If every_tick is set to true, the  [Processing()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertprocessing) method is called at each tick of the working symbol. otherwise, the [Processing()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertprocessing) is called only when a new bar is formed on the working timeframe of the EA's working symbol.
