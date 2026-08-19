# SingularSpectrumAnalysisReconstructComponents

A method function for calculating reconstructed components of the input time series and their contributions.

Calculations for vector<double> type

```
bool  vector::SingularSpectrumAnalysisReconstructComponents(
   ulong    window_length,      // window size for constructing the trajectory matrix
   matrix&  components,         // matrix of reconstructed components
   vector&  contributions       // vector of component contributions to the input series
   );

```

Calculations for vector<float> type

```
bool  vectorf::SingularSpectrumAnalysisReconstructComponents(
   ulong    window_length,      // window size for constructing the trajectory matrix
   matrixf& components,         // matrix of reconstructed components
   vectorf& contributions       // vector of component contributions to the input series
   );

```

Parameters

window_length

[in]  Window size for constructing the trajectory matrix, the number of components the input time series should be decomposed into.

components

[out]  A matrix of reconstructed components, where each column describes a separate component.

contributions

[out]  Vector of component contributions to the input series (eigenvalues of the covariance matrix of the input time series).

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

The window_length parameter value should be less than the size of the input time series. To construct a full-fledged trajectory matrix, the optimal size is considered to be approximately equal to half the size of the input time series.
