# LevelDescription (Get Method)

Gets a description (text) of the level of a graphical object.

```
string  LevelDescription(
   int  level       // level number
   ) const

```

Parameters

level

[in]  Number of a graphical object level.

Return Value

Description (text) of the specified level of a graphical object that is bound to an instance of the class. Returns NULL if there is no bound object or the object has no specified level.

# LevelDescription (Set Method)

Sets the description (text) of the specified graphical object level.

```
bool  LevelDescription(
   int     level ,     // level number
   string  text        // text
   )

```

Parameters

level

[in]  Number of a graphical object level.

text

[in]  New value of description (text) of the specified graphical object level.

Return Value

true – success, false - cannot change the description (text).

Example:

```
//--- example for CChartObject::LevelDescription 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get level description of chart object  
      string level_description=object.LevelDescription(i); 
      if(level_description=="") 
        { 
         //--- set level description of chart object 
         object.LevelDescription(i,"Level_"+IntegerToString(i)); 
        } 
     } 
  } 

```
