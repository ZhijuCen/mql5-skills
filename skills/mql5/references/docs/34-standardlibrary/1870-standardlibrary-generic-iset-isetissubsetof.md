# IsSubsetOf

Determines whether the current set is a subset of the specified collection or array.

A version for working with the collection that implements the ICollection<T> interface.

```
bool IsSubsetOf(
   ICollection<T>*  collection     // a collection to determine the relation
   );

```

A version for working with an array.

```
bool IsSubsetOf(
   T&  array[]                     // an array to determine the relation
   );

```

Parameters

*collection

[in]  A collection to determine the relation.

&collection[]

[in]  An array to determine the relation.

Return Value

Returns true if the current set is a subset, or false otherwise.
