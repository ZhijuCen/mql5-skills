# SetString

Sets new value for the chart property of the string type.

```
bool  SetString(
   ENUM_CHART_PROPERTY_STRING  prop_id,     // property identifier
   string                      value        // value
   )

```

Parameters

prop_id

[in]  Chart property identifier (from [ENUM_CHART_PROPERTY_STRING](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_string) enumeration).

value

[in]  New value for the property.

Return Value

true - successful, false - cannot change the string property.
