# Undocking chart window

Chart windows in the terminal can be undocked from the main window, after which they can be moved to any place on the desktop, including other monitors. MQL5 allows you to find out and change this setting: the corresponding properties are included in the ENUM_CHART_PROPERTY_INTEGER enumeration.

| Identifier | Description | Value type |
| --- | --- | --- |
| CHART_IS_DOCKED | The chart window is docked (true by default). If set to false, then the chart can be dragged outside the terminal | bool |
| CHART_FLOAT_LEFT | The left coordinate of the undocked chart relative to the virtual screen | int |
| CHART_FLOAT_TOP | The top coordinate of the undocked chart relative to the virtual screen | int |
| CHART_FLOAT_RIGHT | The right coordinate of the undocked chart relative to the virtual screen | int |
| CHART_FLOAT_BOTTOM | The bottom coordinate of the undocked chart relative to the virtual screen | int |

Let's set the tracking of these properties in the ChartDock.mq5 script.

```
void OnStart()
{
   const int flags[] =
   {
      CHART_IS_DOCKED,
      CHART_FLOAT_LEFT, CHART_FLOAT_TOP, CHART_FLOAT_RIGHT, CHART_FLOAT_BOTTOM
   };
   ChartModeMonitor m(flags);
   ...
}

```

If you now run the script, then undock the chart using the context menu (unpress the Docked switch command) and move or resize the chart, the corresponding logs will be added to the journal.

```
Initial state:
    [key] [value]
[0]    51       1
[1]    52       0
[2]    53       0
[3]    54       0
[4]    55       0
                              // undocked
CHART_IS_DOCKED 1 -> 0
CHART_FLOAT_LEFT 0 -> 299
CHART_FLOAT_TOP 0 -> 75
CHART_FLOAT_RIGHT 0 -> 1263
CHART_FLOAT_BOTTOM 0 -> 472
                              // changed the vertical size
CHART_FLOAT_BOTTOM 472 -> 500
CHART_FLOAT_BOTTOM 500 -> 539
                              // changed the horizontal size
CHART_FLOAT_RIGHT 1263 -> 1024
CHART_FLOAT_RIGHT 1024 -> 1023
                              // docked back
CHART_IS_DOCKED 0 -> 1

```

This section completes the description of properties managed through the ChartGet and ChartSet functions, so let's summarize the material using a common script ChartFullSet.mq5. It keeps track of the state of all properties of all types. The initialization of the flags array is done by simply filling in successive indexes in a loop. The maximum value is taken with a margin in case of new properties, and extra non-existent numbers will be automatically discarded by the check built into the ChartModeMonitorBase class (remember the detect method).

After activating the script, try changing any settings while watching the program messages in the log.
