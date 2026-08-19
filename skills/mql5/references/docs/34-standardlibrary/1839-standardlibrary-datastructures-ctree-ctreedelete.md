# Delete

Deletes a specified node from a tree.

```
bool  Delete(
   CTreeNode*  node      // node
   )

```

Parameters

node

[in]  Node pointer to delete.

Return Value

true - success, otherwise false.

Note

After deletion, a node pointer is released. The tree is balanced.
