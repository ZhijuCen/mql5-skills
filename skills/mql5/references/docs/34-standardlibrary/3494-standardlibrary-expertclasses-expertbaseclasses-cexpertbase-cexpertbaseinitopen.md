# InitOpen

Initalizes the Open timeseries.

```
bool  InitOpen(
   CIndicators*  indicators    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful, otherwise - false.

Note

The Open timeseries is initialized only if the object uses the symbol/timeframe different from the symbol/timeframe defined at the first initialization (and timeseries is used further).
