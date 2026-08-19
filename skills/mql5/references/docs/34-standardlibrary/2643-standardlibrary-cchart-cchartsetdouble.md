# SetDouble

Sets new value for the chart property of the double type.

```
bool  SetDouble(
   ENUM_CHART_PROPERTY_DOUBLE  prop_id,     // property identifier
   double                      value        // new value
   )

```

Parameters

prop_id

[in]  Chart property identifier (from [ENUM_CHART_PROPERTY_DOUBLE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_double) enumeration).

value

[in]  New value for the property.

Return Value

true - successful, false - cannot change the double property.
