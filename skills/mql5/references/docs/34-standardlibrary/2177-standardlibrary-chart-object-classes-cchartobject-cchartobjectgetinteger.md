# GetInteger

Provides simplified access to the functions of API MQL5 [ObjectGetInteger()](/en/docs/objects/objectgetinteger) to receive values of integer properties (of bool, char, uchar, short, ushort, int, uint, long, ulong, datetime, color types) of a graphical object bound to a class instance. There are two versions of the function call:

Getting a property value without checking the correctness

```
long  GetInteger(
   ENUM_OBJECT_PROPERTY_INTEGER  prop_id,         // integer property ID
   int                           modifier=-1      // modifier 
   ) const

```

Parameters

prop_id

[in]  ID of the graphical object double property.

modifier=-1

[in]  Modifier (index) of a double property.

Return Value

Value of an integer property - success, 0 - cannot receive an integer property.

Getting a property value verifying the correctness of the operation

```
bool  GetInteger(
   ENUM_OBJECT_PROPERTY_INTEGER  prop_id,      // integer property ID
   int                           modifier,     // modifier 
   long&                         value         // link to a variable
   ) const

```

Parameters

prop_id

[in]  ID of a graphical object integer property.

modifier

[in]  Modifier (index) of an integer property.

value

[out]  Link to a variable to place an integer property value.

Return Value

true - success, false - cannot get an integer property.

Example:

```
//--- example for CChartObject::GetInteger 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get color of chart object by easy method 
   printf("Objects color is %s",ColorToString(object.GetInteger(OBJPROP_COLOR),true)); 
   //--- get color of chart object by classic method 
   long color_value; 
   if(!object.GetInteger(OBJPROP_COLOR,0,color_value)) 
     { 
      printf("Get integer property error %d",GetLastError()); 
      return; 
     } 
   else 
      printf("Objects color is %s",color_value); 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get levels width by easy method 
      printf("Level %d width is %d",i,object.GetInteger(OBJPROP_LEVELWIDTH,i)); 
      //--- get levels width by classic method 
      long width_value; 
      if(!object.GetInteger(OBJPROP_LEVELWIDTH,i,width_value)) 
        { 
         printf("Get integer property error %d",GetLastError()); 
         return; 
        } 
      else 
         printf("Level %d width is %d",i,width_value); 
     } 
  } 

```
