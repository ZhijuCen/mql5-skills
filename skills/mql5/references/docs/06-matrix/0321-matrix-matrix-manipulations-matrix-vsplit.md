# Vsplit

Split a matrix vertically into multiple submatrices. Same as Split with axis=1

```
bool matrix::Vsplit(
  const ulong  parts,      // number of submatrices
  matrix&      splitted[]  // array of resulting submatrices
   );
 
void matrix::Vsplit(
  const ulong& parts[],    // sizes of submatrices
  matrix&      splitted[]  // array of resulting submatrices
   );

```

Parameters

parts

[in] The number of submatrices to divide the matrix into.

splitted

[out] Array of resulting submatrices.

Return Value

Returns true on success, false otherwise.

Note

If the number of submatrices is specified, then same size submatrices are obtained. It means that the number of columns must be divisible by 'parts' without a remainder. Submatrices of different sizes can be obtained using an array of submatrix sizes. The elements of the size array are used until the entire matrix is divided. If the array of sizes has ended, and the matrix has not yet been completely divided, the undivided remainder will be the last submatrix.

Example

```
   matrix matrix_a={{ 1, 2, 3, 4, 5, 6},
                    { 7, 8, 9,10,11,12},
                    {13,14,15,16,17,18}};
   matrix splitted[];
   ulong  parts[]={2,3};
 
   matrix_a.Vsplit(2,splitted);
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
   matrix_a.Vsplit(3,splitted);
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
   matrix_a.Vsplit(parts,splitted);
   for(uint i=0; i<splitted.Size(); i++)
      Print("splitted ",i,"\n",splitted[i]);
 
 
  /*
     splitted 0
     [[1,2,3]
      [7,8,9]
      [13,14,15]]
     splitted 1
     [[4,5,6]
      [10,11,12]
      [16,17,18]]
 
     splitted 0
     [[1,2]
      [7,8]
      [13,14]]
     splitted 1
     [[3,4]
      [9,10]
      [15,16]]
     splitted 2
     [[5,6]
      [11,12]
      [17,18]]
 
     splitted 0
     [[1,2]
      [7,8]
      [13,14]]
     splitted 1
     [[3,4,5]
      [9,10,11]
      [15,16,17]]
     splitted 2
     [[6]
      [12]
      [18]]
 
  */

```
