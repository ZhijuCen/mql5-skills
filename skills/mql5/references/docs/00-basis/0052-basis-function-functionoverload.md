# Function Overloading

Usually the function name tends to reflect its main purpose. As a rule, readable programs contain various well selected [identifiers](/en/docs/basis/syntax/identifiers). Sometimes different functions are used for the same purposes. Let's consider, for example, a function that calculates the average value of an array of double precision numbers and the same function, but operating with an array of integers. Both are convenient to be called AverageFromArray:

```
//+------------------------------------------------------------------+
//| The calculation of average for an array of double type           |
//+------------------------------------------------------------------+
double AverageFromArray(const double & array[],int size)
  {
   if(size<=0) return 0.0;
   double sum=0.0;
   double aver;
//---
   for(int i=0;i<size;i++)
     {
      sum+=array[i];    // Summation for the double
     }
   aver=sum/size;       // Just divide the sum by the number
//---
   Print("Calculation of the average for an array of double type");
   return aver;
  }
//+------------------------------------------------------------------+
//| The calculation of average for an array of int type              |
//+------------------------------------------------------------------+
double AverageFromArray(const int & array[],int size)
  {
   if(size<=0) return 0.0;
   double aver=0.0;
   int sum=0;
//---
   for(int i=0;i<size;i++)
     {
      sum+=array[i];     // Summation for the int
     }
   aver=(double)sum/size;// Give the amount of type double, and divide
//---
   Print("Calculation of the average for an array of int type");
   return aver;
  }

```

Each function contains the message output via the [Print()](/en/docs/common/print) function;

```
   Print("Calculation of the average for an array of int type");

```

The compiler selects a necessary function in accordance with the types of arguments and their quantity. The rule, according to which the choice is made, is called the signature matching algorithm. A signature is a list of types used in the function declaration.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int    a[5]={1,2,3,4,5};
   double b[5]={1.1,2.2,3.3,4.4,5.5};
   double int_aver=AverageFromArray(a,5);
   double double_aver=AverageFromArray(b,5);
   Print("int_aver = ",int_aver,"   double_aver = ",double_aver);
  }
//--- Result of the script
// Calculate the average for an array of int type
// Calculate the average for an array of double type
// int_aver= 3.00000000    double_aver= 3.30000000

```

Function overloading is a process of creating several functions with the same name, but different parameters. This means that in overloaded variants of a function, the number of arguments and/or their type must be different. A specific function variant is selected based on the correspondence of the list of arguments when calling the function, to the list of parameters in the function declaration.

When an overloaded function is called, the compiler must have an algorithm to select the appropriate function. The algorithm that performs this choice depends on [castings](/en/docs/basis/types/casting) of what types are present. The best correspondence must be unique. An overloaded function must be the best match among all the other variants for at least one argument. At the same time it must match for all other arguments not worse than other variants.

Below is a matching algorithm for each argument.

## Algorithm of Choosing an Overloaded Function

1. Use strict matching (if possible).
2. Try standard type increase.
3. Try standard typecasting.

The standard type increase is better than other standard conversions. Increase is the conversion of float to double, of bool, char, short or enum to int. Typecasting of arrays of similar [integer types](/en/docs/basis/types/integer) also belongs to typecasting. Similar types are: bool, char, uchar, since all the three types are single-byte integers; double-byte integers short and ushort; 4-byte integers int, uint, and color; long, ulong, and datetime.

Of course, the strict matching is the best. To achieve such a consistency [typecasting](/en/docs/basis/types/casting) can be used. The compiler cannot cope with ambiguous situations. Therefore you should not rely on subtle differences of types and implicit conversions that make the overloaded function unclear.

If you doubt, use explicit conversion to ensure strict compliance.

Examples of overloaded functions in MQL5 can be seen in the example of [ArrayInitialize()](/en/docs/array/arrayinitialize) functions.

Function overloading rules apply to [overload of class methods.](/en/docs/basis/oop/overload)

Overloading of system functions is allowed, but it should be observed that the compiler is able to accurately select the necessary function. For example, we can overload the system function [MathMax()](/en/docs/math/mathmax) in 4 different ways, but only two variants are correct.

Example:

```
// 1. overload is allowed - function differs from built-in MathMax() function in the number of parameters
double MathMax(double a,double b,double c);
 
// 2. overload is not allowed!
// number of parameters is different, but the last has a default value
// this leads to the concealment of the system function when calling, which is unacceptable
double MathMax(double a,double b,double c=DBL_MIN);
 
// 3. overload is allowed - normal overload by type of parameters a and b
double MathMax(int a,int b);
 
// 4. overload is not allowed!
// the number and types of parameters are the same as in original double MathMax(double a,double b)
int MathMax(double a,double b);

```

See also

[Overload](/en/docs/basis/oop/overload), [Virtual Functions](/en/docs/basis/oop/virtual), [Polymorphism](/en/docs/basis/oop/polymorphism)
