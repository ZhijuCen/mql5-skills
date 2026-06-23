# LevelsCount (Get Method)

Gets the number of levels of a graphical object.

```
int  LevelsCount() const

```

Return Value

Number of levels of the graphical object attached to an instance of the class. If there is no attached object, it returns 0.

# LevelsCount (Set Method)

Sets the number of levels of the graphical object.

```
bool  LevelsCount(
   int  levels      // number of levels
   )

```

Parameters

levels

[in]  The new number of levels of the graphical object.

Return Value

true - success, false - cannot change the number of levels.

Example:

```
//--- example for CChartObject::LevelsCount 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get levels count of chart object  
   int levels_count=object.LevelsCount(); 
   //--- set levels count of chart object  
   object.LevelsCount(levels_count+1); 
  } 

```
