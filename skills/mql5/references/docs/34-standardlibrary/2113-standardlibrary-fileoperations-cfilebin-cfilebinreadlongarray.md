# ReadLongArray

Reads an array of long or ulong type variables from file.

```
bool  ReadLongArray(
   long&  array[],            // array
   int    start_item=0,       // start element
   int    items_count=-1      // number of elements
   )

```

Parameters

array[]

[in]  Reference to the variable for placing read data.

start_item=0

[in]  Start element to read from.

items_count=-1

[in]  Number of elements to read (-1 - read to the end of file).

Return Value

true - successful, false - cannot read the data.
