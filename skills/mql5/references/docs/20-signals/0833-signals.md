# Trade Signals

This is the group of functions intended for managing trade signals. The functions allow:

- get information about trade signals, available for copying,
- get and set the signal copy settings,
- subscribe and unsubscribe to the signal copying using MQL5 language functions.

| Function | Action |
| --- | --- |
| SignalBaseGetDouble | Returns the value of double type property for selected signal |
| SignalBaseGetInteger | Returns the value of integer type property for selected signal |
| SignalBaseGetString | Returns the value of string type property for selected signal |
| SignalBaseSelect | Selects a signal from signals, available in terminal for further working with it |
| SignalBaseTotal | Returns the total amount of signals, available in terminal |
| SignalInfoGetDouble | Returns the value of double type property of signal copy settings |
| SignalInfoGetInteger | Returns the value of integer type property of signal copy settings |
| SignalInfoGetString | Returns the value of string type property of signal copy settings |
| SignalInfoSetDouble | Sets the value of double type property of signal copy settings |
| SignalInfoSetInteger | Sets the value of integer type property of signal copy settings |
| SignalSubscribe | Subscribes to the trading signal |
| SignalUnsubscribe | Cancels subscription |
