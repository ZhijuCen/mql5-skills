# Function templates

[Overloaded functions](/en/docs/basis/function/functionoverload) are commonly used to perform similar operations on various data types. [ArraySize()](/en/docs/array/arraysize) is a simple example of such function in MQL5. It returns size of any type of array. In fact, this system function is overloaded and the entire implementation of such an overload is hidden from MQL5 application developers:

```
int  ArraySize(
   void&  array[]      // checked array
   );

```

It means that MQL5 language compiler inserts necessary implementation for each call of this function. For example, that is how it can be done for integer type arrays:

```
int  ArraySize(
   int&  array[]      // array with int type elements
   );

```

[ArraySize()](/en/docs/array/arraysize) function can be displayed the following way for [MqlRates](/en/docs/constants/structures/mqlrates) type array for working with quotations in historical data format:

```
int  ArraySize(
   MqlRates&  array[] // array filled with MqlRates type values
   );

```

Thus, it is very convenient to use the same function for working with different types. However, all preliminary work should be carried out – the necessary function should be [overloaded](/en/docs/basis/function/functionoverload) for all data types it should correctly work with.

There is a convenient solution. If similar operations should be executed for each data type, it is possible to use function templates. In this case, a programmer needs to write only one function template description. When describing the template in such a way, we should specify only some formal parameter instead of some definite data type the function should work with. The compiler will automatically generate various functions for the appropriate handling of each type based on the types of the arguments used when calling the function.

Function template definition starts with the template keyword followed by the list of formal parameters in angle brackets. Each formal parameter is preceded by the typename keyword. Formal parameter types are built-in or user-defined types. They are used:

- to specify the types of function arguments,
- to specify the types of function's return value,
- to declare the variables inside the function definition

Number of template parameters cannot exceed eight. Each formal parameter in the template definition should appear in the list of function parameters at least once. Each name of the formal parameter should be unique.

Below is an example of a function template for searching the highest value in the array of any numeric type (integer and real numbers):

```
template<typename T>
T ArrayMax(T &arr[])
  {
   uint size=ArraySize(arr);
   if(size==0) return(0);          
   
   T max=arr[0];
   for(uint n=1;n<size;n++)
      if(max<arr[n]) max=arr[n];
//---
   return(max);
  }

```

This template defines the function that finds the highest value in the passed array and returns this value as a result. Keep in mind that the [ArrayMaximum()](/en/docs/array/arraymaximum) function built in MQL5 returns only the highest value index that can be used to find the value itself. For example:

```
//--- create an array
   double array[];
   int size=50;
   ArrayResize(array,size);
//---  fill with random values
   for(int i=0;i<size;i++)
     {
      array[i]=MathRand();
     }
 
//--- find position of the highest value in the array
   int max_position=ArrayMaximum(array);
//--- now, get the highest value itself in the array
   double max=array[max_position];
//--- display the found value
   Print("Max value = ",max);

```

Thus, we have performed two steps to get the highest value in the array. With ArrayMax() function template, we can get the result of the necessary type just by passing the array of an appropriate type into this function. It means that instead of two last lines

```
//--- find position of the highest value in the array
   int max_position=ArrayMaximum(array);
//--- now, get the highest value itself in the array
   double max=array[max_position];

```

we now can use only one line, in which the returned result has the same type as the array passed into function:

```
//--- find the highest value
   double max=ArrayMax(array);

```

In this case, the type of result returned by the ArrayMax() function will automatically match the type of array.

Use the typename keyword to get the argument type as a string in order to create general purpose methods of working with various data types. Let's consider a specific example of the function that returns data type as a string:

```
#include <Trade\Trade.mqh>
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- 
   CTrade trade;   
   double d_value=M_PI;
   int i_value=INT_MAX;
   Print("d_value: type=",GetTypeName(d_value), ",   value=", d_value);
   Print("i_value: type=",GetTypeName(i_value), ",   value=", i_value);
   Print("trade: type=",GetTypeName(trade));
//--- 
  }
//+------------------------------------------------------------------+
//| Type is returned as a line                                       |
//+------------------------------------------------------------------+
template<typename T>
string GetTypeName(const T &t)
  {
//--- return the type as a line
   return(typename(T));
//---
  }

```

Function templates can also be used for class methods, for example:

```
class CFile
  {
   ...
public:
   ...
   template<typename T>
   uint WriteStruct(T &data);
  };
 
template<typename T>
uint CFile::WriteStruct(T &data)
  {
   ...
   return(FileWriteStruct(m_handle,data));
  }

```

Function templates should not be declared with [export](/en/docs/basis/function/export), [virtual](/en/docs/basis/oop/virtual) and [#import](/en/docs/basis/function/extfunctions) keywords.

## Template function overload

A template function overload may be necessary sometimes. For example, we have a template function that writes the value of the second parameter to the first one using [typecasting](/en/docs/basis/types/casting). MQL5 does not allow typecasting [string](/en/docs/basis/types/stringconst) to [bool](/en/docs/basis/types/integer/boolconst). We can do that ourselves – let's create an overload of a template function. For example:

```
//+------------------------------------------------------------------+
//| Template function                                                |
//+------------------------------------------------------------------+
template<typename T1,typename T2>
string Assign(T1 &var1,T2 var2)
  {
   var1=(T1)var2;
   return(__FUNCSIG__);
  }
//+------------------------------------------------------------------+
//| Special overload for bool+string                     |
//+------------------------------------------------------------------+
string Assign(bool &var1,string var2)
  {
   var1=(StringCompare(var2,"true",false) || StringToInteger(var2)!=0);
   return(__FUNCSIG__);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   int i;
   bool b;
   Print(Assign(i,"test"));
   Print(Assign(b,"test"));
  }

```

As a result of the code execution, we can see that the Assign() template function has been used for the int+string pair, while the overloaded version has already been used for the bool+string pair during the second call.

```
string Assign<int,string>(int&,string)
string Assign(bool&,string)

```

See also

[Overload](/en/docs/basis/oop/overload)
