# CScroll

CScroll is a base class for creation of scroll bars.

### Description

CScroll is a complex control (with dependent controls), it contains the base functionality for creation of scroll bars. The base class itself is not used as a separate control, two of its heirs ([CScrollV](/en/docs/standardlibrary/controls/cscrollv) and [CScrollH](/en/docs/standardlibrary/controls/cscrollh) classes) are used as controls.

### Declaration

```
   class CScroll : public CWndContainer

```

### Title

```
   #include <Controls\Scrolls.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
           CWndContainer
               CScroll
Direct descendants
CScrollH, CScrollV

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates control |
| Chart object event handlers |  |
| OnEvent | Event handler of all chart events |
| Properties |  |
| MinPos | Gets/sets the minimal position |
| MaxPos | Gets/sets the maximal position |
| CurrPos | Gets/sets the current position |
| Dependent controls creation |  |
| CreateBack | Creates background button |
| CreateInc | Creates increment button of the scroll bar |
| CreateDec | Creates decrement button of the scroll bar |
| CreateThumb | Creates thumb button (can be dragged) of the scroll bar |
| Dependent controls event handlers |  |
| OnClickInc | Event handler used for handling increment button events |
| OnClickDec | Event handler used for handling decrement button events |
| Internal event handlers |  |
| OnShow | "Create" internal event handler |
| OnHide | "Hide" internal event handler |
| OnChangePos | "ChangePosition" internal event handler |
| Object drag handlers |  |
| OnThumbDragStart | "ThumbDragStart" event handler |
| OnThumbDragProcess | "ThumbDragProcess" event handler |
| OnThumbDragEnd | "ThumbDragEnd" event handler |
| Position |  |
| CalcPos | Gets scroll bar position by coordinate |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Name ,  ControlsTotal ,  Control ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  IsEnabled ,  IsVisible ,  Visible ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |
| Methods inherited from class CWndContainer 
 Destroy ,  OnMouseEvent ,  ControlsTotal ,  Control ,  ControlFind ,  MouseFocusKill ,  Add ,  Add ,  Delete ,  Delete ,  Move ,  Move ,  Shift ,  Id ,  Enable ,  Disable ,  Show ,  Hide ,  Save ,  Load |

###
