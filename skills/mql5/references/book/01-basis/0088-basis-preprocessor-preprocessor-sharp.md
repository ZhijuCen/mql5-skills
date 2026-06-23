# Special operators '#' and '##' inside #define definitions

Inside macro definitions, two special operators can be used:

- a single hash symbol '#' before the name of a macro parameter turns the contents of that parameter into a string; it is allowed only in function macros;
- a double hash symbol '##' between two words (tokens) combines them, and if the token is a macro parameter, then its value is substituted, but if the token is a macro name, it is substituted as is, without expanding the macro; if as a result of "gluing" another macro name is obtained, it is expanded;

In the examples in this book, we often used the following macro:

```
#define PRT(A) Print(#A, "=", (A))

```

It calls the Print function, in which the passed expression is displayed as a string thanks to #A, and after the sign "equal", the actual value of A is printed.

To demonstrate '##', let's consider another macro:

```
#define COMBINE(A,B,X) A##B(X)

```

With it, we can actually generate a call to the SQN macro defined above:

```
Print(COMBINE(SQ,N,2)); // 4

```

The literals SQ and N are concatenated, after which the macro SQN expands to ((2)*(2)) and produces the result 4.

The following macro allows you to create a variable definition in code by generating its name given the parameters of the macro:

```
#define VAR(TYPE,N) TYPE var##N = N

```

Then the line of code:

```
VAR(int, 3);

```

is equivalent to the following:

```
int var3 = 3;

```

Concatenation of tokens allows the implementation of a loop shorthand over the array elements using a macro.

```
#define for_each(I, A) for(int I = 0, max_##I = ArraySize(A); I < max_##I; ++I)
  
// describe and somehow fill in the array x
double x[];
// ...
// implement loop through the array
for_each(i, x)
{
   x[i] = i * i;
}

```
