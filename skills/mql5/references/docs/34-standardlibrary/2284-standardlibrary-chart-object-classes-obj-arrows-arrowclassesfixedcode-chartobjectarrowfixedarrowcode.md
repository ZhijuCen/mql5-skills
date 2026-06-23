# ArrowCode

Prohibits "Arrow" symbol code changes.

```
bool  ArrowCode(
   char  code      // code value
   )

```

Parameters

code

[in]  Any value

Return Value

Always false.

Example:

```
//--- example for CChartObjectArrowCheck::ArrowCode      
//--- example for CChartObjectArrowDown::ArrowCode      
//--- example for CChartObjectArrowUp::ArrowCode      
//--- example for CChartObjectArrowStop::ArrowCode       
//--- example for CChartObjectArrowThumbDown::ArrowCode       
//--- example for CChartObjectArrowThumbUp::ArrowCode       
//--- example for CChartObjectArrowLeftPrice::ArrowCode       
//--- example for CChartObjectArrowRightPrice::ArrowCode       
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
//--- set code of arrow      
   if(!arrow.ArrowCode(181))      
     {      
      //--- it is not error      
      printf("Arrow code can not be changed");      
     }      
//--- use arrow      
//--- . . .      
  }      

```
