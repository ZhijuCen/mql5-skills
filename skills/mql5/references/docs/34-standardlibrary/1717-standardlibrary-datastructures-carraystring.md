# CArrayString

CArrayString class is a class of dynamic array of string variables.

### Description

The CArrayString class provides the ability to work with a dynamic array of string variables. The class allows adding/inserting/deleting array elements, performing an array sorting, and searching in a sorted array. In addition, methods of working with files have been implemented.

### Declaration

```
   class CArrayString : public CArray

```

### Title

```
   #include <Arrays\ArrayString.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayString

```

### Class Methods by Groups

| Memory control |  |
| --- | --- |
| Reserve | Allocates memory to increase the size of the array |
| Resize | Sets a new (smaller) size of the array |
| Shutdown | Clears the array with a full memory release |
| Add methods |  |
| Add | Adds an element to the end of the array |
| AddArray | Adds elements of one array to the end of another |
| AddArray | Adds elements of one array to the end of another |
| Insert | Inserts an element to the specified position in the array |
| InsertArray | Inserts to an array elements from another array from the specified position |
| InsertArray | Inserts to an array elements from another array from the specified position |
| AssignArray | Copies the elements of one array to another |
| AssignArray | Copies the elements of one array to another |
| Update methods |  |
| Update | Changes the element at the specified position array |
| Shift | Moves an item from a given position in the array to the specified offset |
| Delete methods |  |
| Delete | Removes the element from the specified array position |
| DeleteRange | Deletes a group of elements from the specified array position |
| Access methods |  |
| At | Gets the element from the specified array position |
| Compare methods |  |
| CompareArray | Compares the array with another one |
| CompareArray | Compares the array with another one |
| Sorted array opetations |  |
| InsertSort | Inserts an element in a sorted array |
| Search | Searches for an element equal to the sample in the sorted array |
| SearchGreat | Searches for an element with a value exceeding the value of the sample in the sorted array |
| SearchLess | Searches for an element with a value less than the value of the sample in the sorted array |
| SearchGreatOrEqual | Searches for an element with a value greater than or equal to the value of the sample in the sorted array |
| SearchLessOrEqual | Searches for an element with a value less than or equal to the value of the sample in the sorted array |
| SearchFirst | Searches for the first element equal to the sample in the sorted array |
| SearchLast | Searches for the last element equal to the sample in the sorted array |
| SearchLinear | Searches for the element equal to the sample in the array |
| Input/output |  |
| virtual  Save | Saves data array in the file |
| virtual  Load | Loads data array from the file |
| virtual  Type | Gets the type identifier of the array |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
