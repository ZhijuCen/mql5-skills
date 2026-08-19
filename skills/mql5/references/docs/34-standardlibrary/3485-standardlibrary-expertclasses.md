# Classes for Creating and Testing Trading Strategies

This section contains technical details of working with classes for creation and testing of trading strategies and description of the relevant components of the MQL5 standard library.

The use of these classes will save time when creating (and especially testing) trading strategies.

MQL5 Standard Library (in terms of trading strategies) is placed in the terminal directory, in the Include\Expert folder.

| Base classes | Description |
| --- | --- |
| CExpertBase | Base class for all trading strategy classes |
| CExpert | Base class for Expert Advisor |
| CExpertSignal | Base class for Trading Signal classes |
| CExpertTrailing | Base class for Trailing Stop classes |
| CExpertMoney | Base class for Money Management classes |

| Trading signal classes | Description |
| --- | --- |
| CSignalAC | The module of signals based on market models of the indicator Accelerator Oscillator. |
| CSignalAMA | The module of signals based on market models of the indicator Adaptive Moving Average. |
| CSignalAO | The module of signals based on market models of the indicator Awesome Oscillator. |
| CSignalBearsPower | The module of signals based on market models of the oscillator Bears Power. |
| CSignalBullsPower | The module of signals based on market models of the oscillator Bulls Power. |
| CSignalCCI | The module of signals based on market models of the oscillator Commodity Channel Index. |
| CSignalDeM | The module of signals based on market models of the oscillator DeMarker. |
| CSignalDEMA | The module of signals based on market models of the indicator Double Exponential Moving Average. |
| CSignalEnvelopes | The module of signals based on market models of the indicator Envelopes. |
| CSignalFrAMA | The module of signals based on market models of the indicator Fractal Adaptive Moving Average. |
| CSignalITF | The module of filtration of signals by time. |
| CSignalMACD | The module of signals based on market models of the oscillator MACD. |
| CSignalMA | The module of signals based on market models of the indicator Moving Average. |
| CSignalSAR | The module of signals based on market models of the indicator Parabolic SAR. |
| CSignalRSI | The module of signals based on market models of the oscillator Relative Strength Index. |
| CSignalRVI | The module of signals based on market models of the oscillator Relative Vigor Index. |
| CSignalStoch | The module of signals based on market models of the oscillator Stochastic. |
| CSignalTRIX | The module of signals based on market models of the oscillator Triple Exponential Average. |
| CSignalTEMA | The module of signals based on market models of the indicator Triple Exponential Moving Average. |
| CSignalWPR | The module of signals based on market models of the oscillator Williams Percent Range. |

| Trailing Stop classes | Description |
| --- | --- |
| CTrailingFixedPips | This class implements Trailing Stop algorithm based on fixed points |
| CTrailingMA | This class implements Trailing Stop algorithm based on the values of Moving Average indicator |
| CTrailingNone | A stub class, it does not use any Trailing Stop algorithm |
| CTrailingPSAR | This class implements Trailing Stop algorithm based on the values of Parabolic SAR indicator |

| Money Management classes | Description |
| --- | --- |
| CMoneyFixedLot | A class with an algorithm based on trading with predefined fixed lot size. |
| CMoneyFixedMargin | A class with an algorithm based on trading with predefined fixed margin. |
| CMoneyFixedRisk | A class with an algorithm based on trading with predefined risk. |
| CMoneyNone | A class with an algorithm based on trading with minimal allowed lot size. |
| CMoneySizeOptimized | A class with an algorithm based on trading with variable lot size, depending on the results of the previous deals. |
