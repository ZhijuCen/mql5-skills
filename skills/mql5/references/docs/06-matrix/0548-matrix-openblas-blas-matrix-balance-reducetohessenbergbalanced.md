# ReduceToHessenbergBalanced

Reduces a real or complex general n-by-n balanced matrix A to upper Hessenberg form B by an orthogonal similarity transformation: Q**T * A * Q = H. LAPACK function [GEHRD](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gehrd.html).

Computing for type matrix<double>

```
bool  matrix::ReduceToHessenbergBalanced(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   matrix&         H,            // upper Hessenberg matrix
   matrix&         reflect_q,    // q-reflectors
   vector&         tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<float>

```
bool  matrixf::ReduceToHessenbergBalanced(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   matrixf&        H,            // upper Hessenberg matrix
   matrixf&        reflect_q,    // q-reflectors
   vectorf&        tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<complex>

```
bool  matrixc::ReduceToHessenbergBalanced(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   matrixc&        H,            // upper Hessenberg matrix
   matrixc&        reflect_q,    // q-reflectors
   vectorc&        tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::ReduceToHessenbergBalanced(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   matrixcf&       H,            // upper Hessenberg matrix
   matrixcf&       reflect_q,    // q and p-reflectors
   vectorcf&       tau_q         // scalar factors of the elementary reflectors Q
   );

```

Parameters

ilo

[in]  Subscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

ihi

[in]  Superscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

H

[out]  Upper Hessenberg matrix.

reflect_q

[out] Owerwritten balanced matrix A, the elements below the first subdiagonal, with the array tau_q, represent the orthogonal matrix Q as a product of elementary reflectors.

tau_q

[out] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

It is assumed that A is already upper triangular in rows and columns 1:ilo-1 and ihi+1:N. ilo and ihi are normally set by a previous call to [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance); otherwise they should be set to 1 and N respectively.

The matrix Q is represented as a product of (ihi-ilo) elementary  reflectors

Q = H(ilo) H(ilo+1) . . . H(ihi-1).

Each H(i) has the form

H(i) = I - tau * v * v**T

where tau is a real scalar, and v is a real vector with v(1:i) = 0, v(i+1) = 1 and v(ihi+1:n) = 0; v(i+2:ihi) is stored on exit in reflect_q(i+2:ihi,i), and tau in tau_q(i)

The contents of reflect_q are illustrated by the following example, with n = 7, ilo = 2 and ihi = 6:

```
input matrix on entry,           reflect_q on exit,
( a   a   a   a   a   a   a )    ( a   a   h   h   h   h   a )
(     a   a   a   a   a   a )    (     a   h   h   h   h   a )
(     a   a   a   a   a   a )    (     h   h   h   h   h   h )
(     a   a   a   a   a   a )    (     v2  h   h   h   h   h )
(     a   a   a   a   a   a )    (     v2  v3  h   h   h   h )
(     a   a   a   a   a   a )    (     v2  v3  v4  h   h   h )
(                         a )    (                         a )
 

```

where a denotes an element of the original matrix A, h denotes a modified element of the upper Hessenberg matrix H, and vi denotes an element of the vector defining H(i).

Matrix Q can be produced with [ReflectHessenbergBalancedToQ](/en/docs/matrix/openblas/blas_matrix_balance/reflecthessenbergbalancedtoq) method applied to the reflect_q matrix.
