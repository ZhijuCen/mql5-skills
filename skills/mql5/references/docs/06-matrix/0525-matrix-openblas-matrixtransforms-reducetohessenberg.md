# ReduceToHessenberg

Reduces a real or complex general n-by-n matrix A to upper Hessenberg form B by an orthogonal similarity transformation: Q**T * A * Q = H. LAPACK function [GEHRD](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gehrd.html).

Computing for type matrix<double>

```
bool  matrix::ReduceToHessenberg(
   matrix&         H,            // upper Hessenberg matrix
   matrix&         reflect_q,    // q-reflectors
   vector&         tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<float>

```
bool  matrixf::ReduceToHessenberg(
   matrixf&        H,            // upper Hessenberg matrix
   matrixf&        reflect_q,    // q-reflectors
   vectorf&        tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<complex>

```
bool  matrixc::ReduceToHessenberg(
   matrixc&        H,            // upper Hessenberg matrix
   matrixc&        reflect_q,    // q-reflectors
   vectorc&        tau_q         // scalar factors of the elementary reflectors Q
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::ReduceToHessenberg(
   matrixcf&       H,            // upper Hessenberg matrix
   matrixcf&       reflect_q,    // q and p-reflectors
   vectorcf&       tau_q         // scalar factors of the elementary reflectors Q
   );

```

Parameters

H

[out]  Upper Hessenberg matrix.

reflect_q

[out] Owerwritten matrix A, the elements below the first subdiagonal, with the array tau_q, represent the orthogonal matrix Q as a product of elementary reflectors.

tau_q

[out] Vector of the scalar factors of the elementary reflectors which represent the orthogonal matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrix Q can be produced with [ReflectHessenbergToQ](/en/docs/matrix/openblas/matrixtransforms/reflecthessenbergtoq) method.
