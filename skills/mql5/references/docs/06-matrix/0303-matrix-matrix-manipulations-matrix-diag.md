# Diag

Extract a diagonal or construct a diagonal matrix.

```
vector matrix::Diag(
  const int     ndiag=0      // number of diagonal
   );
 
void matrix::Diag(
  const vector  v,           // diagonal vector
  const int     ndiag=0      // number of diagonal
   );

```

Parameters

v

[in] A vector whose elements will be contained in the corresponding diagonal (ndiag=0 is the main diagonal).

ndiag=0

[in]  Diagonal in question. The default is 0. Use ndiag>0 for diagonals above the main diagonal, and ndiag<0 for diagonals below the main diagonal.

Note

A diagonal can be set for unallocated matrices (which do not have dimensions). In this case, a zero matrix of the size will be created with the size corresponding to the size of the diagonal vector, after which the vector values will be populated in the corresponding diagonal. If the diagonal is set to an already existing matrix, the matrix dimensions do not change and the values of the matrix elements outside the diagonal vector do not change.

Example

```
   vector v1={1,2,3};
   matrix m1;
   m1.Diag(v1);
   Print("m1\n",m1);
   matrix m2;
   m2.Diag(v1,-1);
   Print("m2\n",m2);
   matrix m3;
   m3.Diag(v1,1);
   Print("m3\n",m3);
   matrix m4=matrix::Full(4,5,9);
   m4.Diag(v1,1);
   Print("m4\n",m4);
   
   Print("diag -1 - ",m4.Diag(-1));
   Print("diag 0 - ",m4.Diag());
   Print("diag 1 - ",m4.Diag(1));
 
  /*
 
  m1
  [[1,0,0]
  [0,2,0]
  [0,0,3]]
  m2
  [[0,0,0]
  [1,0,0]
  [0,2,0]
  [0,0,3]]
  m3
  [[0,1,0,0]
  [0,0,2,0]
  [0,0,0,3]]
  m4
  [[9,1,9,9,9]
  [9,9,2,9,9]
  [9,9,9,3,9]
  [9,9,9,9,9]]
  diag -1 - [9,9,9]
  diag 0 - [9,9,9,9]
  diag 1 - [1,2,3,9]
  */

```
