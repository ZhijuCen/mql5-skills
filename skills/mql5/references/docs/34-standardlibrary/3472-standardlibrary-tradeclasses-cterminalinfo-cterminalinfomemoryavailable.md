# MemoryAvailable

Gets the information about the free memory available to the client terminal/agent (in Mb).

```
int  MemoryTotal() const 

```

Return Value

Free memory (in Mb) available to the terminal/agent.

Note

The free memory available to the client terminal/agent is defined by [TerminalInfoInteger()](/en/docs/check/terminalinfointeger) function ([TERMINAL_MEMORY_TOTAL](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer) property).
