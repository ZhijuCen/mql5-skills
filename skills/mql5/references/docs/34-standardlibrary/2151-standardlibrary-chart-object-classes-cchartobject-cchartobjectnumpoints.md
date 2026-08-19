# NumPoints

Gets the number of anchor points of a graphical object.

```
int  NumPoints() const

```

Return Value

Number of points linking a graphical object attached to an instance of the class. If there is no attached object, it returns 0.

Example:

```
//--- example for CChartObject::NumPoints 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get points count of chart object  
   int points=object.NumPoints(); 
  } 

```
