# InfoInteger

Gets the value of specified integer type property.

```
bool  InfoInteger(
   ENUM_ORDER_PROPERTY_INTEGER  prop_id,     // property ID
   long&                        var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of integer type property from [ENUM_ORDER_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer) enumeration.

var

[out]  Reference to [long](/en/docs/basis/types/integer/integertypes) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
