# Selected (Get Method)

Gets the flag indicating that a graphical object is selected. In other words - if the graphical object is selected or not.

```
bool  Selected() const

```

Return Value

The state that the object, attached to an instance of the class, is selected. If there is no attached object, returns false.

# Selected (Set Method)

Sets the flag indicating that the graphical object is selected.

```
bool  Selected(
   bool  selected      // value of the flag
   )

```

Parameters

selected

[in]  New value of the flag indicating that a graphical object is selected.

Return Value

true - success, false - cannot change the flag.

Example:

```
//--- example for CChartObject::Selected
#include <ChartObjects\ChartObject.mqh>
//---
void OnStart()
  {
   CChartObject object;
   //--- get the "selected" flag of chart object 
   bool selected_flag=object.Selected();
   if(selected_flag)
     {
     //--- set the "selected" flag of chart object
     object.Selected(false);
     }
  }

```
