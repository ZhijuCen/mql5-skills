# Mouse events

We already had the opportunity to make sure that we receive mouse events using the indicator EventAll.mq5 from the section [Event-related chart properties](/en/book/applications/events/events_properties). The CHARTEVENT_CLICK event is sent to the MQL program on each click of the mouse button in the window, and the CHARTEVENT_MOUSE_MOVE cursor movement and CHARTEVENT_MOUSE_WHEEL wheel scroll events require prior activation in the chart settings, for which the CHART_EVENT_MOUSE_MOVE and CHART_EVENT_MOUSE_WHEEL properties serve, respectively (both are disabled by default).

If there is a graphic object under the mouse, when the button is pressed, not only the CHARTEVENT_CLICK event is generated but also [CHARTEVENT_OBJECT_CLICK](/en/book/applications/events/events_objects).

For the CHARTEVENT_CLICK and CHARTEVENT_MOUSE_MOVE events, the parameters of the OnChartEvent handler contain the following information:

- lparam - X coordinate
- dparam - Y coordinate

In addition, for the CHARTEVENT_MOUSE_MOVE event, the sparam parameter contains a string representation of a bitmask describing the status of mouse buttons and control keys (Ctrl, Shift). Setting a particular bit to 1 means pressing the corresponding button or key.

| Bits | Description |
| --- | --- |
| 0 | Left mouse button state |
| 1 | Right mouse button state |
| 2 | SHIFT key state |
| 3 | CTRL key state |
| 4 | Middle mouse button state |
| 5 | State of the first additional mouse button |
| 6 | State of the second additional mouse button |

For example, if the 0th bit is set, it will give the number 1 (1 << 0), and if the 4th bit is set, it will give the number 16 (1 << 4). Simultaneous pressing of buttons or keys is indicated by a superposition of bits.

For the CHARTEVENT_MOUSE_WHEEL event, the X and Y coordinates, as well as the status flags of the mouse buttons and control keys, are encoded in a special way inside the lparam parameter, and the dparam parameter reports the direction (plus/minus) and amount of wheel scrolling (multiples of ±120).

8-byte integer lparam combines several of the mentioned information fields.

| Bytes | Description |
| --- | --- |
| 0 | Value of  short  type with the X coordinate |
| 1 |  |
| 2 | Value of  short  type with the Y coordinate |
| 3 |  |
| 4 | Bitmask of button and key states |
| 5 | Not used |
| 6 |  |
| 7 |  |

Regardless of the type of event, mouse coordinates are transmitted relative to the entire window, including subwindows, so they should be recalculated for a specific subwindow if necessary.

For a better understanding of CHARTEVENT_MOUSE_WHEEL, use the indicator EventMouseWheel.mq5. It receives and decodes the messages, and then outputs their description to the log.

```
#define KEY_FLAG_NUMBER 7
   
const string keyNameByBit[KEY_FLAG_NUMBER] =
{
   "[Left Mouse] ",
   "[Right Mouse] ",
   "(Shift) ",
   "(Ctrl) ",
   "[Middle Mouse] ",
   "[Ext1 Mouse] ",
   "[Ext2 Mouse] ",
};
   
void OnChartEvent(const int id,
   const long &lparam, const double &dparam, const string &sparam)
{
   if(id == CHARTEVENT_MOUSE_WHEEL)
   {
      const int keymask = (int)(lparam >> 32);
      const short x = (short)lparam;
      const short y = (short)(lparam >> 16);
      const short delta = (short)dparam;
      string message = "";
      
      for(int i = 0; i < KEY_FLAG_NUMBER; ++i)
      {
         if(((1 << i) & keymask) != 0)
         {
            message += keyNameByBit[i];
         }
      }
      
      PrintFormat("X=%d Y=%d D=%d %s", x, y, delta, message);
   }
}

```

Run the indicator on the chart and scroll the mouse wheel by pressing various buttons and keys in turn. Here is an example result:

```
X=186 Y=303 D=-120 
X=186 Y=312 D=120 
X=230 Y=135 D=-120 
X=230 Y=135 D=-120 (Ctrl) 
X=230 Y=135 D=-120 (Shift) (Ctrl) 
X=230 Y=135 D=-120 (Shift) 
X=230 Y=135 D=120 
X=230 Y=135 D=-120 [Middle Mouse] 
X=230 Y=135 D=120 [Middle Mouse] 
X=236 Y=210 D=-240 
X=236 Y=210 D=-360 

```
