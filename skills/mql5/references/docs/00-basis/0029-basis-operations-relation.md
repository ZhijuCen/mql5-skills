# Operations of Relation

Boolean FALSE is represented with an integer zero value, while the boolean TRUE is represented by any non-zero value.

The value of expressions containing operations of relation or [logical operations](/en/docs/basis/operations/bool) is FALSE (0) or TRUE (1).

```
True if a is equal to b                      a == b;
True if a is not equal to b                  a != b;
True if a is less than b                     a < b;
True if a is greater than b                  a > b;
True if a is less than or equal to b         a <= b;
True if a is greater than or equal to b      a >= b;

```

The equality of two [real numbers](/en/docs/basis/types/double) can't be compared. In most cases, two seemingly identical numbers can be unequal because of different values in the 15th decimal place. In order to correctly compare two real numbers, compare the normalized difference of these numbers with zero.

Example:

```
bool CompareDoubles(double number1,double number2)
  {
   if(NormalizeDouble(number1-number2,8)==0) return(true);
   else return(false);
  }
void OnStart()
  {
   double first=0.3;
   double second=3.0;
   double third=second-2.7;
   if(first!=third)
     {
      if(CompareDoubles(first,third))
         printf("%.16f and %.16f are equal",first,third);
     }
  }
// Result: 0.3000000000000000  0.2999999999999998   are equal

```

See also

[Precedence Rules](/en/docs/basis/operations/rules)
