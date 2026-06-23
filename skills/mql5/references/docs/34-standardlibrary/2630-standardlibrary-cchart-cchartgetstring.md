# GetString

The function returns the value of the corresponding chart property. The chart property should be of the string type. There are two variants of the function.

1. Immediately returns the property value.

```
string  GetString(
   ENUM_CHART_PROPERTY_STRING  prop_id      // property identifier
   ) const

```

2. If successful, puts the value of property to the specified variable of string type, passed by reference as last parameter.

```
bool  GetString(
   ENUM_CHART_PROPERTY_STRING  prop_id,     // property identifier
   string&                     value        // link to the variable
   ) const

```

Parameters

prop_id

[in]  Chart property identifier (from [ENUM_CHART_PROPERTY_STRING](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_string) enumeration).

value

[in]  Link to the variable that receives the value of the requested property.

Return Value

Value of a chart property assigned to the class instance. If there is no chart assigned, it returns "".

For the second variant, the function returns true, if this property is maintained and the value has been placed into the value variable, otherwise it returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).
