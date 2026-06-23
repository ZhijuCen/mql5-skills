# Manipulating matrices and vectors

When working with matrices and vectors, basic manipulations are available without any calculations. Exclusively matrix methods are provided at the beginning of the list, while the last four methods are also applicable to vectors.

- Transpose: matrix transposition
- Col, Row, Diag: extract and set rows, columns, and diagonals by number
- TriL, TriU: get the lower and upper triangular matrix by the number of the diagonal
- SwapCols, SwapRows: rearrange rows and columns indicated by numbers
- Flat: set and get a matrix element by a through index
- Reshape: reshape a matrix "in place"
- Split, Hsplit, Vsplit: split a matrix into several submatrices
- resize: resize a matrix or vector "in place";
- Compare, CompareByDigits: compare two matrices or two vectors with a given precision of real numbers
- Sort: sort "in place" (permutation of elements) and by getting a vector or matrix of indexes
- clip: limit the range of values of elements "in place"

Note that vector splitting is not provided.

Below are the prototype methods for matrices.

matrix<T> matrix<T>::Transpose()

vector matrix<T>::Col∫Row(const ulong n)

void matrix<T>::Col∫Row(const vector v, const ulong n)

vector matrix<T>::Diag(const int n = 0)

void matrix<T>::Diag(const vector v, const int n = 0)

matrix<T> matrix<T>::TriL∫TriU(const int n = 0)

bool matrix<T>::SwapCols∫SwapRows(const ulong n1, const ulong n2)

T matrix<T>::Flat(const ulong i)

bool matrix<T>::Flat(const ulong i, const T value)

bool matrix<T>::Resize(const ulong rows, const ulong cols, const ulong reserve = 0)

void matrix<T>::Reshape(const ulong rows, const ulong cols)

ulong matrix<T>::Compare(const matrix<T> &m, const T epsilon)

ulong matrix<T>::CompareByDigits(const matrix &m, const int digits)

bool matrix<T>::Split(const ulong nparts, const int axis, matrix<T> &splitted[])

void matrix<T>::Split(const ulong &parts[], const int axis, matrix<T> &splitted[])

bool matrix<T>::Hsplit∫Vsplit(const ulong nparts, matrix<T> &splitted[])

void matrix<T>::Hsplit∫Vsplit(const ulong &parts[], matrix<T> &splitted[])

void matrix<T>::Sort(func_reference compare = NULL, T context)

void matrix<T>::Sort(const int  axis, func_reference compare = NULL, T context)

matrix<T> matrix<T>::Sort(func_reference compare = NULL, T context)

matrix<T> matrix<T>::Sort(const int axis, func_reference compare = NULL, T context)

bool matrix<T>::Clip(const T min, const T max)

For vectors, there is a smaller set of methods.

bool vector<T>::Resize(const ulong size, const ulong reserve = 0)

ulong vector<T>::Compare(const vector<T> &v, const T epsilon)

ulong vector<T>::CompareByDigits(const vector<T> &v, const int digits)

void vector<T>::Sort(func_reference compare = NULL, T context)

vector vector<T>::Sort(func_reference compare = NULL, T context)

bool vector<T>::Clip(const T min, const T max)

Matrix transposition example:

```
matrix a = {{0, 1, 2}, {3, 4, 5}};
Print("matrix a \n", a);
Print("a.Transpose() \n", a.Transpose());
/*
   matrix a
   [[0,1,2]
    [3,4,5]]
   a.Transpose()
   [[0,3]
    [1,4]
    [2,5]]
*/

```

Several examples of setting different diagonals using the Diag method:

```
vector v1 = {1, 2, 3};
matrix m1;
m1.Diag(v1);
Print("m1\n", m1);
/* 
   m1
   [[1,0,0]
    [0,2,0]
    [0,0,3]]
*/
  
matrix m2;
m2.Diag(v1, -1);
Print("m2\n", m2);
/*
   m2
   [[0,0,0]
    [1,0,0]
    [0,2,0]
    [0,0,3]]
*/
  
matrix m3;
m3.Diag(v1, 1);
Print("m3\n", m3);
/*
   m3
   [[0,1,0,0]
    [0,0,2,0]
    [0,0,0,3]]
*/

```

Changing the matrix configuration using Reshape:

```
matrix matrix_a = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}};
Print("matrix_a\n", matrix_a);
/*
   matrix_a
   [[1,2,3]
    [4,5,6]
    [7,8,9]
    [10,11,12]]
*/
  
matrix_a.Reshape(2, 6);
Print("Reshape(2,6)\n", matrix_a);
/*
   Reshape(2,6)
   [[1,2,3,4,5,6]
    [7,8,9,10,11,12]]
*/
  
matrix_a.Reshape(3, 5);
Print("Reshape(3,5)\n", matrix_a);
/*
   Reshape(3,5)
   [[1,2,3,4,5]
    [6,7,8,9,10]
    [11,12,0,3,0]]
*/
  
matrix_a.Reshape(2, 4);
Print("Reshape(2,4)\n", matrix_a);
/*
   Reshape(2,4)
   [[1,2,3,4]
    [5,6,7,8]]
*/

```

We will apply the splitting of matrices into submatrices in an example when [Solving equations](/en/book/common/matrices/matrices_sle).

The Col and Row methods allow not only getting columns or rows of a matrix by their number but also inserting them "in place" into previously defined matrices. In this case, neither the dimensions of the matrix nor the values of elements outside the column vector (for the case Col) or a row vector (for the case Row) will change.

If either of these two methods is applied to a matrix the dimensions of which have not yet been set, then a null matrix of size [N * M] will be created, where N and M are defined differently for Col and Row, based on the length of the vector and the given column or row index:

- For Col, N is the length of the column vector and M is by 1 greater than the specified index of the inserted column
- For Row, N is by 1 greater than the specified index of the inserted row and M is the length of the row vector

At the time of writing this chapter, MQL5 did not provide methods for full-fledged insertion of rows and columns with the expansion of subsequent elements, as well as for excluding specified rows and columns.
