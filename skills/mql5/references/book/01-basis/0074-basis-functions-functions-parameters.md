# Parameters and arguments

The arguments passed to the function with its call are the initial values of the corresponding function parameters. The number, order, and types of arguments must match the function prototype. However, the order in which arguments are computed is not defined (see the [Basic concepts](/en/book/basis/expressions/expressions_overview) section). Depending on the specifics of the source code and optimization considerations, the compiler may choose an option that is convenient for it. For example, given a list of two arguments, the compiler might evaluate the second argument first and then the first. It is only guaranteed that both arguments will be evaluated before the call.

Each argument is mapped to the corresponding parameter in the same way that [variables are initialized](/en/book/basis/variables/initialization), with [implicit casts](/en/book/basis/conversion) if necessary. Before the function starts, all its parameters are guaranteed to have the specified values. For example, depending on the arguments passed, calls to the Fibo function can lead to the following effects (described in the comments):

```
// warnings
double d = 5.5;
Fibo(d);          // possible loss of data due to type conversion
Fibo(5.5);        // truncation of constant value
Fibo("10");       // implicit conversion from 'string' to 'number'
// errors
Fibo();           // wrong parameters count
Fibo(0, 10);      // wrong parameters count

```

All warnings are about implicit conversions that the compiler performs because the value types do not match the parameter types. They should be regarded as potential errors and eliminated. The "wrong parameters count" error occurs when there are too few or too many arguments.

In theory, a function parameter does not have to have a name, i.e. the type alone is sufficient to describe the parameter. This sounds rather strange because we will not be able to access a parameter without a name inside the function. However, when creating programs based on some standard interfaces, sometimes you have to write functions that must correspond to given prototypes. In this case, some parameters inside the function may be unnecessary. Then, to explicitly indicate this fact, the programmer can omit their names. For example, the MQL5 API requires the implementation of the [OnDeinit](/en/book/applications/runtime/runtime_oninit_ondeinit) event handler function with the following prototype:

```
void OnDeinit(const int reason);

```

If we don't need the reason parameter in the function code, we can omit it in the description:

```
void OnDeinit(const int);

```

The terminal event handling function is usually called by the terminal itself, but if we needed to call a similar function (with an anonymous parameter) from our code, then we need to pass all the arguments, regardless of whether the parameters are named or not.
