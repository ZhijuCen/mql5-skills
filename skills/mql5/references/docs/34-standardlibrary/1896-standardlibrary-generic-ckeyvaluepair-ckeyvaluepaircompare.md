# Compare

Compares the current key/value pair to the specified one.

```
int Compare(
   CKeyValuePair<TKeyTValue>*  pair     // the pair to compare
   );

```

Parameters

*pair

[in]  The pair to compare.

Return Value

Returns a number that expresses the ratio of the current and passed key-value pairs:

- if the result is less than zero, the current key/value pair is less than the passed one
- if the result is zero, the current key/value pair is equal to than the passed one
- if the result is greater than zero, the current key/value pair is greater than the passed one

Note

Key/value pairs are compared based on their keys.
