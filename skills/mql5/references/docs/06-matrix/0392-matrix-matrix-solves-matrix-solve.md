# Solve

Solve a linear matrix equation, or system of linear algebraic equations.

```
vector matrix::Solve(
  const vector  b      // ordinate or 'dependent variable' values
   );

```

Parameters

b

[in]  Ordinate or 'dependent variable' values. (Vector of free terms).

Return Value

Vector with solution to the system a * x = b.

Note

If at least one matrix row or column is zero, the system has no solution.

If two or more matrix rows or columns are linearly dependent, the system has no solution.

Example

```
//--- SLAE solution
   vector_x=matrix_a.Solve(vector_b);
//--- check if a * x = b
   result_vector=matrix_a.MatMul(vector_x);
   errors=vector_b.Compare(result_vector,1e-12);

```
