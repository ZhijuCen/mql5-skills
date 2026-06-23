# CDefaultEqualityComparer<T>

CDefaultEqualityComparer<T> is a helper class that implements the IEqualityComparer<T> generic interface based on Equals<T> and GetHashCode global methods.

### Description

The CDefaultEqualityComparer<T> class is used by default in generic data collections, unless the user implicitly uses another class implementing the IEqualityComparer<T> interface.

### Declaration

```
   template<typename T>
   class CDefaultEqualityComparer : public IEqualityComparer<T>

```

### Header

```
   #include <Generic\Internal\DefaultEqualityComparer.mqh>

```

```
Inheritance Hierarchy
   IEqualityComparer
       CDefaultEqualityComparer

```

### Class Methods

| Method | Description |
| --- | --- |
| Equals | Compares two values of type T |
| HashCode | Calculates the hash code value based on the T type object |
