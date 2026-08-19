# Mode (Get Method)

Gets the value of "Mode" property (bars, candles, or line).

```
ENUM_CHART_MODE  Mode() const

```

Return Value

Value of "Mode" property of the object assigned to the class instance. If there is no chart assigned, it returns [WRONG_VALUE](/en/docs/constants/namedconstants/otherconstants).

# Mode (Set Method)

Sets new value for "Mode" property (bars, candles, or line).

```
bool  Mode(
   ENUM_CHART_MODE  mode      // chart mode
   )

```

Parameters

mode

[in]  Chart mode (candles, bars or line) of [ENUM_CHART_MODE](/en/docs/constants/chartconstants/chart_view#enum_chart_mode) enumeration.

Return Value

true - successful, false - cannot change the mode.
