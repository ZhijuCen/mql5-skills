# Optional parameters

MQL5 provides an opportunity to specify default values for parameters when describing a function. For this, the [initialization](/en/book/basis/variables/initialization) syntax is used, that is, a literal of the corresponding type to the right of the parameter, after the '=' sign. For example:

```
void function(int value = 0);

```

When calling a function, arguments for such parameters can be omitted. Then their values will be set to their default values. Such parameters are called optional (optional).

Optional parameters must appear at the end of the parameter list. In other words, if the i-th parameter is declared with initialization, then all subsequent parameters must also have it. Otherwise, a compilation error "missing default value for parameter" is shown. Below is a description of a function with such a problem.

```
double Largest(const double v1, const double v2 = -DBL_MAX,
               const double v3);

```

There are two solutions: either the parameter v3 must also have a default value, or the parameter v2 must become mandatory.

You can only omit optional arguments when calling a function from right to left. That is, if the function has two parameters and both are optional, then when calling, you cannot skip the first one, but specify the second one. The single value passed will be matched against the first parameter, and the second will be considered omitted. If both arguments are missing, the empty parentheses are still needed.

Consider the function of finding the maximum number of three. The first parameter is mandatory, the last two are optional and equal by default to the minimum possible number of type double. Thus, each of them, in the absence of an explicitly passed value, will certainly be less than (or, in extreme cases, equal to) all other parameters.

```
double Largest(const double v1, const double v2 = -DBL_MAX,
               const double v3 = -DBL_MAX)
{
   return v1 > v2 ? (v1 > v3 ? v1 : v3) : (v2 > v3 ? v2 : v3);
}

```

This is how you can call it:

```
Print(Largest(1));       // ok: 1
Print(Largest(0, -2));   // ok: 0
Print(Largest(1, 2, 3)); // ok: 3

```

With the help of optional parameters, MQL5 implements the concept of functions with a variable number of parameters in custom functions.

MQL5 does not support the ellipsis syntax for defining functions with a variable number of parameters, as C++ does. At the same time, there are built-in functions in the MQL5 API, which are described using ellipsis and accept a variable number of arbitrary parameters. For example, it is the [Print](/en/book/common/output/output_print) function. Its prototype looks like this: void Print(argument, ...). Therefore, we can call it with up to 64 arguments separated by commas (excluding arrays) and it will display them in the log.
