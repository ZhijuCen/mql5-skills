# CChartObjectText

CChartObjectText is a class for simplified access to "Text" graphical object properties.

### Description

CChartObjectText class provides access to "Text" object properties.

### Declaration

```
   class CChartObjectText : public CChartObject

```

### Title

```
   #include <ChartObjects\ChartObjectsTxtControls.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectText
Direct descendants
CChartObjectLabel

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates "Text"  graphical object |
| Properties |  |
| Angle | Gets/sets "Angle" property |
| Font | Gets/sets "Font" property |
| FontSize | Gets/sets "FontSize" property |
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

Derived classes:

- [CChartObjectLabel](/en/docs/standardlibrary/chart_object_classes/obj_controls/cchartobjectlabel)

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Methods of object binding](/en/docs/constants/objectconstants/enum_anchorpoint), [Graphic objects](/en/docs/objects)
