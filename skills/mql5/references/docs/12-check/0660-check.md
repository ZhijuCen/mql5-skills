# State Checking

Functions that return parameters of the current state of the client terminal

| Function | Action |
| --- | --- |
| GetLastError | Returns the last error |
| IsStopped | Returns true, if an mql5 program has been commanded to stop its operation |
| UninitializeReason | Returns the code of the reason for deinitialization |
| TerminalInfoInteger | Returns an integer value of a corresponding property of the mql5 program environment |
| TerminalInfoDouble | Returns a double value of a corresponding property of the mql5 program environment |
| TerminalInfoString | Returns a string value of a corresponding property of the mql5 program environment |
| MQLInfoInteger | Returns an integer value of a corresponding property of a running mql5 program |
| MQLInfoString | Returns a string value of a corresponding property of a running mql5 program |
| Symbol | Returns the name of a symbol of the current chart |
| Period | Returns the current chart timeframe |
| Digits | Returns the number of decimal digits determining the accuracy of the price value of the current chart symbol |
| Point | Returns the point size of the current symbol in the quote currency |
