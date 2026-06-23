# CChartObjectEdit

CChartObjectEdit is a class for simplified access to "Edit" graphical object properties.

### Description

CChartObjectEdit class provides access to "Edit" object properties.

### Declaration

```
   class CChartObjectEdit : public CChartObjectLabel

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
                   CChartObjectEdit
Direct descendants
CChartObjectButton

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates "Edit" graphical object |
| Properties |  |
| TextAlign | Gets/sets "TextAlign" property |
| X_Size | Gets "X Size" property |
| Y_Size | Gets "Y Size" property |
| BackColor | Gets/sets "Background Color" property |
| BorderColor | Gets/sets "Border Color" property |
| ReadOnly | Gets/sets "Read Only" property |
| Angle | Gets/sets "Angle" property |
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

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Chart angle](/en/docs/constants/objectconstants/enum_basecorner), [Methods of Object Binding](/en/docs/constants/objectconstants/enum_anchorpoint), [Graphic objects](/en/docs/objects)
