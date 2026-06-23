# Comparison operations

As the name implies, these operations are intended for comparing two operands and returning a logic feature, true or false, depending on the condition to hold in the comparison.

The table below gives all comparison operations and their properties, such as symbols used, priorities, examples, and associativity.

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 6 | < | Less | e1 < e2 | L |
| 6 | > | Greater | e1 > e2 | L |
| 6 | <= | Less than or equal | e1 <= e2 | L |
| 6 | >= | greater than or equal | e1 >= e2 | L |
| 7 | == | Equal | e1 == e2 | L |
| 7 | != | Not equal | e1 != e2 | L |

The principle of each operation is to compare two operands using the criterion from the column containing its description. For example, entry "x < y" means checking whether "x is lesser than y". Correspondingly, the comparison result will be true if x is really lesser than y, and false in all other cases.

Comparisons work for the operands of any type (for different types, [typecasting](/en/book/basis/conversion/conversion_implicit) is performed).

Considering the left associativity and the return of the bool type result, constructing a sequence of comparisons does not work so obviously. For example, a hypothetic expression to check whether the value y lies between the values of x and z, could seemingly appear as follows:

```
int x = 10, y = 5, z = 2;
bool range = x < y < z;   // true (!)

```

However, such an expression is processed in a different manner. Even the compiler distinguishes it by the warning: "unsafe use of type 'bool' in operation".

Due to the left associativity, the left condition x < y is checked first, and its result is substituted as a temporary value of the bool type into the expression that goes as follows: b < z. Then the value of z is compared to true or false in the temporary variable b. To check whether y ranges between x and z, you should use two comparison operations combined with the logic operation AND (it will be considered in the [next section](/en/book/basis/expressions/operators_logical)).

```
int x = 10, y = 5, z = 2;
bool range = x < y && y < z;   // false

```

When using the comparing for equality/inequality, the features of the operand types shall be considered. For instance, floating-point numbers often contain "approximate" values after calculations (we considered the accuracy of representing double and float in the section [Real Numbers](/en/book/basis/builtin_types/float_numbers)). For example, the sum of 0.6 and 0.3 is not strictly 0.9:

```
double p = 0.3, q = 0.6;
bool eq = p + q == 0.9;        // false
double diff = p + q - 0.9;     // -0.000000000000000111

```

The difference makes 1*10-16, but it is sufficient for the comparison operation to return false.

Therefore, real numbers should be compared for equality/inequality using the greater-/less-then operators for their difference and acceptable deviation that is sorted out manually, based on the features of the computation, or a universal one is taken. Recall that for double and float, the embedded accuracy constants, DBL_EPSILON and FLT_EPSILON, are defined, valid for the value of 1.0. They must be scaled to compare other values. In script ExprRelational.mq5, one of the possible realizations of function isEqual is presented to compare real numbers, which considers this aspect.

```
bool isEqual(const double x, const double y)
{
   const double diff = MathAbs(x - y);
   const double eps = MathMax(MathAbs(x), MathAbs(y)) * DBL_EPSILON;
   return diff < eps;
}

```

Here we use the function of obtaining an absolute unsigned value (MathAbs) and the highest of the two values (MathMax). They will be described in the section [Mathematical Functions](/en/book/common/maths) of Part 4. The absolute difference between the parameters of function isEqual is compared to the calibrated tolerance in variable eps using operation '<'.

This function cannot be used to compare with absolute zero, anyway. For this purpose, you can use the following approach (it will probably require some adaptation to your specific needs):

```
bool isZero(const double x)
{
   return MathAbs(x) < DBL_EPSILON;
}

```

Strings are compared lexicographically, i.e., letter by letter. The code of each character is compared to the code of the character in the same position of the second string. Comparison is performed until a difference in the codes is found or one of the strings ends. The string ratio will be equal to that of the first differing characters, or a longer string will be considered greater than the shorter one. Remember that upper- and lowercase letters have different codes, and strange enough, uppercase ones have smaller codes than the lowercase ones.

An empty string "" (in fact, it stores one terminal 0) is not equal to the special value of NULL which means no string.

```
bool cmp1 = "abcdef" > "abs";     // false, [2]: 's' > 'c'
bool cmp2 = "abcdef" > "abc";     // true,  by length
bool cmp3 = "ABCdef" > "abcdef";  // false, by case
bool cmp4 = "" == NULL;           // false

```

Moreover, to compare strings, MQL5 provides some functions that will be described in the section [Working with Strings](/en/book/common/strings).

In comparing for equality/inequality, it is not recommended to use bool constants: true or false. The matter is that, in expressions like v == true or v == false, operand v can be interpreted intuitively as a logical type, while in fact, it is a number. As it is known, zero value is considered false in numbers, while all others are interpreted as true (we often want to use it as an indication of some result being present or absent). However, in this case, typecasting goes backward: true or false are "expanded" to a numeric type v and actually become equal to 1 and 0, respectively. Such a comparison will have a result other than the expected one (for example, comparison 100 == true will turn out to be false).
