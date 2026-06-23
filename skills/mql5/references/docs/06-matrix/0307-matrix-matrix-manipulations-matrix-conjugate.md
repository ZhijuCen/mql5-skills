# Conjugate

Changing the sign of the imaginary part of a complex number, return the modified matrix or vector.

```
matrixc matrixc::Conjugate();
 
vectorc vectorc::Conjugate();

```

Return Value

Complex conjugated matrix or vector.

Note

Conjugate can be applied to real (non-complex) matrix or vector. In this case matrix or vector just copied on return.

Simple algorithm of conjugation - method explanation

```
//--- Complex vector conjugation
vectorc VectorConjugate(const vectorc& vector_a)
  {
   //--- create a new vector_c
   vectorc vector_c(vector_a.Size());
 
   //--- go through all values of the new vector
   for(ulong i=0; i<vector_c.Size(); i++)
     {
      //--- transfer the real part of the element
      vector_c[i].real = vector_a[i].real;
      //--- transfer the imaginary part of the element by changing the sign (conjugation)
      vector_c[i].imag = -vector_a[i].imag;
     }
 
    //--- return the conjugated vector
    return(vector_c);
  }

```
