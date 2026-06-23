# CheckPointer

The function returns the type of the object [pointer](/en/docs/basis/types/object_pointers).

```
ENUM_POINTER_TYPE  CheckPointer(
   object* anyobject      // object pointer
   );

```

Parameters

anyobject

[in]  Object pointer.

Return value

Returns a value from the [ENUM_POINTER_TYPE](/en/docs/constants/namedconstants/enum_pointer_type) enumeration.

Note

An attempt to call an incorrect pointer results in the [critical termination](/en/docs/runtime/errors) of a program. That's why it's necessary to call the CheckPointer function before using a pointer. A pointer can be incorrect in the following cases:

- the pointer is equal to [NULL](/en/docs/basis/types/void);
- the object has been deleted using the [delete](/en/docs/basis/operators/deleteoperator) operator.

This function can be used for checking pointer validity. A non-zero value warranties that the pointer can be used for accessing.

To quickly validate the pointer, you can also use operator "!" ([example](/en/docs/basis/types/object_pointers#lnot)) which checks it via an implicit call of the [CheckPointer](/en/docs/common/checkpointer) function.

Example:

```
//+------------------------------------------------------------------+
//| Deletes list by deleting its elements                            |
//+------------------------------------------------------------------+
void CMyList::Destroy()
  {
//--- service pointer for working in the loop
   CItem* item;
//--- go through loop and try to delete dynamic pointers
   while(CheckPointer(m_items)!=POINTER_INVALID)
     {
      item=m_items;
      m_items=m_items.Next();
      if(CheckPointer(item)==POINTER_DYNAMIC)
        {
         Print("Dynamic object ",item.Identifier()," to be deleted");
         delete (item);
        }
      else Print("Non-dynamic object ",item.Identifier()," cannot be deleted");
     }
//---
  }

```

See also

[Object Pointers](/en/docs/basis/types/object_pointers), [Checking the Object Pointer](/en/docs/constants/namedconstants/enum_pointer_type), [Object Delete Operator delete](/en/docs/basis/operators/deleteoperator)
