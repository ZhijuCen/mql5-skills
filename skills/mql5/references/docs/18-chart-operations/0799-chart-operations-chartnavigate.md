# ChartNavigate

Performs shift of the specified chart by the specified number of bars relative to the specified position in the chart.

```
bool  ChartNavigate(
   long                  chart_id,     // Chart ID
   ENUM_CHART_POSITION   position,     // Position
   int                   shift=0       // Shift value
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

position

[in]  Chart position to perform a shift. Can be one of the [ENUM_CHART_POSITION](/en/docs/constants/chartconstants/enum_chart_position) values.

shift=0

[in]  Number of bars to shift the chart. Positive value means the right shift (to the end of chart), negative value means the left shift (to the beginning of chart). The zero shift can be used to navigate to the beginning or end of chart.

Return Value

Returns true if successful, otherwise returns false.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get handle of the current chart
   long handle=ChartID();
   string comm="";
   if(handle>0) // if successful, additionally set up the chart
     {
      //--- disable auto scroll
      ChartSetInteger(handle,CHART_AUTOSCROLL,false);
      //--- set a shift from the right chart border
      ChartSetInteger(handle,CHART_SHIFT,true);
      //--- draw candlesticks
      ChartSetInteger(handle,CHART_MODE,CHART_CANDLES);
      //--- set the display mode for tick volumes
      ChartSetInteger(handle,CHART_SHOW_VOLUMES,CHART_VOLUME_TICK);
 
      //--- prepare a text to output in Comment()
      comm="Scroll 10 bars to the right of the history start";
      //--- show comment
      Comment(comm);
      //--- scroll 10 bars to the right of the history start
      ChartNavigate(handle,CHART_BEGIN,10);
      //--- get the number of the first bar visible on the chart (numeration like in timeseries)
      long first_bar=ChartGetInteger(0,CHART_FIRST_VISIBLE_BAR,0);
      //--- add line feed character
      comm=comm+"\r\n";
      //--- add to comment
      comm=comm+"The first bar on the chart is number "+IntegerToString(first_bar)+"\r\n";
      //--- show comment
      Comment(comm);
      //--- wait 5 seconds to see how the chart moves
      Sleep(5000);
 
      //--- add to the comment text
      comm=comm+"\r\n"+"Scroll 10 bars to the left of the right chart border";
      Comment(comm);
      //--- scroll 10 bars to the left of the right chart border
      ChartNavigate(handle,CHART_END,-10);
      //--- get the number of the first bar visible on the chart (numeration like in timeseries)
      first_bar=ChartGetInteger(0,CHART_FIRST_VISIBLE_BAR,0);
      comm=comm+"\r\n";
      comm=comm+"The first bar on the chart is number "+IntegerToString(first_bar)+"\r\n";
      Comment(comm);
      //--- wait 5 seconds to see how the chart moves
      Sleep(5000);
 
      //--- new block of chart scrolling
      comm=comm+"\r\n"+"Scroll 300 bars to the right of the history start";
      Comment(comm);
      //--- scroll 300 bars to the right of the history start
      ChartNavigate(handle,CHART_BEGIN,300);
      first_bar=ChartGetInteger(0,CHART_FIRST_VISIBLE_BAR,0);
      comm=comm+"\r\n";
      comm=comm+"The first bar on the chart is number "+IntegerToString(first_bar)+"\r\n";
      Comment(comm);
      //--- wait 5 seconds to see how the chart moves
      Sleep(5000);
 
      //--- new block of chart scrolling
      comm=comm+"\r\n"+"Scroll 300 bars to the left of the right chart border";
      Comment(comm);
      //--- scroll 300 bars to the left of the right chart border
      ChartNavigate(handle,CHART_END,-300);
      first_bar=ChartGetInteger(0,CHART_FIRST_VISIBLE_BAR,0);
      comm=comm+"\r\n";
      comm=comm+"The first bar on the chart is number "+IntegerToString(first_bar)+"\r\n";
      Comment(comm);
     }
  }

```
