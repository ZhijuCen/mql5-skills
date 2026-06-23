# MathBinomialCoefficientLog

Calculates the logarithm of the binomial coefficient: Log(C(n,k))=Log(n!/(k!*(n-k)!))

Version for integer arguments:

```
double  MathBinomialCoefficientLog(
   const int     n,      // the total number of elements
   const int     k       // the number of elements in combination
   )

```

Version for real arguments:

```
double  MathBinomialCoefficientLog(
   const double  n,      // the total number of elements
   const double  k       // the number of elements in combination
   )

```

Parameters

n

[in] The number of elements.

k

[in] The number of elements for each combination.

Return Value

The logarithm of C(n,k).
