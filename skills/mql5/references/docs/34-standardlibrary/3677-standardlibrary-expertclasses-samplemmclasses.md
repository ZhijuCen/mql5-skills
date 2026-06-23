# Money Management classes

This section contains technical details of working with money and risk management classes and description of the relevant components of the MQL5 standard library.

The use of these classes will save time when creating (and testing) trading strategies.

MQL5 Standard Library (in terms of money and risk management classes) is placed in the terminal directory, in the Include\Expert\Money\ folder.

| Class | Description |
| --- | --- |
| CMoneyFixedLot | This class implements money management algorithm based on trading with predefined fixed lot size. |
| CMoneyFixedMargin | This class implements money management algorithm based on trading with predefined fixed margin. |
| CMoneyFixedRisk | This class implements money management algorithm based on trading with predefined risk. |
| CMoneyNone | This class implements money management algorithm based on trading with minimal allowed lot size. |
| CMoneySizeOptimized | This class implements money management algorithm based on trading with variable lot size, depending on results of the previous deals. |
