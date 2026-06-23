# CHistogramChart

Class for plotting histograms.

### Description

All methods for working with the plotting of histograms are implemented in this class. They can be used to set the column width and for configuring the work with data series. The methods for working with gradient filling of histogram columns are included, which allow to visualize the data more clearly.

![The code of the above figure is provided  below .](pics/ccanvas_histogramchart.png)

The code of the above figure is provided [below](/en/docs/standardlibrary/canvasgraphics/chistogramchart#sample).

### Declaration

```
   class CHistogramChart : public CChartCanvas

```

### Title

```
   #include <Canvas\Charts\HistogramChart.mqh>

```

```
Inheritance hierarchy
   CCanvas
       CChartCanvas
           CHistogramChart

```

### Class methods

| Method | Action |
| --- | --- |
| Gradient | Sets the flag indicating whether the gradient fill of the histogram columns will be applied. |
| BarGap | Set the value of the histogram offset from the origin. |
| BarMinSize | Sets the minimum width of the histogram columns. |
| BarBorder | Sets the flag indicating the need to draw the border for each column. |
| Create | Virtual method that creates a graphical resource. |
| SeriesAdd | Adds a new data series. |
| SeriesInsert | Inserts data series to the chart. |
| SeriesUpdate | Updates data series on the chart. |
| SeriesDelete | Deletes data series from the chart. |
| ValueUpdate | Updates the element value in the specified series. |
| DrawData | Virtual method that plots a histogram for the specified series. |
| DrawBar | Draws a histogram column as a filled rectangle. |
| GradientBrush | Creates a brush for the gradient fill. |

| Methods inherited from class CCanvas 
 CreateBitmap ,  CreateBitmap ,  CreateBitmapLabel ,  CreateBitmapLabel ,  Attach ,  Attach ,  Destroy ,  ChartObjectName ,  ResourceName ,  Width ,  Height ,  Update ,  Resize ,  Erase ,  PixelGet ,  PixelSet ,  LineVertical ,  LineHorizontal ,  Line ,  Polyline ,  Polygon ,  Rectangle ,  Triangle ,  Circle ,  Ellipse ,  Arc ,  Arc ,  Arc ,  Pie ,  Pie ,  FillRectangle ,  FillTriangle ,  FillPolygon ,  FillCircle ,  FillEllipse ,  Fill ,  Fill ,  PixelSetAA ,  LineAA ,  PolylineAA ,  PolygonAA ,  TriangleAA ,  CircleAA ,  EllipseAA ,  LineWu ,  PolylineWu ,  PolygonWu ,  TriangleWu ,  CircleWu ,  EllipseWu ,  LineThickVertical ,  LineThickHorizontal ,  LineThick ,  PolylineThick ,  PolygonThick ,  PolylineSmooth ,  PolygonSmooth ,  FontSet ,  FontNameSet ,  FontSizeSet ,  FontFlagsSet ,  FontAngleSet ,  FontGet ,  FontNameGet ,  FontSizeGet ,  FontFlagsGet ,  FontAngleGet ,  TextOut ,  TextWidth ,  TextHeight ,  TextSize ,  GetDefaultColor ,  TransparentLevelSet ,  LoadFromFile , LineStyleGet,  LineStyleSet |
| --- |
| Methods inherited from class CChartCanvas 
 ColorBackground ,  ColorBackground ,  ColorBorder ,  ColorBorder ,  ColorText ,  ColorText ,  ColorGrid ,  ColorGrid ,  MaxData ,  MaxData ,  MaxDescrLen ,  MaxDescrLen ,  AllowedShowFlags ,  ShowFlags ,  ShowFlags ,  IsShowLegend ,  IsShowScaleLeft ,  IsShowScaleRight ,  IsShowScaleTop ,  IsShowScaleBottom ,  IsShowGrid ,  IsShowDescriptors ,  IsShowPercent ,  ShowLegend ,  ShowScaleLeft ,  ShowScaleRight ,  ShowScaleTop ,  ShowScaleBottom ,  ShowGrid ,  ShowDescriptors ,  ShowValue ,  ShowPercent ,  LegendAlignment ,  Accumulative ,  VScaleMin ,  VScaleMin ,  VScaleMax ,  VScaleMax ,  NumGrid ,  NumGrid ,  VScaleParams ,  DataOffset ,  DataOffset ,  DataTotal ,  DescriptorUpdate ,  ColorUpdate |

Example

```
//+------------------------------------------------------------------+
//|                                         HistogramChartSample.mq5 |
//|                   Copyright 2009-2017, MetaQuotes Software Corp. |
//|                                              http://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright   "2009-2017, MetaQuotes Software Corp."
#property link        "http://www.mql5.com"
#property description "Example of using histogram"
//---
#include <Canvas\Charts\HistogramChart.mqh>
//+------------------------------------------------------------------+
//| inputs                                                           |
//+------------------------------------------------------------------+
input bool Accumulative=true;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
int OnStart(void)
  {
   int k=100;
   double arr[10];
//--- create chart
   CHistogramChart chart;
   if(!chart.CreateBitmapLabel("SampleHistogramChart",10,10,600,450))
     {
      Print("Error creating histogram chart: ",GetLastError());
      return(-1);
     }
   if(Accumulative)
     {
      chart.Accumulative();
      chart.VScaleParams(20*k*10,-10*k*10,20);
     }
   else
      chart.VScaleParams(20*k,-10*k,20);
   chart.ShowValue(true);
   chart.ShowScaleTop(false);
   chart.ShowScaleBottom(false);
   chart.ShowScaleRight(false);
   chart.ShowLegend();
   for(int j=0;j<5;j++)
     {
      for(int i=0;i<10;i++)
        {
         k=-k;
         if(k>0)
            arr[i]=k*(i+10-j);
         else
            arr[i]=k*(i+10-j)/2;
        }
      chart.SeriesAdd(arr,"Item"+IntegerToString(j));
     }
//--- play with values
   while(!IsStopped())
     {
      int i=rand()%5;
      int j=rand()%10;
      k=rand()%3000-1000;
      chart.ValueUpdate(i,j,k);
      Sleep(200);
     }
//--- finish
   chart.Destroy();
   return(0);
  }

```
