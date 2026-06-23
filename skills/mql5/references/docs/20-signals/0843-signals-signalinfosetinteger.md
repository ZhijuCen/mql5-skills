# SignalInfoSetInteger

Sets the value of [integer](/en/docs/basis/types/integer) type property of signal copy settings.

```
bool  SignalInfoSetInteger(
   ENUM_SIGNAL_INFO_INTEGER     property_id,     // property identifier
   long                         value            // new value
   );

```

Parameters

property_id

[in]  Signal copy settings property identifier. The value can be one of the values of the [ENUM_SIGNAL_INFO_INTEGER](/en/docs/constants/tradingconstants/signalproperties#enum_signal_info_integer) enumeration.

value

[in]  The value of signal copy settings property.

Return Value

Returns true if property has been changed, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).
