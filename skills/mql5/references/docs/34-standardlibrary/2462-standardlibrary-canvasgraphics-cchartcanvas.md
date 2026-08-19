# CChartCanvas

Base class for implementing classes, which are used for drawing charts and their elements.

### Description

This class includes methods for working with the basic elements of any chart: coordinate axes and their marks, chart legend, grid, background, etc. Here you can customize the options for displaying elements: visibility, text color, etc.

### Declaration

```
   class CChartCanvas : public CCanvas

```

### Title

```
   #include <Canvas\Charts\ChartCanvas.mqh>

```

```
Inheritance hierarchy
   CCanvas
       CChartCanvas
Direct descendants
CHistogramChart, CLineChart, CPieChart

```

### Class methods

| Method | Action |
| --- | --- |
| ColorBackground | Returns and sets the background color. |
| ColorBorder | Returns and sets the border color. |
| ColorText | Returns and sets the text color. |
| ColorGrid | Returns and sets the grid color. |
| MaxData | Returns and sets the maximum amount of data (series) allowed. |
| MaxDescrLen | Returns and sets the maximum length of the descriptors. |
| ShowFlags | Returns and sets the visibility flag of the chart elements. |
| IsShowLegend | Returns and sets the visibility flag of the legend on the chart. |
| IsShowScaleLeft | Returns the visibility flag of the scale of values on the left. |
| IsShowScaleRight | Returns the visibility flag of the scale of values on the right. |
| IsShowScaleTop | Returns the visibility flag of the scale of values at the top. |
| IsShowScaleBottom | Returns the visibility flag of the scale of values at the bottom. |
| IsShowGrid | Returns the visibility flag of the grid on the chart. |
| IsShowDescriptors | Returns the visibility flag of the descriptors on the chart. |
| IsShowPercent | Returns the visibility flag of the percentages on the chart. |
| VScaleMin | Returns and sets the minimum on the vertical scale of values. |
| VScaleMax | Returns and sets the maximum on the vertical scale of values. |
| NumGrid | Returns and sets the number of vertical scale divisions when plotting the chart grid. |
| DataOffset | Returns and sets the data offset value. |
| DataTotal | Returns the total number of data series on the chart. |
| DrawDescriptors | Virtual method for drawing descriptors. |
| DrawData | Virtual method for drawing data series at the specified index. |
| Create | Virtual method that creates a graphical resource. |
| AllowedShowFlags | Sets the set of allowed visibility flags for chart elements. |
| ShowLegend | Sets the visibility flag for the legend. |
| ShowScaleLeft | Sets the visibility flag for the left scale. |
| ShowScaleRight | Sets the visibility flag for the right scale. |
| ShowScaleTop | Sets the visibility flag for the top scale. |
| ShowScaleBottom | Sets the visibility flag for the bottom scale. |
| ShowGrid | Sets the visibility flag for the grid. |
| ShowDescriptors | Sets the visibility flag for the descriptors. |
| ShowValue | Sets the visibility flag for the values. |
| ShowPercent | Sets the visibility flag for the percentages. |
| LegendAlignment | Sets the text alignment for the legend. |
| Accumulative | Sets the value accumulation flag for the series. |
| VScaleParams | Sets the parameters for the vertical scale of values. |
| DescriptorUpdate | Updates the value of the series descriptor (at the specified position). |
| ColorUpdate | Updates the series colors (at the specified position). |
| ValuesCheck | Performs internal calculations for plotting the chart. |
| Redraw | Redraw the chart. |
| DrawBackground | Draws the background. |
| DrawLegend | Redraws the legend. |
| DrawLegendVertical | Draws a vertical legend. |
| DrawLegendHorizontal | Draws a horizontal legend. |
| CalcScales | Calculates the coordinates of the scale. |
| DrawScales | Redraws all scales of values. |
| DrawScaleLeft | Redraws the left scale of values. |
| DrawScaleRight | Redraws the right scale of values. |
| DrawScaleTop | Redraws the top scale of values |
| DrawScaleBottom | Redraws the bottom value scale. |
| DrawGrid | Redraw the chart. |
| DrawChart | Redraw the chart. |

```
Methods inherited from class CCanvas
CreateBitmap, CreateBitmap, CreateBitmapLabel, CreateBitmapLabel, Attach, Attach, Destroy, ChartObjectName, ResourceName, Width, Height, Update, Resize, Erase, PixelGet, PixelSet, LineVertical, LineHorizontal, Line, Polyline, Polygon, Rectangle, Triangle, Circle, Ellipse, Arc, Arc, Arc, Pie, Pie, FillRectangle, FillTriangle, FillPolygon, FillCircle, FillEllipse, Fill, Fill, PixelSetAA, LineAA, PolylineAA, PolygonAA, TriangleAA, CircleAA, EllipseAA, LineWu, PolylineWu, PolygonWu, TriangleWu, CircleWu, EllipseWu, LineThickVertical, LineThickHorizontal, LineThick, PolylineThick, PolygonThick, PolylineSmooth, PolygonSmooth, FontSet, FontNameSet, FontSizeSet, FontFlagsSet, FontAngleSet, FontGet, FontNameGet, FontSizeGet, FontFlagsGet, FontAngleGet, TextOut, TextWidth, TextHeight, TextSize, GetDefaultColor, TransparentLevelSet, LoadFromFile, LineStyleGet, LineStyleSet

```
