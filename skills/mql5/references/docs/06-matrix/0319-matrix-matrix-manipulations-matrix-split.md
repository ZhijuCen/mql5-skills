# Split

Split a matrix into multiple submatrices.

```
bool matrix::Split(
  const ulong  parts,      // number of submatrices
  const int    axis,       // axis
  matrix&      splitted[]  // array of resulting submatrices
   );
 
void matrix::Split(
  const ulong& parts[],    // sizes of submatrices
  const int    axis,       // axis
  matrix&      splitted[]  // array of resulting submatrices
   );

```

Parameters

parts

[in] The number of submatrices to divide the matrix into.

axis

[in]  Axis. 0 - horizontal axis, 1 - vertical axis.

splitted

[out] Array of resulting submatrices.

Return Value

Returns true on success, false otherwise.

Note

If the number of submatrices is specified, then same size submatrices are obtained. It means that the matrix size (0 - the number of rows, 1 - the number of columns) must be divisible by 'parts' without a remainder. Submatrices of different sizes can be obtained using an array of submatrix sizes. The elements of the size array are used until the entire matrix is divided. If the array of sizes has ended, and the matrix has not yet been completely divided, the undivided remainder will be the last submatrix.

Example

```
   matrix matrix_a={{ 1, 2, 3, 4, 5, 6},
                    { 7, 8, 9,10,11,12},
                    {13,14,15,16,17,18},
                    {19,20,21,22,23,24},
                    {25,26,27,28,29,30}};
   matrix splitted[];
   ulong  parts[]={2,2};
 
   bool res=matrix_a.Split(2,0,splitted);
   Print(res,"  ",GetLastError());
   ResetLastError();
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
   res=matrix_a.Split(2,1,splitted);
   Print(res,"  ",GetLastError());
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
   res=matrix_a.Split(parts,0,splitted);
   Print(res,"  ",GetLastError());
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
  /*
  false  4003
  true  0
  splitted 0
  [[1,2,3]
   [7,8,9]
   [13,14,15]
   [19,20,21]
   [25,26,27]]
  splitted 1
  [[4,5,6]
   [10,11,12]
   [16,17,18]
   [22,23,24]
   [28,29,30]]
  true  0
  splitted 0
  [[1,2,3,4,5,6]
   [7,8,9,10,11,12]]
  splitted 1
  [[13,14,15,16,17,18]
   [19,20,21,22,23,24]]
  splitted 2
  [[25,26,27,28,29,30]]
  */

```
