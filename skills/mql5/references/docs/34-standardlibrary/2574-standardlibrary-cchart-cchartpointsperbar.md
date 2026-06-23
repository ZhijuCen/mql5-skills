# PointsPerBar (Get Method)

Gets the value of "PointsPerBar" property (in points per bar).

```
double  PointsPerBar() const

```

Return Value

Value of "PointsPerBar" property of the chart assigned to the class instance. If there is no chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# PointsPerBar (Set Method)

Sets new value for "PointsPerBar" property.

```
bool  PointsPerBar(
   double  ppb      // scale
   )

```

Parameters

ppb

[in]  New scale (in points per bar).

Return Value

true - successful, false - cannot change the scale.
