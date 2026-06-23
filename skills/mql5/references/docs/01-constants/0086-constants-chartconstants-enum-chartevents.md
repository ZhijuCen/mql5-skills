# Types of Chart Events

There are 11 types of events that can be processed using the predefined function [OnChartEvent()](/en/docs/event_handlers/onchartevent). For custom events 65535 identifiers are provided in the range of CHARTEVENT_CUSTOM to CHARTEVENT_CUSTOM_LAST inclusive. To generate a custom event, the [EventChartCustom()](/en/docs/eventfunctions/eventchartcustom) function should be used.

ENUM_CHART_EVENT

| ID | Description |
| --- | --- |
| CHARTEVENT_KEYUP | Releasing a key |
| CHARTEVENT_KEYDOWN | Keystrokes |
| CHARTEVENT_MOUSE_MOVE | Mouse move, mouse clicks (if  CHART_EVENT_MOUSE_MOVE =true is set for the chart) |
| CHARTEVENT_MOUSE_WHEEL | Pressing or scrolling the mouse wheel (if  CHART_EVENT_MOUSE_WHEEL =True for the chart) |
| CHARTEVENT_OBJECT_CREATE | Graphical object  created (if  CHART_EVENT_OBJECT_CREATE =true is set for the chart) |
| CHARTEVENT_OBJECT_CHANGE | Graphical object  property changed via the properties dialog |
| CHARTEVENT_OBJECT_DELETE | Graphical object  deleted (if  CHART_EVENT_OBJECT_DELETE =true is set for the chart) |
| CHARTEVENT_CLICK | Clicking on a chart |
| CHARTEVENT_OBJECT_CLICK | Clicking on a  graphical object |
| CHARTEVENT_OBJECT_DRAG | Drag and drop of a  graphical object |
| CHARTEVENT_OBJECT_ENDEDIT | End of text editing in the graphical object Edit |
| CHARTEVENT_CHART_CHANGE | Change of the chart size or modification of chart properties through the Properties dialog |
| CHARTEVENT_CUSTOM | Initial number of an event from a range of custom events |
| CHARTEVENT_CUSTOM_LAST | The final number of an event from a range of custom events |

### 

### CHARTEVENT_KEYUP event

CHARTEVENT_KEYUP event occurs when a user releases a key while the chart window has input focus. This event complements the existing CHARTEVENT_KEYDOWN, which is generated when a key is pressed. Using both events allows us to accurately determine when keys are pressed and released, which is useful when creating user interfaces and tools with interactive controls.

```
void OnChartEvent(const int id,
                      const long &lparam,
                      const double &dparam,
                      const string &sparam)
  {
    if(id == CHARTEVENT_KEYUP)
      {
        int key = (int)lparam;
        ::Print("Key released: ", TranslateKey(key));
      }
  } 

```

lparam contains (KeyCode) similar to CHARTEVENT_KEYDOWN event. Use the [TranslateKey()](/en/docs/common/translatekey) function to get the text representation of a key.

### 

### Handling dead keys

Handling the so-called "dead keys" is supported. These are keys that do not enter a character immediately, but change the appearance of the next character entered. For example, in the Greek layout the key ; is used to place stress on vowels (ά, έ, ύ etc.).

Now such keys can be tracked using the [TranslateKey()](/en/docs/common/translatekey) function in the CHARTEVENT_KEYDOWN and CHARTEVENT_KEYUP handlers. This allows for correct detection of pressing and releasing complex key combinations in multilingual layouts.

```
void OnChartEvent(const int id,
                      const long &lparam,
                      const double &dparam,
                      const string &sparam)
  {
    if(id == CHARTEVENT_KEYDOWN)
      {
        int key = (int)lparam;
        string text = TranslateKey(key);
        ::Print("Pressed: ", text);
      }
    if(id == CHARTEVENT_KEYUP)
      {
        int key = (int)lparam;
        string text = TranslateKey(key);
        ::Print("Released: ", text);
      }
  }

```

Handling dead keys is useful when implementing custom text fields, hotkey systems, and interfaces that respond to international keyboard layouts.

### 

### OnChartEvent function inputs

For each type of event, the input parameters of the OnChartEvent() function have definite values that are required for the processing of this event. The events and values passed through this parameters are listed in the below table.

| Event | Value of the id parameter | Value of the lparam parameter | Value of the dparam parameter | Value of the sparam parameter |
| --- | --- | --- | --- | --- |
| Key release event | CHARTEVENT_KEYUP | Released key code | The number of event repetitions is always 1 | A bitmask string value describing the status of modifier keys. See  WM_KEYUP message |
| Keypress event | CHARTEVENT_KEYDOWN | Pressed key code | Number of event repetitions while a key remains pressed | A bitmask string value describing the status of modifier keys. See   WM_KEYDOWN message |
| Mouse events  (if  CHART_EVENT_MOUSE_MOVE =true is set for the chart) | CHARTEVENT_MOUSE_MOVE | the X coordinate | the Y coordinate | The string value of a bit mask describing the status of mouse buttons |
| Mouse wheel event (if  CHART_EVENT_MOUSE_WHEEL =true for the chart) | CHARTEVENT_MOUSE_WHEEL | Flags of states of keys and mouse buttons, the X and Y coordinates of the mouse pointer. See description in the  example below | The Delta value of the mouse wheel scroll | — |
| event of graphical object creation  (if  CHART_EVENT_OBJECT_CREATE =true is set for the chart) | CHARTEVENT_OBJECT_CREATE | — | — | Name of the created graphical object |
| Event of change of an object property via the properties dialog | CHARTEVENT_OBJECT_CHANGE | — | — | Name of the modified graphical object |
| Event of graphical object deletion  (if  CHART_EVENT_OBJECT_DELETE =true is set for the chart) | CHARTEVENT_OBJECT_DELETE | — | — | Name of the deleted graphical object |
| Event of a mouse click on the chart | CHARTEVENT_CLICK | the X coordinate | the Y coordinate | — |
| Event of a mouse click in a graphical object belonging to the chart | CHARTEVENT_OBJECT_CLICK | the X coordinate | the Y coordinate | Name of the graphical object, on which the event occurred |
| Event of a graphical object dragging using the mouse | CHARTEVENT_OBJECT_DRAG | — | — | Name of the moved graphical object |
| Event of the finished text editing in the entry box of the LabelEdit graphical object | CHARTEVENT_OBJECT_ENDEDIT | — | — | Name of the  LabelEdit graphical object, in which text editing has completed |
| Event of change  of the chart size or modification of chart properties through the Properties dialog | CHARTEVENT_CHART_CHANGE | — | — | — |
| ID of the user event under the N number | CHARTEVENT_CUSTOM+N | Value set by the  EventChartCustom()  function | Value set by the  EventChartCustom()  function | Value set by the  EventChartCustom()  function |

Example:

```
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
//---
   Print("The expert with name ",MQL5InfoString(MQL5_PROGRAM_NAME)," is running");
//--- enable object create events
   ChartSetInteger(ChartID(),CHART_EVENT_OBJECT_CREATE,true);
//--- enable object delete events
   ChartSetInteger(ChartID(),CHART_EVENT_OBJECT_DELETE,true);
//--- forced updating of chart properties ensures readiness for event processing
   ChartRedraw();
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,         // Event identifier  
                  const long& lparam,   // Event parameter of long type
                  const double& dparam, // Event parameter of double type
                  const string& sparam  // Event parameter of string type
                  )
  {
//--- the left mouse button has been pressed on the chart
   if(id==CHARTEVENT_CLICK)
     {
      Print("The coordinates of the mouse click on the chart are: x = ",lparam,"  y = ",dparam);
     }
//--- the mouse has been clicked on the graphic object
   if(id==CHARTEVENT_OBJECT_CLICK)
     {
      Print("The mouse has been clicked on the object with name '"+sparam+"'");
     }
//--- the key has been pressed
   if(id==CHARTEVENT_KEYDOWN)
     {
      switch(lparam)
        {
         case KEY_NUMLOCK_LEFT:  Print("The KEY_NUMLOCK_LEFT has been pressed");   break;
         case KEY_LEFT:          Print("The KEY_LEFT has been pressed");           break;
         case KEY_NUMLOCK_UP:    Print("The KEY_NUMLOCK_UP has been pressed");     break;
         case KEY_UP:            Print("The KEY_UP has been pressed");             break;
         case KEY_NUMLOCK_RIGHT: Print("The KEY_NUMLOCK_RIGHT has been pressed");  break;
         case KEY_RIGHT:         Print("The KEY_RIGHT has been pressed");          break;
         case KEY_NUMLOCK_DOWN:  Print("The KEY_NUMLOCK_DOWN has been pressed");   break;
         case KEY_DOWN:          Print("The KEY_DOWN has been pressed");           break;
         case KEY_NUMPAD_5:      Print("The KEY_NUMPAD_5 has been pressed");       break;
         case KEY_NUMLOCK_5:     Print("The KEY_NUMLOCK_5 has been pressed");      break;
         default:                Print("Some not listed key has been pressed");
        }
      ChartRedraw();
     }
//--- the object has been deleted
   if(id==CHARTEVENT_OBJECT_DELETE)
     {
      Print("The object with name ",sparam," has been deleted");
     }
//--- the object has been created
   if(id==CHARTEVENT_OBJECT_CREATE)
     {
      Print("The object with name ",sparam," has been created");
     }
//--- the object has been moved or its anchor point coordinates has been changed
   if(id==CHARTEVENT_OBJECT_DRAG)
     {
      Print("The anchor point coordinates of the object with name ",sparam," has been changed");
     }
//--- the text in the Edit of object has been changed
   if(id==CHARTEVENT_OBJECT_ENDEDIT)
     {
      Print("The text in the Edit field of the object with name ",sparam," has been changed");
     }
  }

```

For CHARTEVENT_MOUSE_MOVE event the sparam string parameter contains information about state of the keyboard and mouse buttons:

| Bit | Description |
| --- | --- |
| 1 | State of the left mouse button |
| 2 | State of the right mouse button |
| 3 | State of the SHIFT button |
| 4 | State of the CTRL button |
| 5 | State of the middle mouse button |
| 6 | State of the first extra mouse button |
| 7 | State of the second extra mouse button |

Example:

```
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- enable CHART_EVENT_MOUSE_MOVE messages
   ChartSetInteger(0,CHART_EVENT_MOUSE_MOVE,1);
//--- disable the context menu of the chart (on the right)
   ChartSetInteger(0,CHART_CONTEXT_MENU,0);     
//--- disable the crosshair (by the middle button)
   ChartSetInteger(0,CHART_CROSSHAIR_TOOL,0); 
//--- forced updating of chart properties ensures readiness for event processing
   ChartRedraw();
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
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   if(id==CHARTEVENT_MOUSE_MOVE)
      Comment("POINT: ",(int)lparam,",",(int)dparam,"\n",MouseState((uint)sparam));
  }

```

For the CHARTEVENT_MOUSE_WHEEL event, parameters lparam and dparam contain information about the states of the Ctrl and Shift keys, of mouse buttons, cursor coordinates and the mouse wheel scroll value. For a better understanding, run this Expert Advisor on a chart and scroll the mouse wheel, while pressing different buttons and holding down the keys described in the code.

Example of CHARTEVENT_MOUSE_WHEEL event processing:

```
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
init OnInit()
  {
//--- Enabling mouse wheel scrolling messages
   ChartSetInteger(0,CHART_EVENT_MOUSE_WHEEL,1);
//--- Forced updating of chart properties ensures readiness for event processing
   ChartRedraw();
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   if(id==CHARTEVENT_MOUSE_WHEEL)
     {
      //--- Consider the state of mouse buttons and wheel for this event
      int flg_keys = (int)(lparam>>32);          // The flag of states of the Ctrl and Shift keys, and mouse buttons
      int x_cursor = (int)(short)lparam;         // the X coordinate where the mousse wheel event occurred
      int y_cursor = (int)(short)(lparam>>16);   // the Y coordinate where the mousse wheel event occurred
      int delta    = (int)dparam;                // the total value of mouse scroll, triggers when +120 or -120 is reached
      //--- Processing the flag
      string str_keys="";
      if((flg_keys&0x0001)!=0) str_keys+="LMOUSE ";
      if((flg_keys&0x0002)!=0) str_keys+="RMOUSE ";
      if((flg_keys&0x0004)!=0) str_keys+="SHIFT ";
      if((flg_keys&0x0008)!=0) str_keys+="CTRL ";
      if((flg_keys&0x0010)!=0) str_keys+="MMOUSE ";
      if((flg_keys&0x0020)!=0) str_keys+="X1MOUSE ";
      if((flg_keys&0x0040)!=0) str_keys+="X2MOUSE ";
      
      if(str_keys!="")
         str_keys=", keys='"+StringSubstr(str_keys,0,StringLen(str_keys)-1) + "'";
      PrintFormat("%s: X=%d, Y=%d, delta=%d%s",EnumToString(CHARTEVENT_MOUSE_WHEEL),x_cursor,y_cursor,delta,str_keys);
     }
  }
//+------------------------------------------------------------------+ /*
   Example of the output
   CHARTEVENT_MOUSE_WHEEL: Ctrl pressed: X=193, Y=445, delta=-120
   CHARTEVENT_MOUSE_WHEEL: Shift pressed: X=186, Y=446, delta=120
   CHARTEVENT_MOUSE_WHEEL:  X=178, Y=447, delta=-120
   CHARTEVENT_MOUSE_WHEEL:  X=231, Y=449, delta=120
   CHARTEVENT_MOUSE_WHEEL: MiddleButton pressed: X=231, Y=449, delta=120
   CHARTEVENT_MOUSE_WHEEL: LeftButton pressed: X=279, Y=320, delta=-120
   CHARTEVENT_MOUSE_WHEEL: RightButton pressed: X=253, Y=330, delta=120  */

```

See also

[Event Handling Functions](/en/docs/basis/function/events), [Working with events](/en/docs/eventfunctions)
