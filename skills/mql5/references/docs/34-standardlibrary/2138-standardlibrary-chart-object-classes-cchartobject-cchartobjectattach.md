# Attach

Attaches a graphical object to an instance of the class.

```
bool  Attach(
   long    chart_id,     // chart ID
   string  name,         // name of the object
   int     window,       // chart window
   int     points        // number of points
   )

```

Parameters

chart_id

[out]  Chart identifier.

name

[in]  Name of the graphical object.

window

[in]  Chart window number (0 – main window).

points

[in]  Number of anchor points of the graphical object.

Return Value

true - success, false - cannot bind the object.

Example:

```
//--- example for CChartObject::Attach 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- attach chart object  
   if(!object.Attach(ChartID(),"MyObject",0,2)) 
     { 
      printf("Object attach error"); 
      return; 
     } 
  } 

```
