# At

Gets the element from the specified array position.

```
CObject*  At(
   int  pos      // position 
   )

```

Parameters

pos

[in] Position of the desired element in the array.

Return Value

The value of the element - successful, NULL- there was an attempt to get an element of a non-existent position.

Example:

```
//--- example for CArrayObj::At(int)
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
   //--- add elements
   //--- . . .
   for(int i=0;i<array.Total();i++)
     {
      CObject *result=array.At(i);
      if(result==NULL)
        {
         //--- Error reading from array
         printf("Get element error");
         delete array;
         return;
        }
      //--- use element
      //--- . . .
     }
   delete array;
  }

```
