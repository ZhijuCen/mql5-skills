# CRedBlackTreeNode<T>

CRedBlackTreeNode<T> is a helper class used in implementing the CRedBlackTree<T> class.

### Description

The CRedBlackTreeNode<T> class is a node of the CRedBlackTree<T>. Tree navigation methods are implemented in the class.

### Declaration

```
   template<typename T>
   class CRedBlackTreeNode

```

### Header

```
   #include <Generic\RedBlackTree.mqh>

```

### Class Methods

| Method | Description |
| --- | --- |
| Value | Returns and sets a node value |
| Parent | Returns and sets a pointer to the parent node |
| Left | Returns and sets a pointer to the left node |
| Right | Returns and sets a pointer to the right node |
| Color | Returns and sets a node color |
| IsLeaf | Determines whether the specified node is a leaf |
| CreateEmptyNode | Creates a new black node with no parent and children, and returns a pointer to it |
