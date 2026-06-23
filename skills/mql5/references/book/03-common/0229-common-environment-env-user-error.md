# User-defined errors

The developer can use the built-in _LastError variable for their own applied purposes. This is facilitated by the SetUserError function.

void SetUserError(ushort user_error)

The function sets the built-in _LastError variable to the ERR_USER_ERROR_FIRST + user_error value, where ERR_USER_ERROR_FIRST is 65536. All codes below this value are reserved for system errors.

Using this mechanism, you can partially bypass the MQL5 limitation associated with the fact that exceptions are not supported in the language.

Quite often, functions use the return value as a sign of an error. However, there are algorithms where the function must return a value of the application type. Let's talk about double. If the function has a definition range from minus to plus infinity, any value we choose to indicate an error (for example, 0) will be indistinguishable from the actual result of the calculation. In the case of double, of course, there is an option to return a specially constructed NaN value (Not a Number, see section [Checking real numbers for normality](/en/book/common/maths/maths_nan)). But what if the function returns a structure or a class object? One of the possible solutions is to return the result via a parameter by reference or pointer, but such a form makes it impossible to use functions as operands of expressions.

In the context of classes, let's consider the special functions called 'constructors'. They return a new instance of the object. However, sometimes circumstances prevent you from constructing the whole object, and then the calling code seems to get the object but should not use it. It's good if the class can provide an additional method that would allow you to check the usefulness of the object. But as a uniform alternative approach (for example, covering all classes), we can use SetUserError.

In the [Operator overloading](/en/book/oop/classes_and_interfaces/classes_operator_overloading) section, we encountered the Matrix class. We will supplement it with methods for calculating the determinant and inverse matrix, and then use it to demonstrate user errors (see file Matrix.mqh). Overloaded operators were defined for matrices, allowing them to be combined into chains of operators in a single expression, and therefore it would be inconvenient to implement a check for potential errors in it.

Our Matrix class is a custom alternative implementation for the recently added MQL5 built-in object type [matrix](/en/book/common/matrices).

We start by validating input parameters in the Matrix main class constructors. If someone tries to create a zero-size matrix, let's set a custom error ERR_USER_MATRIX_EMPTY (one of several provided).

```
enum ENUM_ERR_USER_MATRIX
{
   ERR_USER_MATRIX_OK = 0, 
   ERR_USER_MATRIX_EMPTY =  1, 
   ERR_USER_MATRIX_SINGULAR = 2, 
   ERR_USER_MATRIX_NOT_SQUARE = 3
};
   
class Matrix
{
   ...
public:
   Matrix(const int r, const int c) : rows(r), columns(c)
   {
      if(rows <= 0 || columns <= 0)
      {
         SetUserError(ERR_USER_MATRIX_EMPTY);
      }
      else
      {
         ArrayResize(m, rows * columns);
         ArrayInitialize(m, 0);
      }
   }

```

These new operations are only defined for square matrices, so let's create a derived class with an appropriate size constraint.

```
class MatrixSquare : public Matrix
{
public:
   MatrixSquare(const int n, const int _ = -1) : Matrix(n, n)
   {
      if(_ != -1 && _ != n)
      {
         SetUserError(ERR_USER_MATRIX_NOT_SQUARE);
      }
   }
   ...

```

The second parameter in the constructor should be absent (it is assumed to be equal to the first one), but we need it because the Matrix class has a template transposition method, in which all types of T must support a constructor with two integer parameters.

```
class Matrix
{
   ...
   template<typename T>
   T transpose() const
   {
      T result(columns, rows);
      for(int i = 0; i < rows; ++i)
      {
         for(int j = 0; j < columns; ++j)
         {
            result[j][i] = this[i][(uint)j];
         }
      }
      return result;
   }

```

Due to the fact that there are two parameters in the MatrixSquare constructor, we also have to check them for mandatory equality. If they are not equal, we set the ERR_USER_MATRIX_NOT_SQUARE error.

Finally, during the calculation of the inverse matrix, we can find that the matrix is degenerate (the determinant is 0). The error ERR_USER_MATRIX_SINGULAR is reserved for this case.

```
class MatrixSquare : public Matrix
{
public:
   ...
   MatrixSquare inverse() const
   {
      MatrixSquare result(rows);
      const double d = determinant();
      if(fabs(d) > DBL_EPSILON)
      {
         result = complement().transpose<MatrixSquare>() * (1 / d);
      }
      else
      {
         SetUserError(ERR_USER_MATRIX_SINGULAR);
      }
      return result;
   }
   
   MatrixSquare operator!() const
   {
      return inverse();
   }
   ...

```

For visual error output, a static method has been added to the log, returning the ENUM_ERR_USER_MATRIX enumeration, which is easy to pass to EnumToString:

```
   static ENUM_ERR_USER_MATRIX lastError()
   {
      if(_LastError >= ERR_USER_ERROR_FIRST)
      {
         return (ENUM_ERR_USER_MATRIX)(_LastError - ERR_USER_ERROR_FIRST);
      }
      return (ENUM_ERR_USER_MATRIX)_LastError;
   }

```

The full code of all methods can be found in the attached file.

We will check application error codes in the test script EnvError.mq5.

First, let's make sure that the class works: invert the matrix and check that the product of the original matrix and the inverted one is equal to the identity matrix.

```
void OnStart()
{
   Print("Test matrix inversion (should pass)");
   double a[9] =
   {
      1,  2,  3, 
      4,  5,  6, 
      7,  8,  0, 
   };
      
   ResetLastError();
   Matrix SquaremA(a);   // assign data to the original matrix
   Print("Input");
   mA.print();
   MatrixSquare mAinv(3);
   mainv = !mA;          // invert and store in another matrix
   Print("Result");
   mAinv.print();
   
   Print("Check inverted by multiplication");
   Matrix Squaretest(3); // multiply the first by the second
   test = mA * mAinv;
   test.print();         // get identity matrix
   Print(EnumToString(Matrix::lastError())); // ok
   ...

```

This code snippet generates the following log entries.

```
Test matrix inversion (should pass)
Input
1.00000 2.00000 3.00000
4.00000 5.00000 6.00000
7.00000 8.00000 0.00000
Result
-1.77778  0.88889 -0.11111
 1.55556 -0.77778  0.22222
-0.11111  0.22222 -0.11111
Check inverted by multiplication
 1.00000 +0.00000  0.00000
 -0.00000   1.00000  +0.00000
0.00000 0.00000 1.00000
ERR_USER_MATRIX_OK

```

Note that in the identity matrix, due to floating point errors, some zero elements are actually very small values close to zero, and therefore they have signs.

Then, let's see how the algorithm handles the degenerate matrix.

```
   Print("Test matrix inversion (should fail)");
   double b[9] =
   {
     -22, -7, 17, 
     -21, 15,  9, 
     -34,-31, 33
   };
   
   MatrixSquare mB(b);
   Print("Input");
   mB.print();
   ResetLastError();
   Print("Result");
   (!mB).print();
   Print(EnumToString(Matrix::lastError())); // singular
   ...

```

The results are presented below.

```
Test matrix inversion (should fail)
Input
-22.00000  -7.00000  17.00000
-21.00000  15.00000   9.00000
-34.00000 -31.00000  33.00000
Result
0.0 0.0 0.0
0.0 0.0 0.0
0.0 0.0 0.0
ERR_USER_MATRIX_SINGULAR

```

In this case, we simply display an error description. But in a real program, it should be possible to choose a continuation option, depending on the nature of the problem.

Finally, we will simulate situations for the two remaining applied errors.

```
   Print("Empty matrix creation");
   MatrixSquare m0(0);
   Print(EnumToString(Matrix::lastError()));
   
   Print("'Rectangular' square matrix creation");
   MatrixSquare r12(1, 2);
   Print(EnumToString(Matrix::lastError()));
}

```

Here we describe an empty matrix and a supposedly square matrix but with different sizes.

```
Empty matrix creation
ERR_USER_MATRIX_EMPTY
'Rectangular' square matrix creation
ERR_USER_MATRIX_NOT_SQUARE

```

In these cases, we cannot avoid creating an object because the compiler does this automatically.

Of course, this test clearly violates contracts (the specifications of data and actions, that classes and methods "consider" as valid). However, in practice, arguments are often obtained from other parts of the code, in the course of processing large, "third-party" data, and detecting deviations from expectations is not that easy.

The ability of a program to "digest" incorrect data without fatal consequences is the most important indicator of its quality, along with producing correct results for correct input data.
