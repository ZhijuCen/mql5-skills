# OpenCLSupport

Gets the information about the version of OpenCL supported by video card.

```
int  OpenCLSupport() const 

```

Return Value

OpenCL version having the following form: 0x00010002 = "1.2". 0 means that OpenCL is not supported.

Note

OpenCL version is defined by [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_OPENCL_SUPPORT](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
