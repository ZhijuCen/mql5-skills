# SetString

Provides simplified access to the functions of API MQL5 [ObjectSetString()](/en/docs/objects/objectsetstring) for changing string properties of a graphical object bound to a class instance. There are two versions of a function call:

Setting a property value that does not require a modifier

```
bool  SetString(
   ENUM_OBJECT_PROPERTY_STRING   prop_id,     // string property ID
   string                        value        // value
   )

```

Parameters

prop_id

[in]  ID of a graphical object string property.

value

[in]  New value of a changed string property.

Setting a property value indicating the modifier

```
bool  SetString(
   ENUM_OBJECT_PROPERTY_STRING   prop_id,      // string property ID
   int                           modifier,     // modifier 
   string                        value         // value
   )

```

Parameters

prop_id

[in]  ID of a graphical object string property.

modifier

[in]  Modifier (index) of a string property.

value

[in]  New value of a changed string property.

Return Value

true - success, false - cannot change a string property.

Example:

```
//--- example for CChartObject::SetString  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //--- set new name of chart object   
   if(!object.SetString(OBJPROP_NAME,"MyObject"))  
     {  
      printf("Set string property error %d",GetLastError());  
      return;  
     }  
   for(int i=0;i<object.LevelsCount();i++)  
     {  
      //--- set levels description  
      if(!object.SetString(OBJPROP_LEVELTEXT,i,"Level_"+IntegerToString(i)))  
        {  
         printf("Set string property error %d",GetLastError());  
         return;  
        }  
     }  
  }  

```
