# Overlaps

Determines whether the current sorted set overlaps the specified collection or array.

A version for working with the collection that implements the ICollection<T> interface.

```
bool Overlaps(
   ICollection<T>*  collection     // a collection to compare
   );

```

A version for working with an array.

```
bool Overlaps(
   T&  array[]                     // an array to compare
   );

```

Parameters

*collection

[in]  A collection to determine overlapping.

&collection[]

[in]  An array to determine overlapping.

Return Value

Returns true if the current sorted set and a collection or an array overlap, or false otherwise.
