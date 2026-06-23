# The predefined Variables

For each executable mql5-program a set of predefined variables is supported, which reflect the state of the current price chart by the moment a mql5-program (Expert Advisor, script or custom indicator) is started.

Values of predefined variables are set by the client terminal before a mql5-program is started. Predefined variables are constant and cannot be changed from a mql5-program. As exception, there is a special variable _LastError, which can be reset to 0 by the [ResetLastError](/en/docs/common/resetlasterror) function.

| Variable | Value |
| --- | --- |
| _AppliedTo | The _AppliedTo variable allows finding out the type of data, used for indicator calculation |
| _Digits | Number of decimal places |
| _Point | Size of the current symbol point in the quote currency |
| _LastError | The last error code |
| _Period | Timeframe of the current chart |
| _RandomSeed | Current status of the generator of pseudo-random integers |
| _StopFlag | Program stop flag |
| _Symbol | Symbol name of the current chart |
| _UninitReason | Uninitialization reason code |
| _IsX64 | The _IsX64 variable allows finding out the bit version of the terminal, in which an MQL5 application is running |

Predefined variables cannot be defined in a library. A library uses such variables that are defined in program from which this library is called.
