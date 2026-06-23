# Function call

A function is called when its name is mentioned in an expression. After the name, there should be a pair of parentheses, in which the arguments corresponding to the function parameters (if there is a list of parameters in its definition) are indicated, separated by commas.

A little later, we will look at the [function pointer](/en/book/basis/functions/functions_typedef) type, which allows you to create variables that point to a function with specific characteristics, and then call it not by name, but through this variable.

Continuing the example with the Fibo function, let's call it from the OnStart function. To do this, let's create a variable f to store the resulting number and in its initialization expression we indicate the name of the function Fibo and an integer (for example, 10) as an argument, in parentheses.

```
void OnStart()
{
   int f = Fibo(10); 
   Print(f); // 89
}

```

We are not required to create a variable to receive a value from a function. Instead, you can call the function directly from an expression, such as "2*Fibo(10)" or "Print(Fibo(10))". Then its value will be substituted into the expression at the place of the call. Here, the auxiliary variable f is introduced to implement the call and return of a value in a separate statement.

The call process includes the following steps:

- Execution of the statement sequence of the calling function (OnStart) is suspended;
- The value of the argument gets into the input parameter n of the called function (Fibo);
- The execution of its statements starts;
- When it is completely finished, it sends the result back (remember the return statement inside);
- The result is written to the variable f; and
- After that, the execution of the OnStart function continues, that is, the number is printed to the log (Print).

For each function call, the compiler generates auxiliary binary code (the programmer does not need to worry about it). The idea of this code is that before calling the function, it pushes the current position in the program onto the stack, and after the call is completed, it retrieves it and uses it to return to the statements following the function call. When one function calls another, that one calls one more function, the second calls a third, and so on, the return addresses of transitions throughout the hierarchy of called functions are accumulated on the stack (hence the name stack). As nested function calls are processed, the stack will be cleared in reverse order. Note that the stack also allocates memory for the local variables of each function.
