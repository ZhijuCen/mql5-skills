# MathCeil

The function returns integer numeric value closest from above.

```
double  MathCeil(
   double  val      // number
   );

```

Parameters

val

[in]  Numeric value.

Return Value

Numeric value representing the smallest integer that exceeds or equals to val.

Note

Instead of the MathCeil() function you can use ceil().

Example:

```
#define VALUES_TOTAL 31
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare variables for conversion
   double value=0;                     // real number for MathCeil conversion
   int    ceil_value=0;                // get the result here
//--- in a loop by the number of decimal increments of a real number
   for(int i=0; i<VALUES_TOTAL; i++)
     {
      //--- increase the number value,
      //--- get the nearest integer value from above
      //--- and display control values in the journal
      value+=0.1;
      ceil_value=(int)MathCeil(NormalizeDouble(value,1));
      PrintFormat("value: %.1f, ceil value: %d",value,ceil_value);
      /*
      result:
      value: 0.1, ceil value: 1
      value: 0.2, ceil value: 1
      value: 0.3, ceil value: 1
      value: 0.4, ceil value: 1
      value: 0.5, ceil value: 1
      value: 0.6, ceil value: 1
      value: 0.7, ceil value: 1
      value: 0.8, ceil value: 1
      value: 0.9, ceil value: 1
      value: 1.0, ceil value: 1
      value: 1.1, ceil value: 2
      value: 1.2, ceil value: 2
      value: 1.3, ceil value: 2
      value: 1.4, ceil value: 2
      value: 1.5, ceil value: 2
      value: 1.6, ceil value: 2
      value: 1.7, ceil value: 2
      value: 1.8, ceil value: 2
      value: 1.9, ceil value: 2
      value: 2.0, ceil value: 2
      value: 2.1, ceil value: 3
      value: 2.2, ceil value: 3
      value: 2.3, ceil value: 3
      value: 2.4, ceil value: 3
      value: 2.5, ceil value: 3
      value: 2.6, ceil value: 3
      value: 2.7, ceil value: 3
      value: 2.8, ceil value: 3
      value: 2.9, ceil value: 3
      value: 3.0, ceil value: 3
      value: 3.1, ceil value: 4
      */
     }
  }

```
