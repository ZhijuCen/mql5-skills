# Trailing Stop classes

This section contains technical details of working with trailing stop classes and description of the relevant components of the MQL5 standard library.

The use of these classes will save time when creating (and testing) trading strategies.

MQL5 Standard Library (in terms of trading strategies) is placed in the terminal directory, in the  Include\Expert\Trailing folder.

| Class | Description |
| --- | --- |
| CTrailingFixedPips | This class implements Trailing Stop algorithm based on fixed points |
| CTrailingMA | This class implements Trailing Stop algorithm based on the values of Moving Average indicator |
| CTrailingNone | A stub class, it does not uses any Trailing Stop algorithm |
| CTrailingPSAR | This class implements Trailing Stop algorithm based on the values of Parabolic SAR indicator |
