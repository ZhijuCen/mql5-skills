# InfoDouble

Gets the value of specified double type property.

```
bool  InfoDouble(
   ENUM_SYMBOL_INFO_DOUBLE  prop_id,     // property ID
   double&                  var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of double type property from [ENUM_SYMBOL_INFO_DOUBLE](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_double) enumeration.

var

[out]  Reference to [double](/en/docs/basis/types/double) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The symbol should be selected by [Name](/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfoname) method.
