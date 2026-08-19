# IntersectWith

Produces the operation of intersection of the current collection and a passed collection (array). It modifies the current collection to only contain elements that are present in the specified collection (array).

A version for working with the collection that implements the ICollection<T> interface.

```
void IntersectWith(
   ICollection<T>*  collection     // collection
   );

```

A version for working with an array.

```
void IntersectWith(
   T&  array[]                     // array
   );

```

Parameters

*collection

[in]  A collection with which the current set will be intersected.

&collection[]

[in]  An array with which the current set will be intersected.

Note

The result is written to the current collection (array).
