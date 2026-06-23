# Type

Returns graphical object type identifier

```
virtual int  Type() const

```

Return Value

Object type identifier:

CChartObjectArrowCheck - OBJ_ARROW_CHECK,

CChartObjectArrowDown - OBJ_ARROW_DOWN,

CChartObjectArrowUp - OBJ_ARROW_UP,

CChartObjectArrowStop - OBJ_ARROW_STOP,

CChartObjectArrowThumbDown - OBJ_ARROW_THUMB_DOWN,

CChartObjectArrowThumbUp - OBJ_ARROW_THUMB_UP,

CChartObjectArrowLeftPrice - OBJ_ARROW_LEFT_PRICE,

CChartObjectArrowRightPrice - OBJ_ARROW_RIGHT_PRICE.

Example:

```
//--- example for CChartObjectArrowCheck::Type  
//--- example for CChartObjectArrowDown::Type  
//--- example for CChartObjectArrowUp::Type  
//--- example for CChartObjectArrowStop::Type   
//--- example for CChartObjectArrowThumbDown::Type   
//--- example for CChartObjectArrowThumbUp::Type   
//--- example for CChartObjectArrowLeftPrice::Type   
//--- example for CChartObjectArrowRightPrice::Type   
#include <ChartObjects\ChartObjectsArrows.mqh>  
//---  
void OnStart()  
  {  
//--- for example, take CChartObjectArrowCheck  
   CChartObjectArrowCheck arrow;  
//--- get arrow type  
   int type=arrow.Type();  
  }  

```
