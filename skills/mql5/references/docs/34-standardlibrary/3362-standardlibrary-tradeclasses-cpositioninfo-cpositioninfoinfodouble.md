# InfoDouble

Gets the value of specified double type property.

```
bool  InfoDouble(
   ENUM_POSITION_PROPERTY_DOUBLE  prop_id,     // property ID
   double&                        var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of double type property from [ENUM_POSITION_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_double) enumeration.

var

[in]  Reference to [double](/en/docs/basis/types/double) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The position should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselectbyindex) (by index) methods.
