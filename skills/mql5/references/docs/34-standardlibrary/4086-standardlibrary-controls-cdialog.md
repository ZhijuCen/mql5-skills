# CDialog

CDialog is class of the Dialog complex control.

### Description

CDialog class is intended to combine the controls with different functions in the group.

### Declaration

```
   class CDialog : public CWndContainer

```

### Title

```
   #include <Controls\Dialog.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
           CWndContainer
               CDialog
Direct descendants
CAppDialog

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates control |
| Chart event handlers |  |
| OnEvent | Event handler of all chart events |
| Properties |  |
| Caption | Gets/sets the value of the "Caption" property |
| Add |  |
| Add | Adds control to the client area |
| Dependent controls |  |
| CreateWhiteBorder | Creates dependent control (white border) |
| CreateBackground | Creates dependent control (background) |
| CreateCaption | Creates dependent control (caption) |
| CreateButtonClose | Creates dependent control (close button) |
| CreateClientArea | Creates dependent control (client area) |
| Dependent controls event handlers |  |
| OnClickCaption | "ClickCaption" internal event handler |
| OnClickButtonClose | "ClickButtonClose" internal event handler |
| Access to client area properties |  |
| ClientAreaVisible | Sets a value indicating whether the client area is visible |
| ClientAreaLeft | Gets X coordinate of the upper-left corner of the control client area |
| ClientAreaTop | Gets Y coordinate of the upper-left corner of the control client area |
| ClientAreaRight | Gets X coordinate of the lower-right corner of the control client area |
| ClientAreaBottom | Gets Y coordinate of the lower-right corner of the control client area |
| ClientAreaWidth | Gets the client area width |
| ClientAreaHeight | Gets the client area height |
| Drag event handlers |  |
| OnDialogDragStart | "DialogDragStart" event handler (virtual) |
| OnDialogDragProcess | "DialogDragProcess" event handler (virtual) |
| OnDialogDragEnd | "DialogDragEnd" event handler (virtual) |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Name ,  ControlsTotal ,  Control ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  IsEnabled ,  IsVisible ,  Visible ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |
| Methods inherited from class CWndContainer 
 Destroy ,  OnMouseEvent ,  ControlsTotal ,  Control ,  ControlFind ,  MouseFocusKill ,  Add ,  Add ,  Delete ,  Delete ,  Move ,  Move ,  Shift ,  Id ,  Enable ,  Disable ,  Show ,  Hide |

###
