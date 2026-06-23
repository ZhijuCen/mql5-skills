# MathAbs

The function returns the absolute value (modulus) of the specified numeric value.

```
double  MathAbs(
   double  value      // numeric value
   );

```

Parameters

value

[in]  Numeric value.

Return Value

Value of double type more than or equal to zero.

Note

Instead the MathAbs() function you can use fabs().

Example:

```
//--- input parameters
input int      InpValue = -10;   // Enter any value here
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the absolute value of the number entered in the inputs
   uint abs_value=MathAbs(InpValue);
//--- print the values in the journal
   PrintFormat("The entered value %d received the value %u after using the MathAbs() function",InpValue,abs_value);
  }

```
