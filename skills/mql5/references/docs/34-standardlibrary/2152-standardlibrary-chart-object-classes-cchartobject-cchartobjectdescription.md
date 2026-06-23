# Description (Get Method)

Gets a description (text) of a graphical object.

```
string  Description() const

```

Return Value

Description (text) of the graphical object attached to an instance of the class. If there is no attached object, it returns NULL.

# Description (Set Method)

Sets the description (text) of the graphical object.

```
bool  Description(
   string  text      // text
   )

```

Parameters

text

[in]  New description (text) of a graphical object.

Return Value

true - success, false - cannot change the description (text).

Example:

```
//--- example for CChartObject::Description 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart() 
  { 
   CChartObject object; 
   //--- get description of chart object  
   string description=object.Description(); 
   if(description=="") 
     { 
      //--- set description of chart object 
      object.Description("MyObject"); 
     } 
  } 

```
