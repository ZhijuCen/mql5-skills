# CHashSet<T>

CHashSet<T> is a generic class that implements the ISet<T> interface.

### Description

The CHashSet<T> class is an implementation of the unordered dynamic data set of type T, with the required uniqueness of each value. This class provides basic methods to work with sets and related operations, such as: the union and intersection of sets, definition of strict and non-strict subsets, and others.

### Declaration

```
   template<typename T>
   class CHashSet : public ISet<T>

```

### Header

```
   #include <Generic\HashSet.mqh>

```

```
Inheritance Hierarchy
   ICollection
       ISet
           CHashSet

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a set |
| Count | Returns the number of elements in a set |
| Comparer | Determines whether a set contains an element with the specified value |
| Contains | Returns a pointer to the IEqualityComparer<T> interface, used to organize a set |
| TrimExcess | Sets the capacity of a set to the actual number of elements, and thus frees up unused memory |
| CopyTo | Copies all elements of a set to the specified array starting at the specified index |
| Clear | Removes all elements from a set |
| Remove | Removes the specified element from a set |
| ExceptWith | Produces the operation of difference between the current collection and a passed collection (array) |
| IntersectWith | Produces the operation of intersection of the current collection and a passed collection (array) |
| SymmetricExceptWith | Produces the operation of symmetrical difference between the current collection and a passed collection (array) |
| UnionWith | Produces the union of the current collection and a passed collection (array) |
| IsProperSubsetOf | Determines whether the current set is a proper subset of the specified collection or array |
| IsProperSupersetOf | Determines whether the current set is a proper superset of the specified collection or array |
| IsSubsetOf | Determines whether the current set is a subset of the specified collection or array |
| IsSupersetOf | Determines whether the current set is a superset of the specified collection or array |
| Overlaps | Determines whether the current set overlaps the specified collection or array |
| SetEquals | Determines whether the current set contains all elements of the specified collection or array |
