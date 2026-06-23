# Mouse and keyboard control

In this section, we will get acquainted with a group of properties that affect how the chart will capture certain mouse and keyboard manipulations, which are regarded by default as control actions. In particular, MetaTrader 5 users are well aware that the chart can be scrolled with the mouse, and the context menu can be called to execute the most requested commands. MQL5 allows you to disable this behavior of the chart completely or partially. It is important to note that this can only be done programmatically: there are no similar options in the terminal user interface.

The only exception is the CHART_DRAG_TRADE_LEVELS option (see in the table below): the terminal settings provide the Charts tab with a drop-down list that controls the permission to drag trading levels with the mouse.

All properties of this group have a boolean type (true for allowed and false for disabled) and they are in the ENUM_CHART_PROPERTY_INTEGER enumeration.

| Identifier | Description |
| --- | --- |
| CHART_CONTEXT_MENU | Enabling/disabling access to the context menu by pressing the right mouse button. The  false  value disables only the context menu of the chart, while the context menu for objects on the chart remains available. The default value is  true . |
| CHART_CROSSHAIR_TOOL | Enable/disable access to the Crosshair tool by pressing the middle mouse button. The default value is  true . |
| CHART_MOUSE_SCROLL | Scrolling the chart with the left mouse button or wheel. When scrolling is enabled, this applies not only to scrolling horizontally, but also vertically, but the latter is only available when a fixed scale is set: one of the CHART_SCALEFIX, CHART_SCALEFIX_11, or CHART_SCALE_PT_PER_BAR properties. The default value is  true . |
| CHART_KEYBOARD_CONTROL | Ability to manage the chart from the keyboard (buttons  Home ,  End ,  PageUp/PageDown , +/-, up/down arrows, etc.). Setting to  false  allows you to disable scrolling and scaling of the chart, but at the same time, it is possible to receive keystroke events for these keys in  OnChartEvent . The default value is  true . |
| CHART_QUICK_NAVIGATION | Enabling the quick navigation bar in the chart, which automatically appears in the left corner of the timeline when you double-click the mouse or press the  Space  or  Input  keys. Using the bar, you can quickly change the symbol, timeframe, or date of the first visible bar. By default, the property is set to true and quick navigation is enabled. |
| CHART_DRAG_TRADE_LEVELS | Permission to drag trading levels on the chart with the mouse. Drag mode is enabled by default ( true ). |

In the test script ChartInputControl.mq5, we will set the monitor to all of the above properties, and in addition, we will provide input variables for arbitrary setting of values by the user. Our script saves a backup copy of the settings at startup, so all changed properties will be restored when the script ends.

```
#property script_show_inputs
   
#include <MQL5Book/ChartModeMonitor.mqh>
   
input bool ContextMenu = true; // CHART_CONTEXT_MENU
input bool CrossHairTool = true; // CHART_CROSSHAIR_TOOL
input bool MouseScroll = true; // CHART_MOUSE_SCROLL
input bool KeyboardControl = true; // CHART_KEYBOARD_CONTROL
input bool QuickNavigation = true; // CHART_QUICK_NAVIGATION
input bool DragTradeLevels = true; // CHART_DRAG_TRADE_LEVELS
   
void OnStart()
{
   const bool Inputs[] =
   {
      ContextMenu, CrossHairTool, MouseScroll,
      KeyboardControl, QuickNavigation, DragTradeLevels
   };
   const int flags[] =
   {
      CHART_CONTEXT_MENU, CHART_CROSSHAIR_TOOL, CHART_MOUSE_SCROLL,
      CHART_KEYBOARD_CONTROL, CHART_QUICK_NAVIGATION, CHART_DRAG_TRADE_LEVELS
   };
   ChartModeMonitor m(flags);
   Print("Initial state:");
   m.print();
   m.backup();
   
   for(int i = 0; i < ArraySize(flags); ++i)
   {
      ChartSetInteger(0, (ENUM_CHART_PROPERTY_INTEGER)flags[i], Inputs[i]);
   }
   
   while(!IsStopped())
   {
      m.snapshot();
      Sleep(500);
   }
   m.restore();
}

```

For example, when we run the script, we can reset the permissions for the context menu, crosshair tool, mouse, and keyboard controls to false. The result is in the following log.

```
Initial state:
    [key] [value]
[0]    50       1
[1]    49       1
[2]    42       1
[3]    47       1
[4]    45       1
[5]    43       1
CHART_CONTEXT_MENU 1 -> 0
CHART_CROSSHAIR_TOOL 1 -> 0
CHART_MOUSE_SCROLL 1 -> 0
CHART_KEYBOARD_CONTROL 1 -> 0

```

In this case, you will not be able to move the chart with either the mouse or the keyboard, and even call the context menu. Therefore, in order to restore its performance, you will have to drop the same or another script on the chart (recall that there can be only one script on the chart, and when a new one is applied, the previous one is unloaded;). It is enough to drop a new instance of the script, but not to run it (press Cancel in the dialog for entering input variables).
