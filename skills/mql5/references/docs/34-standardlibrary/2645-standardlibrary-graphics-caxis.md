# CAxis

CAxis is an auxiliary graphics library class for working with the coordinate axes.

### Description

The CAxis class receives and stores various parameters of the coordinate axes. The class implements the ability to auto scale the coordinate axes dynamically.

### Declaration

```
   class CAxis

```

### Title

```
   #include <Graphics\Axis.mqh>

```

### Class methods

| Method | Description |
| --- | --- |
| AutoScale | Get/set the auto-scaling flag |
| Min | Get/set the minimum axis value |
| Max | Get/set the maximum axis value |
| Step | Get the step value by axis |
| Name | Get/set the axis name |
| Color | Get/set the axis color |
| ValuesSize | Get/set the size of the axis numbers |
| ValuesWidth | Get/set the maximum displayed length of the axis numbers |
| ValuesFormat | Get/set the format of the axis numbers |
| ValuesDateTimeMode | Get the format of converting a date into a string. |
| ValuesFunctionFormat | Get the pointer to the function defining the format of displaying values on the axis. |
| ValuesFunctionFormatCBData | Get the pointer to the object that may contain additional data on converting axis values. |
| NameSize | Get/set the font size of the axis name |
| ZeroLever | Get/set the "zero lever" value |
| DefaultStep | Get/set the initial step value by axis |
| MaxLabels | Get/set the maximum amount of numbers on the axis |
| MinGrace | Get/set the "tolerance" value for the axis minimum |
| MaxGrace | Get/set the "tolerance" value for the axis maximum |
| SelectAxisScale | Auto scale the axis. |
