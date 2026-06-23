# EventChartCustom

The function generates a custom event for the specified chart.

```
bool  EventChartCustom(
   long    chart_id,            // identifier of the event receiving chart
   ushort  custom_event_id,     // event identifier
   long    lparam,              // parameter of type long
   double  dparam,              // parameter of type double
   string  sparam               // string parameter of the event
   );

```

Parameters

chart_id

[in] Chart identifier. 0 means the current chart.

custom_event_id

[in] ID of the user events. This identifier is automatically added to the value [CHARTEVENT_CUSTOM](/en/docs/constants/chartconstants/enum_chartevents) and converted to the integer type.

lparam

[in] Event parameter of the long type passed to the [OnChartEvent](/en/docs/event_handlers/onchartevent) function.

dparam

[in] Event parameter of the double type passed to the [OnChartEvent](/en/docs/event_handlers/onchartevent) function.

sparam

[in] Event parameter of the string type passed to the [OnChartEvent](/en/docs/event_handlers/onchartevent) function. If the string is longer than 63 characters, it is truncated.

Return Value

Returns true if a custom event has been successfully placed in the events queue of the chart that receives the events. In case of failure, it returns false. Use [GetLastError()](/en/docs/check/getlasterror) to get an error code.

Note

An Expert Advisor or indicator attached to the specified chart handles the event using the function [OnChartEvent](/en/docs/event_handlers/onchartevent)(int event_id, long& lparam, double& dparam, string& sparam).

For each type of event, the input parameters of the OnChartEvent() function have definite values that are required for the processing of this event. The events and values passed through this parameters are listed in the below table.

| Event | Value of the id parameter | Value of the lparam parameter | Value of the dparam parameter | Value of the sparam parameter |
| --- | --- | --- | --- | --- |
| Event of a keystroke | CHARTEVENT_KEYDOWN | code of a pressed key | Repeat count (the number of times the keystroke is repeated as a result of the user holding down the key) | The string value of a bit mask describing the status of keyboard buttons |
| Mouse event  (if property  CHART_EVENT_MOUSE_MOVE =true is set for the chart) | CHARTEVENT_MOUSE_MOVE | the X coordinate | the Y coordinate | The string value of a bit mask describing the status of mouse buttons |
| Event of graphical object creation  (if  CHART_EVENT_OBJECT_CREATE =true is set for the chart) | CHARTEVENT_OBJECT_CREATE | — | — | Name of the created graphical object |
| Event of change of an object property via the properties dialog | CHARTEVENT_OBJECT_CHANGE | — | — | Name of the modified graphical object |
| Event of graphical object deletion  (if  CHART_EVENT_OBJECT_DELETE =true is set for the chart) | CHARTEVENT_OBJECT_DELETE | — | — | Name of the deleted graphical object |
| Event of a mouse click on the chart | CHARTEVENT_CLICK | the X coordinate | the Y coordinate | — |
| Event of a mouse click in a graphical object belonging to the chart | CHARTEVENT_OBJECT_CLICK | the X coordinate | the Y coordinate | Name of the graphical object, on which the event occurred |
| Event of a graphical object dragging using the mouse | CHARTEVENT_OBJECT_DRAG | — | — | Name of the moved graphical object |
| Event of the finished text editing in the entry box of the LabelEdit graphical object | CHARTEVENT_OBJECT_ENDEDIT | — | — | Name of the  LabelEdit graphical object, in which text editing has completed |
| Event of changes on a chart | CHARTEVENT_CHART_CHANGE | — | — | — |
| ID of the user event under the N number | CHARTEVENT_CUSTOM+N | Value set by the EventChartCustom() function | Value set by the EventChartCustom() function | Value set by the EventChartCustom() function |

Example:

```
//+------------------------------------------------------------------+
//|                                            ButtonClickExpert.mq5 |
//|                        Copyright 2009, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2009, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
string buttonID="Button";
string labelID="Info";
int broadcastEventID=5000;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- Create a button to send custom events
   ObjectCreate(0,buttonID,OBJ_BUTTON,0,100,100);
   ObjectSetInteger(0,buttonID,OBJPROP_COLOR,clrWhite);
   ObjectSetInteger(0,buttonID,OBJPROP_BGCOLOR,clrGray);
   ObjectSetInteger(0,buttonID,OBJPROP_XDISTANCE,100);
   ObjectSetInteger(0,buttonID,OBJPROP_YDISTANCE,100);
   ObjectSetInteger(0,buttonID,OBJPROP_XSIZE,200);
   ObjectSetInteger(0,buttonID,OBJPROP_YSIZE,50);
   ObjectSetString(0,buttonID,OBJPROP_FONT,"Arial");
   ObjectSetString(0,buttonID,OBJPROP_TEXT,"Button");
   ObjectSetInteger(0,buttonID,OBJPROP_FONTSIZE,10);
   ObjectSetInteger(0,buttonID,OBJPROP_SELECTABLE,0);
 
//--- Create a label for displaying information
   ObjectCreate(0,labelID,OBJ_LABEL,0,100,100);
   ObjectSetInteger(0,labelID,OBJPROP_COLOR,clrRed);
   ObjectSetInteger(0,labelID,OBJPROP_XDISTANCE,100);
   ObjectSetInteger(0,labelID,OBJPROP_YDISTANCE,50);
   ObjectSetString(0,labelID,OBJPROP_FONT,"Trebuchet MS");
   ObjectSetString(0,labelID,OBJPROP_TEXT,"No information");
   ObjectSetInteger(0,labelID,OBJPROP_FONTSIZE,20);
   ObjectSetInteger(0,labelID,OBJPROP_SELECTABLE,0);
 
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   ObjectDelete(0,buttonID);
   ObjectDelete(0,labelID);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
 
  }
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//--- Check the event by pressing a mouse button
   if(id==CHARTEVENT_OBJECT_CLICK)
     {
      string clickedChartObject=sparam;
      //--- If you click on the object with the name buttonID
      if(clickedChartObject==buttonID)
        {
         //--- State of the button - pressed or not
         bool selected=ObjectGetInteger(0,buttonID,OBJPROP_STATE);
         //--- log a debug message
         Print("Button pressed = ",selected);
         int customEventID; // Number of the custom event to send
         string message;    // Message to be sent in the event
         //--- If the button is pressed
         if(selected)
           {
            message="Button pressed";
            customEventID=CHARTEVENT_CUSTOM+1;
           }
         else // Button is not pressed
           {
            message="Button in not pressed";
            customEventID=CHARTEVENT_CUSTOM+999;
           }
         //--- Send a custom event "our" chart
         EventChartCustom(0,customEventID-CHARTEVENT_CUSTOM,0,0,message);
         ///--- Send a message to all open charts
         BroadcastEvent(ChartID(),0,"Broadcast Message");
         //--- Debug message
         Print("Sent an event with ID = ",customEventID);
        }
      ChartRedraw();// Forced redraw all chart objects
     }
 
//--- Check the event belongs to the user events
   if(id>CHARTEVENT_CUSTOM)
     {
      if(id==broadcastEventID)
        {
         Print("Got broadcast message from a chart with id = "+lparam);
        }
      else
        {
         //--- We read a text message in the event
         string info=sparam;
         Print("Handle the user event with the ID = ",id);
         //--- Display a message in a label
         ObjectSetString(0,labelID,OBJPROP_TEXT,sparam);
         ChartRedraw();// Forced redraw all chart objects
        }
     }
  }
//+------------------------------------------------------------------+
//| sends broadcast event to all open charts                         |
//+------------------------------------------------------------------+
void BroadcastEvent(long lparam,double dparam,string sparam)
  {
   int eventID=broadcastEventID-CHARTEVENT_CUSTOM;
   long currChart=ChartFirst();
   int i=0;
   while(i<CHARTS_MAX)                 // We have certainly no more than CHARTS_MAX open charts
     {
      EventChartCustom(currChart,eventID,lparam,dparam,sparam);
      currChart=ChartNext(currChart); // We have received a new chart from the previous
      if(currChart==-1) break;        // Reached the end of the charts list
      i++;// Do not forget to increase the counter
     }
  }
//+------------------------------------------------------------------+

```

See also

[Events of the client terminal](/en/docs/runtime/event_fire), [Event handler functions](/en/docs/basis/function/events)
