# ValuesWidth (Get method)

Returns the maximum allowed length in pixels for displaying the axis numbers.

```
int  ValuesWidth()

```

Return Value

Length of the axis numbers in pixels.

Note

If a length in pixels for a specified number exceeds the maximum allowed display length, it is truncated and ends in dots.

# ValuesWidth (Set method)

Sets the maximum allowed length in pixels for displaying the axis numbers.

```
void  ValuesWidth(
   const int  width      // maximum allowed length in pixels
   )

```

Parameters

width

[in]  Maximum allowed length of the axis numbers.

Note

If a length in pixels for a specified number exceeds the maximum allowed display length, it is truncated and ends in dots.
