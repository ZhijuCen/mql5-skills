# CChartObjectStdDevChannel

CChartObjectStdDevChannel is a class for simplified access to "Standard Deviation Channel" graphical object properties.

### Description

CChartObjectStdDevChannel class provides access to "Standard Deviation Channel" object properties.

### Declaration

```
   class CChartObjectStdDevChannel : public CChartObjectTrend

```

### Title

```
   #include <ChartObjects\ChartObjectsChannels.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectTrend
               CChartObjectStdDevChannel

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates " Standard Deviation Channel " graphical object |
| Properties |  |
| Deviations | Gets/sets "Deviation" property |
| Input/output |  |
| virtual  Save | Virtual method for writing to file |
| virtual  Load | Virtual method for reading from file |
| virtual  Type | Virtual method of identification |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CChartObject 
 ChartId ,  Window ,  Name ,  Name ,  NumPoints ,  Attach ,  SetPoint ,  Delete ,  Detach ,  Time ,  Time ,  Price ,  Price ,  Color ,  Color ,  Style ,  Style ,  Width ,  Width ,  Background ,  Background , Fill, Fill,  Z_Order ,  Z_Order ,  Selected ,  Selected ,  Selectable ,  Selectable ,  Description ,  Description ,  Tooltip ,  Tooltip ,  Timeframes ,  Timeframes ,  CreateTime ,  LevelsCount ,  LevelsCount ,  LevelColor ,  LevelColor ,  LevelStyle ,  LevelStyle ,  LevelWidth ,  LevelWidth ,  LevelValue ,  LevelValue ,  LevelDescription ,  LevelDescription ,  GetInteger ,  GetInteger ,  SetInteger ,  SetInteger ,  GetDouble ,  GetDouble ,  SetDouble ,  SetDouble ,  GetString ,  GetString ,  SetString ,  SetString ,  ShiftObject ,  ShiftPoint |
| Methods inherited from class CChartObjectTrend 
 RayLeft ,  RayLeft ,  RayRight ,  RayRight ,  Create |

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Graphic objects](/en/docs/objects)
