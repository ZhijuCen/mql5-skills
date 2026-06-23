# ParameterGetRange

Receives data on the values range and the change step for an [input variable](/en/docs/basis/variables/inputvariables) when optimizing an Expert Advisor in the Strategy Tester. There are 2 variants of the function.

1. Receiving data for the integer type input parameter

```
bool  ParameterGetRange(
   const string  name,          // parameter (input variable) name
   bool&         enable,        // parameter optimization enabled
   long&         value,         // parameter value
   long&         start,         // initial value
   long&         step,          // change step
   long&         stop           // final value
   );

```

2. Receiving data for the real type input parameter

```
bool  ParameterGetRange(
   const string  name,          // parameter (input variable) name
   bool&         enable,        // parameter optimization enabled
   double&       value,         // parameter value
   double&       start,         // initial value
   double&       step,          // change step
   double&       stop           // final value
   );

```

Parameters

name

[in]  [input variable](/en/docs/basis/variables/inputvariables) ID. These variables are external parameters of an application. Their values can be specified when launching on a chart or during a single test.

enable

[out]  Flag that this parameter can be used to enumerate the values during the optimization in the Strategy Tester.

value

[out]  Parameter value.

start

[out]  Initial parameter value during the optimization.

step

[out]  Parameter change step when enumerating its values.

stop

[out]  Final parameter value during the optimization.

Return Value

Returns true if successful, otherwise false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function can be called only from [OnTesterInit()](/en/docs/event_handlers/ontesterinit), [OnTesterPass()](/en/docs/event_handlers/ontesterpass) and [OnTesterDeinit()](/en/docs/event_handlers/ontesterdeinit) handlers. It has been introduced to receive Expert Advisor input parameters' values and variation ranges during the optimization in the Strategy Tester.

When called in OnTesterInit(), the obtained data can be used to redefine the rules for enumeration of any [input variable](/en/docs/basis/variables/inputvariables) using [ParameterSetRange()](/en/docs/optimization_frames/parametersetrange) function. Therefore, new Start, Stop and Step values can be set and the input parameter can even be completely excluded from optimization regardless of the Strategy Tester settings. This allows you to manage the area of the input parameters during the optimization by excluding some parameters from the optimization depending on the Expert Advisor's key parameters' values.

Example:

```
#property description "Expert Advisor for ParameterGetRange() function demonstration."
#property description "Should be launched in the optimization mode of the Strategy Tester"
//--- input parameters
input int                 Input1=1;
input double              Input2=2.0;
input bool                Input3=false;
input ENUM_DAY_OF_WEEK    Input4=SUNDAY;
 
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- Expert Advisor is designed for operation only in the Strategy Tester
   if(!MQL5InfoInteger(MQL5_OPTIMIZATION))
     {
      MessageBox("Should be launched in the optimization mode of the Strategy Tester!");
      //--- finish the Expert Advisor operation in advance and remove from the chart
      return(INIT_FAILED);
     }
//--- successful completion of initialization
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| TesterInit function                                              |
//+------------------------------------------------------------------+
void OnTesterInit()
  {
//--- example for long type input parameter
   string name="Input1";
   bool enable;
   long par1,par1_start,par1_step,par1_stop;
   ParameterGetRange(name,enable,par1,par1_start,par1_step,par1_stop);
   Print("First parameter");
   PrintFormat("%s=%d  enable=%s  from %d to %d with step=%d",
               name,par1,(string)enable,par1_start,par1_stop,par1_step);
//--- example for double type input parameter
   name="Input2";
   double par2,par2_start,par2_step,par2_stop;
   ParameterGetRange(name,enable,par2,par2_start,par2_step,par2_stop);
   Print("Second parameter");
   PrintFormat("%s=%G  enable=%s  from %G to %G with step=%G",
               name,par2,(string)enable,par2_start,par2_stop,par2_step);
 
//--- example for bool type input parameter
   name="Input3";
   long par3,par3_start,par3_step,par3_stop;
   ParameterGetRange(name,enable,par3,par3_start,par3_step,par3_stop);
   Print("Third parameter");
   PrintFormat("%s=%s  enable=%s  from %s to %s",
               name,(string)par3,(string)enable,
               (string)par3_start,(string)par3_stop);
//--- example for enumeration type input parameter
   name="Input4";
   long par4,par4_start,par4_step,par4_stop;
   ParameterGetRange(name,enable,par4,par4_start,par4_step,par4_stop);
   Print("Fourth parameter");
   PrintFormat("%s=%s  enable=%s  from %s to %s",
               name,EnumToString((ENUM_DAY_OF_WEEK)par4),(string)enable,
               EnumToString((ENUM_DAY_OF_WEEK)par4_start),
               EnumToString((ENUM_DAY_OF_WEEK)par4_stop));
  }
//+------------------------------------------------------------------+
//| TesterDeinit function                                            |
//+------------------------------------------------------------------+
void OnTesterDeinit()
  {
//--- this message will be shown after optimization is complete
   Print(__FUNCTION__," Optimization completed");
  }

```
