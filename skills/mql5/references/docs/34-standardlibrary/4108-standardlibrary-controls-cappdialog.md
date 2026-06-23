# CAppDialog

CAppDialog is a class of Application Dialog complex control (with dependent controls).

### Description

CAppDialog class is intended to combine the controls with different functions in the group inside the MQL5 program.

### Declaration

```
   class CAppDialog : public CDialog

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
                   CAppDialog

```

### Class Methods by Groups

| Create and destroy |  |
| --- | --- |
| Create | Creates control |
| Destroy | Destroys control |
| Events processing |  |
| OnEvent | Event handler of all chart events |
| Run |  |
| Run | Runs control |
| Chart events processing |  |
| ChartEvent | Event handler of all chart events |
| Settings |  |
| Minimized | Sets a value indicating whether the control is minimized |
| Save/Load |  |
| IniFileSave | Saves the control state to file |
| IniFileLoad | Loads the control state from file |
| IniFileName | Sets the file name for loading/saving the control state |
| IniFileExt | Sets the file extension for loading/saving the control state |
| Initialization |  |
| CreateCommon | Common initialization method |
| CreateExpert | Initialization method for working in Expert Advisors |
| CreateIndicator | Initialization method for working in indicators |
| Dependent controls |  |
| CreateButtonMinMax | Creates dependent controls (minimize/maximize buttons) |
| Dependent controls event handlers |  |
| OnClickButtonClose | "ClickButtonClose" internal event handler (virtual) |
| OnClickButtonMinMax | "ClickButtonMinMax" internal event handler (virtual) |
| External events |  |
| OnAnotherApplicationClose | Event handler of external events (virtual) |
| Methods |  |
| Rebound | Sets new coordinates of the control using CRect class coordinates |
| Minimize | Shows the control in the minimized state |
| Maximize | Shows the control in the maximized (restored) state |
| CreateInstanceId | Creates a unique Id for the names of the control objects |
| ProgramName | Gets the name of MQL5 program, at which the control is used |
| SubwinOff | Get the Y offset of the control subwindow |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Type ,  Compare |
| --- |
| Methods inherited from class CWnd 
 Name ,  ControlsTotal ,  Control ,  Rect ,  Left ,  Left ,  Top ,  Top ,  Right ,  Right ,  Bottom ,  Bottom ,  Width ,  Width ,  Height ,  Height , Size, Size, Size,  Contains ,  Contains ,  Alignment ,  Align ,  Id ,  IsEnabled ,  IsVisible ,  Visible ,  IsActive ,  Activate ,  Deactivate ,  StateFlags ,  StateFlags ,  StateFlagsSet ,  StateFlagsReset ,  PropFlags ,  PropFlags ,  PropFlagsSet ,  PropFlagsReset ,  MouseX ,  MouseX ,  MouseY ,  MouseY ,  MouseFlags ,  MouseFlags ,  MouseFocusKill , BringToTop |
| Methods inherited from class CWndContainer 
 OnMouseEvent ,  ControlsTotal ,  Control ,  ControlFind ,  MouseFocusKill ,  Add ,  Add ,  Delete ,  Delete ,  Move ,  Move ,  Shift ,  Id ,  Enable ,  Disable ,  Show ,  Hide |
| Methods inherited from class CDialog 
 Caption ,  Caption ,  Add ,  Add |

###
