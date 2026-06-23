# CArray

CArray class is the base class of a dynamic array of variables.

### Description

Class CArray is intended to operate on dynamic arrays of variables: memory allocation, sorting, and working with files.

### Declaration

```
   class CArray : public CObject

```

### Title

```
   #include <Arrays\Array.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
Direct descendants
CArrayChar, CArrayDouble, CArrayFloat, CArrayInt, CArrayLong, CArrayObj, CArrayShort, CArrayString

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Step | Gets the increment size of the array |
| Step | Sets the increment size of the array |
| Total | Gets the number of elements in the array |
| Available | Gets the number of free elements of the array that are available without additional memory allocation |
| Max | Gets the maximum possible size of the array without memory reallocation |
| IsSorted | Gets the flag of array being sorted using specified sorting mode |
| SortMode | Gets the sorting mode for an array |
| Clear methods |  |
| Clear | Deletes all of the array elements without memory release |
| Sort methods |  |
| Sort | Sorts an array to the specified option |
| Input/output |  |
| virtual  Save | Saves data array in a file |
| virtual  Load | Loads data array from a file |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Type, Compare

```
