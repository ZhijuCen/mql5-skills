# Technical Indicator Functions

All functions like iMA, iAC, iMACD, iIchimoku etc. create a copy of the corresponding technical indicator in the global cache of the client terminal. If a copy of the indicator with such parameters already exists, the new copy is not created, and the counter of references to the existing copy increases.

These functions return the handle of the appropriate copy of the indicator. Further, using this handle, you can receive data calculated by the corresponding indicator. The corresponding buffer data (technical indicators contain calculated data in their internal buffers, which can vary from 1 to 5, depending on the indicator) can be copied to a mql5-program using the [CopyBuffer()](/en/docs/series/copybuffer) function.

You can't refer to the indicator data right after it has been created, because calculation of indicator values requires some time, so it's better to create indicator handles in OnInit(). Function [iCustom()](/en/docs/indicators/icustom) creates the corresponding custom indicator, and returns its handle in case it is successfully create. Custom indicators can contain up to 512 indicator buffers, the contents of which can also be obtained by the [CopyBuffer()](/en/docs/series/copybuffer) function, using the obtained handle.

There is a universal method for creating any technical indicator using the [IndicatorCreate()](/en/docs/series/indicatorcreate) function. This function accepts the following data as input parameters:

- symbol name;
- timeframe;
- type of the indicator to create;
- number of input parameters of the indicator;
- an array of [MqlParam](/en/docs/constants/structures/mqlparam) type containing all the necessary input parameters.

The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Note. Repeated call of the indicator function with the same parameters within one mql5-program does not lead to a multiple increase of the reference counter; the counter will be increased only once by 1. However, it's recommended to get the indicators handles in function [OnInit()](/en/docs/event_handlers/oninit) or in the class constructor, and further use these handles in other functions. The reference counter decreases when a mql5-program is deinitialized.

All indicator functions have at least 2 parameters - symbol and period. The [NULL](/en/docs/basis/types/void) value of the symbol means the current symbol, the 0 value of the period means the current [timeframe](/en/docs/constants/chartconstants/enum_timeframes).

| Function | Returns the handle of the indicator: |
| --- | --- |
| iAC | Accelerator Oscillator |
| iAD | Accumulation/Distribution |
| iADX | Average Directional Index |
| iADXWilder | Average Directional Index by Welles Wilder |
| iAlligator | Alligator |
| iAMA | Adaptive Moving Average |
| iAO | Awesome Oscillator |
| iATR | Average True Range |
| iBearsPower | Bears Power |
| iBands | Bollinger Bands® |
| iBullsPower | Bulls Power |
| iCCI | Commodity Channel Index |
| iChaikin | Chaikin Oscillator |
| iCustom | Custom indicator |
| iDEMA | Double Exponential Moving Average |
| iDeMarker | DeMarker |
| iEnvelopes | Envelopes |
| iForce | Force Index |
| iFractals | Fractals |
| iFrAMA | Fractal Adaptive Moving Average |
| iGator | Gator Oscillator |
| iIchimoku | Ichimoku Kinko Hyo |
| iBWMFI | Market Facilitation Index by Bill Williams |
| iMomentum | Momentum |
| iMFI | Money Flow Index |
| iMA | Moving Average |
| iOsMA | Moving Average of Oscillator (MACD histogram) |
| iMACD | Moving Averages Convergence-Divergence |
| iOBV | On Balance Volume |
| iSAR | Parabolic Stop And Reverse System |
| iRSI | Relative Strength Index |
| iRVI | Relative Vigor Index |
| iStdDev | Standard Deviation |
| iStochastic | Stochastic Oscillator |
| iTEMA | Triple Exponential Moving Average |
| iTriX | Triple Exponential Moving Averages Oscillator |
| iWPR | Williams' Percent Range |
| iVIDyA | Variable Index Dynamic Average |
| iVolumes | Volumes |
