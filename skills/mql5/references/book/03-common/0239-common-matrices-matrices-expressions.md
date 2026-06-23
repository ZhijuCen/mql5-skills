# Evaluation of expressions with matrices and vectors

You can perform mathematical operations element by element (use operators) over matrices and vectors, such as addition, subtraction, multiplication, and division. For these operations, both objects must be of the same type and have the same dimensions. Each member of the matrix/vector interacts with the corresponding element of the second matrix/vector.

As the second term (multiplier, subtrahend, or divisor), you can also use a scalar of the corresponding type (double, float, or complex). In this case, each element of the matrix or vector will be processed taking into account that scalar.

```
matrix matrix_a = {{0.1, 0.2, 0.3}, {0.4, 0.5, 0.6}};
matrix matrix_b = {{1, 2, 3}, {4, 5, 6}};
matrix matrix_c1 = matrix_a + matrix_b;
matrix matrix_c2 = matrix_b - matrix_a;
matrix matrix_c3 = matrix_a * matrix_b;   // Hadamard product (element-by-element)
matrix matrix_c4 = matrix_b / matrix_a;
matrix_c1 = matrix_a + 1;
matrix_c2 = matrix_b - double_value;
matrix_c3 = matrix_a * M_PI;
matrix_c4 = matrix_b / 0.1;
matrix_a += matrix_b;                     // operations "in place" are possible 
matrix_a /= 2;

```

In-place operations modify the original matrix (or vector) by placing the result into it, unlike regular binary operations in which the operands are left unchanged, and a new object is created for the result.

Besides, matrices and vectors can be passed as a parameter to most [mathematical functions](/en/book/common/maths). In this case, the matrix or vector is processed element by element. For example:

```
matrix a = {{1, 4}, {9, 16}};
Print("matrix a=\n", a);
a = MathSqrt(a);
Print("MatrSqrt(a)=\n", a);
/*
   matrix a=
   [[1,4]
    [9,16]]
   MatrSqrt(a)=
   [[1,2]
    [3,4]]
*/

```

In the case of MathMod and MathPow, the second parameter can be either a scalar, or a matrix, or a vector of the appropriate size.
