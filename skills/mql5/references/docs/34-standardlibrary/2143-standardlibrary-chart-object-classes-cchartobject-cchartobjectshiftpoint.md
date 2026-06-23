# ShiftPoint

Shifts a specified anchor point of the graphical object.

```
bool  ShiftPoint(
   int       point,       // point number
   datetime  d_time,      // increment of time coordinate
   double    d_price      // increment of price coordinate
   )

```

Parameters

point

[in]  Number of a graphical object anchor point.

d_time

[in]  Increment of the time coordinate of the specified point.

d_price

[in]  Increment of the price coordinate of the specified point.

Return Value

true - success, false - cannot shift the point.

Example:

```
//--- example for CChartObject::ShiftPoint  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   datetime     d_time;  
   double       d_price;  
   //---  
   if(object.NumPoints()>0)  
     {  
      //--- shift point of chart object  
      object.ShiftPoint(0,d_time,d_price);  
     }  
  }  

```
