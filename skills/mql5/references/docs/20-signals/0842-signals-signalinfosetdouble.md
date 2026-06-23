# SignalInfoSetDouble

Sets the value of [double](/en/docs/basis/types/double) type property of signal copy settings.

```
bool  SignalInfoSetDouble(
   ENUM_SIGNAL_INFO_DOUBLE      property_id,     // property identifier
   double                       value            // new value
   );

```

Parameters

property_id

[in]  Signal copy settings property identifier. The value can be one of the values of the [ENUM_SIGNAL_INFO_DOUBLE](/en/docs/constants/tradingconstants/signalproperties#enum_signal_info_double) enumeration.

value

[in]  The value of signal copy settings property.

Return Value

Returns true if property has been changed, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).
