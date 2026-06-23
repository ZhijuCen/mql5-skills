# SymmetricExceptWith

Produces the operation of symmetrical difference between the current collection and a passed collection (array). It modifies the current collection to only contain elements that are present in the source object or in the specified collection (array), but not in both of them.

A version for working with the collection that implements the ICollection<T> interface.

```
void SymmetricExceptWith(
   ICollection<T>*  collection     // collection
   );

```

A version for working with an array.

```
void SymmetricExceptWith(
   T&  array[]                     // array
   );

```

Parameters

*collection

[in]  A collection to produce the symmetrical difference with.

&collection[]

[in]  An array to produce the symmetrical difference with.

Note

The result is written to the current collection (array).
