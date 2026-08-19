# LevelStyle (Get Method)

Gets the line style of the specified level of a graphical object.

```
ENUM_LINE_STYLE  LevelStyle(
   int  level      // level number
   ) const

```

Parameters

level

[in]  Number of graphical object level.

Return Value

Line style of the specified level of the graphical object attached to an instance of the class. If there is no attached object or the object does not have the specified level, it returns WRONG_VALUE.

# LevelStyle (Set Method)

Sets the line style of the specified level of the graphic object.

```
int  LevelStyle(
   int              level,     // level number
   ENUM_LINE_STYLE  style      // line style
   )

```

Parameters

level

[in]  Number of graphical object level.

style

[in]  New line style of the specified level of a graphical object.

Return Value

true - success, false - cannot change the style.

Example:

```
//--- example for CChartObject::LevelStyle 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get level style of chart object  
      ENUM_LINE_STYLE level_style=object.LevelStyle(i); 
      if(level_style!=STYLE_SOLID) 
        { 
         //--- set level style of chart object 
         object.LevelStyle(i,STYLE_SOLID); 
        } 
     } 
  } 

```
