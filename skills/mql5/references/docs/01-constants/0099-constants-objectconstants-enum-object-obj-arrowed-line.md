# OBJ_ARROWED_LINE

Arrowed line.

![Example](pics/objarrowedline.png)

Example

The following script creates and moves an arrow line on the chart. Special functions have been developed to create and change graphical object's properties. You can use these functions "as is" in your own applications.

```
//--- description
#property description "Script draws \"Arrowed line\" graphical object."
#property description "Anchor point coordinates are set in percentage of"
#property description "the chart window size."
//--- display window of the input parameters during the script's launch
#property script_show_inputs
//--- input parameters of the script
input string          InpName="ArrowedLine"; // Line name
input int             InpDate1=35;           // 1 st point's date, %
input int             InpPrice1=60;          // 1 st point's price, %
input int             InpDate2=65;           // 2 nd point's date, %
input int             InpPrice2=40;          // 2 nd point's price, %
input color           InpColor=clrRed;       // Line color
input ENUM_LINE_STYLE InpStyle=STYLE_DASH;   // Line style
input int             InpWidth=2;            // Line width
input bool            InpBack=false;         // Background line
input bool            InpSelection=true;     // Highlight to move
input bool            InpHidden=true;        // Hidden in the object list
input long            InpZOrder=0;           // Priority for mouse click
//+------------------------------------------------------------------+
//| Create an arrowed line by the given coordinates                  |
//+------------------------------------------------------------------+
bool ArrowedLineCreate(const long            chart_ID=0,         // chart's ID
                       const string          name="ArrowedLine", // line name
                       const int             sub_window=0,       // subwindow index
                       datetime              time1=0,            // first point time
                       double                price1=0,           // first point price
                       datetime              time2=0,            // second point time
                       double                price2=0,           // second point price
                       const color           clr=clrRed,         // line color
                       const ENUM_LINE_STYLE style=STYLE_SOLID,  // line style
                       const int             width=1,            // line width
                       const bool            back=false,         // in the background
                       const bool            selection=true,     // highlight to move
                       const bool            hidden=true,        // hidden in the object list
                       const long            z_order=0)          // priority for mouse click
  {
//--- set anchor points' coordinates if they are not set
   ChangeArrowedLineEmptyPoints(time1,price1,time2,price2);
//--- reset the error value
   ResetLastError();
//--- create an arrowed line by the given coordinates
   if(!ObjectCreate(chart_ID,name,OBJ_ARROWED_LINE,sub_window,time1,price1,time2,price2))
     {
      Print(__FUNCTION__,
            ": failed to create an arrowed line! Error code = ",GetLastError());
      return(false);
     }
//--- set line color
   ObjectSetInteger(chart_ID,name,OBJPROP_COLOR,clr);
//--- set line display style
   ObjectSetInteger(chart_ID,name,OBJPROP_STYLE,style);
//--- set line width
   ObjectSetInteger(chart_ID,name,OBJPROP_WIDTH,width);
//--- display in the foreground (false) or background (true)
   ObjectSetInteger(chart_ID,name,OBJPROP_BACK,back);
//--- enable (true) or disable (false) the mode of moving the line by mouse
//--- when creating a graphical object using ObjectCreate function, the object cannot be
//--- highlighted and moved by default. Inside this method, selection parameter
//--- is true by default making it possible to highlight and move the object
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTABLE,selection);
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTED,selection);
//--- hide (true) or display (false) graphical object name in the object list
   ObjectSetInteger(chart_ID,name,OBJPROP_HIDDEN,hidden);
//--- set the priority for receiving the event of a mouse click in the chart
   ObjectSetInteger(chart_ID,name,OBJPROP_ZORDER,z_order);
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Move arrowed line's anchor point                                 |
//+------------------------------------------------------------------+
bool ArrowedLinePointChange(const long   chart_ID=0,         // chart's ID
                            const string name="ArrowedLine", // line name
                            const int    point_index=0,      // anchor point index
                            datetime     time=0,             // anchor point time coordinate
                            double       price=0)            // anchor point price coordinate
  {
//--- if point position is not set, move it to the current bar having Bid price
   if(!time)
      time=TimeCurrent();
   if(!price)
      price=SymbolInfoDouble(Symbol(),SYMBOL_BID);
//--- reset the error value
   ResetLastError();
//--- move the line's anchor point
   if(!ObjectMove(chart_ID,name,point_index,time,price))
     {
      Print(__FUNCTION__,
            ": failed to move the anchor point! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| The function removes the arrowed line from the chart             |
//+------------------------------------------------------------------+
bool ArrowedLineDelete(const long   chart_ID=0,         // chart's ID
                       const string name="ArrowedLine") // line name
  {
//--- reset the error value
   ResetLastError();
//--- delete an arrowed line
   if(!ObjectDelete(chart_ID,name))
     {
      Print(__FUNCTION__,
            ": failed to create an arrowed line! Error code = ",GetLastError());
      return(false);
     }
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Check anchor points' values and set default values               |
//| for empty ones                                                   |
//+------------------------------------------------------------------+
void ChangeArrowedLineEmptyPoints(datetime &time1,double &price1,
                                  datetime &time2,double &price2)
  {
//--- if the first point's time is not set, it will be on the current bar
   if(!time1)
      time1=TimeCurrent();
//--- if the first point's price is not set, it will have Bid value
   if(!price1)
      price1=SymbolInfoDouble(Symbol(),SYMBOL_BID);
//--- if the second point's time is not set, it is located 9 bars left from the second one
   if(!time2)
     {
      //--- array for receiving the open time of the last 10 bars
      datetime temp[10];
      CopyTime(Symbol(),Period(),time1,10,temp);
      //--- set the second point 9 bars left from the first one
      time2=temp[0];
     }
//--- if the second point's price is not set, it is equal to the first point's one
   if(!price2)
      price2=price1;
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- check correctness of the input parameters
   if(InpDate1<0 || InpDate1>100 || InpPrice1<0 || InpPrice1>100 || 
      InpDate2<0 || InpDate2>100 || InpPrice2<0 || InpPrice2>100)
     {
      Print("Error! Incorrect values of input parameters!");
      return;
     }
//--- number of visible bars in the chart window
   int bars=(int)ChartGetInteger(0,CHART_VISIBLE_BARS);
//--- price array size
   int accuracy=1000;
//--- arrays for storing the date and price values to be used
//--- for setting and changing line anchor points' coordinates
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
//--- define points for drawing the line
   int d1=InpDate1*(bars-1)/100;
   int d2=InpDate2*(bars-1)/100;
   int p1=InpPrice1*(accuracy-1)/100;
   int p2=InpPrice2*(accuracy-1)/100;
//--- create an arrowed line
   if(!ArrowedLineCreate(0,InpName,0,date[d1],price[p1],date[d2],price[p2],
      InpColor,InpStyle,InpWidth,InpBack,InpSelection,InpHidden,InpZOrder))
     {
      return;
     }
//--- redraw the chart and wait for 1 second
   ChartRedraw();
   Sleep(1000);
//--- now, move the line's anchor points
//--- loop counter
   int v_steps=accuracy/5;
//--- move the second anchor point vertically
   for(int i=0;i<v_steps;i++)
     {
      //--- use the following value
      if(p2<accuracy-1)
         p2+=1;
      //--- move the point
      if(!ArrowedLinePointChange(0,InpName,1,date[d2],price[p2]))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
     }
//--- move the first anchor point vertically
   for(int i=0;i<v_steps;i++)
     {
      //--- use the following value
      if(p1>1)
         p1-=1;
      //--- move the point
      if(!ArrowedLinePointChange(0,InpName,0,date[d1],price[p1]))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
     }
//--- half a second of delay
   Sleep(500);
//--- loop counter
   int h_steps=bars/2;
//--- move both anchor points horizontally at the same time
   for(int i=0;i<h_steps;i++)
     {
      //--- use the following values
      if(d1<bars-1)
         d1+=1;
      if(d2>1)
         d2-=1;
      //--- shift the points
      if(!ArrowedLinePointChange(0,InpName,0,date[d1],price[p1]))
         return;
      if(!ArrowedLinePointChange(0,InpName,1,date[d2],price[p2]))
         return;
      //--- check if the script's operation has been forcefully disabled
      if(IsStopped())
         return;
      //--- redraw the chart
      ChartRedraw();
      // 0.03 seconds of delay
      Sleep(30);
     }
//--- 1 second of delay
   Sleep(1000);
//--- delete an arrowed line
   ArrowedLineDelete(0,InpName);
   ChartRedraw();
//--- 1 second of delay
   Sleep(1000);
//---
  }

```
