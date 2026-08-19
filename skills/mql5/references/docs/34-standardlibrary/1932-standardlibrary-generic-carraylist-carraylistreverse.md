# Reverse

Reverses the order of elements in the list.

The version for working with the entire list.

```
bool Reverse();

```

The version for working with the specified range of list elements.

```
bool Reverse(
   const int  start_index,     // the starting index
   const int  count            // the number of elements
   );

```

Parameters

start_index

[in]  The starting index.

count

[in]  The number of list elements participating in the operation.

Return Value

Returns true on successful, or false otherwise.
