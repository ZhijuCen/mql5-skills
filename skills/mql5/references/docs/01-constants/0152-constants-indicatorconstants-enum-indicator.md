# Types of Technical Indicators

There are two ways to create an indicator handle for further [accessing to its values](/en/docs/series). The first way is to directly specify a function name from the list of [technical indicators](/en/docs/indicators). The second method using the [IndicatorCreate()](/en/docs/series/indicatorcreate) is to uniformly create a handle of any indicator by assigning an identifier from the ENUM_INDICATOR enumeration. Both ways of handle creation are equal, you can use the one that is most convenient in a particular case when writing a program in MQL5.

When creating an indicator of type IND_CUSTOM, the type field of the first element of an array of [input parameters MqlParam](/en/docs/constants/structures/mqlparam) must have the TYPE_STRING value of the enumeration [ENUM_DATATYPE](/en/docs/constants/indicatorconstants/enum_datatype), while the field string_value of the first element must contain the name of the custom indicator.

ENUM_INDICATOR

| Identifier | Indicator |
| --- | --- |
| IND_AC | Accelerator Oscillator |
| IND_AD | Accumulation/Distribution |
| IND_ADX | Average Directional Index |
| IND_ADXW | ADX by Welles Wilder |
| IND_ALLIGATOR | Alligator |
| IND_AMA | Adaptive Moving Average |
| IND_AO | Awesome Oscillator |
| IND_ATR | Average True Range |
| IND_BANDS | Bollinger Bands® |
| IND_BEARS | Bears Power |
| IND_BULLS | Bulls Power |
| IND_BWMFI | Market Facilitation Index |
| IND_CCI | Commodity Channel Index |
| IND_CHAIKIN | Chaikin Oscillator |
| IND_CUSTOM | Custom indicator |
| IND_DEMA | Double Exponential Moving Average |
| IND_DEMARKER | DeMarker |
| IND_ENVELOPES | Envelopes |
| IND_FORCE | Force Index |
| IND_FRACTALS | Fractals |
| IND_FRAMA | Fractal Adaptive Moving Average |
| IND_GATOR | Gator Oscillator |
| IND_ICHIMOKU | Ichimoku Kinko Hyo |
| IND_MA | Moving Average |
| IND_MACD | MACD |
| IND_MFI | Money Flow Index |
| IND_MOMENTUM | Momentum |
| IND_OBV | On Balance Volume |
| IND_OSMA | OsMA |
| IND_RSI | Relative Strength Index |
| IND_RVI | Relative Vigor Index |
| IND_SAR | Parabolic SAR |
| IND_STDDEV | Standard Deviation |
| IND_STOCHASTIC | Stochastic Oscillator |
| IND_TEMA | Triple Exponential Moving Average |
| IND_TRIX | Triple Exponential Moving Averages Oscillator |
| IND_VIDYA | Variable Index Dynamic Average |
| IND_VOLUMES | Volumes |
| IND_WPR | Williams' Percent Range |
