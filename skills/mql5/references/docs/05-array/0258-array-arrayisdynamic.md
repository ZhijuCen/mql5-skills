# ArrayIsDynamic

The function checks whether an array is dynamic.

```
bool  ArrayIsDynamic(
   const void&  array[]    // checked array
   );

```

Parameters

array[]

[in]  Checked array.

Return Value

It returns true if the selected array is [dynamic](/en/docs/basis/types/dynamic_array), otherwise it returns false.

Example:

```
#property description "This indicator does not calculate values. It makes a single attempt to"
#property description "apply the call of ArrayFree() function to three arrays: dynamic one, static one and"
#property description "an indicator buffer. Results are shown in Experts journal."
//--- indicator settings
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
//--- global variables
double ExtDynamic[];   // dynamic array
double ExtStatic[100]; // static array
bool   ExtFlag=true;   // flag
double ExtBuff[];      // indicator buffer
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- allocate memory for the array
   ArrayResize(ExtDynamic,100);
//--- indicator buffers mapping
   SetIndexBuffer(0,ExtBuff);
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0);
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const int begin,
                const double &price[])
  {
//--- perform a single analysis
   if(ExtFlag)
     {
      //--- attempt to free memory for arrays
      //--- 1. Dynamic array
      Print("+============================+");
      Print("1. Check dynamic array:");
      Print("Size before memory is freed = ",ArraySize(ExtDynamic));
      Print("Is this a dynamic array = ",ArrayIsDynamic(ExtDynamic) ? "Yes" : "No");
      //--- attempt to free array memory
      ArrayFree(ExtDynamic);
      Print("Size after memory is freed = ",ArraySize(ExtDynamic));
      //--- 2. Static array
      Print("2. Check static array:");
      Print("Size before memory is freed = ",ArraySize(ExtStatic));
      Print("Is this a dynamic array = ",ArrayIsDynamic(ExtStatic) ? "Yes" : "No");
      //--- attempt to free array memory
      ArrayFree(ExtStatic);
      Print("Size after memory is freed = ",ArraySize(ExtStatic));
      //--- 3. Indicator buffer
      Print("3. Check indicator buffer:");
      Print("Size before memory is freed = ",ArraySize(ExtBuff));
      Print("Is this a dynamic array = ",ArrayIsDynamic(ExtBuff) ? "Yes" : "No");
      //--- attempt to free array memory
      ArrayFree(ExtBuff);
      Print("Size after memory is freed = ",ArraySize(ExtBuff));
      //--- change the flag value
      ExtFlag=false;
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```

See also

[Access to timeseries and indicators](/en/docs/series)
