# Characteristics of matrices and vectors

The following group of methods can be used to obtain the main characteristics of matrices:

- Rows, Cols: the number of rows and columns in the matrix
- Norm: one of the predefined matrix norms (ENUM_MATRIX_NORM)
- Cond: the condition number of the matrix
- Det: the determinant of a square nondegenerate matrix
- SLogDet: calculates the sign and logarithm of the matrix determinant
- Rank: the rank of the matrix
- Trace: the sum of elements along the diagonals of the matrix (trace)
- Spectrum: the spectrum of a matrix as a set of its eigenvalues

In addition, the following characteristics are defined for vectors:

- Size: the length of the vector
- Norm: one of the predefined vector norms (ENUM_VECTOR_NORM)

The sizes of objects (as well as the indexing of elements in them) use values of the ulong type.

ulong matrix<T>::Rows()

ulong matrix<T>::Cols()

ulong vector<T>::Size()

Most of the other characteristics are real numbers.

double vector<T>::Norm(const ENUM_VECTOR_NORM norm, const int norm_p = 2)

double matrix<T>::Norm(const ENUM_MATRIX_NORM norm)

double matrix<T>::Cond(const ENUM_MATRIX_NORM norm)

double matrix<T>::Det()

double matrix<T>::SLogDet(int &sign)

double matrix<T>::Trace()

The rank and spectrum are, respectively, an integer and a vector.

int matrix<T>::Rank()

vector matrix<T>::Spectrum()

Matrix rank calculation example:

```
matrix a = matrix::Eye(4, 4);
Print("matrix a (eye)\n", a);
Print("a.Rank()=", a.Rank());
   
a[3, 3] = 0;
Print("matrix a (defective eye)\n", a);
Print("a.Rank()=", a.Rank());
   
matrix b = matrix::Ones(1, 4);
Print("b \n", b);
Print("b.Rank()=", b.Rank());
   
matrix zeros = matrix::Zeros(4, 1);
Print("zeros \n", zeros);
Print("zeros.Rank()=", zeros.Rank());

```

And here is the result of the script execution:

```
matrix a (eye)
[[1,0,0,0]
 [0,1,0,0]
 [0,0,1,0]
 [0,0,0,1]]
a.Rank()=4
  
matrix a (defective eye)
[[1,0,0,0]
 [0,1,0,0]
 [0,0,1,0]
 [0,0,0,0]]
a.Rank()=3
  
b
[[1,1,1,1]]
b.Rank()=1
   
zeros
[[0]
 [0]
 [0]
 [0]]
zeros.Rank()=0

```
