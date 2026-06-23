# QR

Compute the qr factorization of a matrix.

```
bool  QR(
  matrix&  Q,     // matrix with orthonormal columns
  matrix&  R      // upper-triangular matrix
   );

```

Parameters

Q

[out]  A matrix with orthonormal columns. When mode = 'complete' the result is an orthogonal/unitary matrix depending on whether or not a is real/complex. The determinant may be either +/- 1 in that case. In case the number of dimensions in the input array is greater than 2 then a stack of the matrices with above properties is returned.

R key

[out]  Upper triangular matrix.

Return Value

Returns true on success, false otherwise.

Example

```
//---  A*x = b
  matrix A = {{0, 1}, {1, 1}, {1, 1}, {2, 1}};
  Print("A \n", A);
  vector b = {1, 2, 2, 3};
  Print("b \n", b);
//--- A = Q*R
  matrix q, r;
  A.QR(q, r);
  Print("q \n", q);
  Print("r \n", r);
  matrix qr=q.MatMul(r);
  Print("qr \n", qr);
  /* 
  A
  [[0,1]
  [1,1]
  [1,1]
  [2,1]]
  b
  [1,2,2,3]
  q
  [[0.4082482904638631,-0.8164965809277259,-1.110223024625157e-16,-0.4082482904638631]
  [0.4625425214347352,-0.03745747856526496,0.7041241452319315,0.5374574785652647]
  [-0.5374574785652648,-0.03745747856526496,0.7041241452319316,-0.4625425214347352]
  [-0.5749149571305296,-0.5749149571305299,-0.09175170953613698,0.5749149571305296]]
  r
  [[-1.224744871391589,-0.2415816237971962]
  [-1.22474487139159,-1.466326495188786]
  [1.224744871391589,1.316496580927726]
  [1.224744871391589,0.2415816237971961]]
  qr
  [[-1.110223024625157e-16,1]
  [1,0.9999999999999999]
  [1,1]
  [2,1]]
  */

```
