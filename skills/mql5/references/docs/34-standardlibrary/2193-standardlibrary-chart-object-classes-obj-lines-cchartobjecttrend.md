# CChartObjectTrend

CChartObjectTrend is a class for simplified access to "Trend Line" graphical object properties.

### Description

CChartObjectTrend class provides access to "Trend Line" object properties.

### Declaration

```
   class CChartObjectTrend : public CChartObject

```

### Title

```
   #include <ChartObjects\ChartObjectsLines.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectTrend
Direct descendants
CChartObjectChannel, CChartObjectFibo, CChartObjectFiboChannel, CChartObjectFiboExpansion, CChartObjectGannFan, CChartObjectGannGrid, CChartObjectPitchfork, CChartObjectRegression, CChartObjectStdDevChannel, CChartObjectTrendByAngle

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates "Trend Line" graphical object |
| Properties |  |
| RayLeft | Gets/sets "Ray Left" property |
| RayRight | Gets/sets "Ray Right" property |
| Input/output |  |
| virtual  Save | Virtual method for writing to file |
| virtual  Load | Virtual method for reading from file |
| virtual  Type | Virtual method of identification |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CChartObject 
 ChartId ,  Window ,  Name ,  Name ,  NumPoints ,  Attach ,  SetPoint ,  Delete ,  Detach ,  Time ,  Time ,  Price ,  Price ,  Color ,  Color ,  Style ,  Style ,  Width ,  Width ,  Background ,  Background , Fill, Fill,  Z_Order ,  Z_Order ,  Selected ,  Selected ,  Selectable ,  Selectable ,  Description ,  Description ,  Tooltip ,  Tooltip ,  Timeframes ,  Timeframes ,  CreateTime ,  LevelsCount ,  LevelsCount ,  LevelColor ,  LevelColor ,  LevelStyle ,  LevelStyle ,  LevelWidth ,  LevelWidth ,  LevelValue ,  LevelValue ,  LevelDescription ,  LevelDescription ,  GetInteger ,  GetInteger ,  SetInteger ,  SetInteger ,  GetDouble ,  GetDouble ,  SetDouble ,  SetDouble ,  GetString ,  GetString ,  SetString ,  SetString ,  ShiftObject ,  ShiftPoint |

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Graphic objects](/en/docs/objects)
