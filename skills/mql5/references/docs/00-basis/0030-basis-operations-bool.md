# Boolean Operations

### Logical Negation NOT (!)

Operand of the logical negation (!) must be of arithmetic type. The result is TRUE (1), if the operand value is FALSE (0); and it is equal to FALSE (0), if the operand differs from FALSE (0).

```
if(!a) Print("not 'a'");

```

### Logical Operation OR (||)

Logical OR operation (||) of x and y values. The expression value is TRUE (1), if x or y value is true (not null). Otherwise - FALSE (0).

```
if(x<0 || x>=max_bars) Print("out of range");

```

### Logical Operation AND (&&)

Logical operation AND (&&) of x and y values. The expression value is TRUE (1), if the values of x and y are true (not null). Otherwise - FALSE (0).

### Brief Estimate of Boolean Operations

The scheme of the so called "brief estimate" is applied to boolean operations, i.e. the calculation of the expression is terminated when the result of the expression can be precisely estimated.

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- the first example of the brief estimate
   if(func_false() && func_true())
     {
      Print("Operation &&: You will never see this expression");
     }
   else
     {
      Print("Operation &&: Result of the first expression is false, so the second wasn't calculated");
     }
//--- the second example of the brief estimate
   if(!func_false() || !func_true())
     {
      Print("Operation ||: Result of the first expression is true, so the second wasn't calculated");
     }
   else
     {
      Print("Operation ||: You will never see this expression");
     }
  }
//+------------------------------------------------------------------+
//| the function always returns false                                |
//+------------------------------------------------------------------+
bool func_false()
  {
   Print("Function func_false()");
   return(false);
  }
//+------------------------------------------------------------------+
//| the function always returns true                                 |
//+------------------------------------------------------------------+
bool func_true()
  {
   Print("Function func_true()");
   return(true);
  }

```

See also

[Precedence Rules](/en/docs/basis/operations/rules)
