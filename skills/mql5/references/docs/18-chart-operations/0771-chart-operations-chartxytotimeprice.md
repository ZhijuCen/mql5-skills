# ChartXYToTimePrice

Converts the X and Y coordinates on a chart to the time and price values.

```
bool  ChartXYToTimePrice(
   long           chart_id,     // Chart ID
   int            x,            // The X coordinate on the chart
   int            y,            // The Y coordinate on the chart
   int&           sub_window,   // The number of the subwindow
   datetime&      time,         // Time on the chart
   double&        price         // Price on the chart
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

x

[in]  The X coordinate.

y

[in]  The Y coordinate.

sub_window

[out]  The variable, into which the chart subwindow number will be written. 0 means the main chart window.

time

[out]  The time value on the chart, for which the value in pixels along the X axis will be received. The origin is in the upper left corner of the main chart window.

price

[out]  The price value on the chart, for which the value in pixels along the Y axis will be received. The origin is in the upper left corner of the main chart window.

Return Value

Returns true if successful, otherwise false. To get information about [the error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//--- Show the event parameters on the chart
   Comment(__FUNCTION__,": id=",id," lparam=",lparam," dparam=",dparam," sparam=",sparam);
//--- If this is an event of a mouse click on the chart
   if(id==CHARTEVENT_CLICK)
     {
      //--- Prepare variables
      int      x     =(int)lparam;
      int      y     =(int)dparam;
      datetime dt    =0;
      double   price =0;
      int      window=0;
      //--- Convert the X and Y coordinates in terms of date/time
      if(ChartXYToTimePrice(0,x,y,window,dt,price))
        {
         PrintFormat("Window=%d X=%d  Y=%d  =>  Time=%s  Price=%G",window,x,y,TimeToString(dt),price);
         //--- Perform reverse conversion: (X,Y) => (Time,Price)
         if(ChartTimePriceToXY(0,window,dt,price,x,y))
            PrintFormat("Time=%s  Price=%G  =>  X=%d  Y=%d",TimeToString(dt),price,x,y);
         else
            Print("ChartTimePriceToXY return error code: ",GetLastError());
         //--- delete lines
         ObjectDelete(0,"V Line");
         ObjectDelete(0,"H Line");
         //--- create horizontal and vertical lines of the crosshair
         ObjectCreate(0,"H Line",OBJ_HLINE,window,dt,price);
         ObjectCreate(0,"V Line",OBJ_VLINE,window,dt,price);
         ChartRedraw(0);
        }
      else
         Print("ChartXYToTimePrice return error code: ",GetLastError());
      Print("+--------------------------------------------------------------+");
     }
  }

```

See also

[ChartTimePriceToXY()](/en/docs/chart_operations/charttimepricetoxy)
