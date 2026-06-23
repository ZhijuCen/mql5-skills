# Find

Searches for the first match of a substring from a specified position.

```
int  Find(
   uint          start,         // position
   const string  substring      // substring
   ) const;

```

Parameters

start

[in]  Initial position for substring search.

substring

[in]  Sample substring to search for.

Return Value

The index of the first match of a substring (-1 - substring is not found).
