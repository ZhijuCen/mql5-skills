# Anchor (Get Method)

Gets anchor type of the "Arrow" object

```
ENUM_ARROW_ANCHOR  Anchor() const

```

Return Value

Anchor type of the "Arrow" object assigned to the class instance (to the chart). If there is no object assigned, it returns WRONG_VALUE.

# Anchor (Set Method)

Sets anchor type for the "Arrow" object

```
bool  Anchor(
   ENUM_ARROW_ANCHOR  anchor      // anchor type
   )

```

Parameters

anchor

[in]  New anchor type value

Return Value

true - successful, false - cannot change the anchor type.

Example:

```
//--- example for CChartObject::Anchor  
#include <ChartObjects\ChartObjectsArrows.mqh>  
//---  
void OnStart()  
  {  
   CChartObjectArrow arrow;  
   ENUM_ARROW_ANCHOR anchor=ANCHOR_BOTTOM;  
//--- set object parameters  
   double price=SymbolInfoDouble(Symbol(),SYMBOL_BID);  
   if(!arrow.Create(0,"Arrow",0,TimeCurrent(),price,181))  
     {  
      //--- arrow create error  
      printf("Arrow create: Error %d!",GetLastError());  
      //---  
      return;  
     }     
//--- get anchor of arrow  
   if(arrow.Anchor()!=anchor)  
     {  
     //--- set anchor of arrow  
     arrow.Anchor(anchor);  
     }  
//--- use arrow  
//--- . . .  
  }  

```
