# OnChartEvent

The function is called in indicators and EAs when the [ChartEvent](/en/docs/runtime/event_fire#chartevent) event occurs. The function is meant for handling chart changes made by a user or an MQL5 program.

```
void  OnChartEvent()
   const int       id,       // event ID 
   const long&     lparam,   // long type event parameter
   const double&   dparam,   // double type event parameter
   const string&   sparam    // string type event parameter
   );

```

Parameters

id

[in]  Event ID from the [ENUM_CHART_EVENT](/en/docs/constants/chartconstants/enum_chartevents) enumeration.

lparam

[in]  [long](/en/docs/basis/types/integer/integertypes#long) type event parameter

dparam

[in]  [double](/en/docs/basis/types/double) type event parameter

sparam

[in]  [string](/en/docs/basis/types/stringconst) type event parameter

Return Value

No return value

Note

There are 13 types of events that can be handled using the predefined OnChartEvent() function. 65535 IDs from CHARTEVENT_CUSTOM to CHARTEVENT_CUSTOM_LAST inclusive are provided for custom events. To generate a custom event, use the [EventChartCustom()](/en/docs/eventfunctions/eventchartcustom) function.

Short event description from the [ENUM_CHART_EVENT](/en/docs/constants/chartconstants/enum_chartevents) enumeration:

- CHARTEVENT_KEYUP — occurs when a keyboard key is released, provided that the chart window has input focus;
- CHARTEVENT_KEYDOWN — pressing a key on the keyboard when a chart window is in focus;
- CHARTEVENT_MOUSE_MOVE — moving the mouse and mouse button clicks (if [CHART_EVENT_MOUSE_MOVE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer)=true for a chart);
- CHARTEVENT_OBJECT_CREATE — create a [graphical object](/en/docs/constants/objectconstants/enum_object) (if [CHART_EVENT_OBJECT_CREATE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer)=true for a chart);
- CHARTEVENT_OBJECT_CHANGE — change object properties via the properties dialog;
- CHARTEVENT_OBJECT_DELETE — delete a graphical object (if [CHART_EVENT_OBJECT_DELETE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer)=true for a chart);
- CHARTEVENT_CLICK — clicking on a chart;
- CHARTEVENT_OBJECT_CLICK — mouse click on a graphical object belonging to a chart;
- CHARTEVENT_OBJECT_DRAG — dragging a graphical object with a mouse;
- CHARTEVENT_OBJECT_ENDEDIT — finish editing text in the Edit input box of a graphical object ([OBJ_EDIT](/en/docs/constants/objectconstants/enum_object/obj_edit));
- CHARTEVENT_CHART_CHANGE — change a chart;
- CHARTEVENT_CUSTOM+n — custom event ID, where n is within the range from 0 to 65535. CHARTEVENT_CUSTOM_LAST contains the last acceptable custom event ID (CHARTEVENT_CUSTOM+65535).

All [MQL5 programs](/en/docs/runtime) work in threads other than the main thread of the application. The main application thread is responsible for handling all Windows system messages and, in its turn, generates Windows messages for its own application as a result of this handling. For example, moving the mouse on a chart (WM_MOUSE_MOVE event) generates several system messages for subsequent rendering of the application window, and also sends internal messages to experts and indicators launched on the chart. A situation may occur, where the main application thread has not yet processed the WM_PAINT system message (and therefore has not yet rendered the modified chart), while an EA or an indicator has already received the mouse movement event. In this case, the chart property CHART_FIRST_VISIBLE_BAR will be changed only after the chart is rendered.

For each event type, the inputs of the OnChartEvent() function have certain values necessary for handling that event. The table lists events and values passed via the parameters.

| Event | 'id' parameter value | 'lparam' parameter value | 'dparam' parameter value | 'sparam' parameter value |
| --- | --- | --- | --- | --- |
| Key release event | CHARTEVENT_KEYUP | Released key code | The number of event repetitions is always 1 | A bitmask string value describing the status of modifier keys. See  WM_KEYUP message |
| Keypress event | CHARTEVENT_KEYDOWN | Pressed key code | Number of event repetitions while a key remains pressed | A bitmask string value describing the status of modifier keys. See   WM_KEYDOWN message |
| Mouse events  (if  CHART_EVENT_MOUSE_MOVE =true for a chart) | CHARTEVENT_MOUSE_MOVE | X coordinate | Y coordinate | String value of the bit mask, which describes the status of the mouse keys |
| Mouse wheel event (if  CHART_EVENT_MOUSE_WHEEL =true for the chart) | CHARTEVENT_MOUSE_WHEEL | Flags of states of keys and mouse buttons, X and Y coordinates of the cursor. See the description in the  example | The Delta value of the mouse wheel scroll | — |
| Creating a graphical object (if  CHART_EVENT_OBJECT_CREATE =true for a chart) | CHARTEVENT_OBJECT_CREATE | — | — | Name of a created graphical object |
| Changing object properties via the properties dialog | CHARTEVENT_OBJECT_CHANGE | — | — | Name of a changed graphical object |
| Removing a graphical object (if  CHART_EVENT_OBJECT_DELETE =true for a chart) | CHARTEVENT_OBJECT_DELETE | — | — | Name of a removed graphical object |
| Mouse click on a chart | CHARTEVENT_CLICK | X coordinate | Y coordinate | — |
| Mouse click on a graphical object | CHARTEVENT_OBJECT_CLICK | X coordinate | Y coordinate | Name of a graphical object the event has occurred on |
| Moving a graphical object with mouse | CHARTEVENT_OBJECT_DRAG | — | — | Name of a moved graphical object |
| Finishing a text editing in the "Input field" graphical object input box | CHARTEVENT_OBJECT_ENDEDIT | — | — | Name of the "Input field" graphical object, in which text editing completed |
| Resizing the chart or modifying the chart properties via the properties dialog window | CHARTEVENT_CHART_CHANGE | — | — | — |
| Custom event with N number | CHARTEVENT_CUSTOM+N | Value defined by the  EventChartCustom()  function | Value defined by the  EventChartCustom()  function | Value defined by the  EventChartCustom()  function |

Sample chart event listener:

```
//+------------------------------------------------------------------+
//|                                          OnChartEvent_Sample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Sample chart event listener and custom events generator"
//--- service keys IDs
#define KEY_NUMPAD_5       12
#define KEY_LEFT           37
#define KEY_UP             38
#define KEY_RIGHT          39
#define KEY_DOWN           40
#define KEY_NUMLOCK_DOWN   98
#define KEY_NUMLOCK_LEFT  100
#define KEY_NUMLOCK_5     101
#define KEY_NUMLOCK_RIGHT 102
#define KEY_NUMLOCK_UP    104
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- display the CHARTEVENT_CUSTOM constant value
   Print("CHARTEVENT_CUSTOM=",CHARTEVENT_CUSTOM);
//---
   Print("Launched the EA ",MQLInfoString(MQL5_PROGRAM_NAME));
//--- set the flag of receiving chart object creation events
   ChartSetInteger(ChartID(),CHART_EVENT_OBJECT_CREATE,true);
//--- set the flag of receiving chart object removal events
   ChartSetInteger(ChartID(),CHART_EVENT_OBJECT_DELETE,true);
//--- enabling mouse wheel scrolling messages
   ChartSetInteger(0,CHART_EVENT_MOUSE_WHEEL,1);
//--- forced updating of chart properties ensures readiness for event processing
   ChartRedraw();
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- tick counter for generating a custom event
   static int tick_counter=0;
//--- divide accumulated ticks by this value
   int simple_number=113;
//--- 
   tick_counter++;
//--- send a custom event if the tick counter is multiple of simple_number
   if(tick_counter%simple_number==0)
     {
      //--- form custom event ID from 0 to 65535
      ushort custom_event_id=ushort(tick_counter%65535);
      //---  send a custom event with parameters filling
      EventChartCustom(ChartID(),custom_event_id,tick_counter,SymbolInfoDouble(Symbol(),SYMBOL_BID),__FUNCTION__);
      //--- add to a log for analyzing the example results
      Print(__FUNCTION__,": Sent a custom event ID=",custom_event_id);
     }
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
//--- keypress
   if(id==CHARTEVENT_KEYDOWN)
     {
      switch((int)lparam)
        {
         case KEY_NUMLOCK_LEFT:  Print("Pressed KEY_NUMLOCK_LEFT");   break;
         case KEY_LEFT:          Print("Pressed KEY_LEFT");           break;
         case KEY_NUMLOCK_UP:    Print("Pressed KEY_NUMLOCK_UP");     break;
         case KEY_UP:            Print("Pressed KEY_UP");             break;
         case KEY_NUMLOCK_RIGHT: Print("Pressed KEY_NUMLOCK_RIGHT");  break;
         case KEY_RIGHT:         Print("Pressed KEY_RIGHT");          break;
         case KEY_NUMLOCK_DOWN:  Print("Pressed KEY_NUMLOCK_DOWN");   break;
         case KEY_DOWN:          Print("Pressed KEY_DOWN");           break;
         case KEY_NUMPAD_5:      Print("Pressed KEY_NUMPAD_5");       break;
         case KEY_NUMLOCK_5:     Print("Pressed KEY_NUMLOCK_5");      break;
         default:                Print("Pressed unlisted key");
        }
     }
//--- left-clicking on a chart
   if(id==CHARTEVENT_CLICK)
      Print("Mouse click coordinates on a chart: x = ",lparam,"  y = ",dparam);
//--- clicking on a graphical object
   if(id==CHARTEVENT_OBJECT_CLICK)
      Print("Clicking a mouse button on an object named '"+sparam+"'");
//--- object removed
   if(id==CHARTEVENT_OBJECT_DELETE)
      Print("Removed object named ",sparam);
//--- object created
   if(id==CHARTEVENT_OBJECT_CREATE)
      Print("Created object named ",sparam);
//--- changed object
   if(id==CHARTEVENT_OBJECT_CHANGE)
      Print("Changed object named ",sparam);
//--- object moved or anchor point coordinates changed
   if(id==CHARTEVENT_OBJECT_DRAG)
      Print("Changing anchor points of object named ",sparam);
//--- changed a text in the input field of the Edit graphical object
   if(id==CHARTEVENT_OBJECT_ENDEDIT)
      Print("Changed text in Edit object ",sparam,"  id=",id);
//--- mouse movement events
   if(id==CHARTEVENT_MOUSE_MOVE)
      Comment("POINT: ",(int)lparam,",",(int)dparam,"\n",MouseState((uint)sparam));
   if(id==CHARTEVENT_MOUSE_WHEEL)
     {
      //--- Consider the state of mouse buttons and wheel for this event
      int flg_keys = (int)(lparam>>32);          // The flag of states of the Ctrl and Shift keys, and mouse buttons
      int x_cursor = (int)(short)lparam;         // X coordinate where the mouse wheel event occurred
      int y_cursor = (int)(short)(lparam>>16);   // Y coordinate where the mouse wheel event occurred
      int delta    = (int)dparam;                // Total value of mouse scroll, triggers when +120 or -120 is reached
      //--- handling the flag
      string str_keys="";
      if((flg_keys&0x0001)!=0)
         str_keys+="LMOUSE ";
      if((flg_keys&0x0002)!=0)
         str_keys+="RMOUSE ";
      if((flg_keys&0x0004)!=0)
         str_keys+="SHIFT ";
      if((flg_keys&0x0008)!=0)
         str_keys+="CTRL ";
      if((flg_keys&0x0010)!=0)
         str_keys+="MMOUSE ";
      if((flg_keys&0x0020)!=0)
         str_keys+="X1MOUSE ";
      if((flg_keys&0x0040)!=0)
         str_keys+="X2MOUSE ";
 
      if(str_keys!="")
         str_keys=", keys='"+StringSubstr(str_keys,0,StringLen(str_keys)-1)+"'";
      PrintFormat("%s: X=%d, Y=%d, delta=%d%s",EnumToString(CHARTEVENT_MOUSE_WHEEL),x_cursor,y_cursor,delta,str_keys);
     }
//--- event of resizing the chart or modifying the chart properties using the properties dialog window
   if(id==CHARTEVENT_CHART_CHANGE)
      Print("Changing the chart size or properties");
//--- custom event
   if(id>CHARTEVENT_CUSTOM)
      PrintFormat("Custom event ID=%d, lparam=%d, dparam=%G, sparam=%s",id,lparam,dparam,sparam);
  }
//+------------------------------------------------------------------+
//| MouseState                                                       |
//+------------------------------------------------------------------+
string MouseState(uint state)
  {
   string res;
   res+="\nML: "   +(((state& 1)== 1)?"DN":"UP");   // mouse left
   res+="\nMR: "   +(((state& 2)== 2)?"DN":"UP");   // mouse right 
   res+="\nMM: "   +(((state&16)==16)?"DN":"UP");   // mouse middle
   res+="\nMX: "   +(((state&32)==32)?"DN":"UP");   // mouse first X key
   res+="\nMY: "   +(((state&64)==64)?"DN":"UP");   // mouse second X key
   res+="\nSHIFT: "+(((state& 4)== 4)?"DN":"UP");   // shift key
   res+="\nCTRL: " +(((state& 8)== 8)?"DN":"UP");   // control key
   return(res);
  }

```

See also

[EventChartCustom](/en/docs/eventfunctions/eventchartcustom), [Types of chart events](/en/docs/constants/chartconstants/enum_chartevents), [Event handling functions](/en/docs/basis/function/events), [Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire)
