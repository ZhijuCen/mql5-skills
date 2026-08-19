# LevelWidth (Get Method)

Gets the line width of the specified level of a graphical object.

```
int  LevelWidth(
   int  level      // level number
   ) const

```

Parameters

level

[in]  Number of graphical object level.

Return Value

Line width of the specified level of the graphical object attached to the instance of the class. If there is no attached object or the object does not have the specified level, it returns -1.

# LevelWidth (Set Method)

Sets the line width of the specified level of the graphical object.

```
bool  LevelWidth(
   int  level,         // level number
   int  new_width      // new width
   )

```

Parameters

level

[in]  Number of graphical object level.

new_width

[in]  New line width of the specified level of a graphical object.

Return Value

true - success, false - cannot change the width.

Example:

```
//--- example for CChartObject::LevelWidth 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get level width of chart object  
      int level_width=object.LevelWidth(i); 
      if(level_width!=1) 
        { 
         //--- set level width of chart object 
         object.LevelWidth(i,1); 
        } 
     } 
  } 

```
