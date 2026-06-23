# SetPriceSeries

Sets pointers to external price series.

```
virtual bool  SetPriceSeries(
   CiOpen*    open,        // pointer
   CiHigh*    high,        // pointer
   CiLow*     low,         // pointer
   CiClose*   close        // pointer
   )

```

Parameters

open

[in]  Pointer to Open timeseries.

high

[in]  Pointer to High timeseries.

low

[in]  Pointer to Low timeseries.

close

[in]  Pointer to Close timeseries.

Return Value

true - successful, otherwise - false.

Note

The setting of pointers to external timeseries (price series) is necessary if the object uses the symbol and timeframe (set during the first initialization) and price timeseries necessary for further work.
