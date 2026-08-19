# CreateTime

Gets the graphical object creation time.

```
datetime  CreateTime() const

```

Return Value

Creation time of the graphical object attached to the instance of the class. If there is no attached object, it returns 0.

Example:

```
//--- example for CChartObject::CreateTime  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //--- get create time of chart object   
   datetime create_time=object.CreateTime();  
  }  

```
