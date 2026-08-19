# InfoDouble

Gets the value of specified double type property.

```
bool  InfoDouble(
   ENUM_ORDER_PROPERTY_DOUBLE  prop_id,     // property ID
   double&                     var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of double type property from [ENUM_ORDER_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_double) enumeration.

var

[out]  Reference to [double](/en/docs/basis/types/double) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
