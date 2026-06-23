# IsConnected

Gets the information about connection to trade server.

```
bool  IsConnected() const 

```

Return Value

true - the terminal is connected to a trade server, otherwise - false.

Note

Connection status is defined by [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_CONNECTED](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
