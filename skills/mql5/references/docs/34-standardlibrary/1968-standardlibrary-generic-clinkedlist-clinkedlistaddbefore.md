# AddBefore

Adds an element before the specified node in the linked list.

The version that adds an element by value.

```
CLinkedListNode<T>* AddBefore(
   CLinkedListNode<T>*  node,        // the node before which the element should be added
   T                    value        // the element to add
   );

```

Return Value

Returns a pointer to the added node.

The version that adds an element as a formed node by value.

```
bool AddBefore(
   CLinkedListNode<T>*  node,        // the node before which the element should be added
   CLinkedListNode<T>*  new_node     // the node to be added
   );

```

Parameters

*node

[in] The node of the linked list, before which a new element will be added.

value

[in]  An element to be added.

*new_node

[in]  A node to be added.

Return Value

Returns true on successful, or false otherwise.
