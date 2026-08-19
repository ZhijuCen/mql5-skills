# Time (Get Method)

Gets the time coordinate of the specified anchor point of a graphical object.

```
datetime  Time(
   int  point      // point number
   ) const

```

Parameters

point

[in]  Number of a graphical object anchor point.

Return Value

Time coordinate of the specified anchor point of the graphical object attached to an instance of the class. If there is no attached object or the object does not have this point, it returns 0.

# Time (Set Method)

Sets the time coordinate of the specified anchor point of a graphical object.

```
bool  Time(
   int       point,        // point number
   datetime  new_time      // time
   )

```

Parameters

point

[in]  Number of a graphical object anchor point.

new_time

[in]  New value for the time coordinate of the specified graphical object anchor point.

Return Value

true - success, false - cannot change the time coordinate.

Example:

```
//--- example for CChartObject::Time  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //---  
   for(int i=0;i<object.NumPoints();i++)  
     {  
      //--- get time of the chart object point
      datetime point_time=object.Time(i);  
      if(point_time==0)  
        {  
         //--- set time of the chart object point
         object.Time(i,TimeCurrent());  
        }  
     }  
  }  

```
