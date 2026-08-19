# CChartObjectLabel

CChartObjectLabel is a class for simplified access to "Label" graphical object properties.

### Description

CChartObjectLabel class provides access to "Label" object properties.

### Declaration

```
   class CChartObjectLabel : public CChartObjectText

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
Direct descendants
CChartObjectEdit, CChartObjectRectLabel

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates "Label" graphical object |
| Properties |  |
| X_Distance | Gets/sets "X_Distance" property |
| Y_Distance | Gets/sets "Y_Distance" property |
| X_Size | Gets/sets "X_Size" property |
| Y_Size | Gets/sets "Y_Size" property |
| Corner | Gets/sets "Corner" property |
| Time | "Stub" for time coordinate change |
| Price | "Stub" for price coordinate change |
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

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Chart angle](/en/docs/constants/objectconstants/enum_basecorner), [Methods of Object Binding](/en/docs/constants/objectconstants/enum_anchorpoint), [Graphic objects](/en/docs/objects)
