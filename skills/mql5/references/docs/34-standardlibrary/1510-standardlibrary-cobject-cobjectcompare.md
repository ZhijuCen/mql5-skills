# Compare

Compares the data on a list element with data on another list element.

```
virtual int  Compare(
   const CObject*  node,     // element
   const int       mode=0    // variant
   ) const

```

Parameters

node

[in]  Pointer to a list element to compare

mode=0

[in]  Comparison variant

Return Value

0 - in case the list elements are equal, -1 - if the list element is less than the element used for comparison (node), 1 - if the list element is greater than the element used for comparison (node).

Note

Compare() method in CObject class always returns 0 and does not perform any action. If you want to compare data in derived class, the Compare(...) method should be implemented. The 'mode' parameter should be used when implementing multivariate comparison.

Example:

```
//--- example for CObject::Compare(...)
#include <Object.mqh>
//---
void OnStart()
  {
   CObject *object_first,*object_second;
   //---
   object_first=new CObject;
   if(object_first==NULL)
     {
      printf("Object create error");
      return;
     }
   object_second=new CObject;
   if(object_second==NULL)
     {
      printf("Object create error");
      delete object_first;
      return;
     }
   //--- set interconnect
   object_first.Next(object_second);
   object_second.Prev(object_first);
   //--- compare objects
   int result=object_first.Compare(object_second);
   //--- delete objects
   delete object_first;
   delete object_second;
  }

```
