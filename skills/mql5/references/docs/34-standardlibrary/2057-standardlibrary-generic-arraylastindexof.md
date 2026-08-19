# ArrayLastIndexOf

Searches for the last occurrence of a value in a one-dimensional array.

```
template<typename T>
int ArrayLastIndexOf(
   T&         array[],         // an array for search
   T          value,           // the search value
   const int  start_index,     // the starting index
   const int  count            // the search range
   );

```

Parameters

&array[]

[out]  The array to search in.

value

[in]  The searched value.

start_index

[in] The starting index from which the search begins.

count

[in]  The length of the search range.

Return Value

Returns the index of the last found element. If the value is not found, returns -1.
