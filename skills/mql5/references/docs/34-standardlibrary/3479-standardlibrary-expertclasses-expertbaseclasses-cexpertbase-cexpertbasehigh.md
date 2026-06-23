# High

Gets the element of the High timeseries by index.

```
double  High(
   int    ind         // index
   )

```

Parameters

ind

[in]  Element index.

Return Value

If successful, it returns the numerical value of the High timeseries element with specified index, otherwise it returns EMPTY_VALUE.

Note

The EMPTY_VALUE is returned in two cases:

1. Timeseries is not used (the corresponding bit is not set).
2. Element index is out of range.
