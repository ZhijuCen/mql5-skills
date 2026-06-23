# Function Call

If a name that has not been described before, appears in the expression and is followed by the left parenthesis, it is contextually considered as the name of a function.

```
function_name (x1, x2,..., xn)

```

Arguments ([formal parameters](/en/docs/basis/variables/formal)) are passed by value, i.e. each expression x1,..., xn is calculated, and the value is passed to the function. The order of expressions calculation and the order of values loading are not guaranteed. During the execution, the system checks the number and type of arguments passed to the function. Such way of addressing to the function is called a value call.

Function call is an expression, the value of which is the value returned by the function. The function type described above must correspond with the type of the return value. The function can be declared or described in any part of the program on the [global scope](/en/docs/basis/variables/global), i.e., outside other functions. The function cannot be declared or described inside of another function.

Examples:

```
int start()
  {
   double some_array[4]={0.3, 1.4, 2.5, 3.6};
   double a=linfunc(some_array, 10.5, 8);
   //...
  }
double linfunc(double x[], double a, double b)
  {
   return (a*x[0] + b);
  }

```

At calling of a function with default parameters, the list of parameters to be passed can be limited, but not before the first default parameter.

Examples:

```
void somefunc(double init,
              double sec=0.0001, //set default values
              int level=10);  
//...
somefunc();                      // Wrong call. The first parameter must be presented.
somefunc(3.14);                  // Correct call
somefunc(3.14,0.0002);           // Correct call
somefunc(3.14,0.0002,10);        // Correct call

```

When calling a function, one may not skip parameters, even those having default values:

```
somefunc(3.14, , 10);           // Wrong call -> the second parameter was skipped.

```

See also

[Overload](/en/docs/basis/oop/overload), [Virtual Functions](/en/docs/basis/oop/virtual), [Polymorphism](/en/docs/basis/oop/polymorphism)
