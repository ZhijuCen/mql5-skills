# CKeyValuePair<TKey,TValue>

The CKeyValuePair<TKey,TValue> class implements a key/value pair.

### Description

The CKeyValuePair<TKey,TValue> class implements methods for working with the key and the value of the key/value pair.

### Declaration

```
   template<typename TKey, typename TValue>
   class CKeyValuePair : public IComparable<CKeyValuePair<TKey,TValue>*>

```

### Header

```
   #include <Generic\HashMap.mqh>

```

```
Inheritance Hierarchy
   IEqualityComparable
       IComparable
           CKeyValuePair

```

### Class Methods

| Method | Description |
| --- | --- |
| Key | Gets and sets the key in the key/value pair |
| Value | Gets and sets the value in the key/value pair |
| Clone | Creates a new key/value pair whose key and value are equal to the current ones |
| Compare | Compares the current key/value pair to the specified one |
| Equals | Checks whether the current key/value pair and the specified one are equal |
| HashCode | Calculates the hash value based on the key/value pair |
