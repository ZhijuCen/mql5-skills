# Create

Creates "Arrow" graphical object.

```
bool  Create(
   long      chart_id,     // chart ID
   string    name,         // object Name
   int       window,       // chart Window
   datetime  time,         // time
   double    price,        // price
   char      code          // arrow code
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  A unique object name.

window

[in]  Chart window number (0 – main window).

time

[in]  Time coordinate.

price

[in]  Price coordinate.

code

[in]  "Arrow" code (Wingdings).

Return Value

true – success, false - error.

Example:

```
//--- example for CChartObjectArrow::Create   
#include <ChartObjects\ChartObjectsArrows.mqh>   
//---   
void OnStart()   
  {   
   CChartObjectArrow arrow;   
//--- set object parameters   
   double price=SymbolInfoDouble(Symbol(),SYMBOL_BID);   
   if(!arrow.Create(0,"Arrow",0,TimeCurrent(),price,181))   
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
