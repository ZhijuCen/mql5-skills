# Types of matrices and vectors

A vector is a one-dimensional array of the real or complex type, while a matrix is a two-dimensional array of the real or complex type. Thus, the list of valid numeric types for the elements of these objects includes double (considered the default type), float, and complex.

From the point of view of linear algebra (but not the compiler!) a prime number is also a minimal vector, and a vector, in turn, can be considered as a special case of a matrix.

The vector, depending on the type of elements, is described using one of the vector (with or without suffix) keywords:

- vector is a vector with elements of type double
- vectorf is a vector with elements of type float
- vectorc is a vector with elements of type complex

Although vectors can be vertical and horizontal, MQL5 does not make such a division. The required orientation of the vector is determined (implied) by the position of the vector in the expression.

The following operations are defined on vectors: addition and multiplication, as well as the Norm (with the relevant [norm](/en/book/common/matrices/matrices_characteristics) method) which gets the vector length or module.

You can think of a matrix as an array, where the first index is the row number and the second index is the column number. However, the numbering of rows and columns, unlike linear algebra, starts from zero, as in arrays.

![Two dimensions of matrices are also called axes and are numbered as follows: 0 for the horizontal axis (along rows) and 1 for the vertical axis (along columns). Axis numbers are used in many matrix functions. In particular, when we talk about splitting a matrix into parts, horizontal splitting means cutting between rows, and vertical splitting means cutting between columns.](pics/matrix.png)

Two dimensions of matrices are also called axes and are numbered as follows: 0 for the horizontal axis (along rows) and 1 for the vertical axis (along columns). Axis numbers are used in many matrix functions. In particular, when we talk about splitting a matrix into parts, horizontal splitting means cutting between rows, and vertical splitting means cutting between columns.

Depending on the type of elements, the matrix is described using one of the matrix (with or without suffix) keywords:

- matrix is a matrix with elements of type double
- matrixf is a matrix with elements of type float
- matrixc is a matrix with elements of type complex

For application in template functions, you can use the notation matrix<double> , matrix<float> , matrix<complex> , vector<double> , vector<float> , vector<complex> instead of the corresponding types.

```
vectorf v_f1 = {0, 1, 2, 3,};
vector<float> v_f2 = v_f1;
matrix m = {{0, 1}, {2, 3}};
 
void OnStart()
{
   Print(v_f2);
   Print(m);
}

```

When logged, matrices and vectors are printed as sequences of numbers separated by commas and enclosed in square brackets.

```
[0,1,2,3]
[[0,1]
 [2,3]]

```

The following algebraic operations are defined for matrices:

- Addition of same-size matrices
- Multiplication of matrices of a suitable size, when the number of columns in the first matrix must be equal to the number of rows in the second matrix
- Multiplication of a matrix by a column vector and multiplication of a row vector by a matrix according to the matrix multiplication rules (a vector is, in this sense, a special case of a matrix)
- Multiplying a matrix by a number

In addition, matrix and vector types have built-in methods that correspond to analogs of the NumPy library (a popular package for machine learning in [Python](/en/book/advanced/python)), so you can get more hints in the documentation and library examples. A complete list of methods can be found in the corresponding section [of MQL5 help](https://www.mql5.com/en/docs/basis/types/matrix_vector).

Unfortunately, MQL5 does not provide for casting matrices and vectors of one type to another (for example, from double to float). Also, a vector is not automatically treated by the compiler as a matrix (with one column or row) in expressions where a matrix is expected. This means that the concept of inheritance (characteristic of OOP) between matrices and vectors does not exist, despite the apparent relationship between these structures.
