# IndexOf

Searches for the first occurrence of a value in a list.

Version that searches in the entire list.

```
int IndexOf(
   T  item                     // the search value
   );

```

Version that searches from the specified position and to the end of the list.

```
int IndexOf(
   T          item,            // the search value
   const int  start_index      // the starting index
   );

```

Version that searches from the specified position in the specified range.

```
int IndexOf(
   T          item,            // the search value
   const int  start_index,     // the starting index
   const int  count            // the search range
   );

```

Parameters

item

[in]  The searched value.

start_index

[in] The starting index from which the search begins.

count

[in]  The length of the search range.

Return Value

Returns the index of the first found element. If the value is not found, returns -1.
