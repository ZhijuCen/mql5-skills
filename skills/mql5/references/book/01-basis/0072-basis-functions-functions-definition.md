# Function definition

A function definition consists of the value type it returns, an identifier, a list of parameters in parentheses, and a body — a block of code with statements. Parameters in the list are separated by commas. Each parameter is given a type, a name, and optionally a default value.

```
result_type function_identifier ( [parameter_type parameter_identifier
                                       = value_by_default] ,... )
{
  [statement]
   ...
}

```

It is allowed to create functions without parameters: then there is no list, and empty brackets are placed after the function name (they cannot be omitted). Optionally, you can write the void keyword between the brackets to emphasize that there are no parameters. For example, like this:

```
void OnStart(void)
{
}

```

The combination of return type, number and types of parameters in the list is called a function prototype or signature. Different functions can have the same prototype.

In previous sections, we have already seen function definitions such as OnStart and Greeting. Now let's try to implement the calculation of Fibonacci numbers as a test function. These numbers are calculated by the following formula:

```
f[0] = 1
f[1] = 1
f[i] = f[i - 1] + f[i - 2], i > 1

```

The first two numbers are 1, and all subsequent numbers are the sum of the previous two. We give the beginning of the series: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55...

You can calculate the number at a given index using the following function (FuncFibo.mq5).

```
int Fibo(const int n)
{
   int prev = 0;
   int result = 1;
   for(int i = 0; i < n; ++i)
   {
      int temp = result;
      result = result + prev;
      prev = temp;
   }
   return result;
}

```

It takes one parameter n of type int and returns a result of type int. The n parameter has the const modifier because we are not going to change n inside the function (such an explicit declaration of restrictions on the "rights" of variables is welcome because it helps avoid random errors).

Local variables prev and result will store the current values of the last two numbers in the series. In the loop over i we calculate their sum, getting the next number of the sequence. Previously, the old value result is written to the variable temp, so that after summation, it is transferred to prev.

After executing the loop a given number of times, the result variable contains the desired number. We return it from the function using the result statement.

The input parameter of a function is also a local variable that will be initialized to the actual value during the function call. This value is passed "outside" from the statement with the function call.

Parameter names must be unique and must not match local variable names.

The body of a function is a block of code that defines the [scope and lifetime of local variables](/en/book/basis/variables/scope_and_lifetime). Their definition and operation principles were discussed in the sections [Declaration/definition statements](/en/book/basis/statements/statements_declaration) and [Initialization](/en/book/basis/variables/initialization).
