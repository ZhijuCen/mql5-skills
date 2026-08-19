# Sylvester Equations

This section provides functions for solving Sylvester equations of the form A*X + X*B = C, where A and B are square matrices, C is the right-hand side, and X is the unknown solution matrix. The methods support real and complex matrix types (double, float, complex, complexf) and use LAPACK routines such as GEES, TRSYL, and TRSYL3.

The section includes a general solver for arbitrary square matrices, solvers for triangular or Schur-form matrices, and blocked variants optimized for BLAS level 3 computations. Some functions also support transposed or conjugate-transposed operands and a scale factor to avoid overflow in the computed solution.

| Function | Action |
| --- | --- |
| SylvesterEquation | Solves Sylvester equation for real or complex square matrices: A*X + X*B = scale*C where A is m-by-m and B is n-by-n general matrices; the right hand side C and the solution X are m-by-n; and scale is an output scale factor, set <= 1 to avoid overflow in X. LAPACK functions  GEES  and  TRSYL  are used |
| SylvesterEquationTriangular | Solves Sylvester equation for real quasi-triangular or complex triangular matrices:  op(A)*X + X*op(B) = scale*C or op(A)*X - X*op(B) = scale*C where op(A) = A or A**T or A**H, and  A and B are both upper triangular. LAPACK function  TRSYL . |
| SylvesterEquationTriangularBlocked | Solves Sylvester equation for real quasi-triangular or complex triangular matrices:  op(A)*X + X*op(B) = scale*C or op(A)*X - X*op(B) = scale*C where op(A) = A or A**T or A**H, and  A and B are both upper triangular. LAPACK function  TRSYL3 . This is the block (BLAS level 3) version of  TRSYL . Faster up to 5 times but not so accurate. |
| SylvesterEquationSchur | Solves Sylvester equation for real quasi-triangular or complex triangular matrices: A*X + X*B = C where  A and B are both upper triangular. A is m-by-m and B is n-by-n; the right hand side C and the solution X are m-by-n. LAPACK function  TRSYL . |
| SylvesterEquationSchurBlocked | Solves Sylvester equation for real quasi-triangular or complex triangular matrices: A*X + X*B = C where  A and B are both upper triangular. A is m-by-m and B is n-by-n; the right hand side C and the solution X are m-by-n. LAPACK function  TRSYL3 . This is the block (BLAS level 3) version of  TRSYL . Faster up to 5 times but not so accurate. |
