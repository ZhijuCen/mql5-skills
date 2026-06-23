# ReadIntegerArray

Reads an array of int or uint type variables from file.

```
bool  ReadIntegerArray(
   int&  array[],            // array
   int   start_item=0,       // start element
   int   items_count=-1      // number of elements
   )

```

Parameters

array[]

[in]  Reference to the target array of type int or uint.

start_item=0

[in]  Start element to read from.

items_count=-1

[in]  Number of elements to read (-1 - read to the end of file).

Return Value

true - successful, false - cannot read the data.
