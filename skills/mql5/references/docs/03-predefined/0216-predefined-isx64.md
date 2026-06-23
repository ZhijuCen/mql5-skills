# int _IsX64

The _IsX64 variable allows finding out the bit version of the terminal, in which an MQL5 application is running: _IsX64=0 for the 32-bit terminal and _IsX64!=0 for the 64-bit terminal.

Also, function [TerminalInfoInteger(](/en/docs/check/terminalinfointeger)[TERMINAL_X64](/en/docs/check/terminalinfointeger)[)](/en/docs/check/terminalinfointeger) can be used.

Example:

```
// Checking the terminal, in which the program is running
   Print("_IsX64=",_IsX64);
   if(_IsX64)
      Print("Program ",__FILE__," is running in the 64-bit terminal");
   else
      Print("Program ",__FILE__," is running in the 32-bit terminal");
   Print("TerminalInfoInteger(TERMINAL_X64)=",TerminalInfoInteger(TERMINAL_X64));

```

See also

[MQLInfoInteger](/en/docs/check/mqlinfointeger), [Importing functions (#import)](/en/docs/basis/preprosessor/import)
