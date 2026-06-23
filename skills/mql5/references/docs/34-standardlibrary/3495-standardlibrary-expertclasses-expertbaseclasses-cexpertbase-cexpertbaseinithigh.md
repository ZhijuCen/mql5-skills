# InitHigh

Initalizes the High timeseries.

```
bool  InitHigh(
   CIndicators*  indicators    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful, otherwise - false.

Note

The High timeseries is initialized only if the object uses the symbol/timeframe different from the symbol/timeframe defined at the first initialization (and timeseries is used further).
