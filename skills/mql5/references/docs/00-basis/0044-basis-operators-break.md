# Break Operator

The break operator terminates the execution of the nearest nested outward [switch](/en/docs/basis/operators/switch), [while](/en/docs/basis/operators/while), [do-while](/en/docs/basis/operators/dowhile) or [for](/en/docs/basis/operators/for) operator. The control is passed to the operator that follows the terminated one. One of the purposes of this operator is to finish the looping execution when a certain value is assigned to a variable.

Example:

```
//--- searching for the first zero element
for(i=0;i<array_size;i++)
  if(array[i]==0)
    break;

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
