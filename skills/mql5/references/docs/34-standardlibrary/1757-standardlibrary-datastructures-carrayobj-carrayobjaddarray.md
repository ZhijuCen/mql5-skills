# AddArray

Adds elements from one array to the end of another.

```
bool  AddArray(
   const CArrayObj *  src      // pointer to the source array
   )

```

Parameters

src

[in] Pointer to an instance of the [CArrayDouble](/en/docs/standardlibrary/datastructures/carraydouble) class - source of elements to add.

Return Value

true - successful, false - cannot add items.

Note

Adding elements from array to array is actually copying the pointers. Therefore, when calling the method, there is a pitfall - there may be a pointer to a dynamic object in more than one variable.

```
//--- example
extern bool       make_error;
extern int        error;
extern CArrayObj *src;
//--- create a new instance CArrayObj
//--- default memory management is turned on
CArrayObj *array=new CArrayObj;
//--- add (copy) the elements from the source array 
if(array!=NULL)
   bool result=array.AddArray(src);
if(make_error)
  {
   //--- perform erroneous actions 
   switch(error)
     {
      case 0:
         //--- remove the source array without checking its memory management flag 
         delete src;
         //--- result:
         //--- it is possible to address an element by invalid pointer in the receiver array
         break;
      case 1:
         //--- disable the mechanism of memory management in the source array
         if(src.FreeMode()) src.FreeMode(false);
         //--- but do not remove the source array
         //--- result:
         //--- after removing the receiver array, it is possible to address an element by invalid pointer in the source array
         break;
      case 2:
         //--- disable the mechanism of memory management in the source array
         src.FreeMode(false);
         //--- disable the mechanism of memory management in the receiver array 
         array.FreeMode(false);
         //--- result:
         //--- after the program termination, get a "memory leak"
         break;
     }
  }
else
  {
   //--- disable the mechanism of memory management in the source array
   if(src.FreeMode()) src.FreeMode(false);
   //--- delete the source array
   delete src;
   //--- result:
   //--- addressing the receiver array element will be correct
   //--- deleting the receiver array will lead to deleting its elements
  }
 

```

Example:

```
//--- example for CArrayObj::AddArray(const CArrayObj*)
#include <Arrays\ArrayObj.mqh>
//---
void OnStart()
  {
   CArrayObj *array=new CArrayObj;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- create source array
   CArrayObj *src=new CArrayObj;
   if(src==NULL)
     {
      printf("Object create error");
      delete array;
      return;
     }
   //--- reset free mode flag
   src.FreeMode(false);
   //--- fill source array
   //--- . . .
   //--- add another array
   if(!array.AddArray(src))
     {
      printf("Array addition error");
      delete src;
      delete array;
      return;
     }
   //--- delete source array without elements
   delete src;
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
