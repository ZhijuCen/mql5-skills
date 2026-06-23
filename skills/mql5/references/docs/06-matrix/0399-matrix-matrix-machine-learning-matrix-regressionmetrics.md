# RegressionMetric

Compute the regression metric to evaluate the quality of the predicted data compared to the true data

```
double vector::RegressionMetric(
   const vector&           vector_true,   // vector of true values
   ENUM_REGRESSION_METRIC  metric         // metric type
   );
 
double matrix::RegressionMetric(
   const matrix&           matrix_true,   // matrix of true values
   ENUM_REGRESSION_METRIC  metric         // metric type
);
 
vector matrix::RegressionMetric(
   const matrix&           matrix_true,   // matrix of true values
   ENUM_REGRESSION_METRIC  metric,        // metric type
   int                     axis           // axis
   );

```

Parameters

vector_true/matrix_true

[in]  Vector or matrix of true values.

metric

[in]  Metric type from the [ENUM_REGRESSION_METRIC](/en/docs/matrix/matrix_types/matrix_enumerations#enum_regression_metric) enumeration.

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

The calculated metric which evaluates the quality of the predicted data compared to the true data.

Note

- REGRESSION_MAE — mean absolute error which represents the absolute differences between predicted values and corresponding true values
- REGRESSION_MSE — mean square error which represents the squared differences between predicted values and corresponding true values
- REGRESSION_RMSE — square root of MSE
- REGRESSION_R2 - 1 — MSE(regression) / MSE(mean)
- REGRESSION_MAPE — MAE as a percentage
- REGRESSION_MSPE — MSE as a percentage
- REGRESSION_RMSLE — RMSE computed on a logarithmic scale

Example:

```
   vector y_true = {3, -0.5, 2, 7};
   vector y_pred = {2.5, 0.0, 2, 8};
//---
   double mse=y_pred.RegressionMetric(y_true,REGRESSION_MSE);
   Print("mse=",mse);
//---
   double mae=y_pred.RegressionMetric(y_true,REGRESSION_MAE);
   Print("mae=",mae);
//---
   double r2=y_pred.RegressionMetric(y_true,REGRESSION_R2);
   Print("r2=",r2);
 
  /* Result
   mae=0.375
   mse=0.5
   r2=0.9486081370449679
   */

```
