# CWndContainer

CWndContainer is a base class for a complex control (containing dependent controls) of the Standard library.

### Description

CWndContainer class implements base methods of the complex control.

### Declaration

```
   class CWndContainer : public CWnd

```

### Title

```
   #include <Controls\WndContainer.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
           CWndContainer
Direct descendants
CCheckBox, CComboBox, CDateDropList, CDatePicker, CDialog, CRadioButton, CScroll, CSpinEdit, CWndClient

```

### Class Methods by Groups

| Destroy |  |
| --- | --- |
| Destroy | Destroys all the container controls |
| Chart event handlers |  |
| OnEvent | Event handler of all chart events |
| OnMouseEvent | The  CHARTEVENT_MOUSE_MOVE  event handler |
| Access to container |  |
| ControlsTotal | Gets the number of controls in the container |
| Control | Gets control by index |
| ControlFind | Gets control by ID |
| Add/Delete |  |
| Add | Adds control to a group (container) |
| Delete | Deletes control from a group (container) |
| Geometry |  |
| Move | Performs a absolute displacement of an element group |
| Shift | Performs a relative displacement of an element group |
| Identification |  |
| Id | Sets the ID for all controls of the container |
| State |  |
| Enable | Enables all controls of the container |
| Disable | Disables all controls of the container |
| Show | Shows all controls of the container |
| Hide | Hides all controls of the container |
| Mouse operations |  |
| MouseFocusKill | Kills mouse focus |
| File operations |  |
| Save | Saves container information to file |
| Load | Loads container information from file |
| Internal event handlers |  |
| OnResize | "Resize" event handler |
| OnActivate | "Activate" event handler |
| OnDeactivate | "Deactivate" event handler |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Create ,  Name ,  ControlsTotal ,  Control ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  IsEnabled ,  IsVisible ,  Visible ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |

###
