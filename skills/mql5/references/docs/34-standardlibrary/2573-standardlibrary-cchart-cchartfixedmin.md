# FixedMin (Get Method)

Gets the value of "FixedMin" property (fixed minimal price).

```
double  FixedMin() const

```

Return Value

Value of "FixedMin" property of the chart assigned to the class instance. If there is no chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# FixedMin (Set Method)

Sets new value for "FixedMin" property.

```
bool  FixedMax(
   double  min      // fixed minimum
   )

```

Parameters

max

[in]  New value for "FixedMin" property.

Return Value

true - successful, false - cannot change the property.
