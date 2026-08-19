# TerminalInfoDouble

Returns the value of a corresponding property of the mql5 program environment.

```
double  TerminalInfoDouble(
   int  property_id      // identifier of a property
   );

```

Parameters

property_id

[in] Identifier of a property. Can be one of the values of the [ENUM_TERMINAL_INFO_DOUBLE](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_double) enumeration.

Return Value

Value of double type.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the build number of the running terminal and its "64-bit terminal" property
   int  build = TerminalInfoInteger(TERMINAL_BUILD);
   bool x64   = TerminalInfoInteger(TERMINAL_X64);
   
//--- print the obtained terminal data in the journal
   PrintFormat("MetaTrader 5 %s build %d", (x64 ? "x64" : "x32"), build);
   /*
   result:
   MetaTrader 5 x64 build 4330
   */
  }

```
