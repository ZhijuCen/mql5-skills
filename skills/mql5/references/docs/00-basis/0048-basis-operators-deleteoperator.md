# Object Delete Operator delete

The delete operator deletes an object created by the [new](/en/docs/basis/operators/newoperator) operator, calls the corresponding class destructor and frees up memory occupied by the object. A real descriptor of an existing object is used as an operand. After the delete operation is executed, the [object descriptor](/en/docs/basis/types/object_pointers) becomes invalid.

Example:

```
      //--- delete figure
      delete m_shape;
      m_shape=NULL;
      //--- create a new figure
      NewShape();

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
