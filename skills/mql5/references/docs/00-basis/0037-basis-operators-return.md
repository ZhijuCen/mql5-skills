# Return Operator

The return operator terminates the current [function](/en/docs/basis/function) execution and returns control to the calling program. The expression calculation result is returned to the calling function. The expression can contain an assignment operator.

Example:

```
int CalcSum(int x, int y)
  {
   return(x+y);
  }

```

In functions with the [void](/en/docs/basis/types/void) return type, the return operator without expression must be used:

```
void SomeFunction()
  {
   Print("Hello!");
   return;    // this operator can be removed
  }

```

The right brace of the function means implicit execution of the return operator without expression.

What can be returned: [simple types](/en/docs/basis/types#base_types), [simple structures](/en/docs/basis/types/classes#simple_structure), [object pointers](/en/docs/basis/types/object_pointers). With  the return operator you can't return any arrays, class objects, variables of compound structure type.

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
