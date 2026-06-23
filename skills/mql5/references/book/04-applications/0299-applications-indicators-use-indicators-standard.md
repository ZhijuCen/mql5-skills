# Overview of built-in indicators

The terminal provides a large set of popular indicators, which are also available through the API. So, you don't need to implement their algorithms in MQL5. Such indicators are created using built-in functions similar to iCustom. For example, we previously created our own versions of the WPR and EMA Triple Moving Average for educational purposes. However, the corresponding indicators can be used right out of the box via the iWPR and iTEMA functions. All the available indicators are listed in the table below.

All built-in indicators take a string with a working symbol and a timeframe as the first two parameters, and also return an integer which is the indicator descriptor. In general, the prototype of all functions looks like this:

int iFunction(const string symbol, ENUM_TIMEFRAMES timeframe, ...)

Instead of an ellipsis, specific parameters of a particular indicator follow. Their number and types differ. Some indicators do not have parameters.

For example, WPR has one parameter, as in our homemade version — a period: int iWPR(const string symbol, ENUM_TIMEFRAMES timeframe, int period). And the built-in fractal indicator, unlike our version, does not have special parameters: int iFractals(const string symbol, ENUM_TIMEFRAMES period). In this case, the order of fractals is hard coded and is equal to 2, that is, before the extremum (top or bottom) and after it, there must be at least two bars with less pronounced high and low prices, respectively.

It is allowed to set the value NULL instead of a symbol. NULL means the working symbol of the current chart, and the value 0 in the timeframe parameter corresponds to the current chart timeframe, since it is also the PERIOD_CURRENT value in the ENUM_TIMEFRAMES enumeration (see section [Symbols and timeframes](/en/book/applications/timeseries/timeseries_symbol_period)).

You should also keep in mind that different types of indicators have different numbers of buffers. For example, a moving average or WPR has only one buffer, while fractals have two. The number of buffers is also noted in the table in a separate column.

| Function | Name of the indicator | Options | Buffers |
| --- | --- | --- | --- |
| iAC | Accelerator Oscillator | – | 1 * |
| iAD | Accumulation / Distribution | ENUM_APPLIED_VOLUME volume | 1 * |
| iADX | Average Directional Index | int period | 3 * |
| iADXWilder | Average Directional Index by Welles Wilder | int period | 3 * |
| iAlligator | Alligator | int jawPeriod, int jawShift, int teethPeriod,int teethShift, int lipsPeriod, int lipsShift, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price | 3 |
| iAMA | Adaptive Moving Average | int period, int fast, int slow, int shift, ENUM_APPLIED_PRICE price | 1 |
| iAO | Awesome Oscillator | – | 1 * |
| iATR | Average True Range | int period | 1 * |
| iBands | Bollinger Bands | int period, int shift, double deviation, ENUM_APPLIED_PRICE price | 3 |
| iBearsPower | Bears Power | int period | 1 * |
| iBullsPower | Bulls Power | int period | 1 * |
| iBWMFI | Market Facilitation Index by Bill Williams | ENUM_APPLIED_VOLUME volume | 1 * |
| iCCI | Commodity Channel Index | int period, ENUM_APPLIED_PRICE price | 1 * |
| iChaikin | Chaikin Oscillator | int fast, int slow, ENUM_MA_METHOD method, ENUM_APPLIED_VOLUME volume | 1 * |
| iDEMA | Double Exponential Moving Average | int period, int shift, ENUM_APPLIED_PRICE price | 1 |
| iDeMarker | DeMarker | int period | 1 * |
| iEnvelopes | Envelopes | int period, int shift, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price, double deviation | 2 |
| iForce | Force Index | int period, ENUM_MA_METHOD method, ENUM_APPLIED_VOLUME volume | 1 * |
| iFractals | Fractals | – | 2 |
| iFrAMA | Fractal Adaptive Moving Average | int period, int shift, ENUM_APPLIED_PRICE price | 1 |
| iGator | Gator Oscillator | int jawPeriod, int jawShift, int teethPeriod, int teethShift, int lipsPeriod, int lipsShift, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price | 4 * |
| iIchimoku | Ichimoku Kinko Hyo | int tenkan, int kijun, int senkou | 5 |
| iMomentum | Momentum | int period, ENUM_APPLIED_PRICE price | 1 * |
| iMFI | Money Flow Index | int period, ENUM_APPLIED_VOLUME volume | 1 * |
| iMA | Moving Average | int period, int shift, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price | 1 |
| iMACD | Moving Averages Convergence-Divergence | int fast, int slow, int signal, ENUM_APPLIED_PRICE price | 2 * |
| iOBV | On Balance Volume | ENUM_APPLIED_VOLUME volume | 1 * |
| iOsMA | Moving Average of Oscillator (MACD histogram) | int fast, int slow, int signal, ENUM_APPLIED_PRICE price | 1 * |
| iRSI | Relative Strength Index | int period, ENUM_APPLIED_PRICE price | 1 * |
| iRVI | Relative Vigor Index | int period | 1 * |
| iSAR | Parabolic Stop And Reverse System | double step, double maximum | 1 |
| iStdDev | Standard Deviation | int period, int shift, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price | 1 * |
| iStochastic | Stochastic Oscillator | int Kperiod, int Dperiod, int slowing, ENUM_MA_METHOD method, ENUM_APPLIED_PRICE price | 2 * |
| iTEMA | Triple Exponential Moving Average | int period, int shift, ENUM_APPLIED_PRICE price | 1 |
| iTriX | Triple Exponential Moving Averages Oscillator | int period, ENUM_APPLIED_PRICE price | 1 * |
| iVIDyA | Variable Index Dynamic Average | int momentum, int smooth, int shift, ENUM_APPLIED_PRICE price | 1 |
| iVolumes | Volumes | ENUM_APPLIED_VOLUME volume | 1 * |
| iWPR | Williams Percent Range | int period | 1 * |

In the right column indicators with their own window are indicated with an asterisk * (they are displayed under the main chart).

The most commonly used parameters are those that define indicator periods (period, fast, slow and other variations), as well as line shift: when it is positive, the plots are shifted to the right, when it is negative they are shifted to the left by a given number of bars.

Many parameters have application enumeration types: ENUM_APPLIED_PRICE, ENUM_APPLIED_VOLUME, ENUM_MA_METHOD. We already got acquainted with ENUM_APPLIED_PRICE in the section [Enumerations](/en/book/common/conversions/conversions_enums). All available types are presented below in tables with descriptions.

| Identifier | Description | Value |
| --- | --- | --- |
| PRICE_CLOSE | Bar closing price | 1 |
| PRICE_OPEN | Bar opening price | 2 |
| PRICE_HIGH | Bar high price | 3 |
| PRICE_LOW | Bar low price | 4 |
| PRICE_MEDIAN | Median price, (high+low)/2 | 5 |
| PRICE_TYPICAL | Typical price, (high+low+close)/3 | 6 |
| PRICE_WEIGHTED | Weighted average price, (high+low+close+close)/4 | 7 |

Indicators that work with volumes can operate with tick volumes (in fact, this is a tick counter) or real volumes (they are usually available only for exchange instruments). Both types are summarized in the ENUM_APPLIED_VOLUME enum.

| Identifier | Description | Value |
| --- | --- | --- |
| VOLUME_TICK | Tick volume | 0 |
| VOLUME_REAL | Trading volume | 1 |

Many technical indicators smooth (or average) timeseries. The terminal supports the four most common smoothing methods, which are specified in MQL5 using the elements of the ENUM_MA_METHOD enumeration.

| Identifier | Description | Value |
| --- | --- | --- |
| MODE_SMA | Simple averaging | 0 |
| MODE_EMA | Exponential averaging | 1 |
| MODE_SMMA | Smoothed averaging | 2 |
| MODE_LWMA | Linearly weighted averaging | 3 |

For the Stochastic indicator, an example of which we will consider in the next section, there are two calculation options: by Close prices or by High/Low prices. These values are provided in the special enumeration ENUM_STO_PRICE.

| Identifier | Description | Value |
| --- | --- | --- |
| STO_LOWHIGH | Calculation by Low/High prices | 0 |
| STO_CLOSECLOSE | Calculation by Close/Close prices | 1 |

The purpose and numbering of buffers for those indicators that have more than one buffer is shown in the following table.

| Indicators | Constants | Descriptions | Value |
| --- | --- | --- | --- |
| ADX, ADXW |  |  |  |
|  | MAIN_LINE | Main line | 0 |
|  | PLUSDI_LINE | Line +DI | 1 |
|  | MINUSDI_LINE | Line -DI | 2 |
| iAlligator |  |  |  |
|  | GATORJAW_LINE | Jaw line | 0 |
|  | GATORTEETH_LINE | Teeth line | 1 |
|  | GATORLIPS_LINE | Lip line | 2 |
| iBands |  |  |  |
|  | BASE_LINE | Main line | 0 |
|  | UPPER_BAND | Upper band | 1 |
|  | LOWER_BAND | Lower band | 2 |
| iEnvelopes, iFractals |  |  |  |
|  | UPPER_LINE | Upper line | 0 |
|  | LOWER_LINE | Lower line | 1 |
| iGator |  |  |  |
|  | UPPER_HISTOGRAM | Upper histogram | 0 |
|  | LOWER_HISTOGRAM | Lower histogram | 2 |
| iIchimoku |  |  |  |
|  | TENKANSEN_LINE | Tenkan-sen line | 0 |
|  | KIJUNSEN_LINE | Kijun-sen line | 1 |
|  | SENKOUSPANA_LINE | Senkou Span A Line | 2 |
|  | SENKOUSPANB_LINE | Senkou Span B line | 3 |
|  | CHIKOUSPAN_LINE | Chikou span line | 4 |
| iMACD, iRVI, iStochastic |  |  |  |
|  | MAIN_LINE | Main line | 0 |
|  | SIGNAL_LINE | Signal line | 1 |

Formulas for calculating all indicators are given in [MetaTrader 5 documentation](https://www.metatrader5.com/en/terminal/help/charts_analysis/indicators).

Full technical information on calling indicator functions, including examples of source codes, can be found in [MQL5 documentation](https://www.mql5.com/en/docs/indicators). We will consider some examples in this book later.
