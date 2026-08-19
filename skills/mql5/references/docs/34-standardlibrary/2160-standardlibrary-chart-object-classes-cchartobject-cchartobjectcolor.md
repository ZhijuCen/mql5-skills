# Color (Get Method)

Gets the line color of the graphical object.

```
color  Color() const

```

Return Value

Line color of the graphical object attached to the class instance. If there is no object attached, it returns CLR_NONE.

# Color (Set Method)

Sets the line color of the graphical object.

```
bool  Color(
   color  new_color      // new color
   )

```

Parameters

new_color

[in]  New value of a graphical object line color.

Return Value

true - success, false - cannot change the color.

Example:

```
//--- example for CChartObject::Color 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get color of chart object  
   color object_color=object.Color(); 
   if(object_color!=clrRed) 
     { 
     //--- set color of chart object 
     object.Color(clrRed); 
     } 
  } 

```
