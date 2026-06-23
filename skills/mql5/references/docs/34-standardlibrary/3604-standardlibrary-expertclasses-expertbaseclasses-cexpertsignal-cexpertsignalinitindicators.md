# InitIndicators

Initializes all necessary indicators and timeseries.

```
virtual bool  InitIndicators(
   CIndicators*  indicators    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful completion, otherwise - false.

Note

The necessary timeseries are initialized only if the object uses the symbol or timeframe different from the one defined at initialization.
