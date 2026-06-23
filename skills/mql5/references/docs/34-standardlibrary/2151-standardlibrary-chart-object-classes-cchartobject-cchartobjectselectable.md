# Selectable (Get Method)

Gets the flag indicating an ability of a graphical object to be selected. In other words - if the graphical object can be selected or not.

```
bool  Selectable() const

```

Return Value

Flag indicating the ability of the graphical object, attached to an instance of the class, to be selected. If there is no attached object, returns false.

# Selectable (Set Method)

Sets the flag indicating the ability of a graphical object to be selected.

```
bool  Selectable(
   bool  selectable      // value of the flag
   )

```

Parameters

selectable

[in]  New value of the flag indicating an ability of a graphical object to be selected.

Return Value

true - success, false - cannot change the flag.

Example:

```
//--- example for CChartObject::Selectable  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //--- get the "selectable" flag of chart object   
   bool selectable_flag=object.Selectable();  
   if(selectable_flag)  
     {  
     //--- set the "selectable" flag of chart object  
     object.Selectable(false);  
     }  
  }  

```
