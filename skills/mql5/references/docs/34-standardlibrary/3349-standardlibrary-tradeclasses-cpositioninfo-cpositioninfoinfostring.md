# InfoString

Gets the value of specified string type property.

```
bool  InfoString(
   ENUM_POSITION_PROPERTY_STRING  prop_id,     // property ID
   string&                        var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of text property from [ENUM_POSITION_PROPERTY_STRING](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_string) enumeration.

var

[out]  Reference to [string](/en/docs/basis/types/stringconst) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The position should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselectbyindex) (by index) methods.
