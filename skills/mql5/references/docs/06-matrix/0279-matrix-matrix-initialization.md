# Initialization

There are several ways to declare and initialize matrices and vectors.

| Function | Action |
| --- | --- |
| Assign | Copies a matrix, vector or array with auto cast |
| CopyIndicatorBuffer | Get the data of the specified  indicator  buffer in the specified quantity to a  vector |
| CopyRates | Gets the historical series of the  MqlRates  structure of the specified symbol-period in the specified amount into a matrix or vector |
| CopyTicks | Get ticks from an  MqlTick  structure into a matrix or a vector |
| CopyTicksRange | Get ticks from an  MqlTick  structure into a matrix or a vector within the specified date range |
| Eye | Return a matrix with ones on the diagonal and zeros elsewhere |
| Identity | Create an identity matrix of the specified size |
| Ones | Create and return a new matrix filled with ones |
| Zeros | Create and return a new matrix filled with zeros |
| Full | Create and return a new matrix filled with given value |
| Tri | Construct a matrix with ones at and below the given diagonal and zeros elsewhere |
| Init | Initialize a matrix or a vector |
| Fill | Fill an existing matrix or vector with the specified value |
| Random | Static function. Create and return a new matrix or vector filled with random values. Random values are generated uniformly within the specified range |

Declaration without specifying the size (no memory allocation for the data):

```
  matrix         matrix_a;   // double type matrix
  matrix<double> matrix_a1;  // another way to declare a double matrix; can be used in templates
  matrixf        matrix_a2;  // float matrix
  matrix<float>  matrix_a3;  // float matrix
  vector         vector_a;   // double vector
  vector<double> vector_a1;
  vectorf        vector_a2;  // float vector
  vector<float>  vector_a3;

```

Declaration with the specified size (with memory allocation for the data, but without any initialization):

```
  matrix         matrix_a(128,128);           // the parameters can be either constants
  matrix<double> matrix_a1(InpRows,InpCols);  // or variables
  matrixf        matrix_a2(1,128);            // analog of a horizontal vector
  matrix<float>  matrix_a3(InpRows,1);        // analog of a vertical vector
  vector         vector_a(256);
  vector<double> vector_a1(InpSize);
  vectorf        vector_a2(SomeFunc());       // function SomeFunc returns a number of type ulong, which is used to set the vector size
  vector<float>  vector_a3(InpSize+16);       // expression can be used as a parameter

```

Declaration with initialization (matrix and vector sizes are determined by the initializing sequence):

```
  matrix         matrix_a={{0.1,0.2,0.3},{0.4,0.5,0.6}};
  matrix<double> matrix_a1=matrix_a;                      // must be matrices of the same type
  matrixf        matrix_a2={{1,0,0},{0,1,0},{0,0,1}};
  matrix<float>  matrix_a3={{1,2},{3,4}};
  vector         vector_a={-5,-4,-3,-2,-1,0,1,2,3,4,5};
  vector<double> vector_a1={1,5,2.4,3.3};
  vectorf        vector_a2={0,1,2,3};
  vector<float>  vector_a3=vector_a2;                     // must be vectors of the same type

```

Declaration with initialization:

```
template<typename T>
void MatrixArange(matrix<T> &mat,T value=0.0,T step=1.0)
  {
   for(ulong i=0; i<mat.Rows(); i++)
     {
      for(ulong j=0; j<mat.Cols(); j++,value+=step)
         mat[i][j]=value;
     }
  }
template<typename T>
void VectorArange(vector<T> &vec,T value=0.0,T step=1.0)
  {
   for(ulong i=0; i<vec.Size(); i++,value+=step)
      vec[i]=value;
  }
...
 
  matrix  matrix_a(size_m,size_k,MatrixArange,-M_PI,0.1); // first an uninitialized matrix sized size_m x size_k is created, then function MatrixArange with the parameters specified at initialization is called
  matrixf matrix_a1(10,20,MatrixArange);                  // after creating the matrix, function MatrixArange with default parameters is called
  vector  vector_a(size,VectorArange,-10.0);              // after creating the vector, function VectorArange with one parameter is called while the second parameter is default
  vectorf vector_a1(128,VectorArange);

```

Please note that the matrix or vector dimensions can be changed, since the memory for data is always dynamic.

### Static methods

Static methods for creating matrices and vectors of the specified size, initialized in a certain way:

```
  matrix         matrix_a =matrix::Eye(4,5,1);
  matrix<double> matrix_a1=matrix::Full(3,4,M_PI);
  matrixf        matrix_a2=matrixf::Identity(5,5);
  matrixf<float> matrix_a3=matrixf::Ones(5,5);
  matrix         matrix_a4=matrix::Tri(4,5,-1);
  vector         vector_a =vector::Ones(256);
  vectorf        vector_a1=vector<float>::Zeros(16);
  vector<float>  vector_a2=vectorf::Full(128,float_value);

```

Methods for initializing already created matrices and vectors:

```
  matrix  matrix_a;
  matrix_a.Init(size_m,size_k,MatrixArange,-M_PI,0.1);
  matrixf matrix_a1(3,4);
  matrix_a1.Init(10,20,MatrixArange);
  vector  vector_a;
  vector_a.Init(128,VectorArange);
  vectorf vector_a1(10);
  vector_a1.Init(vector_size,VectorArange,start_value,step);
 
  matrix_a.Fill(double_value);
  vector_a1.Fill(FLT_MIN);
  matrix_a1.Identity();

```
