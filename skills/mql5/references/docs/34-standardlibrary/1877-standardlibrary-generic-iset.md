# ISet<T>

ISet<T> is an interface for implementing generic data sets.

### Description

The ISet interface defines basic methods to work with sets, such as: the union and intersection of sets, definition of strict and non-strict subsets, and others.

### Declaration

```
   template<typename T>
   interface ISet : public ICollection<T>

```

### Header

```
   #include <Generic\Interfaces\ISet.mqh>

```

```
Inheritance Hierarchy
   ICollection
       ISet
Direct descendants
CHashSet, CSortedSet

```

### Class Methods

| Method | Description |
| --- | --- |
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
