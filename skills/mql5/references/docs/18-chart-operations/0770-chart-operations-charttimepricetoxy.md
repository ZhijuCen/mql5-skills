# ChartTimePriceToXY

Converts the coordinates of a chart from the time/price representation to the X and Y coordinates.

```
bool  ChartTimePriceToXY(
   long           chart_id,     // Chart ID
   int            sub_window,   // The number of the subwindow
   datetime       time,         // Time on the chart
   double         price,        // Price on the chart
   int&           x,            // The X coordinate for the time on the chart
   int&           y             // The Y coordinates for the price on the chart
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

sub_window

[in]  The number of the chart subwindow. 0 means the main chart window.

time

[in]  The time value on the chart, for which the value in pixels along the X axis will be received. The origin is in the upper left corner of the main chart window.

price

[in]   The price value on the chart, for which the value in pixels along the Y axis will be received. The origin is in the upper left corner of the main chart window.

x

[out]  The variable, into which the conversion of time to X will be received.

y

[out]  The variable, into which the conversion of price to Y will be received.

Return Value

Returns true if successful, otherwise false. To get information about [the error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
#define   BAR_NUMBER    0  // number of the bar we get the price and time from
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- copy data of a single bar by the BAR_NUMBER index
   MqlRates rates[]={};
   if(CopyRates(_Symbol, _Period, BAR_NUMBER, 1, rates)!=1)
     {
      PrintFormat("CopyRates() failed for bar %d. Error %d", BAR_NUMBER, GetLastError());
      return;
     }
       
//--- convert the obtained price and time into chart pixel coordinates
   int x=0, y=0;
   ResetLastError();
   if(!ChartTimePriceToXY(ChartID(), 0, rates[0].time, rates[0].close, x, y))
     {
      Print("ChartTimePriceToXY() failed. Error ", GetLastError());
      return;
     }
     
//--- print the obtained result in the journal
   PrintFormat("For bar[%d] with opening time %s and price %.*f, the chart coordinates are x: %d, y: %d", BAR_NUMBER, TimeToString(rates[0].time), _Digits, rates[0].close, x, y);
   
   /*
   result:
   For bar[0] with opening time 2024.08.09 15:06 and price 1.27378, the chart coordinates are x: 784, y: 240
   */
  }

```

See also

[ChartXYToTimePrice()](/en/docs/chart_operations/chartxytotimeprice)
