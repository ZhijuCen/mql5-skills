# While Loop Operator

The while operator consists of a checked expression and the operator, which must be fulfilled:

```
while(expression)
  operator;

```

If the expression is true, the operator is executed until the expression becomes false. If the expression is false, the control is passed to the next operator. The expression value is defined before the operator is executed. Therefore, if the expression is false from the very beginning, the operator will not be executed at all.

Note

If it is expected that a large number of iterations will be handled in a loop, it is advisable that you check the fact of forced program termination using the [IsStopped()](/en/docs/check/isstopped) function.

Example:

```
while(k<n && !IsStopped())
  {
   y=y*x;
   k++;
  }

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
