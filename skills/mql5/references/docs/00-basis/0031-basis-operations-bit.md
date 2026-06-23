# Bitwise Operations

### Complement to One

Complement of the variable value up to one. The value of the expression contains 1 in all digits where the variable value contains 0, and 0 in all digits where the variable contains 1.

```
b = ~n;

```

Example:

```
   char a='a',b;
   b=~a;
   Print("a = ",a, "  b = ",b);  
// The result will be:
// a = 97   b = -98

```

### Right Shift

The binary representation of x is shifted to the right by y digits. If the value to shift is of the unsigned type, the logical right shift is made, i.e. the freed left-side bits will be filled with zeroes.

If the value to shift is of a sign type, the arithmetic right shift is made, i.e. the freed left-side digits will be filled with the value of a sign bit (if the number is positive, the value of the sign bit is 0; if the number is negative, the value of the sign bit is 1).

```
x = x >> y;

```

Example:

```
   char a='a',b='b';
   Print("Before:  a = ",a, "  b = ",b); 
//--- shift to the right
   b=a>>1;
   Print("After:   a = ",a, "  b = ",b); 
// The result will be:
// Before:  a = 97   b = 98
// After:   a = 97   b = 48

```

### Left Shift

The binary representation of x is shifted to the left by y digits, the freed right-side digits are filled with zeros.

```
x = x << y;

```

Example:

```
   char a='a',b='b';
   Print("Before:  a = ",a, "  b = ",b); 
//--- shift to the left
   b=a<<1;
   Print("After:   a = ",a, "  b = ",b); 
// The result will be:
// Before:  a = 97   b = 98
// After:   a = 97   b = -62

```

It is not recommended to shift by the number of bits larger or equal to the length of the variable shifted, because the result of such an operation is undefined.

### Bitwise AND Operation

The bitwise AND operation of binary-coded x and y representations. The value of the expression contains a 1 (TRUE) in all digits where both x and y contain non-zero, and it contains 0 (FALSE) in all other digits.

```
b = ((x & y) != 0);

```

Example:

```
   char a='a',b='b';
//--- AND operation
   char c=a&b;
   Print("a = ",a,"  b = ",b);
   Print("a & b = ",c);
// The result will be:
// a = 97   b = 98
// a & b = 96

```

### Bitwise OR Operation

The bitwise OR operation of binary representations of x and y. The value of the expression contains 1 in all digits where x or y does not contain 0, and it contains 0 in all other digits.

```
b = x | y;

```

Example:

```
   char a='a',b='b';
//--- OR operation
   char c=a|b;
   Print("a = ",a,"  b = ",b);
   Print("a | b = ",c);
// The result will be:
// a = 97   b = 98
// a | b = 99

```

### Bitwise Exclusive Operation OR

The bitwise exclusive OR (eXclusive OR) operation of binary representations of x and y. The value of the expression contains a 1 in all digits where x and y have different binary values, and it contains 0 in all other digits.

```
b = x ^ y;

```

Example:

```
   char a='a', b='b';
//--- Excluding OR operation
   char c=a^b;
   Print("a = ",a,"  b = ",b);
   Print("a ^ b = ",c);
// The result will be:
// a = 97   b = 98
// a ^ b = 3

```

Bitwise operations are performed with [integers](/en/docs/basis/types/integer) only.

See also

[Precedence Rules](/en/docs/basis/operations/rules)
