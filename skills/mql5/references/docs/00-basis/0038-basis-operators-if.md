# If-Else Conditional Operator

The IF - ELSE operator is used when a choice must be made. Formally, the syntax is as follows:

```
if (expression)
     operator1
else
     operator2

```

If the expression is true, operator1 is executed and control is given to the operator that follows operator2 (operator2 is not executed). If the expression is false, operator2 is executed.

The else part of the if operator can be omitted. Thus, a divergence may appear in nested if operators with omitted else part. In this case, else addresses to the nearest previous if operator in the same block that has no else part.

Examples:

```
//--- The else part refers to the second if operator:
if(x>1)
   if(y==2) z=5;
else     z=6;
//--- The else part refers to the first if operator:
if(x>l)
  {
   if(y==2) z=5;
  }
else        z=6;
//--- Nested operators
if(x=='a')
  {
   y=1;
  }
else if(x=='b')
  {
   y=2;
   z=3;
  }
else if(x=='c')
  {   
   y=4;
  }
else Print("ERROR");

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
