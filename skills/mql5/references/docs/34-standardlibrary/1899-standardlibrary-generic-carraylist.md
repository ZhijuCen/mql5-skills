# CArrayList<T>

CArrayList<T> is a generic class that implements the IList<T> interface.

### Description

The CArrayList<T> class is an implementation of the dynamic data list of the T type. This class provides the basic methods to work with the list, such as to access an element by index, to search and delete elements, sort, and others.

### Declaration

```
   template<typename T>
   class CArrayList : public IList<T>

```

### Header

```
   #include <Generic\ArrayList.mqh>

```

```
Inheritance Hierarchy
   ICollection
       IList
           CArrayList

```

### Class Methods

| Method | Description |
| --- | --- |
| Capacity | Gets and sets the current capacity of a list |
| Count | Returns the number of elements in the list |
| Contains | Determines whether a list contains an element with the specified value |
| TrimExcess | Sets the capacity of a list to the actual number of elements |
| TryGetValue | Gets an element of the list at the specified index |
| TrySetValue | Sets the value of the list element at the specified index |
| Add | Adds an element to the list |
| AddRange | Adds a collection or an array of elements to the list |
| Insert | Inserts an element into the list at the specified index |
| InsertRange | Inserts a collection or an array of elements into the list at the specified index |
| CopyTo | Copies all elements of a list to the specified array starting at the specified index |
| BinarySearch | Searches for the specified value in an ascending-sorted list |
| IndexOf | Searches for the first occurrence of a value in a list |
| LastIndexOf | Searches for the last occurrence of a value in a list |
| Clear | Removes all elements from a collection |
| Remove | Removes the first occurrence of the specified element from the list |
| RemoveAt | Removes an element at the specified index of the list |
| RemoveRange | Removes a range of elements from the list |
| Reverse | Reverses the order of elements in the list |
| Sort | Sorts elements in the list |
