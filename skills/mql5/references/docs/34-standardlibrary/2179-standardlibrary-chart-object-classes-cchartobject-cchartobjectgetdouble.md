# GetDouble

Provides simplified access to the functions of API MQL5 [ObjectGetDouble()](/en/docs/objects/objectgetdouble) to receive double values (of float and double types) of a graphical object bound to a class instance. There are two versions of the function call:

Getting a property value without checking the correctness

```
double  GetDouble(
   ENUM_OBJECT_PROPERTY_DOUBLE  prop_id,         // integer property ID
   int                          modifier=-1      // modifier 
   ) const

```

Parameters

prop_id

[in]  ID of the graphical object double property.

modifier=-1

[in]  Modifier (index) of a double property.

Return Value

Value of a double property - success, [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants) - cannot receive a double property.

Getting a property value in verifying the correctness of such treatment

```
bool  GetDouble(
   ENUM_OBJECT_PROPERTY_DOUBLE  prop_id,      // double property ID
   int                          modifier,     // modifier 
   double&                      value         // link to a variable
   ) const

```

Parameters

prop_id

[in]  ID of a graphical object double property.

modifier

[in]  Modifier (index) of a double property.

value

[out]  Link to a variable to place a double property value.

Return Value

true - success, false - cannot get a double property.

Example:

```
//--- example for CChartObject::GetDouble 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get levels value by easy method 
      printf("Level %d value=%f",i,object.GetDouble(OBJPROP_LEVELVALUE,i)); 
      //--- get levels value by classic method 
      double value; 
      if(!object.SetDouble(OBJPROP_LEVELVALUE,i,value)) 
        { 
         printf("Get double property error %d",GetLastError()); 
         return; 
        } 
      else 
         printf("Level %d value=%f",i,value); 
     } 
  } 

```
