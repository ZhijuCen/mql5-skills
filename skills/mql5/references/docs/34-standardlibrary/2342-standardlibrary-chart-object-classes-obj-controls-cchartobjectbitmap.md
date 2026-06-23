# CChartObjectBitmap

CChartObjectBitmap is a class for simplified access to "Bitmap" graphical object properties.

### Description

CChartObjectBitmap class provides access to "Bitmap" object properties.

### Declaration

```
   class CChartObjectBitmap : public CChartObject

```

### Title

```
   #include <ChartObjects\ChartObjectsBmpControls.mqh>

```

```
Inheritance hierarchy
   CObject
       CChartObject
           CChartObjectBitmap

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates " Bitmap " graphical object |
| Properties |  |
| BmpFile | Gets/sets "BMP Filename" property |
| X_Offset | Gets/sets "X_Offset" property |
| Y_Offset | Gets/sets "Y_Offset" property |
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

[Object types](/en/docs/constants/objectconstants/enum_object), [Object properties](/en/docs/constants/objectconstants/enum_object_property), [Graphic objects](/en/docs/objects)
