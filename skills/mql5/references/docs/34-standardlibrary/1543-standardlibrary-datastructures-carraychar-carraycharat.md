# At

Gets the element from the specified array position.

```
char  At(
   int  pos      // position 
   ) const

```

Parameters

pos

[in]  Position of the desired element in the array.

Return Value

The value of the element - success, CHAR_MAX - there was an attempt to get an element from a non-existing position (the last error code is ERR_OUT_OF_RANGE).

Note

Of course, CHAR_MAX may be a valid value of an array element. Therefore, always check the last error code after receiving such a value.

Example:

```
//--- example for CArrayChar::At(int)
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
   //--- add arrays elements
   //--- . . .
   for(int i=0;i<array.Total();i++)
     {
      char result=array.At(i);
      if(result==CHAR_MAX && GetLastError()==ERR_OUT_OF_RANGE)
        {
         //--- error of reading from array
         printf("Get element error");
         delete array;
         return;
        }
      //--- use element
      //--- . . .
     }
   //--- delete array
   delete array;
  }

```
