# ShiftSize (Get Method)

Gets the value of "ShiftSize" property (in percents).

```
double  ShiftSize() const

```

Return Value

Value of "ShiftSize" property of the chart assigned to the class instance. If there is no chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# ShiftSize (Set Method)

Sets new value for "Shift" property (in percents).

```
bool  ShiftSize(
   double  shift_size      // property value
   )

```

Parameters

shift_size

[in]  New value for "ShiftSize" property (in percents).

Return Value

true - successful, false - cannot change the property.
