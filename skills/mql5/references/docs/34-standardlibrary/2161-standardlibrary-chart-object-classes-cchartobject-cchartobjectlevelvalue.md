# LevelValue (Get Method)

Gets the value of the specified level of a graphical object.

```
double  LevelValue(
   int  level      // level number
   ) const

```

Parameters

level

[in]  Number of a graphical object level.

Return Value

The value of the specified level of a graphical object that is bound to an instance of the class. If there is no bound object or the object has no level specified, returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).

# LevelValue (Set Method)

Sets the value of the specified level of the graphical object.

```
bool  LevelValue(
   int     level,         // level number
   double  new_value      // new value
   )

```

Parameters

level

[in]  Number of a graphical object level.

new_value

[in]  New value of the specified level of a graphical object.

Return Value

true - successful, false - cannot change the value.

Example:

```
//--- example for CChartObject::LevelValue  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //---  
   for(int i=0;i<object.LevelsCount();i++)  
     {  
      //--- get level value of chart object   
      double level_value=object.LevelValue(i);  
      if(level_value!=0.1*i)  
        {  
         //--- set level value of chart object  
         object.LevelValue(i,0.1*i);  
        }  
     }  
  }  

```
