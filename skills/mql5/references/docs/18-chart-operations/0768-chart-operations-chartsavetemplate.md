# ChartSaveTemplate

Saves current chart settings in a template with a specified name.

```
bool  ChartSaveTemplate(
   long          chart_id,     // Chart ID
   const string  filename      // Filename to save the template
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

filename

[in]  The filename to save the template. The ".tpl" extension will be added to the filename automatically; there is no need to specify it. The template is saved in data_folder\Profiles\Templates\ and can be used for manual application in the terminal. If a template with the same filename already exists, the contents of this file will be overwritten.

Return Value

If successful, the function returns true, otherwise it returns false. To get information about [the error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Using templates, you can save chart settings with all applied indicators and graphical objects, to then apply it to another chart.

Example:

```
//+------------------------------------------------------------------+
//|                                       Test_ChartSaveTemplate.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property script_show_inputs
//--- input parameters
input string               symbol="GBPUSD";  // The symbol of a new chart
input ENUM_TIMEFRAMES      period=PERIOD_H3; // The timeframe of a new chart
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- First attach indicators to the chart
   int handle;
//--- Prepare the indicator for use
   if(!PrepareZigzag(NULL,0,handle)) return; // Failed, so exit
//--- Attach the indicator to the current chart, but in a separate window.
   if(!ChartIndicatorAdd(0,1,handle))
     {
      PrintFormat("Failed to attach to chart %s/%s an indicator with the handle=%d. Error code %d",
                  _Symbol,
                  EnumToString(_Period),
                  handle,
                  GetLastError());
      //--- Terminate the program operation
      return;
     }
//--- Refresh the chart to see the indicator
   ChartRedraw();
//--- Find the last two last fractures of the zigzag
   double two_values[];
   datetime two_times[];
   if(!GetLastTwoFractures(two_values,two_times,handle))
     {
      PrintFormat("Failed to find two last fractures in the Zigzag!");
      //--- Terminate the program operation
      return;
     }
//--- Now attach a standard deviation channel
   string channel="StdDeviation Channel";
   if(!ObjectCreate(0,channel,OBJ_STDDEVCHANNEL,0,two_times[1],0))
     {
      PrintFormat("Failed to create object %s. Error code %d",
                  EnumToString(OBJ_STDDEVCHANNEL),GetLastError());
      return;
     }
   else
     {
      //--- The channel has been created, define the second point
      ObjectSetInteger(0,channel,OBJPROP_TIME,1,two_times[0]);
      //--- Set a tooltip text for the channel
      ObjectSetString(0,channel,OBJPROP_TOOLTIP,"Demo from MQL5 Help");
      //--- Refresh the chart
      ChartRedraw();
     }
//--- Save the result in a template
   ChartSaveTemplate(0,"StdDevChannelOnZigzag");
//--- Open a new chart and apply a saved template to it
   long new_chart=ChartOpen(symbol,period);
   //--- Enable tooltips for graphical objects
   ChartSetInteger(new_chart,CHART_SHOW_OBJECT_DESCR,true);
   if(new_chart!=0)
     {
      //--- Apply the saved template to a chart
      ChartApplyTemplate(new_chart,"StdDevChannelOnZigzag");
     }
   Sleep(10000);
  }
//+------------------------------------------------------------------+
//| Creates a zigzag handle and ensures readiness of its data        |
//+------------------------------------------------------------------+
bool PrepareZigzag(string sym,ENUM_TIMEFRAMES tf,int &h)
  {
   ResetLastError();
//--- The Zigzag indicator must be located in terminal_data_folder\MQL5\Examples
   h=iCustom(sym,tf,"Examples\\Zigzag");
   if(h==INVALID_HANDLE)
     {
      PrintFormat("%s: Failed to create the handle of the Zigzag indicator. Error code %d",
                  __FUNCTION__,GetLastError());
      return false;
     }
//--- When creating an indicator handle, it requires time to calculate values
   int k=0; // The number of attempts to wait for the indicator calculation
//--- Wait for the calculation in a loop, pausing to 50 milliseconds if the calculation is not yet ready
   while(BarsCalculated(h)<=0)
     {
      k++;
      //--- Show the number of attempts
      PrintFormat("%s: k=%d",__FUNCTION__,k);
      //--- Wait 50 milliseconds to wait until the indicator is calculated
      Sleep(50);
      //--- If more than 100 attempt, then something is wrong
      if(k>100)
        {
         //--- Report a problem
         PrintFormat("Failed to calculate the indicator for %d attempts!");
         //--- Terminate the program operation
         return false;
        }
     }
//--- Everything is ready, the indicator is created and values are calculated
   return true;
  }
//+------------------------------------------------------------------+
//| Searches for the last 2 zigzag fractures and places to arrays    |
//+------------------------------------------------------------------+
bool GetLastTwoFractures(double &get_values[],datetime &get_times[],int handle)
  {
   double values[];         // An array for the values of the zigzag
   datetime times[];        // An array to get time
   int size=100;            // Size of the array
   ResetLastError();
//--- Copy the last 100 values of the indicator
   int copied=CopyBuffer(handle,0,0,size,values);
//--- Check the number of values copied
   if(copied<100)
     {
      PrintFormat("%s: Failed to copy %d values of the indicator with the handle=%d. Error code %d",
                  __FUNCTION__,size,handle,GetLastError());
      return false;
     }
//--- Define the order of access to the array as in a timeseries
   ArraySetAsSeries(values,true);
//--- Write here the numbers of bars, in which fractures were found
   int positions[];
//--- Set array sizes
   ArrayResize(get_values,3); ArrayResize(get_times,3); ArrayResize(positions,3);
//--- Counters
   int i=0,k=0;
//--- Start to search for fractures
   while(i<100)
     {
      double v=values[i];
      //--- We are not interested in empty values
      if(v!=0.0)
        {
         //--- Remember the bar number
         positions[k]=i;
         //--- Remember the value of a zigzag on the fracture
         get_values[k]=values[i];
         PrintFormat("%s: Zigzag[%d]=%G",__FUNCTION__,i,values[i]);
         //--- Increase the counter
         k++;
         //--- If two fractures found, break the loop
         if(k>2) break;
        }
      i++;
     }
//--- Define the order of access to the arrays as in a timeseries
   ArraySetAsSeries(times,true);   ArraySetAsSeries(get_times,true);
   if(CopyTime(_Symbol,_Period,0,size,times)<=0)
     {
      PrintFormat("%s: Failed to copy %d values from CopyTime(). Error code %d",
                  __FUNCTION__,size,GetLastError());
      return false;
     }
//--- Open the bar open time, on which the last 2 fractures occurred
   get_times[0]=times[positions[1]];// The last but one value will be written as the first fracture
   get_times[1]=times[positions[2]];// The value third from the end will be the second fracture
   PrintFormat("%s: first=%s,  second=%s",__FUNCTION__,TimeToString(get_times[1]),TimeToString(get_times[0]));
//--- Successful
   return true;
  }

```

See also

[ChartApplyTemplate()](/en/docs/chart_operations/chartapplytemplate), [Resources](/en/docs/runtime/resources)
