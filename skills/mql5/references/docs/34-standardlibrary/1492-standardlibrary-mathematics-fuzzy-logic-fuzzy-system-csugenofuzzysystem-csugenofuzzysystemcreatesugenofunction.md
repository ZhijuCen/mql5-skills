# CreateSugenoFunction

Creates a linear Sugeno function for the system.

```
CLinearSugenoFunction*  CreateSugenoFunction(
   const string  name,          // function name
   const double& coeffs[]       // function ratios
   )

```

Parameters

name

[in]  Function name.

coeffs[]

[in]  Function ratios.

Return Value

Linear Sugeno function.

Note

The size of the ratio array may be equal to a number of inputs or exceed that number by one. In the first case, the free term of the Sugeno linear function is equal to zero, while in the second case, it is equal to the last ratio.

# CreateSugenoFunction

Creates a linear Sugeno function for the system.

```
CLinearSugenoFunction*  CreateSugenoFunction(
   const string  name,          // function name
   CList*&       coeffs,        // list of pairs fuzzy variable - its ratio
   const double  constValue     // function free term ratio
   )

```

Parameters

name

[in]  Function name.

coeffs[]

[in]  Function ratios.

Return Value

Linear Sugeno function.
