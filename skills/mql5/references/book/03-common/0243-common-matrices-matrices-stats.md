# Obtaining statistics

The methods listed below are designed to obtain descriptive statistics for matrices and vectors. All of them apply to a vector or a matrix as a whole, as well as to a given matrix axis (horizontally or vertically). When applied entirely to an object, these functions return a scalar (singular). When applied to a matrix along any of the axes, a vector is returned.

The general appearance of prototypes:

T vector<T>::Method(const vector<T> &v)

T matrix<T>::Method(const matrix<T> &m)

vector<T> matrix<T>::Method(const matrix<T> &m, const int axis)

The list of methods:

- ArgMax, ArgMin: find indexes of maximum and minimum values
- Max, Min: find the maximum and minimum values
- Ptp: find a range of values
- Sum, Prod: calculate the sum or product of elements
- CumSum, CumProd: calculate the cumulative sum or product of elements
- Median, Mean, Average: calculate the median, arithmetic mean, or weighted arithmetic mean
- Std, Var: calculate standard deviation and variance
- Percentile, Quantile: calculate percentiles and quantiles
- RegressionMetric: calculate one of the predefined regression metrics, such as errors of deviation from the regression line on the matrix/vector data

An example of calculating the standard deviation and percentiles for the range of bars (in points) of the current symbol and timeframe is given in the MatrixStdPercentile.mq5 file.

```
input int BarCount = 1000;
input int BarOffset = 0;
   
void OnStart()
{
   // getting current chart quotes
   matrix rates;
   rates.CopyRates(_Symbol, _Period, COPY_RATES_OPEN | COPY_RATES_CLOSE, 
      BarOffset, BarCount);
   // calculating price increments on bars
   vector delta = MathRound((rates.Row(1) - rates.Row(0)) / _Point);
   // debug print of initial bars
   rates.Resize(rates.Rows(), 10);
   Normalize(rates);
   Print(rates);
   // printing increment metrics
   PRTF((int)delta.Std());
   PRTF((int)delta.Percentile(90));
   PRTF((int)delta.Percentile(10));
}

```

Log:

```
(EURUSD,H1)        [[1.00832,1.00808,1.00901,1.00887,1.00728,1.00577,1.00485,1.00652,1.00538,1.00409]
(EURUSD,H1)         [1.00808,1.00901,1.00887,1.00728,1.00577,1.00485,1.00655,1.00537,1.00412,1.00372]]
(EURUSD,H1)        (int)delta.Std()=163 / ok
(EURUSD,H1)        (int)delta.Percentile(90)=170 / ok
(EURUSD,H1)        (int)delta.Percentile(10)=-161 / ok

```
