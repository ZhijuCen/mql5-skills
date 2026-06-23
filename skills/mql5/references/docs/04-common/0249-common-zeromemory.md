# ZeroMemory

The function resets a variable passed to it by reference.

```
void  ZeroMemory(
   void & variable      // reset variable
   );

```

Parameters

variable

[in] [out]  Variable passed by reference, you want to reset (initialize by zero values).

Return Value

No return value.

Note

If the function parameter is a string, the call will be equivalent to indicating NULL as its value.  

For simple types and their arrays, as well as for structures/classes consisting of such types, this is a simple reset.  

For objects containing strings and dynamic arrays, ZeroMemory() is called for each element.  

For any arrays not protected by the const modifier, this is the zeroing of all elements.  

For arrays of complex objects, ZeroMemory() is called for each element.

ZeroMemory() can't be applied to classes with protected [members](/en/docs/basis/types/classes#public) or [inheritance](/en/docs/basis/oop/inheritance#protected_inheritance).

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the string
   string str="Test ZeroMemory func";
//--- send the line to the log before applying ZeroMemory() to it
   PrintFormat("The line before applying ZeroMemory() to it: '%s'",str);
//--- reset the string and send the result to the log
   ZeroMemory(str);
   Print("The same line after applying ZeroMemory() to it: '",str,"'");
  /*
   Result:
   The line before applying ZeroMemory() to it: 'Test ZeroMemory func'
   The same line after applying ZeroMemory() to it: ''
  */
 
//--- declare and initialize the variable of int type
   int var=123;
//--- send the line to the log before applying ZeroMemory() to it
   PrintFormat("\nThe integer variable before applying ZeroMemory() to it: %d",var);
//--- reset the variable and send the result to the log
   ZeroMemory(var);
   PrintFormat("The same variable after applying ZeroMemory() to it: %d",var);
  /*
   Result:
   The integer variable before applying ZeroMemory() to it: 123
   The same variable after applying ZeroMemory() to it: 0
  */
 
//--- declare and initialize the array of int type
   int arr[]={0,1,2,3,4,5,6,7,8,9};
//--- send the array to the log before applying ZeroMemory() to it
   Print("\nThe integer array before applying ZeroMemory() to it:");
   ArrayPrint(arr);
//--- reset the array and send the result to the log
   ZeroMemory(arr);
   Print("The same array after applying ZeroMemory() to it:");
   ArrayPrint(arr);
  /*
   Result:
   The integer array before applying ZeroMemory() to it:
   0 1 2 3 4 5 6 7 8 9
   The same array after applying ZeroMemory() to it:
   0 0 0 0 0 0 0 0 0 0
  */
 
//--- declare a structure of two fields - string and integer ones
   struct STest
     {
      string   var_string;
      long     var_long;
     };
//--- declare and initialize the array of STest structure type
   STest arr_struct[]={ {"0",0}, {"1",1}, {"2",2}, {"3",3} };
//--- send the array to the log before applying ZeroMemory() to it
   Print("\nThe array struct before applying ZeroMemory() to it:");
   ArrayPrint(arr_struct);
//--- reset the structure array and send the result to the log
   ZeroMemory(arr_struct);
   Print("The same array struct after applying ZeroMemory() to it:");
   ArrayPrint(arr_struct);
  /*
   Result:
   The array struct before applying ZeroMemory() to it:
       [var_string] [var_long]
   [0] "0"                   0
   [1] "1"                   1
   [2] "2"                   2
   [3] "3"                   3
   The same array struct after applying ZeroMemory() to it:
       [var_string] [var_long]
   [0] null                  0
   [1] null                  0
   [2] null                  0
   [3] null                  0
  */
  }

```
