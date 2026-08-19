# GetString

Provides simplified access to the functions of API MQL5 [ObjectGetString()](/en/docs/objects/objectgetstring) for string property values of a graphical object bound to a class instance. There are two versions of a function call:

Getting a property value without checking the correctness

```
string  GetString(
   ENUM_OBJECT_PROPERTY_STRING  prop_id,         // string property ID
   int                          modifier=-1      // modifier
   ) const

```

Parameters

prop_id

[in]  ID of graphical object string property.

modifier=-1

[in]  Modifier (index) of a string property.

Return Value

Value of a string property - success, "" - cannot receive a string property.

Getting a property value verifying the correctness of such treatment

```
bool  GetString(
   ENUM_OBJECT_PROPERTY_STRING  prop_id,      // string property ID
   int                          modifier,     // modifier
   string&                      value         // link to a variable
   ) const

```

Parameters

prop_id

[in]  ID of a graphical object string property.

modifier

[in]  Modifier (index) of a string property.

value

[out]  Link to a variable to place a string property value.

Return Value

true - successful, false - cannot get a string property.

Example:

```
//--- example for CChartObject::GetString 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   string       value; 
   //--- get name of chart object by easy method 
   printf("Object name is '%s'",object.GetString(OBJPROP_NAME)); 
   //--- get name of chart object by classic method 
   if(!object.GetString(OBJPROP_NAME,0,value)) 
     { 
      printf("Get string property error %d",GetLastError()); 
      return; 
     } 
   else 
      printf("Object name is '%s'",value); 
   for(int i=0;i<object.LevelsCount();i++) 
     { 
      //--- get levels description by easy method 
      printf("Level %d description is '%s'",i,object.GetString(OBJPROP_LEVELTEXT,i)); 
      //--- get levels description by classic method 
      if(!object.GetString(OBJPROP_LEVELTEXT,i,value)) 
        { 
         printf("Get string property error %d",GetLastError()); 
         return; 
        } 
      else 
         printf("Level %d description is '%s'",i,value); 
     } 
  } 

```
