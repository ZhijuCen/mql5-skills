# WriteCharArray

Writes an array of char or uchar type variables to file.

```
uint  WriteCharArray(
   char&  array[],            // array
   int    start_item=0,       // start element
   int    items_count=-1      // number of elements
   )

```

Parameters

array[]

[in]  Array to write.

start_item=0

[in]  Start element to write from.

items_count=-1

[in]  Number of elements to  write (-1 - whole array).

Return Value

Number of bytes written.
