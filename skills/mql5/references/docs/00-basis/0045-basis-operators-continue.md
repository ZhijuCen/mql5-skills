# Continue Operator

The continue operator passes control to the beginning of the nearest outward loop [while](/en/docs/basis/operators/while), [do-while](/en/docs/basis/operators/dowhile) or [for](/en/docs/basis/operators/for) operator, the next iteration being called. The purpose of this operator is opposite to that of [break](/en/docs/basis/operators/break) operator.

Example:

```
//--- Sum of all nonzero elements
int func(int array[])
  {
   int array_size=ArraySize(array);
   int sum=0;
   for(int i=0;i<array_size; i++)
     {
      if(a[i]==0) continue;
      sum+=a[i];
     }
   return(sum);
  }

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
