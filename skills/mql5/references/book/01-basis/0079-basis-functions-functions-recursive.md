# Recursion

It is allowed to call the same function from statements inside a function. Such calls are called recursive.

Let's go back to the example of calculating Fibonacci numbers. Following the formula for calculating each number as the sum of the previous two (except for the first two, which are equal to 1), it is easy to write a recursive function for calculating Fibonacci numbers.

```
int Fibo(const int n)
{
   if(n <= 1) return 1;
   
   return Fibo(n - 1) + Fibo(n - 2);
}

```

A recursive function must be able to return control without recursion, as in our case inside the conditional statement if for indexes 0 and 1. Otherwise, the sequence of function calls could continue indefinitely. In practice, because unfinished function calls accumulate in a limited area of ​​memory called the stack (see the [Declaration/Definition statements](/en/book/basis/statements/statements_declaration) section, and the "Heap" and "Stack" sidebar in the [Describing arrays](/en/book/basis/arrays/arrays_declaration) section), sooner or later the function will terminate with the "Stack overflow" runtime error. This problem is shown in the FiboEndless function.

```
int FiboEndless(const int n)
{
   return FiboEndless(n - 1) + FiboEndless(n - 2);
}

```

Please note that this is not a compilation error. In such a case, the compiler will not even generate a warning (although, technically it could). The error occurs during script execution. It will be printed to the Experts journal in the terminal.

Recursion can occur not only when a function is called from the function itself. For example, if the F function calls the G function which, in turn, calls the F function, this case is an indirect recursion. Thus, recursion can occur as a result of cyclic calls of any depth.
