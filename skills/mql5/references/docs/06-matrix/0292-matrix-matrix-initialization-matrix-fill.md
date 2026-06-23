# Fill

Fill an existing matrix or vector with the specified value.

```
void matrix::Fill(
  const double  value      // value to fill
   );
 
void vector::Fill(
  const double  value      // value to fill
   );

```

Parameters

value

[in]  Value to fill all the matrix elements.

Return Value

No return value. The matrix is filled in place with the specified value.

Example

```
   matrix matrix_a(2,2);
   matrix_a.Fill(10);
   Print("matrix_a\n",matrix_a);
 
/*
  matrix_a
  [[10,10]
   [10,10]]
*/

```
