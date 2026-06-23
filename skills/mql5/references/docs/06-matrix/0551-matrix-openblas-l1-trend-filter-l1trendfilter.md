# L1TrendFilter

Method for calculating the L1 trend for a data vector. The regularization parameter lambda can be specified either in absolute units (relative=false) or in units of λmax.

Calculations for vector<double> type

```
bool  vector::L1TrendFilter(
   double   lambda,              // value of the regularization parameter lambda
   bool     relative,            // flag indicating that lambda is specified in units of λmax
   vector&  data_result          // vector containing the L1-filtered result
   );

```

Calculations for vector<complex> type

```
bool  vectorf::L1TrendFilter(
   float    lambda,              // value of the regularization parameter lambda
   bool     relative,            // flag indicating that lambda is specified in units of λmax
   vectorf& data_result          // vector containing the L1-filtered result
   );

```

Parameters

lambda

[in]  The value of the regularization parameter lambda. When relative=true, lambda must be in the range from 0 to 1.

relative

[in]  Flag indicating how the regularization parameter lambda is specified. If relative=true, lambda is given in units of λmax; otherwise, lambda is treated as an absolute value.

data_result

[out] A vector containing the result of the L1 filtering.

Return Value

Returns true on success, otherwise false if [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

Memory consumption grows linearly with the size of the vector.
