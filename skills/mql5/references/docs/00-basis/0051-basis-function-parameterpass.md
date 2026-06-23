# Passing Parameters

There are two methods, by which the machine language can pass arguments to a subprogram (function). The first method is to send a parameter by value. This method copies the [argument](/en/docs/basis/function/call#argument) value into a formal function parameter. Therefore, any changes in this parameter within the function have no influence on the corresponding call argument.

```
//+------------------------------------------------------------------+
//| Passing parameters by value                                      |
//+------------------------------------------------------------------+
double FirstMethod(int i,int j)
  {
   double res;
//---
   i*=2;
   j/=2;
   res=i+j;
//---
   return(res);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int a=14,b=8;
   Print("a and b before call:",a," ",b);
   double d=FirstMethod(a,b);
   Print("a and b after call:",a," ",b);
  }
//--- Result of script execution
//  a and b before call: 14 8
//  a and b after call: 14 8

```

The second method is to pass by reference. In this case, reference to a parameter (not its value) is passed to a function parameter. Inside the function, it is used to refer to the actual parameter specified in the call. This means that the parameter changes will affect the argument used to call the function.

```
//+------------------------------------------------------------------+
//| Passing parameters by reference                                  |
//+------------------------------------------------------------------+
double SecondMethod(int &i,int &j)
  {
   double res;
//---
   i*=2;
   j/=2;
   res=i+j;
//---
   return(res);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int a=14,b=8;
   Print("a and b before call:",a," ",b);
   double d=SecondMethod(a,b);
   Print("a and b after call:",a," ",b);
  }
//+------------------------------------------------------------------+
//--- result of script execution
//  a and b before call: 14 8
//  a and b after call: 28 4

```

MQL5 uses both methods, with one exception: arrays, structure type variables and class objects are always passed by reference. In order to avoid changes in actual parameters (arguments passed at function call) use the access specifier [const](/en/docs/basis/variables#const). When trying to change the contents of a variable declared with the const specifier, the compiler will generate an error.

### Note

It should be noted that parameters are passed to a function in reversed order, i.e., first the last parameter is calculated and passed, and then the last but one, etc. The last calculated and passed parameter is the one that stands first after opening parenthesis.

Example:

```
void OnStart()
  {
//---
   int a[]={0,1,2};
   int i=0;
 
   func(a[i],a[i++],"First call (i = "+string(i)+")");
   func(a[i++],a[i],"Second call (i = "+string(i)+")");
// Result:
// First call (i = 0) : par1 = 1     par2 = 0
// Second call (i = 1) : par1 = 1     par2 = 1
 
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void func(int par1,int par2,string comment)
  {
   Print(comment,": par1 = ",par1,"    par2 = ",par2);
  }

```

In first call (see example above) the i variable is first used in strings concatenation:

```
  "First call (i = "+string(i)+")"

```

Here its value doesn't change. Then the i variable is used in calculation of the a[i++] array element, i.e. when array element with index i is accessed, the i variable is [incremented](/en/docs/basis/operations/mathoperation#posfix). And only after that the first parameter with changed value of i variable is calculated.

In the second call the same value of i (calculated on the first phase of function calling) is used when calculating all three parameters. Only after the first parameters is calculated the i variable is changed again.

See also

[Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope),[ Overload](/en/docs/basis/oop/overload), [Virtual Functions](/en/docs/basis/oop/virtual), [Polymorphism](/en/docs/basis/oop/polymorphism)
