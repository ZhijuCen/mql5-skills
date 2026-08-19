# Compare

Compares two values of type T.

```
int Compare(
   T  x,     // the first value
   T  y      // the second value
   );

```

Parameters

x

[in]  The first value to compare.

y

[in]  The second value to compare.

Return Value

Returns a number that expresses the ratio of the two compared values:

- if the result is less than zero, x is less than y (x<y)
- if the result is equal to zero, x is equal to y (x=y)
- if the result is greater than zero, x is greater than y (x>y)

Note

The x and y values are compared based one one of he overloads of the Compare global method depending on the T type.
