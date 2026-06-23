# IsProperSubsetOf

Determines whether the current sorted set is a proper subset of the specified collection or array.

A version for working with the collection that implements the ICollection<T> interface.

```
bool IsProperSubsetOf(
   ICollection<T>*  collection     // a collection to determine the relation
   );

```

A version for working with an array.

```
bool IsProperSubsetOf(
   T&  array[]                     // an array to determine the relation
   );

```

Parameters

*collection

[in]  A collection to determine the relation.

&collection[]

[in]  An array to determine the relation.

Return Value

Returns true if the current sorted set is a proper subset, or false otherwise.
