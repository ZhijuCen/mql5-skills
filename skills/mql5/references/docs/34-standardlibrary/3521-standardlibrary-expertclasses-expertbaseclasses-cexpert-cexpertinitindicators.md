# InitIndicators

Initializes necessary indicators and timeseries.

```
virtual bool  InitIndicators(
   CIndicators*  indicators=NULL    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful completion, otherwise - false.

Note

The timeseries are initialized if the object uses a symbol or timeframe other than the one defined in the initialization.

Indicators and timeseries of all auxiliary EA objects are initialized.
