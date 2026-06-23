# At

Gets the element from the specified array position.

```
double  At(
   int  pos      // position 
   ) const

```

Parameters

pos

[in] Position of the desired element in the array.

Return Value

The value of the element - success, DBL_MAX - there was an attempt to get an element from a non-existing position (the last error code is ERR_OUT_OF_RANGE).

Note

Of course, DBL_MAX may be a valid value of an array element. Therefore, always check the last error code after receiving such a value.

Example:

```
//--- example for CArrayDouble::At(int)
#include <Arrays\ArrayDouble.mqh>
//---
void OnStart()
  {
   CArrayDouble *array=new CArrayDouble;
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
      double result=array.At(i);
      if(result==DBL_MAX && GetLastError()==ERR_OUT_OF_RANGE)
        {
         //---  Error reading from the array
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
