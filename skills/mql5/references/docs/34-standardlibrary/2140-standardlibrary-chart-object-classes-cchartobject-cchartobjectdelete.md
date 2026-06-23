# Delete

Removes an attached graphical object from the chart.

```
bool  Delete()

```

Return Value

true - success, false - cannot remove the object.

Example:

```
//--- example for CChartObject::Delete 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- detach chart object  
   if(!object.Delete()) 
     { 
      printf("Object delete error"); 
      return; 
     } 
  } 

```
