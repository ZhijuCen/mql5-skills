# PlotIndexSetString

The function sets the value of the corresponding property of the corresponding indicator line. The indicator property must be of the string type.

```
bool  PlotIndexSetString(
   int     plot_index,     // plotting style index
   int     prop_id,        // property identifier
   string  prop_value      // value to be set
   );

```

Parameters

plot_index

[in]  Index of [graphical plot](/en/docs/constants/indicatorconstants/drawstyles#enum_draw_type)

prop_id

[in] The value can be one of the values of the [ENUM_PLOT_PROPERTY_STRING](/en/docs/constants/indicatorconstants/drawstyles#enum_plot_property_string) enumeration.

prop_value

[in]  The value of the property.

Return Value

If successful, returns [true](/en/docs/basis/types/integer/boolconst), otherwise [false](/en/docs/basis/types/integer/boolconst).
