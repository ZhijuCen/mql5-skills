# CChartObjectGannGrid

CChartObjectGannGrid is a class for simplified access to "Gann Grid" graphical object properties.

### Description

CChartObjectGannGrid class provides access to "Gann Grid" object properties.

### Declaration

```
   class CChartObjectGannGrid : public CChartObjectTrend

```

### Title

```
   #include <ChartObjects\ChartObjectsGann.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectTrend
               CChartObjectGannGrid

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates  "Gann Grid" graphical object |
| Properties |  |
| PipsPerBar | Gets/sets "Pips per bar" property |
| Downtrend | Gets/sets "Downtrend" property |
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
