# CWndObj

CWndObj is a base class for simple controls (based on chart objects) of the Standard Library.

### Description

CWndObj class implements base methods of the simple control.

### Declaration

```
   class CWndObj : public CWnd

```

### Title

```
   #include <Controls\WndObj.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
           CWndObj
Direct descendants
CBmpButton, CButton, CEdit, CLabel, CPanel, CPicture

```

### Class Methods by Groups

| Chart events processing |  |
| --- | --- |
| OnEvent | Event handler of all chart events |
| Properties |  |
| Text | Gets/sets the  OBJPROP_TEXT  property of the chart object |
| Color | Gets/sets the  OBJPROP_COLOR  property of the chart object |
| ColorBackground | Gets/sets the  OBJPROP_BGCOLOR  property of the chart object |
| ColorBorder | Gets/sets the  OBJPROP_BORDER_COLOR  property of the chart object |
| Font | Gets/sets the  OBJPROP_FONT  property of the chart object |
| FontSize | Gets/sets the  OBJPROP_FONTSIZE  property of the chart object |
| ZOrder | Gets/sets the  OBJPROP_ZORDER  property of the chart object |
| Chart objects event handlers |  |
| OnObjectCreate | CHARTEVENT_OBJECT_CREATE  event handler |
| OnObjectChange | CHARTEVENT_OBJECT_CHANGE  event handler |
| OnObjectDelete | CHARTEVENT_OBJECT_DELETE  event handler |
| OnObjectDrag | CHARTEVENT_OBJECT_DRAG  event handler |
| Properties change event handlers |  |
| OnSetText | "SetText" event handler |
| OnSetColor | "SetColor" event handler |
| OnSetColorBackground | "SetColorBackground" event handler |
| OnSetFont | "SetFont" event handler |
| OnSetFontSize | "SetFontSize" event handler |
| OnSetZOrder | "SetZOrder" event handler |
| Internal event handlers |  |
| OnDestroy | "Destroy" internal event handler |
| OnChange | "Change" internal event handler |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Create ,  Destroy ,  OnMouseEvent ,  Name ,  ControlsTotal ,  Control ,  ControlFind ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Move ,  Move ,  Shift ,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  Id ,  IsEnabled ,  Enable ,  Disable ,  IsVisible ,  Visible ,  Show ,  Hide ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |

###
