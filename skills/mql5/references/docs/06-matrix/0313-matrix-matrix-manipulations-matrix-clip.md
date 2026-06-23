# Clip

Limit the elements of a matrix/vector to a specified range of valid values.

```
bool matrix::Clip(
  const double  min_value,     // minimum value
  const double  max_value      // maximum value
   );
bool vector::Clip(
  const double  min_value,     // minimum value
  const double  max_value      // maximum value
   );

```

Parameters

min_value

[in]  Minimum value.

max_value

[in] Maximum value.

Return Value

Returns true on success, false otherwise.

Note

The matrix (or vector) is processed in place. No copies are created.

Example

```
   matrix matrix_a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   bool res=matrix_a.Clip(4,8);
   Print("matrix_a\n",matrix_a);
 
  /*
  matrix_a
  [[4,4,4]
   [4,5,6]
   [7,8,8]
   [8,8,8]]
  */

```
