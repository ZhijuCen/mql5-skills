# CSortedSet<T>

CSortedSet<T> is a generic class that implements the ISet<T> interface.

### Description

The CSortedSet<T> class is an implementation of the sorted dynamic data set of type T, with the required uniqueness of each value. This class provides basic methods to work with sets and related operations, such as: the union and intersection of sets, definition of strict and non-strict subsets, and others.

### Declaration

```
   template<typename T>
   class CSortedSet : public ISet<T>

```

### Header

```
   #include <Generic\SortedSet.mqh>

```

```
Inheritance Hierarchy
   ICollection
       ISet
           CSortedSet

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a sorted set |
| Count | Returns the number of elements in a sorted set |
| Contains | Determines whether a sorted set contains an element with the specified value |
| Comparer | Returns a pointer to the IComparer<T> interface, used to organize a sorted set |
| TryGetMin | Gets the minimum element from a sorted set |
| TryGetMax | Gets the maximum element from a sorted set |
| CopyTo | Copies all elements of a sorted set to the specified array starting at the specified index |
| Clear | Removes all elements from a sorted set |
| Remove | Removes the occurrence of the specified element from a sorted set |
| ExceptWith | Produces the operation of difference between the current collection and a passed collection (array) |
| IntersectWith | Produces the operation of intersection of the current collection and a passed collection (array) |
| SymmetricExceptWith | Produces the operation of symmetrical difference between the current collection and a passed collection (array) |
| UnionWith | Produces the union of the current collection and a passed collection (array) |
| IsProperSubsetOf | Determines whether the current sorted set is a proper subset of the specified collection or array |
| IsProperSupersetOf | Determines whether the current sorted set is a proper superset of the specified collection or array |
| IsSubsetOf | Determines whether the current sorted set is a subset of the specified collection or array |
| IsSupersetOf | Determines whether the current sorted set is a superset of the specified collection or array |
| Overlaps | Determines whether the current sorted set overlaps the specified collection or array |
| SetEquals | Determines whether the current sorted set contains all elements of the specified collection or array |
| GetViewBetween | Gets from the current sorted set a subset specified by the minimum and maximum values |
| GetReverse | Gets a copy of the current sorted set, in which all the elements are arranged in a reverse order |
