# MathMin

The function returns the minimal value of two values.

```
double  MathMin(
   double  value1,     // first value
   double  value2      // second value
   );

```

Parameters

value1

[in]  First numeric value.

value2

[in]  Second numeric value.

Return Value

The smallest of the two values.

Note

Instead of MathMin() you can use fmin(). Functions fmax(), [fmin()](/en/docs/math/mathmin), [MathMax](/en/docs/math/mathmax)(), [MathMin()](/en/docs/math/mathmin) can work with integer types without typecasting them to the type of double.

If parameters of different types are passed into a function, the parameter of the smaller type is automatically [cast](/en/docs/basis/types/casting) to the larger type. The type of the return value corresponds to the larger type.

If data of the same type are passed, no casting is performed.

Example:

```
//--- input parameters
input uint  InpBars  =  100000;  // Desired number of bars
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the number of available bars on the server
   uint bars_total = Bars(Symbol(),Period());
   if(bars_total==0)
     {
      PrintFormat("Data for timeseries %s %s not yet generated in the terminal. Please try again later.",Symbol(),StringSubstr(EnumToString(Period()),7));
      return;
     }
//--- get the minimum number of bars from two values - from those available on the server and from the requested number in the settings
   int bars = (int)MathMin(bars_total,InpBars);
//--- if more bars are requested than are available on the server, report this in the journal
   if(bars_total<InpBars)
      PrintFormat("Number of bars on the server (%u) is less than requested (%u)",bars_total,InpBars);
//--- display the number of bars available for work in the journal
   Print("Bars available for work: ",bars);
  }

```
