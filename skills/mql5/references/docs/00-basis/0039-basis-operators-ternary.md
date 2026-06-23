# Ternary Operator ?:

The general form of the ternary operator is as follows:

```
expression1 ? expression2 : expression3

```

For the first operand - "expression1" - any expression that results in a [bool](/en/docs/basis/types/integer/boolconst) type value can be used. If the result is true, then the operator set by the second operand, i.e. "expression2" is executed.

If the first operand is false, the third operand - "expression3" is performed. The second and third operands, i.e. "expression2" and "expression3" should return values of one type and should not be of [void](/en/docs/basis/types/void) type. The result of the conditional operator execution is the result of expression2 or result of the expression3, depending on the result of expression1.

```
//--- normalize difference between open and close prices for a day range
double true_range = (High==Low)?0:(Close-Open)/(High-Low);

```

This entry is equivalent to the following:

```
   double true_range;
   if(High==Low)true_range=0;               // if High and Low are equal
   else true_range=(Close-Open)/(High-Low); // if the range is not null

```

## Operator Use Restrictions  #

Based on the value of "expression1", the operator must return one of the two values - either "expression2" or "expression3". There are several limitations to these expressions:

1. Do not mix [user-defined type](/en/docs/basis/types/classes) with [simple type](/en/docs/basis/types#base_types) or [enumeration](/en/docs/basis/types/integer/enumeration). [NULL](/en/docs/basis/types/void) can be used for the [pointer](/en/docs/basis/types/object_pointers).
2. If types of values are simple, the operator will be of the maximum type (see [Type casting](/en/docs/basis/types/casting)).
3. If one of the values is an enumeration and the second one is of a numeric type, the enumeration is replaced by int and the second rule is applied.
4. If both values are enumerations, their types must be identical, and the operator will be of type enumeration.

Restrictions for the user-defined types (classes or structures):

1. Types must be identical or one should be [derived](/en/docs/basis/oop/inheritance) from the other one.
2. If types are not identical (inheritance), then the child is implicitly cast to the parent, i.e. the operator will be of the parent type.
3. Do not mix object and the pointer – both expressions must be either objects or [pointers](/en/docs/basis/types/object_pointers). [NULL](/en/docs/basis/types/void) can be used for the pointer.

Note

Be careful when using the conditional operator as an argument of an [overloaded function](/en/docs/basis/function/functionoverload), because the type of the result of a conditional operator is defined at the time of program compilation. And this type is [determined](/en/docs/basis/types/casting) as the larger of the types "expression2" and "expression3".

Example:

```
void func(double d) { Print("double argument: ",d); }
void func(string s) { Print("string argument: ",s); }
 
bool   Expression1=true;
double Expression2=M_PI;
string Expression3="3.1415926";
 
void OnStart()
  {
   func(Expression2);
   func(Expression3);
 
   func(Expression1?Expression2:Expression3);   // warning on implicit casting to string
   func(!Expression1?Expression2:Expression3);  // warning on implicit casting to string
  }
 
//   Result:
//   double argument: 3.141592653589793
//   string argument: 3.1415926
//   string argument: 3.141592653589793
//   string argument: 3.1415926

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
