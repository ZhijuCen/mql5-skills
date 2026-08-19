# Singular Spectrum Analysis

The section contains functions for decomposing a matrix into three components: orthogonal matrices and a diagonal matrix of singular values. SVD is applied to solve various linear algebra problems such as data dimensionality reduction, image compression, solving systems of equations, as well as data analysis and optimization. The main functions allow calculating singular values and vectors, reconstruct matrices, as well as approximate them with reduced rank accuracy.

| Function | Action |
| --- | --- |
| SingularSpectrumAnalysisSpectrum | A method function for calculating the relative contributions of spectral components based on their eigenvalues. |
| SingularSpectrumAnalysisForecast | A method function for calculating reconstructed and predicted data using spectral components of the input time series. |
| SingularSpectrumAnalysisReconstructComponents | A method function for calculating reconstructed components of the input time series and their contributions. |
| SingularSpectrumAnalysisReconstructSeries | A method function for calculating the reconstructed time series using the first component_count components. |
