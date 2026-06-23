# Matrix product operator @

The @ MQL5 operator implements matrix multiplication according to the rules of linear algebra. It allows multiplying [matrices and vectors](/en/docs/matrix), as well as performing scalar multiplication of vectors.

Supported [element](/en/docs/matrix/matrix_types) types:

- float
- double
- complex<float>
- complex<double>

Important: The element types in the left and right operands must match.

Examples of use

1. Matrix multiplication (matrix × matrix)

```
matrix A(2, 3);
matrix B(3, 2);
matrix C = A @ B; // Result: Matrix C of size [2,2]

```

2. Matrix multiplication (matrix × vector)

```
matrix M(2, 3);
vector V(3);
vector R = M @ V; // Result: Vector R of 2 elements

```

3. Matrix multiplication (vector x matrix)

```
matrix M(2, 3);
vector V(1, 2);
vector R = V @ M; // Result: Vector R of 3 elements

```

4. Scalar multiplication (vector × vector)

```
vector V1(1, 3), V2(1, 3);
double r = V1 @ V2; // Result: Scalar

```

Note

The dimensions must comply with the rules of multiplication: the number of columns in the first operand = the number of rows in the second.

In case of a dimension error, an exception will be triggered at runtime.

Vectors on the left are considered horizontal (1×n).

Vectors on the right are considered vertical (n×1).

The priority of the @ operation corresponds to the priority of multiplication, i.e. for an entry of D=C+A@B, first matrix multiplication T=A@B is performed, followed by the element-wise addition D=C+T.

See also

[MatMul](/en/docs/matrix/matrix_products/matrix_matmul), [GeMM](/en/docs/matrix/matrix_products/matrix_gemm), [Kron](/en/docs/matrix/matrix_products/matrix_kron), [Dot](/en/docs/matrix/matrix_products/matrix_dot),
