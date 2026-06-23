# ArrayInitialize

The function initializes a numeric array by a preset value.

For initialization of an array of char type

```
int  ArrayInitialize(
   char    array[],     // initialized array
   char    value        // value that will be set
   );

```

For initialization of an array of short type

```
int  ArrayInitialize(
   short   array[],     // initialized array
   short   value        // value that will be set
   );

```

For initialization of an array of int type

```
int  ArrayInitialize(
   int     array[],     // initialized array
   int     value        // value that will be set
   );

```

For initialization of an array of long type

```
int  ArrayInitialize(
   long    array[],     // initialized array
   long    value        // value that will be set
   );

```

For initialization of an array of float type

```
int  ArrayInitialize(
   float   array[],     // initialized array
   float   value        // value that will be set
   );

```

For initialization of an array of double type

```
int  ArrayInitialize(
   double  array[],     // initialized array
   double  value        // value that will be set
   );

```

For initialization of an array of bool type

```
int  ArrayInitialize(
   bool    array[],     // initialized array
   bool    value        // value that will be set
   );

```

For initialization of an array of uint type

```
int  ArrayInitialize(
   uint    array[],     // initialized array
   uint    value        // value that will be set
   );

```

Parameters

array[]

[out]  Numeric array that should be initialized.

value

[in]  New value that should be set to all array elements.

Return Value

Number of initialized elements.

Note

The [ArrayResize()](/en/docs/array/arrayresize) function allows to set size of an array with a reserve for further expansion without the physical relocation of memory. It is implemented for the better performance, because the operations of memory relocation are reasonably slow.

Initialization of the array using ArrayInitialize(array, init_val) doesn't mean the initialization with the same value of reserve elements allocated for this array. At further expanding of the array using the ArrayResize() function, the elements will be added at the end of the array, their values will be undefined and in most cases will not be equal to init_value.

Example:

```
void OnStart()
  {
//--- dynamic array
   double array[];
//--- let's set the array size for 100 elements and reserve a buffer for another 10 elements
   ArrayResize(array,100,10);
//--- initialize the array elements with EMPTY_VALUE=DBL_MAX value
   ArrayInitialize(array,EMPTY_VALUE);
   Print("Values of 10 last elements after initialization");
   for(int i=90;i<100;i++) printf("array[%d] = %G",i,array[i]);
//--- expand the array by 5 elements
   ArrayResize(array,105);
   Print("Values of 10 last elements after ArrayResize(array,105)");
//--- values of 5 last elements are obtained from reserve buffer
   for(int i=95;i<105;i++) printf("array[%d] = %G",i,array[i]);
  }

```
