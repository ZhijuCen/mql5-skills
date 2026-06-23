# Object Create Operator new

The new operator automatically creates an object of a corresponding size, calls the object constructor and returns [a descriptor of created object](/en/docs/basis/types/object_pointers). In case of failure, the operator returns a null descriptor that can be compared with the [NULL](/en/docs/basis/types/void) constant.

The new operator can be applied only to [class](/en/docs/basis/types/classes) objects. It can't be applied to structures.

The operator shall not be used to create arrays of objects. To do this, use the [ArrayResize()](/en/docs/array/arrayresize) function.

Example:

```
//+------------------------------------------------------------------+
//| Figure creation                                                  |
//+------------------------------------------------------------------+
void CTetrisField::NewShape()
  {
   m_ypos=HORZ_BORDER;
//--- randomly create one of the 7 possible shapes
   int nshape=rand()%7;
   switch(nshape)
     {
      case 0: m_shape=new CTetrisShape1; break;
      case 1: m_shape=new CTetrisShape2; break;
      case 2: m_shape=new CTetrisShape3; break;
      case 3: m_shape=new CTetrisShape4; break;
      case 4: m_shape=new CTetrisShape5; break;
      case 5: m_shape=new CTetrisShape6; break;
      case 6: m_shape=new CTetrisShape7; break;
     }
//--- draw
   if(m_shape!=NULL)
     {
      //--- pre-settings
      m_shape.SetRightBorder(WIDTH_IN_PIXELS+VERT_BORDER);
      m_shape.SetYPos(m_ypos);
      m_shape.SetXPos(VERT_BORDER+SHAPE_SIZE*8);
      //--- draw
      m_shape.Draw();
     }
//---
  }

```

It should be noted that object descriptor is not a pointer to memory address.

An object created with the new operator must be explicitly removed using the [delete](/en/docs/basis/operators/deleteoperator) operator.

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
