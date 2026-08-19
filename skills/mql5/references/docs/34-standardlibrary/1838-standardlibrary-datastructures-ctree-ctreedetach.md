# Detach

Detaches a specified node from a tree.

```
bool  Detach(
   CTreeNode*  node      // node
   )

```

Parameters

node

[in]  Node pointer to detach.

Return Value

true - success, otherwise false.

Note

After detachment, the node pointer is not released. The tree is balanced.
