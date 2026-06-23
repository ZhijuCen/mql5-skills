# IsFtpEnabled

Gets the information about permission to send trade reports to FTP server and login specified in the terminal settings.

```
bool  IsFtpEnabled() const 

```

Return Value

true - sending trade reports to FTP server is allowed, otherwise - false.

Note

Permission to send trade reports is defined [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_FTP_ENABLED](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
