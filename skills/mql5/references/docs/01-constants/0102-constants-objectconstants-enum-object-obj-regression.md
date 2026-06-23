# OBJ_REGRESSION

Linear Regression Channel.

![Note](pics/objregression.png)

Note

For Linear Regression Channel, it is possible to specify the mode of continuation of its display to the right and/or left ([OBJPROP_RAY_RIGHT](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_integer) and [OBJPROP_RAY_LEFT](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_integer) properties accordingly). The mode of filling the channel with color can also be set.

Example

The following script creates and moves Linear Regression Channel on the chart. Special functions have been developed to create and change graphical object's properties. You can use these functions "as is" in your own applications.

```
//--- description
#property description "Script draws \"Linear Regression Channel\" graphical object."
#property description "Anchor point coordinates are set in percentage of the size of"
#property description "the chart window."
//--- display window of the input parameters during the script's launch
#property script_show_inputs
//--- input parameters of the script
input string          InpName="Regression"; // Channel name
input int             InpDate1=10;          // 1 st point's date, %
input int             InpDate2=40;          // 2 nd point's date, %
input color           InpColor=clrRed;      // Channel color
input ENUM_LINE_STYLE InpStyle=STYLE_DASH;  // Style of channel lines
input int             InpWidth=2;           // Width of channel lines
input bool            InpFill=false;        // Filling the channel with color
input bool            InpBack=false;        // Background channel
input bool            InpSelection=true;    // Highlight to move
input bool            InpRayLeft=false;     // Channel's continuation to the left
input bool            InpRayRight=false;    // Channel's continuation to the right
input bool            InpHidden=true;       // Hidden in the object list
input long            InpZOrder=0;          // Priority for mouse click
//+------------------------------------------------------------------+
//| Create Linear Regression Channel by the given coordinates        |
//+------------------------------------------------------------------+
bool RegressionCreate(const long            chart_ID=0,        // chart's ID
                      const string          name="Regression", // channel name
                      const int             sub_window=0,      // subwindow index 
                      datetime              time1=0,           // first point time
                      datetime              time2=0,           // second point time
                      const color           clr=clrRed,        // channel color
                      const ENUM_LINE_STYLE style=STYLE_SOLID, // style of channel lines
                      const int             width=1,           // width of channel lines
                      const bool            fill=false,        // filling the channel with color
                      const bool            back=false,        // in the background
                      const bool            selection=true,    // highlight to move
                      const bool            ray_left=false,    // channel's continuation to the left
                      const bool            ray_right=false,   // channel's continuation to the right
                      const bool            hidden=true,       // hidden in the object list
                      const long            z_order=0)         // priority for mouse click
  {
//--- set anchor points' coordinates if they are not set
   ChangeRegressionEmptyPoints(time1,time2);
//--- reset the error value
   ResetLastError();
//--- create a channel by the given coordinates
   if(!ObjectCreate(chart_ID,name,OBJ_REGRESSION,sub_window,time1,0,time2,0))
     {
      Print(__FUNCTION__,
            ": failed to create linear regression channel! Error code = ",GetLastError());
      return(false);
     }
//--- set channel color
   ObjectSetInteger(chart_ID,name,OBJPROP_COLOR,clr);
//--- set style of the channel lines
   ObjectSetInteger(chart_ID,name,OBJPROP_STYLE,style);
//--- set width of the channel lines
   ObjectSetInteger(chart_ID,name,OBJPROP_WIDTH,width);
//--- enable (true) or disable (false) the mode of filling the channel
   ObjectSetInteger(chart_ID,name,OBJPROP_FILL,fill);
//--- display in the foreground (false) or background (true)
   ObjectSetInteger(chart_ID,name,OBJPROP_BACK,back);
//--- enable (true) or disable (false) the mode of highlighting the channel for moving
//--- when creating a graphical object using ObjectCreate function, the object cannot be
//--- highlighted and moved by default. Inside this method, selection parameter
//--- is true by default making it possible to highlight and move the object
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTABLE,selection);
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTED,selection);
//--- enable (true) or disable (false) the mode of continuation of the channel's display to the left
   ObjectSetInteger(chart_ID,name,OBJPROP_RAY_LEFT,ray_left);
//--- enable (true) or disable (false) the mode of continuation of the channel's display to the right
   ObjectSetInteger(chart_ID,name,OBJPROP_RAY_RIGHT,ray_right);
//--- hide (true) or display (false) graphical object name in the object list
   ObjectSetInteger(chart_ID,name,OBJPROP_HIDDEN,hidden);
//--- set the priority for receiving the event of a mouse click in the chart
   ObjectSetInteger(chart_ID,name,OBJPROP_ZORDER,z_order);
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Move the channel's anchor point                                  |
//+------------------------------------------------------------------+
bool RegressionPointChange(const long   chart_ID=0,     // chart's ID
                           const string name="Channel", // channel name
                           const int    point_index=0,  // anchor point index
                           datetime     time=0)         // anchor point time coordinate
  {
//--- if point time is not set, move the point to the current bar
   if(!time)
      time=TimeCurrent();
//--- reset the error value
   ResetLastError();
//--- move the anchor point
   if(!ObjectMove(chart_ID,name,point_index,time,0))
     {
      Print(__FUNCTION__,
            ": failed to move the anchor point! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Delete the channel                                               |
//+------------------------------------------------------------------+
bool RegressionDelete(const long   chart_ID=0,     // chart's ID
                      const string name="Channel") // channel name
  {
//--- reset the error value
   ResetLastError();
//--- delete the channel
   if(!ObjectDelete(chart_ID,name))
     {
      Print(__FUNCTION__,
            ": failed to delete the channel! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+-------------------------------------------------------------------------+
//| Check the values of the channel's anchor points and set default values  |
//| for empty ones                                                          |
//+-------------------------------------------------------------------------+
void ChangeRegressionEmptyPoints(datetime &time1,datetime &time2)
  {
//--- if the second point's time is not set, it will be on the current bar
   if(!time2)
      time2=TimeCurrent();
//--- if the first point's time is not set, it is located 9 bars left from the second one
   if(!time1)
     {
      //--- array for receiving the open time of the last 10 bars
      datetime temp[10];
      CopyTime(Symbol(),Period(),time2,10,temp);
      //--- set the first point 9 bars left from the second one
      time1=temp[0];
     }
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- check correctness of the input parameters
   if(InpDate1<0 || InpDate1>100 || 
      InpDate2<0 || InpDate2>100)
     {
      Print("Error! Incorrect values of input parameters!");
      return;
     }
//--- number of visible bars in the chart window
   int bars=(int)ChartGetInteger(0,CHART_VISIBLE_BARS);
//--- price array size
   int accuracy=1000;
//--- arrays for storing the date and price values to be used
//--- for setting and changing channel anchor points' coordinates
   datetime date[];
   double   price[];
//--- memory allocation
   ArrayResize(date,bars);
   ArrayResize(price,accuracy);
//--- fill the array of dates
   ResetLastError();
   if(CopyTime(Symbol(),Period(),0,bars,date)==-1)
     {
      Print("Failed to copy time values! Error code = ",GetLastError());
      return;
     }
//--- fill the array of prices
//--- find the highest and lowest values of the chart
   double max_price=ChartGetDouble(0,CHART_PRICE_MAX);
   double min_price=ChartGetDouble(0,CHART_PRICE_MIN);
//--- define a change step of a price and fill the array
   double step=(max_price-min_price)/accuracy;
   for(int i=0;i<accuracy;i++)
      price[i]=min_price+i*step;
//--- define points for drawing the channel
   int d1=InpDate1*(bars-1)/100;
   int d2=InpDate2*(bars-1)/100;
//--- create linear regression channel
   if(!RegressionCreate(0,InpName,0,date[d1],date[d2],InpColor,InpStyle,InpWidth,
      InpFill,InpBack,InpSelection,InpRayLeft,InpRayRight,InpHidden,InpZOrder))
     {
      return;
     }
//--- redraw the chart and wait for 1 second
   ChartRedraw();
   Sleep(1000);
//--- now, move the channel horizontally to the right
//--- loop counter
   int h_steps=bars/2;
//--- move the channel
   for(int i=0;i<h_steps;i++)
     {
      //--- use the following values
      if(d1<bars-1)
         d1+=1;
      if(d2<bars-1)
         d2+=1;
      //--- move the anchor points
      if(!RegressionPointChange(0,InpName,0,date[d1]))
         return;
      if(!RegressionPointChange(0,InpName,1,date[d2]))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
      // 0.05 seconds of delay
      Sleep(50);
     }
//--- 1 second of delay
   Sleep(1000);
//--- delete the channel from the chart
   RegressionDelete(0,InpName);
   ChartRedraw();
//--- 1 second of delay
   Sleep(1000);
//---
  }

```
