# Complex number (complex)

The built-in complex type is a structure with two [double](/en/docs/basis/types/double) fields:

```
struct complex
  {
   double             real;   // Real part
   double             imag;   // Imaginary part
  };

```

The "complex" type can be passed by value as a parameter for MQL5 functions (in contrast to ordinary structures, which are only passed by reference). For functions imported from DLLs, the "complex" type must be passed only by reference.

The 'i' suffix is used to describe complex constants:

```
complex square(complex c)
  {
   return(c*c);
  }  
void OnStart()
  {
   Print(square(1+2i));  // A constant is passed as a parameter
  }
// "(-3,4)" will be output, which is a string representation of the complex number 

```

Only simple operations are currently available for complex numbers: =, +, -, *, /, +=, -=, *=, /=, ==,!=.

Support for additional mathematical functions will be added later, enabling the calculation of the absolute value, sine, cosine and others.

## vectorc

One-dimensional array of [complex](/en/docs/basis/types/complex) type numbers is meant to handle complex numbers. The vector<complex> entry can be used in template functions. Operations on vectorc type vectors are not implemented yet.

## matrixc

Two-dimensional array of [complex](/en/docs/basis/types/complex) type numbers is meant to handle complex numbers. The matrix<complex> entry can be used in template functions. Operations on matrixc type matrices are not implemented yet.
