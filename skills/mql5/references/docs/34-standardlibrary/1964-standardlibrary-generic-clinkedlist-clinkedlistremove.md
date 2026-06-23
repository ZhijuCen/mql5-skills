# Remove

Removes the first occurrence of the specified element from the linked list.

The version that removes an element by value.

```
bool Remove(
   T  item                       // the element value
   );

```

The version that removes an element by a pointer to a node.

```
bool Remove(
   CLinkedListNode<T>*  node     // the element node
   );

```

Parameters

item

[in] The value of the element to be deleted.

*node

[in] The node of the element to be deleted.

Return Value

Returns true on successful, or false otherwise.
