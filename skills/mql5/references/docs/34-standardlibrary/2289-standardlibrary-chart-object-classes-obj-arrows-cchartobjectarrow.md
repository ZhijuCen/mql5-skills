# CChartObjectArrow

CChartObjectArrow is a class for simplified access to "Arrow" graphical object properties.

### Description

CChartObjectArrow class provides access to common properties of "Arrow" objects to all of its descendants.

### Declaration

```
   class CChartObjectArrow : public CChartObject

```

### Title

```
   #include <ChartObjects\ChartObjectsArrows.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectArrow
Direct descendants
CChartObjectArrowCheck, CChartObjectArrowDown, CChartObjectArrowLeftPrice, CChartObjectArrowRightPrice, CChartObjectArrowStop, CChartObjectArrowThumbDown, CChartObjectArrowThumbUp, CChartObjectArrowUp

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates  "Arrow" graphical object |
| Properties |  |
| ArrowCode | Gets/sets "Arrow Code" property |
| Anchor | Gets/sets "Anchor" property |
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

[Object types](/en/docs/constants/objectconstants/enum_object), [Methods of objects binding](/en/docs/constants/objectconstants/enum_anchorpoint), [Graphic objects](/en/docs/objects)
