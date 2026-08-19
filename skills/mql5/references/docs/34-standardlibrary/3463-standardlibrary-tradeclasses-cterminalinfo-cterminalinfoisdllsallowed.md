# IsDLLsAllowed

Gets the information about permission of DLL usage.

```
bool  IsDLLsAllowed() const 

```

Return Value

true - DLL usage is allowed, otherwise - false.

Note

Permission of DLL usage is defined by [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_DLLS_ALLOWED](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
