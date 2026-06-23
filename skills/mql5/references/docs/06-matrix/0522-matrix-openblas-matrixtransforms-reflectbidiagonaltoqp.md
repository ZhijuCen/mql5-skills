# ReflectBidiagonalToQP

Generates orthogonal matrices Q and P**T (or P**H for complex types) determined by [ReduceToBidiagonal](/en/docs/matrix/openblas/matrixtransforms/reducetobidiagonal) method when reducing a real or complex matrix A to bidiagonal form: A = Q * B * P**T.  Q and P**T are defined as products of elementary reflectors H(i) or G(i) respectively. LAPACK functions [ORGBR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/orgbr.html), [UNGBR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ungbr.html).

As input is used transformed matrix reflect_qp with the same sizes m-by-n as in original matrix A.

Computing for type matrix<double>

```
bool  matrix::ReflectBidiagonalToQP(
   vector&         tau_q,        // scalar factors of the elementary reflectors Q
   vector&         tau_p,        // scalar factors of the elementary reflectors P
   matrix&         Q,            // matrix Q
   matrix&         PT            // transposed matrix P
   );

```

Computing for type matrix<float>

```
bool  matrix::ReflectBidiagonalToQP(
   vectorf&        tau_q,        // scalar factors of the elementary reflectors Q
   vectorf&        tau_p,        // scalar factors of the elementary reflectors P
   matrixf&        Q,            // matrix Q
   matrixf&        PT            // transposed matrix P
   );

```

Computing for type matrix<complex>

```
bool  matrix::ReflectBidiagonalToQP(
   vectorc&        tau_q,        // scalar factors of the elementary reflectors Q
   vectorc&        tau_p,        // scalar factors of the elementary reflectors P
   matrixc&        Q,            // matrix Q
   matrixc&        PH            // hermitian conjugated matrix P
   );

```

Computing for type matrix<complexf>

```
bool  matrix::ReflectBidiagonalToQP(
   vectorcf&       tau_q,        // scalar factors of the elementary reflectors Q
   vectorcf&       tau_p,        // scalar factors of the elementary reflectors P
   matrixcf&       Q,            // matrix Q
   matrixcf&       PH            // hermitian conjugated matrix P
   );

```

Parameters

tau_q

[in] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

tau_p

[in] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix P.

Q

[out]  Orthogonal matrix Q.

PT (PH)

[out]  Transposed (or hermitian conjugated) matrix P.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If m >= n, matrix Q is of m-by-n sizes, matrix PT is of n-by-n sizes.

If m < n, matrix Q is of m-by-m sizes, matrix PT is of m-by-n sizes.
