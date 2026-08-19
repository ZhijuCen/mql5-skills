# Background (Get Method)

Gets the flag for drawing a graphical object on the background.

```
bool  Background() const

```

Return Value

Flag for drawing the graphical object, attached to an instance of the class, on the background. If there is no attached object, returns false.

# Background (Set Method)

Sets the flag for drawing a graphical object on the background.

```
bool  Background(
   bool  background      // value of the flag
   )

```

Parameters

background

[in]  New value of the flag for drawing a graphical object on the background.

Return Value

true - success, false - cannot change the flag.

Example:

```
//--- example for CChartObject::Background 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get background flag of chart object  
   bool background_flag=object.Background(); 
   if(!background_flag) 
     { 
     //--- set background flag of chart object 
     object.Background(true); 
     } 
  } 

```
