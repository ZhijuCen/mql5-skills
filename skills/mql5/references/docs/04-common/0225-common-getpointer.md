# GetPointer

The function returns the object [pointer](/en/docs/basis/types/object_pointers).

```
void*  GetPointer(
   any_class anyobject      // object of any class
   );

```

Parameters

anyobject

[in]  Object of any class.

Return Value

The function returns the object pointer.

Note

Only class objects have pointers. Instances of [structures](/en/docs/basis/types/classes) and simple-type variables can't have pointers. The class object not created using the new() operator, but, e.g., automatically created in the array of objects, still has a pointer. But this pointer will be of the automatic type POINTER_AUTOMATIC, therefore the [delete()](/en/docs/basis/operators/deleteoperator) operator can't be applied to it. Aside from that, the type pointer doesn't differ from dynamic pointers of the [POINTER_DYNAMIC](/en/docs/constants/namedconstants/enum_pointer_type) type.

Since variables of structure types and simple types do not have pointers, it's prohibited to apply the GetPointer() function to them. It's also prohibited to pass the pointer as a function argument. In all these cases the compiler will notify an error.

An attempt to call an incorrect pointer causes the [critical termination](/en/docs/runtime/errors) of a program. That's why the [CheckPointer()](/en/docs/common/checkpointer) function should be called prior to using a pointer. A pointer can be incorrect in the following cases:

- the pointer is equal to [NULL](/en/docs/basis/types/void);
- the object has been deleted using the [delete](/en/docs/basis/operators/deleteoperator) operator.

This function can be used to check the validity of a pointer. A non-zero value guarantees, that the pointer can be used for accessing.

Example:

```
//+------------------------------------------------------------------+
//|                                             Check_GetPointer.mq5 |
//|                        Copyright 2009, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2009, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
//+------------------------------------------------------------------+
//| Class implementing the list element                              |
//+------------------------------------------------------------------+
class CItem
  {
   int               m_id;
   string            m_comment;
   CItem*            m_next;
public:
                     CItem() { m_id=0; m_comment=NULL; m_next=NULL; }
                    ~CItem() { Print("Destructor of ",m_id,
                                     (CheckPointer(GetPointer(this))==POINTER_DYNAMIC)?
                                     "dynamic":"non-dynamic"); }
   void              Initialize(int id,string comm) { m_id=id; m_comment=comm; }
   void              PrintMe() { Print(__FUNCTION__,":",m_id,m_comment); }
   int               Identifier() { return(m_id); }
   CItem*            Next() {return(m_next); }
   void              Next(CItem *item) { m_next=item; }
  };
//+------------------------------------------------------------------+
//| Simplest class of the list                                       |
//+------------------------------------------------------------------+
class CMyList
  {
   CItem*            m_items;
public:
                     CMyList() { m_items=NULL; }
                    ~CMyList() { Destroy(); }
    bool             InsertToBegin(CItem* item);
    void             Destroy();
  };
//+------------------------------------------------------------------+
//| Inserts list element at the beginning                            |
//+------------------------------------------------------------------+
bool CMyList::InsertToBegin(CItem* item)
  {
   if(CheckPointer(item)==POINTER_INVALID) return(false);
//---
   item.Next(m_items);
   m_items=item;
//---
   return(true);
  }
//+------------------------------------------------------------------+
//| Deleting the list by deleting elements                           |
//+------------------------------------------------------------------+
void CMyList::Destroy()
  {
//--- service pointer to work in a loop
   CItem* item;
//--- go through the loop and try to delete dynamic pointers
   while(CheckPointer(m_items)!=POINTER_INVALID)
     {
      item=m_items;
      m_items=m_items.Next();
      if(CheckPointer(item)==POINTER_DYNAMIC)
        {
         Print("Dynamyc object ",item.Identifier()," to be deleted");
         delete (item);
        }
      else Print("Non-dynamic object ",item.Identifier()," cannot be deleted");
     }
//---
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   CMyList list;
   CItem   items[10];
   CItem*  item;
//--- create and add into the list a dynamic object pointer
   item=new CItem;
   if(item!=NULL)
     {
      item.Initialize(100,"dynamic");
      item.PrintMe();
      list.InsertToBegin(item);
     }
//--- add automatic pointers into the list
   for(int i=0; i<10; i++)
     {
      items[i].Initialize(i,"automatic");
      items[i].PrintMe();
      item=GetPointer(items[i]);
      if(CheckPointer(item)!=POINTER_INVALID)
         list.InsertToBegin(item);
     }
//--- add one more dynamic object pointer at the list beginning
   item=new CItem;
   if(item!=NULL)
     {
      item.Initialize(200,"dynamic");
      item.PrintMe();
      list.InsertToBegin(item);
     }
//--- delete all the list elements
   list.Destroy();
//--- all the list elements will be deleted after the script is over
//--- see the Experts tab in the terminal
  }

```

See also

[Object Pointers](/en/docs/basis/types/object_pointers), [Checking the Object Pointer](/en/docs/constants/namedconstants/enum_pointer_type), [Object Delete Operator delete](/en/docs/basis/operators/deleteoperator)
