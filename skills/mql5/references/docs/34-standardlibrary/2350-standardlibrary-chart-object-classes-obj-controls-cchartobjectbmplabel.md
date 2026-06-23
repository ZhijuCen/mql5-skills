# CChartObjectBmpLabel

CChartObjectBmpLabel is a class for simplified access to "Bitmap Label" graphical object properties.

### Description

CChartObjectBmpLabel class provides access to "Bitmap Label" object properties.

### Declaration

```
   class CChartObjectBmpLabel : public CChartObject

```

### Title

```
   #include <ChartObjects\ChartObjectsBmpControls.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectBmpLabel

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates " BmpLabel " graphical object |
| Properties |  |
| X_Distance | Gets/sets "X_Distance" property |
| Y_Distance | Gets/sets "Y_Distance" property |
| X_Offset | Gets/sets "X_Offset" property |
| Y_Offset | Gets/sets "Y_Offset" property |
| Corner | Gets/sets "Corner" property |
| X_Size | Gets/sets "X_Size" property |
| Y_Size | Gets/sets "Y_Size" property |
| BmpFileOn | Gets/sets "BmpFileOn" property for button pressed state (On) |
| BmpFileOff | Gets/sets "BmpFileOff" property for button depressed state (Off) |
| State | Gets/sets "Button State" property (Pressed/Depressed) |
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

See also

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Chart angle](/en/docs/constants/objectconstants/enum_basecorner), [Graphic objects](/en/docs/objects)
