# SetInteger

Sets new value for the property of the integer type.

```
bool  SetInteger(
   ENUM_CHART_PROPERTY_INTEGER  prop_id,     // property identifier
   long                         value        // value
   )

```

Parameters

prop_id

[in]  Chart property identifier (from [ENUM_CHART_PROPERTY_INTEGER](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer) enumeration).

value

[in]  New value of the property.

Return Value

true - successful, false - cannot change the integer property.
