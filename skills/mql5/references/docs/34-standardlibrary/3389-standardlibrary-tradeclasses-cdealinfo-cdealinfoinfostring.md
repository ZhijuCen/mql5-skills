# InfoString

Gets the value of specified string type property.

```
bool  InfoString(
   ENUM_DEAL_PROPERTY_STRING  prop_id,     // property ID
   string&                    var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of text property from [ENUM_DEAL_PROPERTY_STRING](/en/docs/constants/tradingconstants/dealproperties#enum_deal_property_string) enumeration.

var

[out]  Reference to [string](/en/docs/basis/types/stringconst) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The deal should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfoselectbyindex) (by index) methods.
