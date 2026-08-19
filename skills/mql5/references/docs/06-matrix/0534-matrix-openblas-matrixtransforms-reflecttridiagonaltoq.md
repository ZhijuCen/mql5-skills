# ReflectTridiagonalToQ

Generates orthogonal matrix Q  which is defined as the product of n-1 elementary reflectors of order n, as returned by [ReduceSymmetricToTridiagonal](/en/docs/matrix/openblas/matrixtransforms/reducesymmetrictotridiagonal):

in upper case Q = H(n-1) . . . H(2) H(1),

in lower case Q = H(1) H(2) . . . H(n-1).

LAPACK functions [ORGTR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/orgtr.html), [UNGTR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ungtr.html).

As input is used transformed matrix reflect_q with the same sizes n-by-n as in original matrix A.

Computing for type matrix<double>

```
bool  matrix::ReflectTridiagonalToQ(
   vector&         tau_q,        // scalar factors of the elementary reflectors Q
   matrix&         Q             // matrix Q
   );

```

Computing for type matrix<float>

```
bool  matrix::ReflectTridiagonalToQ(
   vectorf&        tau_q,        // scalar factors of the elementary reflectors Q
   matrixf&        Q             // matrix Q
   );

```

Computing for type matrix<complex>

```
bool  matrix::ReflectTridiagonalToQ(
   vectorc&        tau_q,        // scalar factors of the elementary reflectors Q
   matrixc&        Q             // matrix Q
   );

```

Computing for type matrix<complexf>

```
bool  matrix::ReflectTridiagonalToQ(
   vectorcf&       tau_q,        // scalar factors of the elementary reflectors Q
   matrixcf&       Q             // matrix Q
   );

```

Parameters

tau_q

[in] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

Q

[out]  Orthogonal matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
