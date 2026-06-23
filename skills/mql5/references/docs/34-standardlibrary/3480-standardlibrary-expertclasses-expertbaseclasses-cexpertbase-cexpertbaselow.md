# Low

Gets the element of the Low timeseries by index.

```
double  Low(
   int    ind         // index
   )

```

Parameters

ind

[in]  Element index.

Return Value

If successful, it returns the numerical value of the Low timeseries element with specified index, otherwise it returns EMPTY_VALUE.

Note

The EMPTY_VALUE is returned in two cases:

1. Timeseries is not used (the corresponding bit is not set).
2. Element index is out of range.
