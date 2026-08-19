# GetDouble

The function returns the value of the corresponding chart property. The object property should be of the double type. There are two variants of the function.

1. Immediately returns the property value.

```
double  GetDouble(
   ENUM_CHART_PROPERTY_DOUBLE  prop_id,          // property identifier
   int                         sub_window=0      // subwindow number
   ) const

```

2. If successful, puts the value of property to the specified variable of double  type, passed by reference as last parameter.

```
bool  GetDouble(
   ENUM_CHART_PROPERTY_DOUBLE  prop_id,        // property identifier
   int                         sub_window,     // subwindow number
   double&                     value           // link to the variable
   ) const

```

Parameters

prop_id

[in]  Chart property identifier (from [ENUM_CHART_PROPERTY_DOUBLE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_double) enumeration).

sub_window

[in]  Chart subwindow number.

value

[in]  Variable of the double type that received the value of the requested property.

Return Value

Value of property of the chart assigned to the class instance. If there is not any chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

For the second variant the function, it returns true if the property value is received, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).
