# MathMod

The function returns the real remainder of division of two numbers.

```
double  MathMod(
   double  value,      // dividend value
   double  value2      // divisor value
   );

```

Parameters

value

[in]  Dividend value.

value2

[in]  Divisor value.

Return Value

The MathMod function calculates the real remainder f from expression val/y so that val = i * y + f , where i is an integer, f has the same sign as val, and the absolute value of f is less than the absolute value of y.

Note

Instead of MathMod() you can use fmod().

Example:

```
#property script_show_inputs
 
//--- input parameters
input double   InpDividentValue  =  10;   // Dividend value
input double   InpDivisorValue   =  3;    // Divisor value
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the real remainder of the division of the numbers entered in the inputs
   double res=MathMod(InpDividentValue,InpDivisorValue);
//--- print the result in the journal
   PrintFormat("Real remainder when dividing %.2f by %.2f = %.2f",InpDividentValue,InpDivisorValue,res);
  }

```
