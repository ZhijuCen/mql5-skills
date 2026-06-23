# ArrayBinarySearch

Searches for the specified value in an ascending-sorted one-dimensional array using the IComparable<T> interface to compare elements.

```
template<typename T>
int ArrayBinarySearch(
   T&             array[],         // an array for search
   const int      start_index,     // the starting index
   const int      count,           // the search range
   T              value,           // the search value
   IComparer<T>*  comparer         // interface to compare
   );

```

Parameters

&array[]

[out]  The array to search in.

value

[in]  The searched value.

*comparer

[in]  An interface for comparing elements.

start_index

[in] The starting index from which the search begins.

count

[in]  The length of the search range.

Return Value

Returns the index of the found element. If the search value is not found, it returns the index of the smallest element, which is closest in value.
