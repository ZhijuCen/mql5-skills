# UnionWith

Produces the union of the current collection and a passed collection (array). It adds to the current collection (array) missing elements from the specified collection (array).

A version for working with the collection that implements the ICollection<T> interface.

```
void UnionWith(
   ICollection<T>*  collection     // collection
   );

```

A version for working with an array.

```
void UnionWith(
   T&  array[]                     // array
   );

```

Parameters

*collection

[in]  A collection with which the current set will be united.

&collection[]

[in]  An array with which the current set will be united.

Note

The result is written to the current collection (array).
