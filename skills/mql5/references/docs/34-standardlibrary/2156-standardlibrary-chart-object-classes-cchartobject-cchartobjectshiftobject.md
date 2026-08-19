# ShiftObject

Shifts a graphical object.

```
bool  ShiftObject(
   datetime  d_time,      // increment of time coordinate
   double    d_price      // increment of price coordinate
   )

```

Parameters

d_time

[in]  Increment of the time coordinate of all anchor points.

d_price

[in]  Increment of the price coordinate of all anchor points.

Return Value

true - success, false - cannot shift the object.

Example:

```
//--- example for CChartObject::ShiftObject  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   datetime     d_time;  
   double       d_price;  
   //--- shift chart object  
   object.ShiftObject(d_time,d_price);  
  }  

```
