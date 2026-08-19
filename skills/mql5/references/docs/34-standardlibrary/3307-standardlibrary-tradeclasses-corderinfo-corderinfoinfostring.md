# InfoString

Gets the value of specified string type property.

```
bool  InfoString(
   ENUM_ORDER_PROPERTY_STRING  prop_id,     // property ID
   string&                     var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of string property from [ENUM_ORDER_PROPERTY_STRING](/en/docs/constants/tradingconstants/orderproperties) enumeration.

var

[out]  Reference to [string](/en/docs/basis/types/stringconst) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
