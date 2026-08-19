# IndicatorParameters

Based on the specified handle, returns the number of input parameters of the indicator, as well as the values and types of the parameters.

```
int  IndicatorParameters(
   int               indicator_handle,     // indicator handle
   ENUM_INDICATOR&   indicator_type,       // a variable for receiving the indicator type
   MqlParam&         parameters[]          // an array for receiving parameters
   );

```

Parameters

indicator_handle

[in]  The handle of the indicator, for which you need to know the number of parameters its is calculated on.

indicator_type

[out]  A variable if the [ENUM_INDICATOR](/en/docs/constants/indicatorconstants/enum_indicator) type, into which the indicator type will be written.

parameters[]

[out]  A dynamic array for receiving values of the [MqlParam](/en/docs/constants/structures/mqlparam) type, into which the list of indicator parameters will be written. The array size is returned by the IndicatorParameters() function.

Return Value

The number of input parameters of the indicator with the specified handle. In case of an error returns -1. For more details about the error call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
 
//--- The number of windows on the chart (at least one main window is always present)
   int windows=(int)ChartGetInteger(0,CHART_WINDOWS_TOTAL);
//--- Go through the chart windows
   for(int w=0;w<windows;w++)
     {
      //--- The number of indicators in this window/subwindow
      int total=ChartIndicatorsTotal(0,w);
      //--- Take all indicators in the window
      for(int i=0;i<total;i++)
        {
         //--- Get the short name of the indicator
         string name=ChartIndicatorName(0,w,i);
         //--- Get the indicator handle
         int handle=ChartIndicatorGet(0,w,name);
         //--- Add to log
         PrintFormat("Window=%d,  indicator #%d,  handle=%d",w,i,handle);
         //---
         MqlParam parameters[];
         ENUM_INDICATOR indicator_type;
         int params=IndicatorParameters(handle,indicator_type,parameters);
         //--- The header of the message
         string par_info="Short name "+name+", type "
                         +EnumToString(ENUM_INDICATOR(indicator_type))+"\r\n";
         //--- 
         for(int p=0;p<params;p++)
           {
            par_info+=StringFormat("parameter %d: type=%s, long_value=%d, double_value=%G,string_value=%s\r\n",
                                   p,
                                   EnumToString((ENUM_DATATYPE)parameters[p].type),
                                   parameters[p].integer_value,
                                   parameters[p].double_value,
                                   parameters[p].string_value
                                   );
           }
         Print(par_info);
        }
      //--- Done for all indicators in the window
     }
//---    
  }

```

See also

[ChartIndicatorGet()](/en/docs/chart_operations/chartindicatorget)
