# Width (Get Method)

Gets the line width of the graphical object.

```
int  Width() const

```

Return Value

The line width of the graphical object attached to an instance of the class. If there is no attached object, it returns -1.

# Width (Set Method)

Sets the line width of the graphical object.

```
bool  Width(
   int  new_width      // thickness
   )

```

Parameters

new_width

[in]  New value of the graphical object line width.

Return Value

true - success, false - cannot change the width.

Example:

```
//--- example for CChartObject::Width  
#include <ChartObjects\ChartObject.mqh>  
//---  
void OnStart()  
  {  
   CChartObject object;  
   //--- get width of chart object   
   int width=object.Width();  
   if(width!=1)  
     {  
      //--- set width of chart object  
      object.Width(1);  
     }  
  }  

```
