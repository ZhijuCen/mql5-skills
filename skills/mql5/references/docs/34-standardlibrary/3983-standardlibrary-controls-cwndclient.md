# CWndClient

CWndClient is a class of the "Client area" complex control (with dependent controls). It is a base class for creation of scroll bars area.

### Description

CWndClient implements the functionality for creation of client area with scroll bars.

### Declaration

```
   class CWndClient : public CWndContainer

```

### Title

```
   #include <Controls\WndClient.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
           CWndContainer
               CWndClient
Direct descendants
CCheckGroup, CListView, CRadioGroup

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates control |
| Chart event handler |  |
| OnEvent | Event handler of all chart events |
| Properties |  |
| ColorBackground | Sets background color |
| ColorBorder | Sets border color |
| BorderType | Sets border type |
| Settings |  |
| VScrolled | Gets/sets the flag indicating that vertical scroll bar is used |
| HScrolled | Gets/sets the flag indicating that horizontal scroll bar is used |
| Dependent controls |  |
| CreateBack | Creates background for scroll bar |
| CreateScrollV | Creates vertical scroll bar |
| CreateScrollH | Creates horizontal scroll bar |
| Internal event handlers |  |
| OnResize | "Resize" internal event handler |
| Dependent controls event handlers |  |
| OnVScrollShow | "Show" internal event handler (virtual) of VScroll dependent control |
| OnVScrollHide | "Hide" internal event handler (virtual) of VScroll dependent control |
| OnHScrollShow | "Show" internal event handler (virtual) of HScroll dependent control |
| OnHScrollHide | "Hide" internal event handler (virtual) of HScroll dependent control |
| OnScrollLineDown | "ScrollLineDown" internal event handler (virtual) of VScroll dependent control |
| OnScrollLineUp | "ScrollLineUp" internal event handler (virtual) of VScroll dependent control |
| OnScrollLineLeft | "ScrollLineLeft" internal event handler (virtual) of HScroll dependent control |
| OnScrollLineRight | "ScrollLineRight" internal event handler (virtual) of HScroll dependent control |
| Resize |  |
| Rebound | Sets new parameters of the control using CRect class coordinates |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Name ,  ControlsTotal ,  Control ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  IsEnabled ,  IsVisible ,  Visible ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |
| Methods inherited from class CWndContainer 
 Destroy ,  OnMouseEvent ,  ControlsTotal ,  Control ,  ControlFind ,  MouseFocusKill ,  Add ,  Add ,  Delete ,  Delete ,  Move ,  Move ,  Shift ,  Enable ,  Disable ,  Hide ,  Save ,  Load |

###
