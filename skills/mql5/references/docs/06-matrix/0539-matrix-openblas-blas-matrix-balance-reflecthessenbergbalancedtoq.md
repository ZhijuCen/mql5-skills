# ReflectHessenbergBalancedToQ

Generates orthogonal matrix Q  which is defined as the product of ihi-ilo elementary reflectors of order n, as returned by [ReduceToHessenbergBalanced](/en/docs/matrix/openblas/blas_matrix_balance/reducetohessenbergbalanced):

Q = H(ilo) H(ilo+1) . . . H(ihi-1).

LAPACK function [ORGHR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/orghr.html).

As input is used transformed matrix reflect_q with the same sizes n-by-n as in original matrix A.

Computing for type matrix<double>

```
bool  matrix::ReflectHessenbergBalancedToQ(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   vector&         tau_q,        // scalar factors of the elementary reflectors Q
   matrix&         Q             // matrix Q
   );

```

Computing for type matrix<float>

```
bool  matrix::ReflectHessenbergBalancedToQ(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   vectorf&        tau_q,        // scalar factors of the elementary reflectors Q
   matrixf&        Q             // matrix Q
   );

```

Computing for type matrix<complex>

```
bool  matrix::ReflectHessenbergBalancedToQ(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   vectorc&        tau_q,        // scalar factors of the elementary reflectors Q
   matrixc&        Q             // matrix Q
   );

```

Computing for type matrix<complexf>

```
bool  matrix::ReflectHessenbergBalancedToQ(
   long            ilo,          // subscript of balanced matrix
   long            ihi,          // superscript of balanced matrix
   vectorcf&       tau_q,        // scalar factors of the elementary reflectors Q
   matrixcf&       Q             // matrix Q
   );

```

Parameters

ilo

[in]  Subscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

ihi

[in]  Superscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

tau_q

[in] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

Q

[out]  Orthogonal matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
