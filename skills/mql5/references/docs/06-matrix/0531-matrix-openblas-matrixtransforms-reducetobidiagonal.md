# ReduceToBidiagonal

Reduces a general real or complex m-by-n matrix A to upper or lower bidiagonal form B by an orthogonal transformation: Q**T * A * P = B. If m >= n, B is upper bidiagonal; if m < n, B is lower bidiagonal. LAPACK function [GEBRD](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gebrd.html).

Computing for type matrix<double>

```
bool  matrix::ReduceToBidiagonal(
   matrix&         B,            // bidiagonal matrix
   matrix&         reflect_qp,   // q and p-reflectors
   vector&         tau_q,        // scalar factors of the elementary reflectors Q
   vector&         tau_p         // scalar factors of the elementary reflectors P
   );

```

Computing for type matrix<float>

```
bool  matrix::ReduceToBidiagonal(
   matrixf&        B,            // bidiagonal matrix
   matrixf&        reflect_qp,   // q and p-reflectors
   vectorf&        tau_q,        // scalar factors of the elementary reflectors Q
   vectorf&        tau_p         // scalar factors of the elementary reflectors P
   );

```

Computing for type matrix<complex>

```
bool  matrix::ReduceToBidiagonal(
   matrixc&        B,            // bidiagonal matrix
   matrixc&        reflect_qp,   // q and p-reflectors
   vectorc&        tau_q,        // scalar factors of the elementary reflectors Q
   vectorc&        tau_p         // scalar factors of the elementary reflectors P
   );

```

Computing for type matrix<complexf>

```
bool  matrix::ReduceToBidiagonal(
   matrixcf&       B,            // bidiagonal matrix
   matrixcf&       reflect_qp,   // q and p-reflectors
   vectorcf&       tau_q,        // scalar factors of the elementary reflectors Q
   vectorcf&       tau_p         // scalar factors of the elementary reflectors P
   );

```

Parameters

B

[out]  Upper or lower bidiagonal matrix.

reflect_qp

[out]  Transformed matrix A. If m >= n, the diagonal and the first superdiagonal are overwritten with the upper bidiagonal matrix B; the elements below the diagonal, with the vector tau_q, represent the orthogonal matrix Q as a product of elementary reflectors, and the elements above the first superdiagonal, with the vector tau_p, represent the orthogonal matrix P as a product of elementary reflectors; if m < n, the diagonal and the first subdiagonal are overwritten with the lower bidiagonal matrix B; the elements below the first subdiagonal, with the vector tau_q, represent the orthogonal matrix Q as a product of elementary reflectors, and the elements above the diagonal, with the vector tau_p, represent the orthogonal matrix P as a product of elementary reflectors.

tau_q

[out] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

tau_p

[out] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix P.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The matrices Q and P are represented as products of elementary reflectors:

If m >= n,

Q = H(1) H(2) . . . H(n)  and  P = G(1) G(2) . . . G(n-1)

Each H(i) and G(i) has the form:

H(i) = I - tauq * v * v**T  and G(i) = I - taup * u * u**T

where tauq and taup are scalars, and v and u are vectors;

v(1:i-1) = 0, v(i) = 1, and v(i+1:m) is stored on exit in A(i+1:m,i);

u(1:i) = 0, u(i+1) = 1, and u(i+2:n) is stored on exit in A(i,i+2:n);

tauq is stored in tau_q(i) and taup in tau_p(i).

If m < n,

Q = H(1) H(2) . . . H(m-1)  and  P = G(1) G(2) . . . G(m)

Each H(i) and G(i) has the form:

H(i) = I - tauq * v * v**T  and G(i) = I - taup * u * u**T

where tauq and taup are scalars, and v and u are vectors;

v(1:i) = 0, v(i+1) = 1, and v(i+2:m) is stored on exit in A(i+2:m,i);

u(1:i-1) = 0, u(i) = 1, and u(i+1:n) is stored on exit in A(i,i+1:n);

tauq is stored in tau_q(i) and taup in tau_p(i).

The contents of A on exit (output matrix reflect_qp) are illustrated by the following examples:

```
m = 6 and n = 5 (m > n):          m = 5 and n = 6 (m < n):
  (  d   e   u1  u1  u1 )           (  d   u1  u1  u1  u1  u1 )
  (  v1  d   e   u2  u2 )           (  e   d   u2  u2  u2  u2 )
  (  v1  v2  d   e   u3 )           (  v1  e   d   u3  u3  u3 )
  (  v1  v2  v3  d   e  )           (  v1  v2  e   d   u4  u4 )
  (  v1  v2  v3  v4  d  )           (  v1  v2  v3  e   d   u5 )
  (  v1  v2  v3  v4  v5 )

```

where d and e denote diagonal and off-diagonal elements of B, vi denotes an element of the vector defining H(i), and ui an element of the vector defining G(i).

Matrices Q and P can be produced with [ReflectBidiagonalToQP](/en/docs/matrix/openblas/matrixtransforms/reflectbidiagonaltoqp) method.
