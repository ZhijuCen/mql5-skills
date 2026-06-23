# Getting indicator settings by its handle

Sometimes an MQL program needs to know the parameters of a running indicator instance. These can be third-party indicators on the chart, or a handle passed from the main program to [library](/en/book/advanced/libraries) or header file. For this purpose, MQL5 provides the IndicatorParameters function.

int IndicatorParameters(int handle, ENUM_INDICATOR &type, MqlParam &params[])

By the specified handle, the function returns the number of indicator input parameters, as well as their types and values.

On success, the function populates the params array passed to it, and the indicator type is saved in the type parameter.

In case of an error, the function returns -1.

As an example of working with this function, let's improve the indicator UseDemoAllLoop.mq5 presented in the section on [Deleting indicator instances](/en/book/applications/indicators_use/indicators_indicatorrelease). Let's call the new version UseDemoAllParams.mq5.

As you remember, we sequentially created some built-in indicators in the loop in the list and left the list of parameters empty, which leads to the fact that the indicators use some unknown default values. In this regard, we displayed a generalized prototype in a comment on the chart: with a name, but without specific values.

```
// UseDemoAllLoop.mq5
void OnTimer()
{
   ...
   Comment("DemoAll: ", (IndicatorSelector == iCustom_ ? IndicatorCustom : s),
      "(default-params)");
   ...
}

```

Now we have the opportunity to find out its parameters based on the indicator handle and display them to the user.

```
// UseDemoAllParams.mq5
void OnTimer()
{
   ...   
   // read the parameters applied by the indicator by default
   ENUM_INDICATOR itype;
   MqlParam defParams[];
   const int p = IndicatorParameters(Handle, itype, defParams);
   ArrayPrint(defParams);
   Comment("DemoAll: ", (IndicatorSelector == iCustom_ ? IndicatorCustom : s),
      "(" + MqlParamStringer::stringify(defParams) + ")");
   ...
}

```

Conversion of the MqlParam array into a string is implemented in the special class MqlParamStringer (see file MqlParamStringer.mqh).

```
class MqlParamStringer
{
public:
   static string stringify(const MqlParam &param)
   {
      switch(param.type)
      {
      case TYPE_BOOL:
      case TYPE_CHAR:
      case TYPE_UCHAR:
      case TYPE_SHORT:
      case TYPE_USHORT:
      case TYPE_DATETIME:
      case TYPE_COLOR:
      case TYPE_INT:
      case TYPE_UINT:
      case TYPE_LONG:
      case TYPE_ULONG:
         return IntegerToString(param.integer_value);
      case TYPE_FLOAT:
      case TYPE_DOUBLE:
         return (string)(float)param.double_value;
      case TYPE_STRING:
         return param.string_value;
      }
      return NULL;
   }
   
   static string stringify(const MqlParam &params[])
   {
      string result = "";
      const int p = ArraySize(params);
      for(int i = 0; i < p; ++i)
      {
         result += stringify(params[i]) + (i < p - 1 ? "," : "");
      }
      return result;
   }
};

```

After compiling and running the new indicator, you can make sure that the specific list of parameters of the indicator being rendered is now displayed in the upper left corner of the chart.

For a single custom indicator from the list (LifeCycle), the first parameter will contain the path and file name of the indicator. The second parameter is described in the source code as an integer. But the third parameter is interesting because it implicitly describes the 'Apply to' property, which is inherent in all indicators with a short form of the OnCalculate handler. In this case, by default, the indicator is applied to PRICE_CLOSE (value 1).

```
Initializing LifeCycle() EURUSD, PERIOD_H1
Handle=10
    [type] [integer_value] [double_value] [string_value]
[0]     14               0        0.00000 "Indicators\MQL5Book\p5\LifeCycle.ex5"
[1]      7               0        0.00000 null
[2]      7               1        0.00000 null
Initializing iAlligator_jawP_jawS_teethP_teethS_lipsP_lipsS_method_price() EURUSD, PERIOD_H1
iAlligator_jawP_jawS_teethP_teethS_lipsP_lipsS_method_price requires 8 parameters, 0 given
Handle=10
    [type] [integer_value] [double_value] [string_value]
[0]      7              13        0.00000 null          
[1]      7               8        0.00000 null          
[2]      7               8        0.00000 null          
[3]      7               5        0.00000 null          
[4]      7               5        0.00000 null          
[5]      7               3        0.00000 null          
[6]      7               2        0.00000 null          
[7]      7               5        0.00000 null          
Initializing iAMA_period_fast_slow_shift_price() EURUSD, PERIOD_H1
iAMA_period_fast_slow_shift_price requires 5 parameters, 0 given
Handle=10
    [type] [integer_value] [double_value] [string_value]
[0]      7               9        0.00000 null          
[1]      7               2        0.00000 null          
[2]      7              30        0.00000 null          
[3]      7               0        0.00000 null          
[4]      7               1        0.00000 null          
 

```

According to the log, the settings of the built-in indicators also correspond to the defaults.
