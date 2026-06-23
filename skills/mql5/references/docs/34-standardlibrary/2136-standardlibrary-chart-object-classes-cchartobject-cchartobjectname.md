# Name (Get Method)

Gets the name of the graphical object.

```
string  Name() const

```

Return Value

Name of the graphical object attached to an instance of the class. If there is no attached object, it returns NULL.

# Name (Set Method)

Sets the name of the graphical object.

```
bool  Name(
   string  name      // new name
   )

```

Parameters

name

[in]  The new name of the graphical object.

Return Value

true - success, false - cannot change the name.

Example:

```
//--- example for CChartObject::Name   
#include <ChartObjects\ChartObject.mqh>   
//---   
void OnStart()   
  {   
   CChartObject object;   
   //--- get name of chart object    
   string object_name=object.Name();   
   if(object_name!="MyChartObject")   
     {   
     //--- set name of chart object   
     object.Name("MyChartObject");   
     }   
  }   

```
