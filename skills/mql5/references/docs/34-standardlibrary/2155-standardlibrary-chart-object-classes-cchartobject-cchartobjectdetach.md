# Detach

Detaches the graphical object.

```
void  Detach()

```

Return Value

None.

Example:

```
//--- example for CChartObject::Detach
#include <ChartObjects\ChartObject.mqh>
//---
void OnStart()
  {
   CChartObject object;
   //--- detach chart object 
   object.Detach();
  }

```
