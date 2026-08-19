# Insert

Inserts an element to the specified position in the array.

```
bool  Insert(
   char  element,     // element to insert
   int   pos          // position
   )

```

Parameters

element

[in]  Value of the element to be inserted into the array

pos

[in]  Position in the array to insert

Return Value

true - successful, false - cannot insert the element.

Example:

```
//--- example for CArrayChar::Insert(char,int)
#include <Arrays\ArrayChar.mqh>
//---
void OnStart()
  {
   CArrayChar *array=new CArrayChar;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- insert elements
   for(int i=0;i<100;i++)
     {
      if(!array.Insert(i,0))
        {
         printf("Insert error");
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
