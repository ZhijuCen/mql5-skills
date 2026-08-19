# L1 Trend Filter

This section provides methods for computing the L1 trend (L1 filtering) of vector data. This approach is used to extract a smooth trend from time series while preserving sharp changes (breakpoints), making it useful for financial and signal analysis.-тренда (L1-фильтрации) данных вектора. Этот подход используется для выделения сглаженного тренда во временных рядах с сохранением резких изменений (изломов), что делает его полезным при анализе финансовых и других сигналов.

The section includes the functions:

- [L1TrendFilterLambdaMax](/en/docs/matrix/openblas/l1_trend_filter/l1trendfilterlambdamax) — computes the maximum value of the regularization parameter λmax for a given vector. This value can be used as a reference when choosing λ.
- [L1TrendFilter](/en/docs/matrix/openblas/l1_trend_filter/l1trendfilter) — performs L1 filtering (trend extraction) using a specified regularization parameter λ.

The parameter λ controls the degree of smoothing:

- small values produce a trend closer to the original data;
- large values result in a smoother trend.

The value of λ can be specified:

- in absolute units;
- relative to λmax, computed in advance using [L1TrendFilterLambdaMax](/en/docs/matrix/openblas/l1_trend_filter/l1trendfilterlambdamax).

All methods operate on vector<double> and vector<float> types, and memory usage grows linearly with the size of the input data.

| Function | Action |
| --- | --- |
| L1TrendFilterLambdaMax | Method for calculating the maximum value of the regularization parameter λmax for a data vector. |
| L1TrendFilter | Method for calculating the L1 trend for a data vector. The regularization parameter lambda can be specified either in absolute units (relative=false) or in units of λmax. |
