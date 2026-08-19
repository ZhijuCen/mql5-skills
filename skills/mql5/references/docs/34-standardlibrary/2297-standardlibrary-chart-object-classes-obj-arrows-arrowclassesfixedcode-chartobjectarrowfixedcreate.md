# Create

Creates "Arrow with fixed code" graphical object.

```
bool  Create(
   long      chart_id,     // chart ID
   string    name,         // object Name
   int       window,       // chart Window
   datetime  time,         // time
   double    price         // price
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  Unique name of the object to create.

window

[in]  Chart window number (0 – main window).

time

[in]  Time coordinate.

price

[in]  Price coordinate.

Return Value

true - successful, false - error.

Example:

```
//--- example for CChartObjectArrowCheck::Create     
//--- example for CChartObjectArrowDown::Create     
//--- example for CChartObjectArrowUp::Create     
//--- example for CChartObjectArrowStop::Create      
//--- example for CChartObjectArrowThumbDown::Create      
//--- example for CChartObjectArrowThumbUp::Create      
//--- example for CChartObjectArrowLeftPrice::Create     
//--- example for CChartObjectArrowRightPrice::Create      
#include <ChartObjects\ChartObjectsArrows.mqh>     
//---     
void OnStart()     
  {     
//--- for example, take CChartObjectArrowCheck     
   CChartObjectArrowCheck arrow;     
//--- set object parameters     
   double price=SymbolInfoDouble(Symbol(),SYMBOL_BID);     
   if(!arrow.Create(0,"ArrowCheck",0,TimeCurrent(),price))     
     {     
      //--- arrow create error     
      printf("Arrow create: Error %d!",GetLastError());     
      //---     
      return;     
     }        
//--- use arrow     
//--- . . .     
  }     

```
