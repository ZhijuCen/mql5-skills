# For Loop Operator

The for operator consists of three expressions and an executable operator:

```
for(expression1; expression2; expression3)
   operator;

```

Expression1 describes the loop initialization. Expression2 checks the conditions of the loop termination. If it is true, the loop body for is executed. The loop repeats expression2 until it becomes false. If it is false, the loop is terminated, and control is given to the next operator. Expression3 is calculated after each iteration.

The for operator is equivalent to the following succession of operators:

```
expression1;
while(expression2)
  {
   operator;
   expression3;
  };

```

Any of the three or all three expressions can be absent in the for operator, but the semicolons (;) that separate them must not be omitted. If expression2 is omitted, it is considered constantly true. The for(;;) operator is a continuous loop, equivalent to the while(1) operator. Each expression 1 or 3 can consist of several expressions combined by a comma operator ','.

Note

If it is expected that a large number of iterations will be handled in a loop, it is advisable that you check the fact of forced program termination using the [IsStopped()](/en/docs/check/isstopped) function.

Examples:

```
for(x=1;x<=7000; x++)
  {
   if(IsStopped())
      break;
   Print(MathPower(x,2));
  }
//--- Another example
for(;!IsStopped();)
  {
   Print(MathPower(x,2));
   x++;
   if(x>10) break;
  }
//--- Third example
for(i=0,j=n-l;i<n && !IsStopped();i++,j--) a[i]=a[j];

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
