# InfoString

The function returns the value of a corresponding property of the mql5 program environment. The property must be of string type.

```
string  TerminalInfoString(
   int  property_id      // property ID
   );

```

Parameters

property_id

[in] Identifier of a property. It can be one the values of the enumeration [ENUM_TERMINAL_INFO_STRING](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_string).

Return Value

Value of string type.

Note

The property value is defined by [TerminalInfoString()](/en/docs/check/terminalinfostring) function.
