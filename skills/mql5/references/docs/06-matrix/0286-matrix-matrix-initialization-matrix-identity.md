# Identity

It is a static function which creates an identity matrix of the specified size (not necessarily square). An identity matrix contains ones on the main diagonal and zeros elsewhere. The main diagonal consists of the matrix elements having equal row and column indexes, such as [0,0],[1,1],[2,2] etc. Creates a new identity matrix.

There is also the method Identity that transforms an already existing matrix into an identity one.

```
static matrix matrix::Identity(
  const ulong  rows,        // number of rows
  const ulong  cols,        // number of columns 
   );
 
void matrix::Identity();
 

```

Parameters

rows

[in]  Number of rows (and columns) in n x n matrix.

Return Value

Return the identity matrix. The identity matrix is a square matrix with ones on the main diagonal.

MQL5 example:

```
  matrix identity=matrix::Identity(3,3);
  Print("identity = \n", identity);  
/* 
   identity = 
   [[1,0,0]
    [0,1,0]
    [0,0,1]]
*/
  matrix identity2(3,5);
  identity2.Identity();
  Print("identity2 = \n", identity2);  
/* 
   identity2 = 
   [[1,0,0,0,0]
    [0,1,0,0,0]
    [0,0,1,0,0]]
*/ 

```

Python example:

```
np.identity(3)
array([[1.,  0.,  0.],
       [0.,  1.,  0.],
       [0.,  0.,  1.]])

```
