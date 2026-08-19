# CChartObject

CChartObject is a base class for the classes of chart graphical objects of the Standard MQL5 library.

### Description

CChartObject class provides the simplified access to MQL5 API functions for all of its descendants.

### Declaration

```
   class CChartObject : public CObject

```

### Title

```
   #include <ChartObjects\ChartObject.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
Direct descendants
CChartObjectArrow, CChartObjectBitmap, CChartObjectBmpLabel, CChartObjectCycles, CChartObjectElliottWave3, CChartObjectEllipse, CChartObjectFiboArc, CChartObjectFiboFan, CChartObjectFiboTimes, CChartObjectHLine, CChartObjectRectangle, CChartObjectSubChart, CChartObjectText, CChartObjectTrend, CChartObjectTriangle, CChartObjectVLine

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| ChartId | Gets the ID of the chart a graphical object belongs to |
| Window | Gets the number of a chart window where a graphical object is located |
| Name | Gets/sets the name of a graphical object |
| NumPoints | Gets the number of anchor points |
| Assign |  |
| Attach | Binds a chart graphical object |
| SetPoint | Sets the anchor point parameters |
| Delete |  |
| Delete | Deletes a chart graphical object |
| Detach | Detaches a chart graphical object |
| Shift |  |
| ShiftObject | The relative object shift |
| ShiftPoint | The relative object point shift |
| Object properties |  |
| Time | Gets/sets the time coordinates of an object point |
| Price | Gets/sets the price coordinate of an object point |
| Color | Gets/sets the color of the object |
| Style | Gets/sets the object line style |
| Width | Gets/sets the object line width |
| BackGround | Gets/sets the flag of drawing an object in the background |
| Selected | Gets/sets the "selected" flag of a graphical object |
| Selectable | Gets/sets the selectable object flag |
| Description | Gets/sets the text of the object |
| Tooltip | Gets/sets the tooltip of the object |
| Timeframes | Gets/sets the mask of the object visibility flags |
| Z_Order | Gets/sets the graphical object priority for receiving an event of mouse clicking on a chart |
| CreateTime | Gets the time of the object creation |
| Object level properties |  |
| LevelsCount | Gets/sets the number of object levels |
| LevelColor | Gets/sets the level line color |
| LevelStyle | Gets/sets the level line style |
| LevelWidth | Gets/sets the level line width |
| LevelValue | Gets/sets the level |
| LevelDescription | Gets/sets the level text |
| Access to API MQL5 functions |  |
| GetInteger | Gets the value of the object property |
| SetInteger | Sets the value of the object property |
| GetDouble | Gets the value of the object property |
| SetDouble | Sets the value of the object property |
| GetString | Gets the value of the object property |
| SetString | Sets the value of the object property |
| Input/Output |  |
| virtual  Save | Virtual method of writing to a file |
| virtual  Load | Virtual method of reading from a file |
| virtual  Type | Virtual method of identification |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Compare

```
