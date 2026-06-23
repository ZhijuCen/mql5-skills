# IndicatorRelease

The function removes an indicator handle and releases the calculation block of the indicator, if it's not used by anyone else.

```
bool  IndicatorRelease(
   int       indicator_handle     // indicator handle
   );

```

Return Value

Returns true in case of success, otherwise returns false.

Note

The function allows removing an indicator handle, if it's no longer needed, thus saving memory. The handle is removed immediately, the calculation block is deleted in some time (if it's not called anymore).

When working in the [strategy tester](/en/docs/runtime/testing#alert_etc), the IndicatorRelease() function is not executed.

Example:

```
//+------------------------------------------------------------------+
//|                                        Test_IndicatorRelease.mq5 |
//|                        Copyright 2010, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2010, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- input parameters
input int                MA_Period=15;
input int                MA_shift=0;
input ENUM_MA_METHOD     MA_smooth=MODE_SMA;
input ENUM_APPLIED_PRICE price=PRICE_CLOSE;
//--- will store indicator handle
int MA_handle=INVALID_HANDLE;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create indicator handle
   MA_handle=iMA(Symbol(),0,MA_Period,MA_shift,MA_smooth,PRICE_CLOSE);
//--- delete global variable
   if(GlobalVariableCheck("MA_value"))
      GlobalVariableDel("MA_value");
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- if the global variable value does not exist
   if(!GlobalVariableCheck("MA_value"))
     {
      //--- obtain the indicator value in the last two bars
      if(MA_handle!=INVALID_HANDLE)
        {
         //--- dynamic array for the indicator values
         double values[];
         if(CopyBuffer(MA_handle,0,0,2,values)==2 && values[0]!=EMPTY_VALUE)
           {
            //--- remember in the global variable value on the last but one bar
            if(GlobalVariableSet("MA_value",values[0]))
              {
               //--- free the handle of the indicator
               if(!IndicatorRelease(MA_handle))
                  Print("IndicatorRelease() failed. Error ",GetLastError());
               else MA_handle=INVALID_HANDLE;
              }
            else
               Print("GlobalVariableSet failed. Error ",GetLastError());
           }
        }
     }
//---
  }

```
