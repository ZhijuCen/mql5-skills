# Subfunctions

Group of functions that perform basic mathematical operations: calculation of the gamma function, beta function, factorial, exponential, logarithms with different bases, square root, etc.

They provide the ability to process both individual numeric values (real and integer) and arrays of such values (with output of the results to a separate or the original array).

| Function | Description |
| --- | --- |
| MathRandomNonZero | Returns a random number with a floating point in the range from 0.0 to 1.0. |
| MathMoments | Calculates the first 4 moments of array elements: mean, variance, skewness, kurtosis. |
| MathPowInt | Raises a number to the specified integer power. |
| MathFactorial | Calculates the factorial of the specified integer. |
| MathTrunc | Calculates the integer part of the specified number or array elements. |
| MathRound | Rounds a number or an array of numbers to the specified number of decimal places. |
| MathArctan2 | Calculates the angle, the tangent of which is equal to the ratio of the two specified numbers in the range of [-pi, pi]. |
| MathGamma | Calculates the value of the gamma function. |
| MathGammaLog | Calculates the logarithm of the gamma function. |
| MathBeta | Calculates the value of the beta function. |
| MathBetaLog | Calculates the logarithm of the beta function. |
| MathBetaIncomplete | Calculates the value of the incomplete beta function. |
| MathGammaIncomplete | Calculates the value of the incomplete gamma function. |
| MathBinomialCoefficient | Calculates the binomial coefficient. |
| MathBinomialCoefficientLog | Calculates the logarithm of the binomial coefficient. |
| MathHypergeometric2F2 | Calculates the value of the hypergeometric function. |
| MathSequence | Generates a sequence based on values: the first element, the last element, the step of the sequence. |
| MathSequenceByCount | Generates a sequence based on values: the first element, the last element, the number of elements in the sequence. |
| MathReplicate | Generates a repeating sequence of values. |
| MathReverse | Generates an array of values with reverse order of elements. |
| MathIdentical | Compares two arrays of values and returns true if all elements match. |
| MathUnique | Generates an array with unique values only. |
| MathQuickSortAscending | Function for sorting in ascending order. |
| MathQuickSortDescending | Function for sorting in descending order. |
| MathQuickSort | Function for sorting. |
| MathOrder | Generates an array with permutation according to order of the array elements after sorting. |
| MathBitwiseNot | Calculates the result of bitwise NOT operation for array elements. |
| MathBitwiseAnd | Calculates the result of bitwise AND operation for elements of arrays. |
| MathBitwiseOr | Calculates the result of bitwise OR operation for elements of arrays. |
| MathBitwiseXor | Calculates the result of bitwise XOR operation for elements of arrays. |
| MathBitwiseShiftL | Calculates the result of bitwise SHL operation for array elements. |
| MathBitwiseShiftR | Calculates the result of bitwise SHR operation for array elements. |
| MathCumulativeSum | Generates an array with the cumulative sums. |
| MathCumulativeProduct | Generates an array with the cumulative products. |
| MathCumulativeMin | Generates an array with the cumulative minima. |
| MathCumulativeMax | Generates an array with the cumulative maxima. |
| MathSin | Calculates the values of the sin(x) function for array elements. |
| MathCos | Calculates the values of the cos(x) function for array elements. |
| MathTan | Calculates the values of the tan(x) function for array elements. |
| MathArcsin | Calculates the values of the arcsin(x) function for array elements. |
| MathArccos | Calculates the values of the arccos(x) function for array elements. |
| MathArctan | Calculates the values of the arctan(x) function for array elements. |
| MathSinPi | Calculates the values of the sin(pi*x) function for array elements. |
| MathCosPi | Calculates the values of the cos(pi*x) function for array elements. |
| MathTanPi | Calculates the values of the tan(pi*x) function for array elements. |
| MathAbs | Calculates the absolute values of array elements. |
| MathCeil | Returns the nearest larger integers for array elements. |
| MathFloor | Returns the nearest smaller integers for array elements. |
| MathSqrt | Calculates the square roots of array elements. |
| MathExp | Calculates the values of the exp(x) function for array elements. |
| MathPow | Calculates the values of the pow(x, power) function for array elements. |
| MathLog | Calculates the values of the log(x) function for array elements. |
| MathLog2 | Calculates the logarithm to the base 2 for the array elements. |
| MathLog10 | Calculates the logarithm to the base 10 for the array elements. |
| MathDifference | Generates an array with element differences of y[i]=x[i+lag]-x[i]. |
| MathSample | Generates a random sample from the array elements. |
| MathTukeySummary | Calculates the Tukey's five-number summary for the array elements. |
| MathRange | Calculates the minima and maxima of array elements. |
| MathMin | Returns the minimum value of all array elements. |
| MathMax | Returns the maximum value of all array elements. |
| MathSum | Returns the sum of array elements. |
| MathProduct | Returns the product of array elements. |
| MathStandardDeviation | Calculates the standard deviation of array elements. |
| MathAverageDeviation | Calculates the average absolute deviation of array elements. |
| MathMedian | Calculates the median value of array elements. |
| MathMean | Calculates the mean values of array elements. |
| MathVariance | Calculates the variance of the array elements. |
| MathSkewness | Calculates the skewness of the array elements. |
| MathKurtosis | Calculates the kurtosis of the array elements. |
| MathLog1p | Calculates the values of the log(1+x) function for array elements. |
| MathExpm1 | Calculates the values of the exp(x)-1 function for array elements. |
| MathSinh | Calculates the values of the sinh(x) function for array elements. |
| MathCosh | Calculates the values of the cosh(x) function for array elements. |
| MathTanh | Calculates the values of the tanh(x) function for array elements. |
| MathArcsinh | Calculates the values of the arcsinh(x) function for array elements. |
| MathArccosh | Calculates the values of the arccosh(x) function for array elements. |
| MathArctanh | Calculates the values of the arctanh(x) function for array elements. |
| MathSignif | Rounds a value to the specified number of digits in the mantissa. |
| MathRank | Calculates the ranks of array elements. |
| MathCorrelationPearson | Calculates the Pearson's correlation coefficient. |
| MathCorrelationSpearman | Calculates the Spearman's correlation coefficient. |
| MathCorrelationKendall | Calculates the Kendall's correlation coefficient. |
| MathQuantile | Calculates sample quantiles corresponding to the specified probabilities. |
| MathProbabilityDensityEmpirical | Calculates the empirical probability density function for random values. |
| MathCumulativeDistributionEmpirical | Calculates the empirical cumulative distribution function for random values. |
