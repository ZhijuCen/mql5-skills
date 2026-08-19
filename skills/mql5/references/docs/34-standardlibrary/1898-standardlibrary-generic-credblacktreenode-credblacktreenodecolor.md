# Color (Get method)

Returns a node color.

```
ENUM_RED_BLACK_TREE_NODE_TYPE Color();

```

Return Value

Returns a node color.

# Color (Set method)

Sets the node color.

```
void Color(
   ENUM_RED_BLACK_TREE_NODE_TYPE  clr     // node color
   );

```

Parameters

clr

[in]  Node color.

Note

The color of the node is set using a value from ENUM_RED_BLACK_TREE_NODE_TYPE. It can be of two types:

- RED_BLACK_TREE_NODE_RED — the red color of the node;
- RED_BLACK_TREE_NODE_BLACK — the black color of the node.
