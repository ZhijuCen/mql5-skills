# CLinkedList<T>

CLinkedList<T> is a generic class that implements the ICollection<T> interface.

### Description

The CLinkedList<T> class is an implementation of the dynamic doubly linked data list of the T type. This class provides basic methods to work with doubly linked lists, such as to add, delete, search elements, and others.

### Declaration

```
   template<typename T>
   class CLinkedList : public ICollection<T>

```

### Header

```
   #include <Generic\LinkedList.mqh>

```

```
Inheritance Hierarchy
   ICollection
       CLinkedList

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds an element to a linked list |
| AddAfter | Adds an element after the specified node in the linked list |
| AddBefore | Adds an element before the specified node in the linked list |
| AddFirst | Adds an element at the beginning of the linked list |
| AddLast | Adds an element at the end of the linked list |
| Count | Returns the number of elements in the linked list |
| Head | Returns a pointer to the first node of the linked list |
| First | Returns a pointer to the first node of the linked list |
| Last | Returns a pointer to the last node of the linked list |
| Contains | Determines whether the linked list contains an element with the specified value |
| CopyTo | Copies all elements of the linked list to the specified array starting at the specified index |
| Clear | Removes all elements from a linked list |
| Remove | Removes the first occurrence of the specified element from the linked list |
| RemoveFirst | Removes the first element of the linked list |
| RemoveLast | Removes the last element of the linked list |
| Find | Searches for the first occurrence of the specified value in the linked list |
| FindLast | Searches for the last occurrence of the specified value in the linked list |
