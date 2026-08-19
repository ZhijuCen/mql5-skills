# IList<T>

IList<T> is an interface for implementing generic data lists.

### Description

The IList<T> interface defines basic methods to work with lists, such as to access an element by index, to search and delete elements, sort, and others.

### Declaration

```
   template<typename T>
   interface IList : public ICollection<T>

```

### Header

```
   #include <Generic\Interfaces\IList.mqh>

```

```
Inheritance Hierarchy
   ICollection
       IList
Direct descendants
CArrayList

```

### Class Methods

| Method | Description |
| --- | --- |
| TryGetValue | Gets a list element at the specified index |
| TrySetValue | Changes a value from the list at the specified index |
| Insert | Inserts an element into the list at the specified index |
| IndexOf | Searches for the first occurrence of a value in a list |
| LastIndexOf | Searches for the last occurrence of a value in a list |
| RemoveAt | Removes a list element at the specified index |
