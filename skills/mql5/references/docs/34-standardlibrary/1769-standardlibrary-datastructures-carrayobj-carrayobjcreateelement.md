# CreateElement

Creates a new array element at the specified position.

```
bool  CreateElement(
   int  index      // position
   )

```

Parameters

index

[in] Position in which you want to create a new element.

Return Value

true - successful, false - cannot create an element.

Note

Method CreateElement (int) in class CArrayObj always returns false and does not perform any action. If necessary, the CreateElement(int) method should be implemented in a derived class.

Example:

```
//--- example for CArrayObj::CreateElement(int)
#include <Arrays\ArrayObj.mqh>
//---
void OnStart()
  {
   int        size=100;
   CArrayObj *array=new CArrayObj;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- fill array
   array.Reserve(size);
   for(int i=0;i<size;i++)
     {
      if(!array.CreateElement(i))
        {
         printf("Element create error");
         delete array;
         return;
        }
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
