# Function pointers (typedef)

MQL5 has the typedef keyword, which allows you to describe a special type of function pointer.

Unlike C++, where typedef has a much wider application, in MQL5 typedef is used only for function pointers.

The syntax for a new type declaration is:

```
typedef function_result_type ( *function_type )( [list_of_input_parameters] ) ;

```

The function_type identifier defines a type name that becomes a synonym (alias) for a pointer to any function that returns a value of the given type function_result_type and accepts a list of input parameters (list_of_input_parameters).

For example, we can have 2 functions with the same prototypes (two input parameters of type double and the result type is also double) that perform different arithmetic operations: addition and subtraction (FuncTypedef.mq5).

```
double plus(double v1, double v2)
{
   return v1 + v2;
}
 
double minus(double v1, double v2)
{
   return v1 - v2;
}

```

Their common prototype is easy to describe for use as a pointer:

```
typedef double (*Calc)(double, double);

```

This entry introduces the Calc type into the program, with which you can define a variable/parameter for storing/passing a reference to any function with such a prototype, including both functions plus and minus. This type is a pointer because the character '*' (*Calc) is used in the description. We will learn more about the features of the asterisk as applied to pointers when studying OOP.

It is convenient to use such a class of pointers to create custom algorithms that can "on the fly" call different functions corresponding to the alias, depending on the input data.

In particular, we can introduce a generalized calculator function:

```
double calculator(Calc ptr, double v1, double v2)
{
   if(ptr == NULL) return 0;
   return ptr(v1, v2);
}

```

Its first parameter is declared with the Calc type. Thanks to this, we can pass an arbitrary function with a suitable prototype to it and, as a result, perform some operation, the essence of which the calculator function itself does not know about. It does this by delegating the call to a pointer: ptr(v1, v2). Because ptr is a function pointer, this syntax not only resembles a function call but actually calls the function that the pointer holds.

Note that we pre-check the ptr parameter against the special value NULL (NULL is the equivalent of zero for pointers). The fact is that the pointer may not point anywhere, that is, it may not be initialized. So, in the script, we have a global variable described:

```
Calc calc;

```

It has no pointers. If it weren't for the "protection" against NULL, calling calculator with an "empty" pointer calc would result in a run-time error "Invalid function pointer call ".

Calls to the calculator function with different pointers in the first parameter will give the following results (shown in the comments):

```
void OnStart()
{
   Print(calculator(plus, 1, 2));   //  3
   Print(calculator(minus, 1, 2));  // -1
   Print(calculator(calc, 1, 2));   //  0
}

```

Note that if there is no explicit initialization, all function pointers are filled with zero values. This applies to both global and local variables of a given type.

A pointer type defined with typedef can be returned from functions, for example:

```
Calc generator(ushort type)
{
   switch(type)
   {
      case '+': return plus;
      case '-': return minus;
   }
   return NULL;
}

```

In addition, the type of function pointers is often used for callback functions (callback, see FuncCallback.mq5). Suppose we have a DoMath function that performs lengthy calculations (probably, it is implemented in a separate [library](/en/book/advanced/libraries)). In terms of user interface convenience and friendliness, it would be great to show the user a progress indication. For this purpose, you can define a special type of function pointer for notifications about the percentage of work completed (ProgressCallback), and add a parameter of this type to the DoMath function. In the DoMath code, you should periodically call the passed function:

```
typedef void (*ProgressCallback)(const float percent);
 
void DoMath(double &bigdata[], ProgressCallback callback)
{
   const int N = 1000000;
   for(int i = 0; i < N; ++i)
   {
      if(i % 10000 == 0 && callback != NULL)
      {
         callback(i * 100.0f / N);
      }
      
      // long calculations
   }
}

```

Then the calling code can define the required callback function, pass a pointer to it to DoMath and receive updates as the calculation progresses.

```
void MyCallback(const float percent)
{
   Print(percent);
}
  
void OnStart()
{
   double data[] = {0};
   DoMath(data, MyCallback);
}

```

Function pointers work only with custom functions defined in MQL5. They cannot point to [built-in functions](/en/book/common) of the MQL5 API.
