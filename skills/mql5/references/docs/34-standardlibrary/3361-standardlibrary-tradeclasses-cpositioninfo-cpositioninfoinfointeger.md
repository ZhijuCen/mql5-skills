# InfoInteger

Gets the value of specified integer type property.

```
bool  InfoInteger(
   ENUM_POSITION_PROPERTY_INTEGER  prop_id,     // property ID
   long&                           var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of integer type property from [ENUM_POSITION_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_integer) enumeration.

var

[out]  Reference to [long](/en/docs/basis/types/integer/integertypes) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The position should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselectbyindex) (by index) methods.
