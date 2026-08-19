# InfoInteger

Gets the value of specified integer type property.

```
bool  InfoInteger(
   ENUM_SYMBOL_INFO_INTEGER  prop_id,     // property ID
   long&                     var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of integer type property from [ENUM_SYMBOL_INFO_INTEGER](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer) enumeration.

var

[out]  Reference to [long](/en/docs/basis/types/integer/integertypes) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The symbol should be selected by [Name](/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfoname) method.
