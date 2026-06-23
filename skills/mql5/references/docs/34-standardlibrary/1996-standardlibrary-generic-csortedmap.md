# CSortedMap<TKey,TValue>

CSortedMap<TKey,TValue> is a generic class that implements the IMap<TKey,TValue> interface.

### Description

The CSortedMap<TKey,TValue> class is an implementation of a dynamic hash table whose data are stored as key/value pairs sorted by key and taking into account the key uniqueness requirement. This class provides basic methods to work with a hash table, such as to access a value by key, to search and delete a key/value pair, and others.

### Declaration

```
   template<typename TKey, typename TValue>
   class CSortedMap : public IMap<TKey, TValue>

```

### Header

```
   #include <Generic\SortedMap.mqh>

```

```
Inheritance Hierarchy
   ICollection
       IMap
           CSortedMap

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds a key/value pair to the hash table |
| Count | Returns the number of elements in the sorted hash table |
| Contains | Determines whether the sorted hash table contains the specified key/value table |
| ContainsKey | Determines whether the sorted hash table contains the key/value table with the specified key |
| ContainsValue | Determines whether the sorted hash table contains the key/value table with the specified value |
| Comparer | Returns a pointer to the IComparer<T> interface, used to organize a sorted hash table |
| CopyTo | Copies all key/value pairs from the sorted hash table to the specified arrays, starting at the specified index |
| Clear | Removes all elements from the sorted hash table |
| Remove | Removes the first occurrence of the key/value pair from the sorted hash table |
| TryGetValue | Gets an element with the specified key from the sorted hash table |
| TrySetValue | Changes a key/value pair with the specified key from the sorted hash table |
