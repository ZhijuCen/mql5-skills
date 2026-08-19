# ExceptWith

Produces the operation of difference between the current collection and a passed collection (array). It removes from the current collection (array) all elements that are present in the specified collection (array).

A version for working with the collection that implements the ICollection<T> interface.

```
void ExceptWith(
   ICollection<T>*  collection     // collection
   );

```

A version for working with an array.

```
void ExceptWith(
   T&  array[]                     // array
   );

```

Parameters

*collection

[in]  A collection to be excepted from the current set.

&collection[]

[in]  An array to be excepted from the current set.

Note

The result is written to the current collection (array).
