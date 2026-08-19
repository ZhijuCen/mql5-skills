# InitIndicators

Initializes all indicators and time series.

```
virtual bool  InitIndicators(
   CIndicators*  indicators=NULL    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful, otherwise - false.

Note

The timeseries are initialized only if the object uses the symbol or timeframe different from the symbol or timeframe defined at initialization.
