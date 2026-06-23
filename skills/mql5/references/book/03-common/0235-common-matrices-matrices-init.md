# Creating and initializing matrices and vectors

There are several ways to declare and initialize matrices and vectors. They can be divided into several categories according to their purpose.

- Declaration without specifying the size
- Declaration with the size specified
- Declaration with initialization
- Static creation methods
- Non-static (re-)configuration and initialization methods

The simplest creation method is a declaration without specifying a size, i.e., without allocating memory for the data. To do this, just specify the type and name of the variable:

```
matrix         matrix_a;   // matrix of type double
matrix<double> matrix_a1;  // double type matrix inside function or class templates
matrix<float>  matrix_a2;  // float matrix
vector         vector_v;   // vector of type double
vector<double> vector_v1;  // another notation of a double-type vector creation
vector<float>  vector_v2;  // vector of type float

```

Then you can change the size of the created objects and fill them with the desired values. They can also be used in built-in matrix and vector methods to get the results of calculations. All of these methods will be discussed by groups in sections within this chapter.

You can declare a matrix or vector with a size specified. This will allocate memory but without any initialization. To do this, after the variable name in parentheses, specify the size(s) (for a matrix, the first one is the number of rows and the second one is the number of columns):

```
matrix         matrix_a(128, 128);      // you can specify as parameters
matrix<double> matrix_a1(nRows, nCols); // both constants and variables
matrix<float>  matrix_a2(nRows, 1);     // analog of column vector
vector         vector_v(256);
vector<double> vector_v1(nSize);
vector<float>  vector_v2(nSize +16);    // expression as a parameter

```

The third way to create objects is by declaration with initialization. The sizes of matrices and vectors in this case are determined by the initialization sequence indicated in curly brackets:

```
matrix         matrix_a = {{0.1, 0.2, 0.3}, {0.4, 0.5, 0.6}};
matrix<double> matrix_a1 =matrix_a;     // must be matrices of the same type
matrix<float>  matrix_a2 = {{1, 2}, {3, 4}};
vector         vector_v = {-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5};
vector<double> vector_v1 = {1, 5, 2.4, 3.3};
vector<float>  vector_v2 =vector_v1;    // must be vectors of the same type

```

There are also static methods for creating matrices and vectors of a specified size with initialization in a certain way (specifically for one or another canonical form). All of them are listed below and have similar prototypes (vectors differ from matrices only in the absence of a second dimension).

static matrix<T> matrix<T>::Eye∫Tri(const ulong rows, const ulong cols, const int diagonal = 0);

static matrix<T> matrix<T>::Identity∫Ones∫Zeros(const ulong rows, const ulong cols);

static matrix<T> matrix<T>::Full(const ulong rows, const ulong cols, const double value);

- Eye constructs a matrix with ones on the specified diagonal and zeros elsewhere
- Tri constructs a matrix with ones on and below the specified diagonal and zeros elsewhere
- Identity constructs an identity matrix of the specified size
- Ones constructs a matrix (or vector) filled with ones
- Zeros constructs a matrix (or vector) filled with zeros
- Full constructs a matrix (or vector) filled with the given value in all elements

If necessary, you can turn any existing matrix into an identity matrix, for which you should apply a non-static method Identity (no parameters).

Let's demonstrate the methods in action:

```
matrix         matrix_a = matrix::Eye(4, 5, 1);
matrix<double> matrix_a1 = matrix::Full(3, 4, M_PI);
matrixf        matrix_a2 = matrixf::Identity(5, 5);
matrixf<float> matrix_a3 = matrixf::Ones(5, 5);
matrix         matrix_a4 = matrix::Tri(4, 5, -1);
vector         vector_v = vector::Ones(256);
vectorf        vector_v1 = vector<float>::Zeros(16);
vector<float>  vector_v2 = vectorf::Full(128, float_value);

```

Additionally, there are non-static methods to initialize a matrix/vector with given values: Init and Fill.

void matrix<T>::Init(const ulong rows, const ulong cols, func_reference rule = NULL, ...)

void matrix<T>::Fill(const T value)

An important advantage of the Init method (which is present for constructors as well) is the ability to specify in the parameters an initializing function for filling the elements of a matrix/vector according to a given law (see example below).

A reference to such a function can be passed after the sizes by specifying its identifier without quotes in the rules parameter (this is not a pointer in the sense of [typedef (*pointer)(...)](/en/book/basis/functions/functions_typedef) and not a string with a name).

The initializing function must have a reference to the object being filled as the first parameter and may also have additional parameters: in this case, the values for them are passed to Init or a constructor after the function reference. If the rule link is not specified, it will simply create a matrix of specified dimensions.

The Init method also allows changing the matrix configuration.

Let's view everything stated above using small examples.

```
matrix m(2, 2);
m.Fill(10);
Print("matrix m \n", m);
/*
  matrix m
  [[10,10]
  [10,10]]
*/
m.Init(4, 6);
Print("matrix m \n", m);
/*
  matrix m
  [[10,10,10,10,0.0078125,32.00000762939453]
  [0,0,0,0,0,0]
  [0,0,0,0,0,0]
  [0,0,0,0,0,0]]
*/

```

Here the Init method was used to resize an already initialized matrix, which resulted in the new elements being filled with random values.

The following function fills the matrix with numbers that increase exponentially:

```
template<typename T>
void MatrixSetValues(matrix<T> &m, const T initial = 1)
{
   T value = initial;
   for(ulong r = 0; r < m.Rows(); r++)
   {
      for(ulong c = 0; c < m.Cols(); c++)
      {
         m[r][c] = value;
         value *= 2;
      }
   }
}

```

Then it can be used to create a matrix.

```
void OnStart()
{
   matrix M(3, 6, MatrixSetValues);
   Print("M = \n", M);
}

```

The execution result is:

```
M = 
[[1,2,4,8,16,32]
 [64,128,256,512,1024,2048]
 [4096,8192,16384,32768,65536,131072]]

```

In this case, the values for the parameter of the initializing function were not specified following its identifier in the constructor call, and therefore the default value (1) was used. But we can, for example, pass a start value of -1 for the same MatrixSetValues, which will fill the matrix with a negative row.

```
   matrix M(3, 6, MatrixSetValues, -1);

```
