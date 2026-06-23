# SetEquals

Determines whether the current set contains all elements of the specified collection or array.

A version for working with the collection that implements the ICollection<T> interface.

```
bool SetEquals(
   ICollection<T>*  collection     // a collection to compare
   );

```

A version for working with an array.

```
bool SetEquals(
   T&  array[]                     // an array to compare
   );

```

Parameters

*collection

[in]  A collection to compare elements.

&collection[]

[in]  A collection to compare elements.

Return Value

Returns true if the current set contains all elements of the specified collection or array, or false otherwise.
