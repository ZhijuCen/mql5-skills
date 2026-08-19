# BinarySearch

Searches for the specified value in an ascending-sorted list.

The version that searches in the specified range of values using the class that implements the IComparable<T> interface for comparing elements.

```
int BinarySearch(
   const int      index,       // the starting index
   const int      count,       // the search range
   T              item,        // the search value
   IComparer<T>*  comparer     // interface to compare
   );

```

The version that searches using the class that implements the IComparable<T> interface for comparing elements.

```
int BinarySearch(
   T              item,        // the search value
   IComparer<T>*  comparer     // interface to compare
   );

```

The version that searches using the ::Compare global method for comparing elements.

```
int BinarySearch(
   T  item                     // the search value
   );

```

Parameters

index

[in] The starting index from which the search begins.

count

[in]  The length of the search range.

item

[in]  The searched value.

*comparer

[in]  An interface for comparing elements.

Return Value

Returns the index of the found element. If the search value is not found, it returns the index of the smallest element, which is closest in value.
