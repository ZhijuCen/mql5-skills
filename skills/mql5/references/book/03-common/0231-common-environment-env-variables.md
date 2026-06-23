# Predefined variables

Each MQL program has a certain general set of global variables provided by the terminal: we have already covered most of them in the previous sections, and below is a summary table. Almost all variables are read-only. The exception is the variable _LastError, which can be reset by the [ResetLastError](/en/book/common/environment/env_last_error) function.

| Variable | Value |
| --- | --- |
| _LastError | Last error value, an analog of the  GetLastError  function |
| _StopFlag | Program stop flag, an analog of the  IsStopped  function |
| _UninitReason | Program deinitialization reason code, an analog of the  UninitializeReason  function |
| _RandomSeed | Current internal state of the  pseudo-random integer generator |
| _IsX64 | Flag of a 64-bit terminal, analog of  TerminalInfoInteger  for the TERMINAL_X64 property |

In addition, for MQL programs running in the chart context of a chart, such as Expert Advisors, scripts, and indicators, the language provides predefined variables with chart properties (they also cannot be changed from the program).

| Variable | Value |
| --- | --- |
| _Symbol | Name of the current chart symbol, an analog of the  Symbol  function |
| _Period | Current chart  timeframe , an analog of the  Period  function |
| _Digits | The number of decimal places in the price of the current chart symbol, an analog of the  Digits  function |
| _Point | Point size in the prices of the current symbol (in the quote currency), an analog of the  Point  function |
| _AppliedTo | Type of data on which the  indicator  is calculated (only for indicators) |
