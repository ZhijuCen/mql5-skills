# Generic Data Collections

The library provides classes and interfaces that define generic collections, which allow users to create strongly typed collections. These collections provide greater convenience and data handling performance than non-generic typed collections.

The library is available in the Include\Generic folder of the terminal working directory.

Objects:

| Object | Description | Type |
| --- | --- | --- |
| ICollection | Interface for implementing generic data collections | INTERFACE |
| IEqualityComparable | Interface for implementing objects that can be compared | INTERFACE |
| IComparable | Interface for implementing objects that can be compared in terms of "greater than, less than or equal to" | INTERFACE |
| IComparer | Interface for implementing a generic class that compares two object of the T type, whether one is "greater than, less than or equal to" the other one | INTERFACE |
| IEqualityComparer | Interface for implementing a generic class that compares two object of the T type for equality | INTERFACE |
| IList | Interface for implementing generic data lists | INTERFACE |
| IMap | Interface for implementing generic collections of key/value pairs | INTERFACE |
| ISet | Interface for implementing generic data sets | INTERFACE |
| CDefaultComparer | A helper class that implements the IComparer<T> generic interface based on Compare global methods | CLASS |
| CDefaultEqualityComparer | A helper class that implements the IEqualityComparer<T> generic interface using Equals<T> and GetHashCode global methods | CLASS |
| CArrayList | A generic class that implements the IList<T> interface | CLASS |
| CKeyValuePair | The class implements the key/value pair | CLASS |
| CHashMap | A generic class that implements the IMap<TKey, TValue> interface | CLASS |
| CHashSet | A generic class that implements the ISet<T> interface | CLASS |
| CLinkedListNode | A helper class for implementing the CLinkedListNode<T> class | CLASS |
| CLinkedList | A generic class that implements the ICollection<T> interface | CLASS |
| CQueue | A generic class that implements the ICollection<T> interface | CLASS |
| CRedBlackTreeNode | A helper class used in implementing the CRedBlackTree<T> class | CLASS |
| CRedBlackTree | A generic class that implements the ICollection<T> interface | CLASS |
| CSortedMap | A generic class that implements the IMap<TKey, TValue> interface | CLASS |
| CSortedSet | A generic class that implements the ISet<T> interface | CLASS |
| CStack | A generic class that implements the ICollection<T> interface | CLASS |

Global methods:

| Method | Description |
| --- | --- |
| ArrayBinarySearch | Searches for the specified value in an ascending-sorted one-dimensional array using the IComparable<T> interface to compare elements |
| ArrayIndexOf | Searches for the first occurrence of a value in a one-dimensional array |
| ArrayLastIndexOf | Searches for the last occurrence of a value in a one-dimensional array |
| ArrayReverse | Changes the sequence of elements in a one-dimensional array |
| Compare | Compares two values, whether one of them is greater than, less than or equal to the other one |
| Equals | Compares two values ​​for equality |
| GetHashCode | Calculates the hash code value |
