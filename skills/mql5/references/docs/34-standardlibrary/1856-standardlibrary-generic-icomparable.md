# IComparable<T>

IComparable<T> is an interface for implementing objects that can be compared to find out whether one is greater than, less than or equal to the other one

### Description

The IComparable<T> interface defines a method to compare the current object to another object of the same type, on the basis of which the collection of these objects can be sorted.

### Declaration

```
   template<typename T>
   interface IComparable : public IEqualityComparable<T>

```

### Header

```
   #include <Generic\Interfaces\IComparable.mqh>

```

```
Inheritance Hierarchy
   IEqualityComparable
       IComparable
Direct descendants
CKeyValuePair

```

### Class Methods

| Method | Description |
| --- | --- |
| Compare | Compares the current object with the specified value |
