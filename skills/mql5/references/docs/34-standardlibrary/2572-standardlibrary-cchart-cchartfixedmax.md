# FixedMax (Get Method)

Gets the value of "FixedMax" property (fixed maximal price).

```
double  FixedMax() const

```

Return Value

Value of "FixedMax" property of the chart assigned to the class instance. If there is no chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# FixedMax (Set Method)

Sets the new value for "FixedMax" property.

```
bool  FixedMax(
   double  max      // fixed maximum
   )

```

Parameters

max

[in]  New value for "FixedMax" property.

Return Value

true - successful, false - cannot change the property.
