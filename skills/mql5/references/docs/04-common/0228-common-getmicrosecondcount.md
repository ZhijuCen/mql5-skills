# GetMicrosecondCount

The GetMicrosecondCount() function returns the number of microseconds that have elapsed since the start of MQL5-program.

```
ulong  GetMicrosecondCount();

```

Return Value

Value of ulong type.

Example:

```
//+------------------------------------------------------------------+
//| Test function                                                    |
//+------------------------------------------------------------------+
void Test()
  {
   int    res_int=0;
   double res_double=0;
//---  
   for(int i=0;i<10000;i++)
     {
      res_int+=i*i;
      res_int++;
      res_double+=i*i;
      res_double++;
     }
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   uint   ui=0,ui_max=0,ui_min=INT_MAX;
   ulong  ul=0,ul_max=0,ul_min=INT_MAX;
//--- number of measurements
   for(int count=0;count<1000;count++)
     {
      uint  ui_res=0;
      ulong ul_res=0;
      //--- 
      for(int n=0;n<2;n++)
        {
         //--- select measurement type
         if(n==0) ui=GetTickCount();
         else     ul=GetMicrosecondCount();
         //--- execute code 
         Test();
         //--- add measurement result (depending on type)
         if(n==0) ui_res+=GetTickCount()-ui;
         else     ul_res+=GetMicrosecondCount()-ul;         
        }
      //--- calculate minimum and maximum time for both measurements
      if(ui_min>ui_res) ui_min=ui_res;
      if(ui_max<ui_res) ui_max=ui_res;
      if(ul_min>ul_res) ul_min=ul_res;
      if(ul_max<ul_res) ul_max=ul_res;
     }
//---
   Print("GetTickCount error(msec): ",ui_max-ui_min);
   Print("GetMicrosecondCount error(msec): ",DoubleToString((ul_max-ul_min)/1000.0,2));
  }

```

See also

[Date and Time](/en/docs/dateandtime), [GetTickCount](/en/docs/common/gettickcount), [GetTickCount64](/en/docs/common/gettickcount64)
