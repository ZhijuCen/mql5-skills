# ChartId

Gets the ID of the chart a graphical object belongs to.

```
long  ChartId() const

```

Return Value

ID of the chart where the graphical object is located. If there is no bound object, it returns -1.

Example:

```
//--- example for CChartObject::ChartId 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get chart idintifier of chart object  
   long chart_id=object.ChartId(); 
  } 

```
