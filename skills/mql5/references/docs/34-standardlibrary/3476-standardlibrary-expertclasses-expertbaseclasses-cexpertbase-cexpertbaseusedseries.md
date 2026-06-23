# UsedSeries

Gets the bitmask of timeseries used.

```
int  UsedSeries()

```

Return Value

The list of used timeseries as bitmask.

Note

If the bit is set, the corresponding timeseries is used, if it is not set, the timeseries is not used.

The bit-timeseries correspondence:

bit 0 - Open timeseries,  

bit 1 - High timeseries,  

bit 2 - Low timeseries,  

bit 3 - Close timeseries,  

bit 4 - Spread timeseries,  

bit 5 - Time timeseries,  

bit 6 - TickVolume timeseries,  

bit 7 - RealVolume timeseries.
