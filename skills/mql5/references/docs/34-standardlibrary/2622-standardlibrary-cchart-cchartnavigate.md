# Navigate

Shifts the chart.

```
bool  Navigate(
   ENUM_CHART_POSITION  position,     // position
   int                  shift=0       // shift
   )

```

Parameters

position

[in]  Chart position (from [ENUM_CHART_POSITION](/en/docs/constants/chartconstants/enum_chart_position) enumeration), relative to which a shift is performed.

shift=0

[in]  Number of bars to shift.

Return Value

true - successful, false - cannot shift the chart.
