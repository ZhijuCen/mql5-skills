# CWnd

CWnd is a base class for all Standard Library controls.

### Description

CWnd class is the implementation of the base control class.

### Declaration

```
   class CWnd : public CObject

```

### Title

```
   #include <Controls\Wnd.mqh>

```

```
Inheritance hierarchy
   CObject
       CWnd
Direct descendants
CDragWnd, CWndContainer, CWndObj

```

### Class Methods by Groups

| Create and destroy |  |
| --- | --- |
| Create | Creates control |
| Destroy | Destroys control |
| Chart event handlers |  |
| OnEvent | Event handler of all chart events |
| OnMouseEvent | Event handler for the  CHARTEVENT_MOUSE_MOVE  event |
| Name |  |
| Name | Gets control name |
| Access to container |  |
| ControlsTotal | Gets the number of controls in the container |
| Control | Gets the control by index |
| ControlFind | Gets the control by ID |
| Geometry |  |
| Rect | Gets the control coordinates |
| Left | Gets/sets the X coordinate of the upper-left corner |
| Top | Gets/sets the Y coordinate of the upper-left corner |
| Right | Gets/sets the X coordinate of the lower-right corner |
| Bottom | Gets/sets the Y coordinate of the lower-right corner |
| Width | Gets/sets the control width |
| Height | Gets/sets the control height |
| Move | Control absolute displacement |
| Shift | Control relative displacement |
| Resize | Changes control size |
| Contains | Checks if the point/control is inside the control area |
| Align |  |
| Alignment | Sets alignment properties of the control |
| Align | Performs control alignment in the specified chart area |
| Identification |  |
| Id | Gets/sets the control ID |
| State |  |
| IsEnabled | Checks the control ability to respond to user's actions |
| Enable | Enables the control ability to respond to user's actions |
| Disable | Disables the control ability to respond to user's actions |
| IsVisible | Checks the visibility flag |
| Visible | Sets the visibility flag |
| Show | Shows the control |
| Hide | Hides the control |
| IsActive | Checks the control activity |
| Activate | Activates the control |
| Deactivate | Deactivates the control |
| State flags |  |
| StateFlags | Gets/sets the control state flags |
| StateFlagsSet | Sets the control state flags |
| StateFlagsReset | Resets the control state flags |
| Properties flags |  |
| PropFlags | Gets/sets the control properties flags |
| PropFlagsSet | Sets the control properties flags |
| PropFlagsReset | Resets the control properties flags |
| Mouse operations |  |
| MouseX | Gets/saves the mouse X coordinate |
| MouseY | Gets/saves the mouse Y coordinate |
| MouseFlags | Gets/saves the mouse buttons state |
| MouseFocusKill | Kills mouse focus |
| Internal event handlers |  |
| OnCreate | "Create" event handler |
| OnDestroy | "Destroy" event handler |
| OnMove | "Move" event handler |
| OnResize | "Resize" event handler |
| OnEnable | "Enable" event handler |
| OnDisable | "Disable" event handler |
| OnShow | "Show" event handler |
| OnHide | "Hide" event handler |
| OnActivate | "Activate" event handler |
| OnDeactivate | "Deactivate" event handler |
| OnClick | "Click" event handler |
| OnChange | "Change" event handler |
| Mouse event handlers |  |
| OnMouseDown | "MouseDown" event handler |
| OnMouseUp | "MouseUp" event handler |
| Drag event handlers |  |
| OnDragStart | "DragStart" event handler |
| OnDragProcess | "DragProcess" event handler |
| OnDragEnd | "DragEnd" event handler |
| Drag object |  |
| DragObjectCreate | Creates drag object |
| DragObjectDestroy | Destroys drag object |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```

###
