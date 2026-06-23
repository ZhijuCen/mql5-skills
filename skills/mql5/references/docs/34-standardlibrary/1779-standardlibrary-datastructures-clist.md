# CList

CList Class is a class of dynamic list of instances of the CObject class and its derived classes.

### Description

Class CList provides the ability to work with a list of instances of [CObject](/en/docs/standardlibrary/cobject) and its derived classes. The class allows adding/inserting/deleting array elements, performing an array sorting, and searching in a sorted array. In addition, methods of working with files have been implemented.

There are some subtleties of working with the CList class. The class has a mechanism to control dynamic memory, so be careful when working with elements of the list.

[Subtleties](/en/docs/standardlibrary/datastructures/carrayobj#carrayobjfeatures) of the mechanism of memory management similar to those described in CArrayObj.

### Declaration

```
   class CList : public CObject

```

### Title

```
   #include <Arrays\List.mqh>

```

```
Inheritance hierarchy
   CObject
       CList

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| FreeMode | Gets the flag of memory management when deleting list elements |
| FreeMode | Sets the flag of memory management when deleting list elements |
| Total | Gets the number of elements in the list |
| IsSorted | Gets sorted list flag |
| SortMode | Gets the sorting mode |
| Create methods |  |
| CreateElement | Creates a new list element |
| Add methods |  |
| Add | Adds an element to the end of the list |
| Insert | Inserts an element to the specified position of the list |
| Delete methods |  |
| DetachCurrent | Removes an element from the current position in the list without deleting it "physically" |
| DeleteCurrent | Removes the element from the current position in the list |
| Delete | Removes the element from the specified position in the list |
| Clear | Removes all list elements |
| Navigation |  |
| IndexOf | Gets the index of the specified list element |
| GetNodeAtIndex | Gets an item with the specified index of the list |
| GetFirstNode | Gets the first element of the list |
| GetPrevNode | Gets the previous element of the list |
| GetCurrentNode | Gets the current list element |
| GetNextNode | Gets the next element in the list |
| GetLastNode | Gets the last element in the list |
| Ordering methods |  |
| Sort | Sorts the list |
| MoveToIndex | Moves the current element in the list to the specified position |
| Exchange | Swaps two elements in the list |
| Compare methods |  |
| CompareList | Compares the list with another one |
| Search methods |  |
| Search | Searches for an element equal to the sample in sorted list |
| Input/output |  |
| virtual  Save | Saves list data in the file |
| virtual  Load | Loads list data from the file |
| virtual  Type | Gets the list type identifier |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Compare

```
