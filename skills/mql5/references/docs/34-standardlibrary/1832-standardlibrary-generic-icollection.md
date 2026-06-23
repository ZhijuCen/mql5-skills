# ICollection<T>

ICollection<T> is an interface for implementing generic data collections.

### Description

The ICollection<T> interface determines basic methods to work with collections, including methods to count elements, to clear a collection, to add or delete elements, and others.

### Declaration

```
   template<typename T>
   interface ICollection

```

### Header

```
   #include <Generic\Interfaces\ICollection.mqh>

```

```
Inheritance Hierarchy
   ICollection
Direct descendants
CLinkedList, CQueue, CRedBlackTree, CStack, IList, IMap, ISet

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a collection |
| Count | Returns the number of elements in a collection |
| Contains | Determines whether a collection contains an element with the specified value |
| CopyTo | Copies all elements of a collection to the specified array starting at the specified index |
| Clear | Removes all elements from a collection |
| Remove | Removes the first occurrence of the specified element from a collection |
