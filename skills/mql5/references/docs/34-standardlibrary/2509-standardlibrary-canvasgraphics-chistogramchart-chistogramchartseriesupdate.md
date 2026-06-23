# SeriesUpdate

Updates data series on the chart.

```
 bool  SeriesUpdate(
   const uint    pos,       // index
   const double  &value[],  // values
   const string  descr,     // label
   const uint    clr,       // color
   )

```

Parameters

pos

[in] Index of the series — the serial number of its addition, starting with 0.

&value[]

[in] New values for the data series.

descr

[in] Series label.

clr

[in] Series display color.

Return Value

true if successful, otherwise false.
