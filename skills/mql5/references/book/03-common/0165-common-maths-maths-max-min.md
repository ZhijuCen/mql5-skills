# Maximum and minimum of two numbers

To find the largest or smallest number out of two, MQL5 offers functions MathMax and MathMin. Their short aliases are respectively fmax and fmin.

numeric MathMax(numeric value1, numeric value2) ≡ numeric fmax(numeric value1, numeric value2)

numeric MathMin(numeric value1, numeric value2) ≡ numeric fmin(numeric value1, numeric value2)

The functions return the maximum or minimum of the two values passed. The functions are overloaded for all built-in types.

If parameters of different types are passed to the function, then the parameter of the "lower" type is automatically converted to the "higher" type, for example, in a pair of types int and double, int will be brought to double. For more information on implicit type casting, see section [Arithmetic type conversions](/en/book/basis/conversion/conversion_arithmetic). The return type corresponds to the "highest" type.

When there is a parameter of type string, it will be "senior", that is, everything is reduced to a string. Strings will be compared lexicographically, as in the [StringCompare](/en/book/common/strings/strings_comparison) function.

The MathMaxMin.mq5 script demonstrates the functions in action.

```
void OnStart()
{
   int i = 10, j = 11;
   double x = 5.5, y = -5.5;
   string s = "abc";
   
   // numbers   
   PRT(MathMax(i, j)); // 11
   PRT(MathMax(i, x)); // 10
   PRT(MathMax(x, y)); // 5.5
   PRT(MathMax(i, s)); // abc
   
   // type conversions
   PRT(typename(MathMax(i, j))); // int, as is
   PRT(typename(MathMax(i, x))); // double
   PRT(typename(MathMax(i, s))); // string
}

```
