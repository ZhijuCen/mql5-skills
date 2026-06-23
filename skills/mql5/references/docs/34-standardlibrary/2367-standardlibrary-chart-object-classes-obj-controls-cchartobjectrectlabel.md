# CChartObjectRectLabel

CChartObjectRectLabel is a class for simplified access to "Rectangle Label" graphical object properties.

### Description

CChartObjectRectLabel class provides access to "Rectangle Label" object properties.

### Declaration

```
   class CChartObjectRectLabel : public CChartObjectLabel

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
               CChartObjectLabel
                   CChartObjectRectLabel

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates "Rect Label " graphical object |
| Properties |  |
| X_Size | Sets the horizontal size |
| Y_Size | Sets the vertical size |
| BackColor | Gets/sets the background color |
| Angle | Prohibits slope angle change |
| BorderType | Gets/sets type of the border |
| Input/output |  |
| virtual  Save | Virtual method for writing to file |
| virtual  Load | Virtual method for reading from file |
| virtual  Type | Virtual method of identification |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CChartObject 
 ChartId ,  Window ,  Name ,  Name ,  NumPoints ,  Attach ,  SetPoint ,  Delete ,  Detach ,  Time ,  Time ,  Price ,  Price ,  Color ,  Color ,  Style ,  Style ,  Width ,  Width ,  Background ,  Background , Fill, Fill,  Z_Order ,  Z_Order ,  Selected ,  Selected ,  Selectable ,  Selectable ,  Description ,  Description ,  Tooltip ,  Tooltip ,  Timeframes ,  Timeframes ,  CreateTime ,  LevelsCount ,  LevelsCount ,  LevelColor ,  LevelColor ,  LevelStyle ,  LevelStyle ,  LevelWidth ,  LevelWidth ,  LevelValue ,  LevelValue ,  LevelDescription ,  LevelDescription ,  GetInteger ,  GetInteger ,  SetInteger ,  SetInteger ,  GetDouble ,  GetDouble ,  SetDouble ,  SetDouble ,  GetString ,  GetString ,  SetString ,  SetString ,  ShiftObject ,  ShiftPoint |
| Methods inherited from class CChartObjectText 
 Angle ,  Angle ,  Font ,  Font ,  FontSize ,  FontSize ,  Anchor ,  Anchor ,  Create |
| Methods inherited from class CChartObjectLabel 
 X_Distance ,  X_Distance ,  Y_Distance ,  Y_Distance ,  X_Size ,  Y_Size ,  Corner ,  Corner ,  Time ,  Price ,  Create |

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Graphic objects](/en/docs/objects)
