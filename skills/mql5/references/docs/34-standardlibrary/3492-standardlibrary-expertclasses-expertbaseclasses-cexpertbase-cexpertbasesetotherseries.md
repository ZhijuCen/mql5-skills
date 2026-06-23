# SetOtherSeries

Sets pointers to external non-price series.

```
virtual bool  SetOtherSeries(
   CiSpread*       spread,        // pointer
   CiTime*         time,          // pointer
   CiTickVolume*   tick_volume,   // pointer
   CiRealVolume*   real_volume    // pointer
   )

```

Parameters

spread

[in]  Pointer to Spread timeseries.

time

[in]  Pointer to Time timeseries.

tick_volume

[in]  Pointer to TickVolume timeseries.

real_volume

[in]  Pointer to RealVolume timeseries.

Return Value

true - successful, otherwise - false.

Note

The setting of pointers to external timeseries (price series) is necessary if the object uses the symbol and timeframe (set during the first initialization) and price timeseries necessary for further work.
