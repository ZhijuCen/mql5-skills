# Spectrum

Compute spectrum of a matrix as the set of its eigenvalues from the product AT*A.

```
vector matrix::Spectrum()

```

Return Value

Spectrum of a matrix as a vector of matrix eigenvalues.

Example

```
double MatrixCondSpectral(matrix& a)
  {
   double norm=0.0;
   vector v=a.Spectrum();
 
   if(v.Size()>0)
     {
      double max_norm=v[0];
      double min_norm=v[0];
      for(ulong i=1; i<v.Size(); i++)
        {
         double real=MathAbs(v[i]);
         if(max_norm<real)
            max_norm=real;
         if(min_norm>real)
            min_norm=real;
        }
      max_norm=MathSqrt(max_norm);
      min_norm=MathSqrt(min_norm);
      if(min_norm>0.0)
         norm=max_norm/min_norm;
     }
 
   return(norm);
  }

```
