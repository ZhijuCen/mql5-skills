# SetPoint

Sets new coordinates of the specified anchor point of the graphical object.

```
bool  SetPoint(
   int       point,         // point number
   datetime  new_time,      // time coordinate
   double    new_price      // price coordinate
   )

```

Parameters

point

[in]  Number of the graphical object anchor point.

new_time

[in]  New value for the time coordinate of the specified anchor point.

new_price

[in]  New value for price coordinate of the specified anchor point.

Return Value

true - success, false - cannot change coordinates of the point.

Example:

```
//--- example for CChartObject::SetPoint  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   double       price;  
   //---  
   if(object.NumPoints()>0)  
     {  
      //--- set point of chart object  
      object.SetPoint(0,CurrTime(),price);  
     }  
  }  

```
