# InsertRange

Inserts a collection or an array of elements into the list at the specified index.

The version that inserts an array.

```
bool InsertRange(
   const int  index,               // index to insert at
   const T&   array[]              // an array to be inserted
   );

```

The version that inserts a collection.

```
bool InsertRange(
   const int        index,         // index to insert at
   ICollection<T>*  collection     // a collection to be inserted
   );

```

Parameters

index

[in]  The index to insert at.

&array[]

[in] An array to be inserted at the specified index.

*collection

[in] A collection to be inserted at the specified index.

Return Value

Returns true on successful, or false otherwise.
