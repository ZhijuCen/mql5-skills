# Type

Returns graphical object type identifier.

```
virtual int  Type() const

```

Return Value

Object type identifier (for example, OBJ_ARROW for [CChartObjectArrow](/en/docs/standardlibrary/chart_object_classes/obj_arrows/cchartobjectarrow))

Example:

```
//--- example for CChartObjectArrow::Type   
#include <ChartObjects\ChartObjectsArrows.mqh>   
//---   
void OnStart()   
  {   
   CChartObjectArrow arrow;   
   //--- get arrow type   
   int type=arrow.Type();   
  }   

```
