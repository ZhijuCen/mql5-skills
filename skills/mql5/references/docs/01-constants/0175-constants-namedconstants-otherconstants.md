# Other Constants

The CLR_NONE constant is used to outline the absence of color, it means that the [graphical object](/en/docs/objects) or [graphical series](/en/docs/constants/indicatorconstants/drawstyles) of an indicator will not be plotted. This constant was not included into the [Web-color](/en/docs/constants/objectconstants/webcolors) constants list, but it can be applied everywhere where the color arguments are required.

The INVALID_HANDLE constant can be used for checking file handles (see [FileOpen()](/en/docs/files/fileopen) and [FileFindFirst()](/en/docs/files/filefindfirst)).

| Constant | Description | Value |
| --- | --- | --- |
| CHARTS_MAX | The maximum possible number of simultaneously open charts in the terminal | 100 |
| clrNONE | Absence of color | -1 |
| EMPTY_VALUE | Empty value in an indicator buffer | DBL_MAX |
| INVALID_HANDLE | Incorrect handle | -1 |
| IS_DEBUG_MODE | Flag that a mq5-program operates in debug mode | non zero in debug mode, otherwise zero |
| IS_PROFILE_MODE | Flag that a mq5-program operates in profiling mode | non zero in profiling mode, otherwise zero |
| NULL | Zero for any types | 0 |
| WHOLE_ARRAY | Means the number of items remaining until the end of the array, i.e., the entire array will be processed | -1 |
| WRONG_VALUE | The constant can be implicitly  cast  to any  enumeration  type | -1 |

The EMPTY_VALUE constant usually corresponds to the values of indicators that are not shown in the chart. For example, for built-in indicator Standard Deviation with a period of 20, the line for the first 19 bars in the history  is not shown in the chart. If you create a handle of this indicator with the [iStdDev()](/en/docs/indicators/istddev) function and copy it to an array of indicator values for these bars through [CopyBuffer()](/en/docs/series/copybuffer), then these values will be equal to EMPTY_VALUE.

You can choose to specify for [a custom indicator](/en/docs/customind) your own empty value of the indicator, when the indicator shouldn't be drawn in the chart. Use the [PlotIndexSetDouble()](/en/docs/customind/plotindexsetdouble) function with the [PLOT_EMPTY_VALUE](/en/docs/constants/indicatorconstants/drawstyles#enum_plot_property_double) modifier.

The [NULL](/en/docs/basis/types/void) constant can be assigned to a variable of any simple type or to an object structure or class pointer. The NULL assignment for a string variable means the full deinitialization of this variable.

The WRONG_VALUE constant is intended for cases, when it is necessary to return value of an [enumeration](/en/docs/basis/types/integer/enumeration), and this must be a wrong value. For example, when we need to inform that a return value is a value from this enumeration. Let's consider as an example some function CheckLineStyle(), which returns the line style for an object, specified by its name. If at style check by ObjectGetInteger() the result is true, a value from [ENUM_LINE_STYLE](/en/docs/constants/indicatorconstants/drawstyles#enum_line_style) is returned; otherwise WRONG_VALUE is returned.

```
void OnStart()
  {
   if(CheckLineStyle("MyChartObject")==WRONG_VALUE)
      printf("Error line style getting.");
  }
//+------------------------------------------------------------------+
//| returns the line style for an object specified by its name       |
//+------------------------------------------------------------------+
ENUM_LINE_STYLE CheckLineStyle(string name)
  {
   long style;
//---
   if(ObjectGetInteger(0,name,OBJPROP_STYLE,0,style))
      return((ENUM_LINE_STYLE)style);
   else
      return(WRONG_VALUE);
  }

```

The WHOLE_ARRAY constant is intended for functions that require specifying the number of elements in processed arrays:

- [ArrayCopy()](/en/docs/array/arraycopy);
- [ArrayMinimum()](/en/docs/array/arrayminimum);
- [ArrayMaximum()](/en/docs/array/arraymaximum);
- [FileReadArray()](/en/docs/files/filereadarray);
- [FileWriteArray()](/en/docs/files/filewritearray).

If you want to specify that all the array values from a specified position till the end must be processed, you should specify just the WHOLE_ARRAY value.

IS_PROFILE_MODE constant  allows changing a program operation for correct data collection in the profiling mode. Profiling allows measuring the execution time of the individual program fragments (usually comprising functions), as well as calculating the number of such calls. Sleep() function calls can be disabled to determine the execution time in the profiling mode, like in this example:

```
//--- Sleep can greatly affect (change) profiling result
if(!IS_PROFILE_MODE) Sleep(100); // disabling Sleep() call in the profiling mode

```

IS_PROFILE_MODE constant value is set by the compiler during the compilation, while it is set to zero in conventional mode. When launching a program in the profiling mode, a special compilation is performed and IS_PROFILE_MODE is replaced with a non-zero value.

The IS_DEBUG_MODE constant can be useful when you need to slightly change the operation of a mql5 program in the debugging mode. For example, in debug mode you may need to display additional debugging information in the terminal log or create additional graphical objects in a chart.

The following example creates a Label object and sets its description and color depending on the script running mode. In order to run a script in the debug mode from MetaEditor, press F5. If you run the script from the browser window in the terminal, then the color and text of the object Label will be different.

Example:

```
//+------------------------------------------------------------------+
//|                                             Check_DEBUG_MODE.mq5 |
//|                      Copyright © 2009, MetaQuotes Software Corp. |
//|                                        https://www.metaquotes.net |
//+------------------------------------------------------------------+
#property copyright "Copyright © 2009, MetaQuotes Software Corp."
#property link      "https://www.metaquotes.net"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   string label_name="invisible_label";
   if(ObjectFind(0,label_name)<0)
     {
      Print("Object",label_name,"not found. Error code = ",GetLastError());
      //--- create Label
      ObjectCreate(0,label_name,OBJ_LABEL,0,0,0);
      //--- set X coordinate
      ObjectSetInteger(0,label_name,OBJPROP_XDISTANCE,200);
      //--- set Y coordinate
      ObjectSetInteger(0,label_name,OBJPROP_YDISTANCE,300);
      ResetLastError();
      if(IS_DEBUG_MODE) // debug mode
        {
         //--- show message about the script execution mode
         ObjectSetString(0,label_name,OBJPROP_TEXT,"DEBUG MODE");
         //--- set text color to red
         if(!ObjectSetInteger(0,label_name,OBJPROP_COLOR,clrRed))
            Print("Unable to set the color. Error",GetLastError());
        }
      else              // operation mode
        {
         ObjectSetString(0,label_name,OBJPROP_TEXT,"RELEASE MODE");
         //--- set text color to invisible
         if(!ObjectSetInteger(0,label_name,OBJPROP_COLOR,CLR_NONE))
            Print("Unable to set the color. Error ",GetLastError());
        }
      ChartRedraw();
      DebugBreak();    // here termination will occur, if we are in debug mode
     }
  }

```

# Crypt Methods

The ENUM_CRYPT_METHOD enumeration is used to specify the data transformation method, used in  [CryptEncode()](/en/docs/common/cryptencode) and [CryptDecode()](/en/docs/common/cryptdecode) functions.

ENUM_CRYPT_METHOD

| Constant | Description |
| --- | --- |
| CRYPT_BASE64 | BASE64 |
| CRYPT_AES128 | AES encryption with 128 bit key (16 bytes) |
| CRYPT_AES256 | AES encryption with 256 bit key (32 bytes) |
| CRYPT_DES | DES encryption with 56 bit key (7 bytes) |
| CRYPT_HASH_SHA1 | SHA1 HASH calculation |
| CRYPT_HASH_SHA256 | SHA256 HASH calculation |
| CRYPT_HASH_MD5 | MD5 HASH calculation |
| CRYPT_ARCH_ZIP | ZIP archives |

See also

[DebugBreak](/en/docs/common/debugbreak), [Executed MQL5 program properties](/en/docs/constants/environment_state/mql5_programm_info), [CryptEncode()](/en/docs/common/cryptencode), [CryptDecode()](/en/docs/common/cryptdecode)
