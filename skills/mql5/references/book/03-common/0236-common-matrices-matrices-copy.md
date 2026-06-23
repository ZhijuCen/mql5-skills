# Copying matrices, vectors, and arrays

The simplest and most common way to copy matrices and vectors is through the assignment operator '='.

```
matrix a = {{2, 2}, {3, 3}, {4, 4}};
matrix b = a + 2;
matrix c;
Print("matrix a \n", a);
Print("matrix b \n", b);
c.Assign(b);
Print("matrix c \n", c);

```

This snippet generates the following log entries:

```
matrix a
[[2,2]
 [3,3]
 [4,4]]
matrix b
[[4,4]
 [5,5]
 [6,6]]
matrix c
[[4,4]
 [5,5]
 [6,6]]

```

The Copy and Assign methods can also be used to copy matrices and vectors. The difference between Assign and Copy is that Assign allows you to copy not only matrices but also arrays.

bool matrix<T>::Copy(const matrix<T> &source)

bool matrix<T>::Assign(const matrix<T> &source)

bool matrix<T>::Assign(const T &array[])

Similar methods and prototypes are also available for vectors.

Through Assign, it is possible to write a vector to a matrix: the result will be a one-row matrix.

bool matrix<T>::Assign(const vector<T> &v)

You can also assign a matrix to a vector: it will be unwrapped, i.e., all rows of the matrix will be lined up in one row (equivalent to calling the [Flat](/en/book/common/matrices/matrices_manipulations) method).

bool vector<T>::Assign(const matrix<T> &m)

At the time of writing this chapter, there was no method in MQL5 for exporting a matrix or vector to an array, although there is a mechanism for "transferring" data (see the Swap method further).

The example below shows how an integer array int_arr is copied into a matrix of type double. In this case, the resulting matrix automatically adjusts to the size of the copied array.

```
matrix double_matrix = matrix::Full(2, 10, 3.14);
Print("double_matrix before Assign() \n", double_matrix);
int int_arr[5][5] = {{1, 2}, {3, 4}, {5, 6}};
Print("int_arr: ");
ArrayPrint(int_arr);
double_matrix.Assign(int_arr);
Print("double_matrix after Assign(int_arr) \n", double_matrix);

```

We have the following output in the log.

```
double_matrix before Assign() 
[[3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14]
 [3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14]]
 
int_arr: 
    [,0][,1][,2][,3][,4]
[0,]   1   2   0   0   0
[1,]   3   4   0   0   0
[2,]   5   6   0   0   0
[3,]   0   0   0   0   0
[4,]   0   0   0   0   0
 
double_matrix after Assign(int_arr) 
[[1,2,0,0,0]
 [3,4,0,0,0]
 [5,6,0,0,0]
 [0,0,0,0,0]
 [0,0,0,0,0]]

```

So, the method Assign can be used to switch from arrays to matrices with automatic size and type conversion.

A more efficient (fast and not involving copying) way to transfer data between matrices, vectors, and arrays is to use Swap methods.

bool matrix<T>::Swap(vector<T> &vec)

bool matrix<T>::Swap(matrix<T> &vec)

bool matrix<T>::Swap(T &arr[])

bool vector<T>::Swap(vector<T> &vec)

bool vector<T>::Swap(matrix<T> &vec)

bool vector<T>::Swap(T &arr[])

They work similarly to [ArraySwap](/en/book/common/arrays/arrays_move_swap): Internal pointers to buffers with data inside two objects are swapped. As a result, elements of a matrix or vector disappear in the source object and appear in the receiving array, or, vice versa, they move from the array to the matrix or vector.

The Swap method allows working with dynamic arrays, including multidimensional ones. A certain condition applies to the constant sizes of the highest dimensions of a multidimensional array (array[][N1][N2]...): The product of these dimensions must be a multiple of the size of the matrix or vector. So, an array of [][2][3] is redistributed in blocks of 6 elements. Therefore, it is interchangeable with matrices and vectors of size 6, 12, 18, etc.
