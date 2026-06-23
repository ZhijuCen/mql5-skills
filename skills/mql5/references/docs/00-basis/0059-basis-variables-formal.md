# Formal Parameters

Parameters passed to the function are [local](/en/docs/basis/variables/local). The scope is the function block. Formal parameters must have names differing from those of external variables and local variables defined within one function. Some values can be assigned to formal parameters in the function block. If a formal parameter is declared with the [const](/en/docs/basis/variables#const) modifier, its value can't be changed within the function.

Example:

```
void func(const int & x[], double y, bool z)
  {
   if(y>0.0 && !z)
      Print(x[0]);
   ...
  }

```

Formal parameters can be [initialized](/en/docs/basis/variables/initialization) by constants. In this case, the initializing value is considered as the default value. Parameters, next to the initialized one, must also be initialized.

Example:

```
void func(int x, double y = 0.0, bool z = true)
  {
   ...
  }

```

When calling such a function, the initialized parameters can be omitted, the defaults being substituted instead of them.

Example:

```
func(123, 0.5);

```

Parameters of [simple types](/en/docs/basis/types#base_types) are passed by value, i.e., modifications of the corresponding [local variable](/en/docs/basis/variables/local) of this type inside the called function will not be reflected in the calling function. Arrays of any type and data of the structure type are always passed by reference. If it is necessary to prohibit modifying the array or structure contents, the parameters of these types must be declared with the const keyword.

There is an opportunity to pass parameters of simple types by reference. In this case, modification of such parameters inside the calling function will affect the corresponding variables passed by reference. In order to indicate that a parameter is passed by reference, put the & modifier after the data type.

Example:

```
void func(int& x, double& y, double & z[])
  {
   double calculated_tp;
   ...
   for(int i=0; i<OrdersTotal(); i++)
     {
      if(i==ArraySize(z))       break;
      if(OrderSelect(i)==false) break;
      z[i]=OrderOpenPrice();
     }
   x=i;
   y=calculated_tp;
  }

```

Parameters passed by reference can't be initialized by default values.

Maximum 64 parameters can be passed into a function.

See also

[Input Variables](/en/docs/basis/variables/inputvariables#icustompassparameters), [Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
