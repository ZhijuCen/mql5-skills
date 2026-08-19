# ChartWindowFind

The function returns the number of a subwindow where an indicator is drawn. There are 2 variants of the function.

1. The function searches in the indicated chart for the subwindow with the specified "short name" of the indicator (the short name is displayed in the left top part of the subwindow), and it returns the subwindow number in case of success.

```
int  ChartWindowFind(
   long     chart_id,                  // chart identifier
   string   indicator_shortname        // short indicator name, see INDICATOR_SHORTNAME

```

2. The function must be called from a custom indicator. It returns the number of the subwindow where the indicator is working.

```
int  ChartWindowFind();

```

Parameters

chart_id

[in]  Chart ID. 0 denotes the current chart.

indicator_shortname

[in]  Short name of the indicator.

Return Value

Subwindow number in case of success. In case of failure the function returns -1.

Note

If the second variant of the function (without parameters) is called from a script or Expert Advisor, the function returns -1.

Don't mix up the short name of an indicator and a file name, which is specified when an indicator is created using [iCustom()](/en/docs/indicators/icustom) and [IndicatorCreate()](/en/docs/series/indicatorcreate) functions. If the indicator's short name is not set explicitly, then the name of the file containing the source code of the indicator, is specified in it during compilation.

It is important to correctly form the short name of an indicator, which is recorded in the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property using the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. It is recommended that the short name contains values of the indicator's input parameters, because the indicator deleted from a chart in the [ChartIndicatorDelete()](/en/docs/chart_operations/chartindicatordelete) function is identified by its short name.

Example:

```
#property script_show_inputs
//--- input parameters
input string   shortname="MACD(12,26,9)";
//+------------------------------------------------------------------+
//| Returns number of the chart window with this indicator           |
//+------------------------------------------------------------------+
int GetIndicatorSubWindowNumber(long chartID=0,string short_name="")
  {
   int window=-1;
//--- 
   if((ENUM_PROGRAM_TYPE)MQL5InfoInteger(MQL5_PROGRAM_TYPE)==PROGRAM_INDICATOR)
     {
      //--- the function is called from the indicator, name is not required
      window=ChartWindowFind();
     }
   else
     {
      //--- the function is called from an Expert Advisor or script
      window=ChartWindowFind(0,short_name);
      if(window==-1) Print(__FUNCTION__+"(): Error = ",GetLastError());
     }
//---
   return(window);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int window=GetIndicatorSubWindowNumber(0,shortname);
   if(window!=-1)
      Print("Indicator "+shortname+" is in the window #"+(string)window);
   else
      Print("Indicator "+shortname+" is not found. window = "+(string)window);
  }

```

See also

[ObjectCreate()](/en/docs/objects/objectcreate), [ObjectFind()](/en/docs/objects/objectfind)
