# PlotIndexSetDouble

The function sets the value of the corresponding property of the corresponding indicator line. The indicator property must be of the double type.

```
bool  PlotIndexSetDouble(
   int     plot_index,     // plotting style index
   int     prop_id,        // property identifier
   double  prop_value      // value to be set
   );

```

Parameters

plot_index

[in]  Index of the [graphical plotting](/en/docs/constants/indicatorconstants/drawstyles#enum_draw_type)

prop_id

[in] The value can be one of the values of the [ENUM_PLOT_PROPERTY_DOUBLE](/en/docs/constants/indicatorconstants/drawstyles#enum_plot_property_double) enumeration.

prop_value

[in]  The value of the property.

Return Value

If successful, returns [true](/en/docs/basis/types/integer/boolconst), otherwise [false](/en/docs/basis/types/integer/boolconst).
