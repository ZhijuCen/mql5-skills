# CStack<T>

CStack<T> is a generic class that implements the ICollection<T> interface.

### Description

The CStack<T> class is a dynamic collection of T type data, which is organized as a stack that operates on the LIFO (last in, first out) principle.

### Declaration

```
   template<typename T>
   class CStack : public ICollection<T>

```

### Header

```
   #include <Generic\Stack.mqh>

```

```
Inheritance Hierarchy
   ICollection
       CStack

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a stack |
| Count | Returns the number of elements in a stack |
| Contains | Determines whether a stack contains an element with the specified value |
| TrimExcess | Sets the capacity of a stack to the actual number of elements |
| CopyTo | Copies all elements of a stack to the specified array starting at the specified index |
| Clear | Removes all elements from a stack |
| Remove | Removes the first occurrence of the specified element from a stack |
| Push | Adds an element to a stack |
| Peek | Returns the head element without removing it from a stack |
| Pop | Returns the head element and removes it from a stack |
