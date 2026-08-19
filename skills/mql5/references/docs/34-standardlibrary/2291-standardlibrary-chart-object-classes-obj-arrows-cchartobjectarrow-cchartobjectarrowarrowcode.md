# ArrowCode (Get Method)

Gets "Arrow" symbol code.

```
char  ArrowCode() const

```

Return Value

"Arrow" symbol code of the object assigned to the class instance. If there is no object assigned, it returns 0.

# ArrowCode (Set Method)

Sets symbol code for "Arrow"

```
bool  ArrowCode(
   char  code      // code value
   )

```

Parameters

code

[in]  New value for "arrow" code (Wingdings).

Return Value

true – success, false – cannot change the code.

Example:

```
//--- example for CChartObjectArrow::ArrowCode  
#include <ChartObjects\ChartObjectsArrows.mqh>  
//---  
void OnStart()  
  {  
   CChartObjectArrow arrow;  
   char              code=181;  
//--- set object parameters  
   double price=SymbolInfoDouble(Symbol(),SYMBOL_BID);  
   if(!arrow.Create(0,"Arrow",0,TimeCurrent(),price,code))  
     {  
      //--- arrow create error  
      printf("Arrow create: Error %d!",GetLastError());  
      //---  
      return;  
     }     
//--- change the code of arrow
//--- . . .  
//--- get code of arrow  
   if(arrow.ArrowCode()!=code)  
     {  
     //--- set code of arrow  
     arrow.ArrowCode(code);  
     }  
//--- use arrow  
//--- . . .  
  }  

```
