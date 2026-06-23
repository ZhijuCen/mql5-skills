# Loop Operator do while

The [for](/en/docs/basis/operators/for) and [while](/en/docs/basis/operators/while) loops check the termination at the beginning, not at the end of a loop. The third loop operator do - while checks the condition of termination at the end, after each loop iteration. The loop body is always executed at least once.

```
do
   operator;
while(expression);

```

First the operator is executed, then the expression is calculated. If it is true, then the operator is executed again, and so on. If the expression becomes false, the loop terminates.

Note

If it is expected that a large number of iterations will be handled in a loop, it is advisable that you check the fact of forced program termination using the [IsStopped()](/en/docs/check/isstopped) function.

Example:

```
//--- Calculate the Fibonacci series
   int counterFibonacci=15;
   int i=0,first=0,second=1;
   int currentFibonacciNumber;
   do
     {
      currentFibonacciNumber=first+second;
      Print("i = ",i,"  currentFibonacciNumber = ",currentFibonacciNumber);
      first=second;
      second=currentFibonacciNumber;
      i++; // without this operator an infinite loop will appear!
     }
   while(i<counterFibonacci && !IsStopped());

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
