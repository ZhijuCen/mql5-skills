# Sort

Sorts elements in the list.

The version that sorts all elements in the list.

```
bool Sort();

```

The version that sorts all elements in the list using the class that implements the IComparable<T> interface for comparing elements.

```
bool Sort(
   IComparer<T>*  comparer         // interface for comparing
   );

```

The version that sorts the specified range of elements in the list using the class that implements the IComparable<T> interface for comparing elements.

```
bool Sort(
   const int  start_index,     // the starting index
   const int  count            // the number of elements
   IComparer<T>*  comparer     // interface to compare
   );

```

Parameters

*comparer

[in]  An interface for comparing elements.

start_index

[in] The starting index from which sorting begins.

count

[in]  The length of the sorting range.

Return Value

Returns true on successful, or false otherwise.
