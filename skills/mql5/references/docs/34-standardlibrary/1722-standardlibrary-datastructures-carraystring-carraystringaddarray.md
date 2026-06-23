# AddArray

Adds elements of one array to the end of another.

```
bool  AddArray(
   const string&  src[]      // source array
   )

```

Parameters

src[]

[in] Reference to an array of source elements to add.

Return Value

true - successful, false - cannot add items.

Example:

```
//--- example for CArrayString::AddArray(const string &[])
#include <Arrays\ArrayString.mqh>
//---
string src[];
//---
void OnStart()
  {
   CArrayString *array=new CArrayString;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- add another array
   if(!array.AddArray(src))
     {
      printf("Array addition error");
      delete array;
      return;
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
