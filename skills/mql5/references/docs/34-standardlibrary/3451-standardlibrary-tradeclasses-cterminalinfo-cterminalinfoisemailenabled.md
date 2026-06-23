# IsEmailEnabled

Gets the information about permission to send e-mails to SMTP server and login specified in the terminal settings.

```
bool  IsEmailEnabled() const 

```

Return Value

true - sending e-mails is allowed, otherwise - false.

Note

Permission to send e-mails is defined by [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_EMAIL_ENABLED](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
