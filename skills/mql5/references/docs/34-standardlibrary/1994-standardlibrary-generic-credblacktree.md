# CRedBlackTree<T>

CRedBlackTree<T> is a generic class that implements the ICollection<T> interface.

### Description

The CRedBlackTree<T> class is an implementation of a dynamic red–black tree whose nodes store T type data. The class provides basic methods to work with red–black trees, such as to add, delete, search for the maximum and minimum value, and more.

### Declaration

```
   template<typename T>
   class CRedBlackTree : public ICollection<T>

```

### Header

```
   #include <Generic\RedBlackTree.mqh>

```

```
Inheritance Hierarchy
   ICollection
       CRedBlackTree

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a red–black tree |
| Root | Returns a pointer to the root of the red–black tree |
| Count | Returns the number of elements in the red–black tree |
| Contains | Determines whether the red–black tree contains an element with the specified value |
| Comparer | Returns a pointer to the IComparer<T> interface used to organize a red–black tree |
| TryGetMin | Gets the minimum element of a red–black tree |
| TryGetMax | Gets the maximum element of a red–black tree |
| CopyTo | Copies all elements of a red–black tree to the specified array starting at the specified index |
| Clear | Removes all elements from a red–black tree |
| Remove | Removes the occurrence of the specified element from a red–black tree |
| RemoveMin | Removes an element with the minimum value from a red–black tree |
| RemoveMax | Removes an element with the maximum value from a red–black tree |
| Find | Searches for the occurrence of a specified value in a red–black tree |
| FindMax | Searches for an element with the maximum value in a red–black tree |
| FindMin | Searches for an element with the minimum value in a red–black tree |
