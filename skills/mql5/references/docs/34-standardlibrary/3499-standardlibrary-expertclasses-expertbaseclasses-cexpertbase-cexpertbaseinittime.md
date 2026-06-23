# InitTime

Initalizes the Time timeseries.

```
bool  InitTime(
   CIndicators*  indicators    // pointer
   )

```

Parameters

indicators

[in]  Pointer to collection of indicators and timeseries.

Return Value

true - successful, otherwise - false.

Note

The Time timeseries is initialized only if Expert Advisor uses the symbol/timeframe different from the symbol/timeframe defined at the first initialization (and timeseries is used further).
