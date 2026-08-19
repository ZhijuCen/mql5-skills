# ParameterSetRange

Specifies the use of [input variable](/en/docs/basis/variables/inputvariables) when optimizing an Expert Advisor in the Strategy Tester: value, change step, initial and final values. There are 2 variants of the function.

1. Specifying the values for the integer type input parameter

```
bool  ParameterSetRange(
   const string  name,          // parameter (input variable) name
   bool          enable,        // parameter optimization enabled
   long          value,         // parameter value
   long          start,         // initial value
   long          step,          // change step
   long          stop           // final value
   );

```

2. Specifying the values for the real type input parameter

```
bool  ParameterSetRange(
   const string  name,          // parameter (input variable) name
   bool          enable,        // parameter optimization enabled
   double        value,         // parameter value
   double        start,         // initial value
   double        step,          // change step
   double        stop           // final value
   );

```

Parameters

name

[in]  [input or sinput](/en/docs/basis/variables/inputvariables) variable ID. These variables are external parameters of an application. Their values can be specified when launching the program.

enable

[in]  Enable this parameter to enumerate the values during the optimization in the Strategy Tester.

value

[in]  Parameter value.

start

[in]  Initial parameter value during the optimization.

step

[in]  Parameter change step when enumerating its values.

stop

[in]  Final parameter value during the optimization.

Return Value

Returns true if successful, otherwise false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function can be called only from [OnTesterInit()](/en/docs/event_handlers/ontesterinit) handler when launching optimization from the Strategy Tester. It is designed for specifying the parameter's range and change step. The parameter can be completely excluded from optimization regardless of the Strategy Tester settings. It also allows using the variables declared with sinput modifier in the optimization process.

ParameterSetRange() function allows you to manage an Expert Advisor optimization in the Strategy Tester depending on its key parameters' values by including or excluding required input parameters from the optimization and setting the required range and the change step.
