# SingularSpectrumAnalysisForecast

A method function for calculating reconstructed and predicted data using spectral components of the input time series.

Calculations for vector<double> type

```
bool  vector::SingularSpectrumAnalysisForecast(
   ulong    window_length,         // window size for constructing the trajectory matrix
   ulong    component_count,       // number of components used for forecasting
   ulong    forecast_horizon,      // number of points to forecast
   vector&  forecast               // vector consisting of reconstructed and predicted values
   );

```

Calculations for vector<float> type

```
bool  vectorf::SingularSpectrumAnalysisForecast(
   ulong    window_length,         // window size for constructing the trajectory matrix
   ulong    component_count,       // number of components used for forecasting
   ulong    forecast_horizon,      // number of points to forecast
   vectorf& forecast               // vector consisting of reconstructed and predicted values
   );

```

Parameters

window_length

[in]  Window size for constructing the trajectory matrix, the number of components the input time series should be decomposed into.

component_count

[in]  Number of components used for forecasting.

forecast_horizon

[in]  Number of points to forecast.

forecast

[out]  Combining points reconstructed by component_count plus forecast_horizon points predicted using the first component_count components. Thus, the forecast vector has the size of (T+forecast_horizon), where T is the input series length.

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

The window_length parameter value should be less than the size of the input time series. To construct a full-fledged trajectory matrix, the optimal size is considered to be approximately equal to half the size of the input time series.
