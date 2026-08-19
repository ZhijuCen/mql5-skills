# CHashMap<TKey, TValue>

CHashMap<TKey, TValue> is a generic class that implements the IMap<TKey, TValue> interface.

### Description

The CHashMap<TKey, TValue> class is an implementation of the dynamic hash table, the data of which are stored in the form of unordered key/value pairs taking into account the key uniqueness requirement. This class provides basic methods to work with a hash table, such as to access a value by key, to search and delete a key/value pair, and others.

### Declaration

```
   template<typename TKey, typename TValue>
   class CHashMap : public IMap<TKey, TValue>

```

### Header

```
   #include <Generic\HashMap.mqh>

```

```
Inheritance Hierarchy
   ICollection
       IMap
           CHashMap

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds a key/value pair to the hash table |
| Count | Returns the number of elements in the hash table |
| Comparer | Returns a pointer to the IEqualityComparer<T> interface, used to organize a hash table |
| Contains | Determines whether the hash table contains the specified key/value pair |
| ContainsKey | Determines whether the hash table contains the key/value pair with the specified key |
| ContainsValue | CHashMap<TKey, TValue> is a generic class that implements the IMap<TKey, TValue> interface |
| CopyTo | Copies all key/value pairs from the hash table to the specified arrays, starting at the specified index |
| Clear | Removes all elements from the hash table |
| Remove | Removes the first occurrence of the key/value pair from the hash table |
| TryGetValue | Gets an element with the specified key from the hash table |
| TrySetValue | Changes the value of a key/value pair from the hash table at the specified key |
