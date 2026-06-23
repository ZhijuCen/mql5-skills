# ObjectCreate

The function creates an object with the specified name, type, and the initial coordinates in the specified chart subwindow. During creation up to 30 coordinates can be specified.

```
bool  ObjectCreate(
   long         chart_id,      // chart identifier
   string       name,          // object name
   ENUM_OBJECT  type,          // object type
   sub_window   nwin,          // window index
   datetime     time1,         // time of the first anchor point
   double       price1,        // price of the first anchor point
   ...
   datetime     timeN=0,       // time of the N-th anchor point
   double       priceN=0,      // price of the N-th anchor point
   ...
   datetime     time30=0,      // time of the 30th anchor point
   double       price30=0      // price of the 30th anchor point
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of the object. The name must be unique within a chart, including its subwindows.

type

[in]  Object type. The value can be one of the values of the [ENUM_OBJECT](/en/docs/constants/objectconstants/enum_object) enumeration.

sub_window

[in]  Number of the chart subwindow. 0 means the main chart window. The specified subwindow must exist, otherwise the function returns false.

time1

[in]  The time coordinate of the first anchor.

price1

[in]  The price coordinate of the first anchor point.

timeN=0

[in]  The time coordinate of the N-th anchor point.

priceN=0

[in]  The price coordinate of the N-th anchor point.

time30=0

[in]  The time coordinate of the thirtieth anchor point.

price30=0

[in]  The price coordinate of the thirtieth anchor point.

Return Value

The function returns true if the command has been successfully added to the queue of the specified chart, or false otherwise. If an object has already been created, an attempt is made to change its coordinates.

Note

An asynchronous call is always used for ObjectCreate(), that is why the function only returns the results of adding the command to a chart queue. In this case, true only means that the command has been successfully enqueued, but the result of its execution is unknown.

To check the command execution result, you can use the [ObjectFind()](/en/docs/objects/objectfind) function or any other function that requests object properties, such as ObjectGetXXX. However, you should keep in mind that such functions are added to the end of the queue of that chart, and they wait for the execution result (due to the synchronous call), and can therefore be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

An object name should not exceed 63 characters.

The numbering of the chart subwindows (if there are subwindows with indicators in the chart) starts with 1. The main chart window of the chart is and always has index 0.

The large number of anchor points (up to 30) is implemented for future use. At the same time, the limit of 30 possible anchor points for graphical objects is determined by the limit on the number of parameters (not more than 64) that can be used when calling a function.

When an object is renamed, two events are formed simultaneously. These events can be handled in an Expert Advisor or indicator by the [OnChartEvent()](/en/docs/event_handlers/onchartevent) function:

- an event of deletion of an object with the old name;
- an event of creation of an object with a new name.

There is a certain number of anchor points that must be specified when creating each [object type](/en/docs/constants/objectconstants/enum_object):

| ID | Description | Anchor Points |
| --- | --- | --- |
| OBJ_VLINE | Vertical Line | One anchor point. Actually only the time coordinate is used. |
| OBJ_HLINE | Horizontal Line | One anchor point. Actually only the price coordinate is used. |
| OBJ_TREND | Trend Line | Two anchor points. |
| OBJ_TRENDBYANGLE | Trend Line By Angle | Two anchor points. |
| OBJ_CYCLES | Cycle Lines | Two anchor points. |
| OBJ_ARROWED_LINE | Arrowed Line | Two anchor points. |
| OBJ_CHANNEL | Equidistant Channel | Three anchor points. |
| OBJ_STDDEVCHANNEL | Standard Deviation Channel | Two anchor points. |
| OBJ_REGRESSION | Linear Regression Channel | Two anchor points. |
| OBJ_PITCHFORK | Andrews’ Pitchfork | Three anchor points. |
| OBJ_GANNLINE | Gann Line | Two anchor points. |
| OBJ_GANNFAN | Gann Fan | Two anchor points. |
| OBJ_GANNGRID | Gann Grid | Two anchor points. |
| OBJ_FIBO | Fibonacci Retracement | Two anchor points. |
| OBJ_FIBOTIMES | Fibonacci Time Zones | Two anchor points. |
| OBJ_FIBOFAN | Fibonacci Fan | Two anchor points. |
| OBJ_FIBOARC | Fibonacci Arcs | Two anchor points. |
| OBJ_FIBOCHANNEL | Fibonacci Channel | Three anchor points. |
| OBJ_EXPANSION | Fibonacci Expansion | Three anchor points. |
| OBJ_ELLIOTWAVE5 | Elliott Motive Wave | Five anchor points. |
| OBJ_ELLIOTWAVE3 | Elliott Correction Wave | Three anchor points. |
| OBJ_RECTANGLE | Rectangle | Two anchor points. |
| OBJ_TRIANGLE | Triangle | Three anchor points. |
| OBJ_ELLIPSE | Ellipse | Three anchor points. |
| OBJ_ARROW_THUMB_UP | Thumbs Up | One anchor point. |
| OBJ_ARROW_THUMB_DOWN | Thumbs Down | One anchor point. |
| OBJ_ARROW_UP | Arrow Up | One anchor point. |
| OBJ_ARROW_DOWN | Arrow Down | One anchor point. |
| OBJ_ARROW_STOP | Stop Sign | One anchor point. |
| OBJ_ARROW_CHECK | Check Sign | One anchor point. |
| OBJ_ARROW_LEFT_PRICE | Left Price Label | One anchor point. |
| OBJ_ARROW_RIGHT_PRICE | Right Price Label | One anchor point. |
| OBJ_ARROW_BUY | Buy Sign | One anchor point. |
| OBJ_ARROW_SELL | Sell Sign | One anchor point. |
| OBJ_ARROW | Arrow | One anchor point. |
| OBJ_TEXT | Text | One anchor point. |
| OBJ_LABEL | Label | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |
| OBJ_BUTTON | Button | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |
| OBJ_CHART | Chart | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |
| OBJ_BITMAP | Bitmap | One anchor point. |
| OBJ_BITMAP_LABEL | Bitmap Label | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |
| OBJ_EDIT | Edit | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |
| OBJ_EVENT | The "Event" object corresponding to an event in the economic calendar | One anchor point. Actually only the time coordinate is used. |
| OBJ_RECTANGLE_LABEL | The "Rectangle label" object for creating and designing the custom graphical interface. | Position is set using the  OBJPROP_XDISTANCE  and  OBJPROP_YDISTANCE  properties. |

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#property script_show_inputs
 
#define   OBJ_NAME   "TestObjectCreate"            // object name
#define   OBJ_X      40                            // object X coordinate
#define   OBJ_Y      40                            // object Y coordinate
#define   OBJ_WIDTH  300                           // object width
#define   OBJ_HEIGHT 200                           // object height
#define   WND        0                             // chart subwindow
 
input ENUM_OBJECT InpObjectToCreate =  OBJ_VLINE;  /* Object type to create   */ // object type to plot on the chart
 
struct SPoint                                      // anchor point structure
  {
   double   price;
   datetime time;
  };
 
SPoint   ExtAnchorPoints[5];                       // array of graphical object anchor points
long     ExtChartID;                               // ID 
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- check the number of available bars
   int bars=Bars(_Symbol,_Period);
   if(bars<7)
     {
      PrintFormat("The number of available bars (%d) is not enough to create some graphical objects",bars);
      return;
     }
//--- current chart ID
   ExtChartID=ChartID();
 
//--- delete the previously created object
   ObjectDelete(ExtChartID, OBJ_NAME);
 
//--- set five anchor points (time/price)
   SetAnchorPointsData();
 
//--- price/time of anchor points
   datetime tm0=ExtAnchorPoints[0].time;
   double   pr0=ExtAnchorPoints[0].price;
   datetime tm1=ExtAnchorPoints[1].time;
   double   pr1=ExtAnchorPoints[1].price;
   datetime tm2=ExtAnchorPoints[2].time;
   double   pr2=ExtAnchorPoints[2].price;
   datetime tm3=ExtAnchorPoints[3].time;
   double   pr3=ExtAnchorPoints[3].price;
   datetime tm4=ExtAnchorPoints[4].time;
   double   pr4=ExtAnchorPoints[4].price;
   
//--- if the object successfully created, set its remaining parameters:
   if(ObjectCreate(ExtChartID,OBJ_NAME,InpObjectToCreate,WND,tm0,pr0,tm1,pr1,tm2,pr2,tm3,pr3,tm4,pr4))
     {
      //--- make the object selectable and select it
      ObjectSetInteger(ExtChartID, OBJ_NAME, OBJPROP_SELECTABLE, true);
      ObjectSetInteger(ExtChartID, OBJ_NAME, OBJPROP_SELECTED, true);
      
      //--- for objects positioned by chart coordinates
      ENUM_OBJECT obj=InpObjectToCreate;
      if(obj==OBJ_LABEL || obj==OBJ_BUTTON || obj==OBJ_CHART || obj==OBJ_BITMAP_LABEL || obj==OBJ_EDIT || obj==OBJ_RECTANGLE_LABEL)
        {
         //--- set the object coordinates 
         ObjectSetInteger(ExtChartID,OBJ_NAME,OBJPROP_XDISTANCE,OBJ_X);
         ObjectSetInteger(ExtChartID,OBJ_NAME,OBJPROP_YDISTANCE,OBJ_Y);
         //--- set the object size 
         ObjectSetInteger(ExtChartID,OBJ_NAME,OBJPROP_XSIZE,OBJ_WIDTH); 
         ObjectSetInteger(ExtChartID,OBJ_NAME,OBJPROP_YSIZE,OBJ_HEIGHT);
        }
      //--- update the chart to show the changes
      ChartRedraw(ExtChartID);
     }
  }
//+------------------------------------------------------------------+
//| Fill the array of object anchor points                           |
//+------------------------------------------------------------------+
void SetAnchorPointsData(void)
  {
//--- left anchor point bar (with index 0)
   int bar_first=(int)ChartGetInteger(ExtChartID,CHART_FIRST_VISIBLE_BAR)-1;
   
//--- set the price/time of the first anchor point (with index 0)
   ExtAnchorPoints[0].price=iOpen(_Symbol,_Period,bar_first);
   ExtAnchorPoints[0].time =iTime(_Symbol,_Period,bar_first);
   
//--- set the price/time of anchor points with indices 1 - 3
   int distance=(int)round(bar_first/4);  // distance in bars between anchor points
   for(int i=1;i<4;i++)
     {
      ExtAnchorPoints[i].price=iOpen(_Symbol,_Period,bar_first-i*distance);
      ExtAnchorPoints[i].time =iTime(_Symbol,_Period,bar_first-i*distance);
     }
   
//--- set the price/time of the last anchor point (with index 4)
   ExtAnchorPoints[4].price=iOpen(_Symbol,_Period,1);
   ExtAnchorPoints[4].time =iTime(_Symbol,_Period,1);
  }

```
