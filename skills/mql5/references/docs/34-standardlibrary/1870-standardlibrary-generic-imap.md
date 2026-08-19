# IMap<TKey, TValue>

IMap<TKey, TValue> is an interface for implementing generic collections of key/value pairs.

### Description

The IMap<TKey, TValue> interface defines basic methods to work with collections whose data are stored as key/value pairs.

### Declaration

```
   template<typename TKey, typename TValue>
   interface IMap : public ICollection<TKey>

```

### Header

```
   #include <Generic\Interfaces\IMap.mqh>

```

```
Inheritance Hierarchy
   ICollection
       IMap
Direct descendants
CHashMap, CSortedMap

```

### Class Methods

| Method | Description |
| --- | --- |
| Add | Adds a key/value pair to a collection |
| Contains | Determines whether a collection contains the key/value table with the specified key |
| Remove | Removes the first occurrence of a key/value pair from a collection |
| TryGetValue | Gets an element with the specified key from a collection |
| TrySetValue | Changes the value of the key/value pair from a collection at the specified key |
| CopyTo | Copies all key/value pairs from a collection to specified arrays, starting at the specified index |
