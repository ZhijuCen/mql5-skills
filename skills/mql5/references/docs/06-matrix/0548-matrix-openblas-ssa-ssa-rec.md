# SingularSpectrumAnalysisReconstructSeries

A method function for calculating the reconstructed time series using the first component_count components.

Calculations for vector<double> type

```
bool  vector::SingularSpectrumAnalysisReconstructSeries(
   ulong    window_length,       // window size for constructing the trajectory matrix
   ulong    component_count,     // number of components used for reconstruction
   vector&  reconstructed        // reconstructed time series
   );

```

Calculations for vector<float> type

```
bool  vectorf::SingularSpectrumAnalysisReconstructSeries(
   ulong    window_length,       // window size for constructing the trajectory matrix
   ulong    component_count,     // number of components used for reconstruction
   vectorf& reconstructed        // reconstructed time series
   );

```

Parameters

window_length

[in]  Window size for constructing the trajectory matrix, the number of components the input time series should be decomposed into.

component_count

[out]  Number of components used for time series reconstruction.

reconstructed

[out]  Vector containing the reconstructed output series.

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

The window_length parameter value should be less than the size of the input time series. To construct a full-fledged trajectory matrix, the optimal size is considered to be approximately equal to half the size of the input time series.
