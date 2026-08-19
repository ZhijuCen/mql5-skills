# CCurve

The CCurve class works with the properties of the curves generated on the chart.

### Description

The CCurve class sets, installs and receives the coordinates and various properties of the curves when working with the CGraphic class.

There are three curve plotting modes: dots, lines and histogram. Separate parameters are implemented for each plotting mode in the class.

### Declaration

```
   class CCurve : public CObject

```

### Title

```
   #include <Graphics\Curve.mqh>

```

```
Inheritance hierarchy
   CObject
       CCurve

```

### Class methods

| Method | Description |
| --- | --- |
| Type | Get the curve type |
| Name | Get the curve name |
| Color | Get the curve color |
| XMax | Get the maximum value of the X function |
| XMin | Get the minimum value of the X function |
| YMax | Get the maximum value of the Y function |
| YMin | Get the minimum value of the Y function |
| Size | Get the number of dots defining a curve |
| PointsSize | Get/set the linear size of dots defining a curve |
| PointsFill | Get/set the flag for filling dots defining a curve |
| PointsColor | Get/set the dot filling color |
| GetX | Gets X values of all curve dots to the array |
| GetY | Gets Y values of all curve dots to the array |
| LinesStyle | Get/set a line style when plotting a curve using lines |
| LinesIsSmooth | Get/set the smoothing flag when drawing using lines |
| LinesSmoothTension | Get/set the curve smoothing parameter when drawing using lines |
| LinesSmoothStep | Get/set the length of the approximating lines for smoothing when plotting by lines |
| LinesWidth | Get/set a line width when plotting a curve using lines |
| HistogramWidth | Get/set the width of columns when plotting using a histogram |
| CustomPlotCBData | Get/set the pointer to the object to be used in the custom curve plotting mode. |
| CustomPlotFunction | Get/set the pointer to the function implementing the custom curve plotting mode. |
| PointsType | Get/set the flag pointing at the type of dots used when plotting a dotted curve. |
| StepsDimension | Get/set the value indicating the dimension used in step-type curve rendering. |
| TrendLineCoefficients | Get/set trend line ratios for writing them into an array. |
| TrendLineColor | Get/set a color of a trend line for a curve. |
| TrendLineVisible | Get/set the trend line visibility flag. |
| Update | Update the curve coordinates. |
| Visible | Get/set the flag defining if a function is visible on the chart. |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Compare

```
