# Switch Operator

Compares the expression value with constants in all the case variants and passes control to the operator that corresponds to the expression value. Each variant of case can be marked with an [integer constant](/en/docs/basis/types/integer/integertypes), a literal constant or a constant expression. The constant expression can't contain variables or function calls. Expression of the switch operator must be of integer type – int or uint.

```
switch(expression)
  {
   case constant: operators
   case constant: operators
      ...
   default: operators
  }

```

Operators marked by the default label are executed if none of the constants in case operators is equal to the expression value. The default variant should not be necessarily declared and should not be necessarily the last one. If none of the constants corresponds to the expression value and the default variant is not available, no actions are executed.

The case keyword with a constant are just labels, and if operators are executed for some case variant, the program will further execute the operators of all subsequent variants until the [break](/en/docs/basis/operators/break) operator occurs. It allows to bind a sequence of operators with several variants.

A constant expression is calculated during compilation. No two constants in one switch operator can have the same value.

Examples:

```
//--- First example
switch(x)
  {
   case 'A':
      Print("CASE A");
      break;
   case 'B':
   case 'C':
      Print("CASE B or C");
      break;
   default:
      Print("NOT A, B or C");
      break;
  }
 
//---  Second example
   string res="";
   int i=0;
   switch(i)
     {
      case 1:
         res=i;break;
      default:
         res="default";break;
      case 2:
         res=i;break;
      case 3:
         res=i;break;
     }
   Print(res);
/*
   Result
   default
*/

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
