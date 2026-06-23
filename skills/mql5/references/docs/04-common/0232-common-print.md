# Print

It enters a message in the Expert Advisor log. Parameters can be of any type.

```
void  Print(
   argument,     // first value
   ...           // next values
   );

```

Parameters

...

[in]  Any values separated by commas. The number of parameters cannot exceed 64.

Note

Arrays cannot be passed to the Print() function. Arrays must be input element-by-element.

Data of double type are shown with the accuracy of up to  16 digits after a decimal point, and can be output either in traditional or in scientific format, depending on what entry will be more compact. Data of float type are output with 5 digits after a decimal point. To output real numbers with another accuracy or in a predefined format, use the [PrintFormat()](/en/docs/common/printformat) function.

Data of bool type are output as "true" or "false" lines. Dates are shown as YYYY.MM.DD HH:MI:SS. To show data in another format, use [TimeToString()](/en/docs/convert/timetostring). Data of color type are returned either as R,G,B line or as a color name, if this color is present in the color set.

Print() function does not work during optimization in the [Strategy Tester](/en/docs/runtime/testing#print).

Example:

```
void OnStart()
  {
//--- Output DBL_MAX using Print(), this is equivalent to PrintFormat(%%.16G,DBL_MAX)
   Print("---- how DBL_MAX looks like -----");
   Print("Print(DBL_MAX)=",DBL_MAX);
//--- Now output a DBL_MAX number using PrintFormat()
   PrintFormat("PrintFormat(%%.16G,DBL_MAX)=%.16G",DBL_MAX);
//--- Output to the Experts journal
// Print(DBL_MAX)=1.797693134862316e+308
// PrintFormat(%.16G,DBL_MAX)=1.797693134862316E+308
 
//--- See how float is output
   float c=(float)M_PI; // We should explicitly cast to the target type
   Print("c=",c, "    Pi=",M_PI, "    (float)M_PI=",(float)M_PI);
// c=3.14159    Pi=3.141592653589793    (float)M_PI=3.14159
   
//--- Show what can happen with arithmetic operations with real types
   double a=7,b=200;
   Print("---- Before arithmetic operations");
   Print("a=",a,"   b=",b);
   Print("Print(DoubleToString(b,16))=",DoubleToString(b,16));
//--- Divide a by b (7/200)
   a=a/b;
//--- Now emulate restoring a value in the b variable
   b=7.0/a; // It is expected that b=7.0/(7.0/200.0)=>7.0/7.0*200.0=200 - but it differs
//--- Output the newly calculated value of b
   Print("----- After arithmetic operations");
   Print("Print(b)=",b);
   Print("Print(DoubleToString(b,16))=",DoubleToString(b,16));
//--- Output to the Experts journal
// Print(b)=200.0
// Print(DoubleToString(b,16))=199.9999999999999716 (see that b is no more equal to 200.0)   
 
//--- Create a very small value epsilon=1E-013
   double epsilon=1e-13;
   Print("---- Create a very small value");
   Print("epsilon=",epsilon); // Get epsilon=1E-013
//--- Now subtract epsilon from b and again output the value to the Experts journal
   b=b-epsilon;
//--- Use two ways
   Print("---- After subtracting epsilon from the b variable");
   Print("Print(b)=",b);
   Print("Print(DoubleToString(b,16))=",DoubleToString(b,16));
//--- Output to the Experts journal
// Print(b)=199.9999999999999  (now the value of b after subtracting epsilon cannot be rounded to 200)
// Print(DoubleToString(b,16))=199.9999999999998578
//    (now the value of b after subtracting epsilon cannot be rounded to 200)
  }

```

See also

[DoubleToString](/en/docs/convert/doubletostring), [StringFormat](/en/docs/convert/stringformat)
