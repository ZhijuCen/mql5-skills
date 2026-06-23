# ChartScreenShot

The function provides a screenshot of the chart in its current state in the GIF, PNG or BMP format depending on specified extension.

```
bool  ChartScreenShot(
   long             chart_id,                   // Chart ID
   string           filename,                   // Symbol name
   int              width,                      // Width
   int              height,                     // Height
   ENUM_ALIGN_MODE  align_mode=ALIGN_RIGHT      // Alignment type
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

filename

[in]  Screenshot file name. Cannot exceed 63 characters. Screenshot files are placed in the \Files directory.

width

[in]  Screenshot width in pixels.

height

[in]  Screenshot height in pixels.

align_mode=ALIGN_RIGHT

[in]  Output mode of a narrow screenshot. A value of the [ENUM_ALIGN_MODE](/en/docs/constants/objectconstants/enum_object_property#enum_align_mode) enumeration. ALIGN_RIGHT means align to the right margin (the output from the end). ALIGN_LEFT means Left justify.

Return Value

Returns true if successful, otherwise false.

Note

If you need to take a screenshot from a chart from a certain position, first it's necessary to position the graph using the [ChartNavigate()](/en/docs/chart_operations/chartnavigate) function. If the horizontal size of the screenshot is smaller than the chart window, either the right part of the chart window, or its left part is output, depending on the align_mode settings.

Example:

```
#property description "The Expert Advisor demonstrates how to create a series of screenshots of the current"
#property description "chart using the ChartScreenShot() function. For convenience, the file name is"
#property description "shown on the chart. The height and width of images is defined through macros."
 
#define        WIDTH  800     // Image width to call ChartScreenShot()
#define        HEIGHT 600     // Image height to call ChartScreenShot()
 
//--- input parameters
input int      pictures=5;    // The number of images in the series
int            mode=-1;       // -1 denotes a shift to the right edge of the chart, 1 - to the left
int            bars_shift=300;// The number of bars when scrolling the chart using ChartNavigate()
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- Disable chart autoscroll
   ChartSetInteger(0,CHART_AUTOSCROLL,false);
//--- Set the shift of the right edge of the chart
   ChartSetInteger(0,CHART_SHIFT,true);
//--- Show a candlestick chart
   ChartSetInteger(0,CHART_MODE,CHART_CANDLES);
//---
   Print("Preparation of the Expert Advisor is completed");
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
 
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//--- Show the name of the function, call time and event identifier
   Print(__FUNCTION__,TimeCurrent(),"   id=",id,"   mode=",mode);
//--- Handle the CHARTEVENT_CLICK event ("A mouse click on the chart")
   if(id==CHARTEVENT_CLICK)
     {
      //--- Initial shift from the chart edge
      int pos=0;
      //--- Operation with the left chart edge
      if(mode>0)
        {
         //--- Scroll the chart to the left edge
         ChartNavigate(0,CHART_BEGIN,pos);
         for(int i=0;i<pictures;i++)
           {
            //--- Prepare a text to show on the chart and a file name
            string name="ChartScreenShot"+"CHART_BEGIN"+string(pos)+".gif";
            //--- Show the name on the chart as a comment
            Comment(name);
            //--- Save the chart screenshot in a file in the terminal_directory\MQL5\Files\
            if(ChartScreenShot(0,name,WIDTH,HEIGHT,ALIGN_LEFT))
               Print("We've saved the screenshot ",name);
            //---
            pos+=bars_shift;
            //--- Give the user time to look at the new part of the chart
            Sleep(3000);
            //--- Scroll the chart from the current position bars_shift bars to the right
            ChartNavigate(0,CHART_CURRENT_POS,bars_shift);
           }
         //--- Change the mode to the opposite
         mode*=-1;
        }
      else // Operation with the right chart edge
        {
         //--- Scroll the chart to the right edge
         ChartNavigate(0,CHART_END,pos);
         for(int i=0;i<pictures;i++)
           {
            //--- Prepare a text to show on the chart and a file name
            string name="ChartScreenShot"+"CHART_END"+string(pos)+".gif";
            //--- Show the name on the chart as a comment
            Comment(name);
            //--- Save the chart screenshot in a file in the terminal_directory\MQL5\Files\
            if(ChartScreenShot(0,name,WIDTH,HEIGHT,ALIGN_RIGHT))
               Print("We've saved the screenshot ",name);
            //---
            pos+=bars_shift;
            //--- Give the user time to look at the new part of the chart
            Sleep(3000);
            //--- Scroll the chart from the current position bars_shift bars to the right
            ChartNavigate(0,CHART_CURRENT_POS,-bars_shift);
           }
         //--- Change the mode to the opposite
         mode*=-1;
        }
     }  // End of CHARTEVENT_CLICK event handling
//--- End of the OnChartEvent() handler  
  }

```

See also

[ChartNavigate()](/en/docs/chart_operations/chartnavigate), [Resources](/en/docs/runtime/resources)
