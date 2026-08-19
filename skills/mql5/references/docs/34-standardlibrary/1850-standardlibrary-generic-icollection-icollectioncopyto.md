# CopyTo

Copies all elements of a collection to the specified array starting at the specified index.

```
int CopyTo(
   T&         dst_array[],     // an array for writing
   const int  dst_start=0      // starting index for writing
   );

```

Parameters

&dst_array[]

[out] An array to which the elements of the collection will be written.

dst_start=0

[in] An index in the array from which copying starts.

Return Value

Returns the number of copied elements.
