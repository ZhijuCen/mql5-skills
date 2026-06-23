# GetInteger

The function returns the value of the corresponding chart property. The chart property should be of the [integer](/en/docs/basis/types/integer) type. There are two variants of the function.

1. Immediately returns the property value.

```
long  GetInteger(
   ENUM_CHART_PROPERTY_INTEGER  prop_id,          // property identifier
   int                          sub_window=0      // subwindow number
   ) const

```

2. If successful, puts the value of property to the specified variable of integer type, passed by reference as last parameter.

```
bool  GetInteger(
   ENUM_CHART_PROPERTY_INTEGER  prop_id,        // property identifier
   int                          sub_window,     // subwindow number
   long&                        value           // link to the variable
   ) const

```

Parameters

prop_id

[in]  Property identifier ([ENUM_CHART_PROPERTY_INTEGER](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer) enumeration).

sub_window

[in]  Chart subwindow number.

value

[in]  Link to the variable that receives the value of the requested property.

Return Value

Value of property of the chart assigned to the class instance. If there is not any chart assigned, it returns -1.

For the second variant, the function returns true, if this property is maintained and the value has been placed into the value variable, otherwise it returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).
