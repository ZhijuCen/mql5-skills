# Statistics

The Statistical Library provides a convenient way of working with the basic statistical distributions.

The library provides 5 functions for each distribution:

1. Calculation of probability density – functions of the form MathProbabilityDensityX()
2. Calculation of probabilities – functions of the form MathCumulativeDistributionX()
3. Calculation of distribution quantiles – functions of the form MathQuantileX()
4. Generation of random numbers with the specified distribution – functions of the form MathRandomX()
5. Calculation of the theoretical moments of the distributions – functions of the form MathMomentsX()

In addition to calculation of values for the individual random variables, the library also provides overloads for the functions, which perform the same calculations for arrays.

- [Statistical Characteristics](/en/docs/standardlibrary/mathematics/stat/array_stat)
- [Normal Distribution](/en/docs/standardlibrary/mathematics/stat/normal)
- [Log-normal distribution](/en/docs/standardlibrary/mathematics/stat/lognormal)
- [Beta distribution](/en/docs/standardlibrary/mathematics/stat/beta)
- [Noncentral beta distribution](/en/docs/standardlibrary/mathematics/stat/noncentralbeta)
- [Gamma distribution](/en/docs/standardlibrary/mathematics/stat/gamma)
- [Chi-squared distribution](/en/docs/standardlibrary/mathematics/stat/chisquare)
- [Noncentral chi-squared distribution](/en/docs/standardlibrary/mathematics/stat/noncentralchisquare)
- [Exponential distribution](/en/docs/standardlibrary/mathematics/stat/exponential)
- [F-distribution](/en/docs/standardlibrary/mathematics/stat/fisher)
- [Noncentral F-distribution](/en/docs/standardlibrary/mathematics/stat/noncentralfisher)
- [t-distribution](/en/docs/standardlibrary/mathematics/stat/student)
- [Noncentral t-distribution](/en/docs/standardlibrary/mathematics/stat/noncentralstudent)
- [Logistic distribution](/en/docs/standardlibrary/mathematics/stat/logistic)
- [Cauchy distribution](/en/docs/standardlibrary/mathematics/stat/cauchy)
- [Uniform distribution](/en/docs/standardlibrary/mathematics/stat/unifrom)
- [Weibull distribution](/en/docs/standardlibrary/mathematics/stat/weibull)
- [Binomial distribution](/en/docs/standardlibrary/mathematics/stat/binomial)
- [Negative binomial distribution](/en/docs/standardlibrary/mathematics/stat/negativebinomial)
- [Geometric distribution](/en/docs/standardlibrary/mathematics/stat/geometric)
- [Hypergeometric distribution](/en/docs/standardlibrary/mathematics/stat/hypergeometric)
- [Poisson distribution](/en/docs/standardlibrary/mathematics/stat/poisson)
- [Subfunctions](/en/docs/standardlibrary/mathematics/stat/mathsubfunctions)

Example:

```
//+------------------------------------------------------------------+
//|                                    NormalDistributionExample.mq5 |
//|                        Copyright 2016, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- include the functions for calculating the normal distribution
#include <Math\Stat\Normal.mqh>
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the parameters of the normal distribution
   double mu=5.0;
   double sigma=1.0;
   PrintFormat("Normal distribution with parameters mu=%G and sigma=%G, calculation examples:",mu,sigma);
//--- set the interval
   double x1=mu-sigma;
   double x2=mu+sigma;
//--- variables for probability calculation
   double cdf1,cdf2,probability;
//--- variables for error codes
   int error_code1,error_code2;
//--- calculate the values of distribution functions
   cdf1=MathCumulativeDistributionNormal(x1,mu,sigma,error_code1);
   cdf2=MathCumulativeDistributionNormal(x2,mu,sigma,error_code2);
//--- check the error codes
   if(error_code1==ERR_OK && error_code2==ERR_OK)
     {
      //--- calculate probability of a random variable in the range
      probability=cdf2-cdf1;
      //--- output the result
      PrintFormat("1. Calculate probability of a random variable within the range of %.5f<x<%.5f",x1,x2);
      PrintFormat("  Answer: Probability = %5.8f",probability);
     }
 
//--- Find the value range of random variable x, corresponding to the 95% confidence level
   probability=0.95; //  set the confidence probability
//--- set the probabilities at the interval bounds
   double p1=(1.0-probability)*0.5;
   double p2=probability+(1.0-probability)*0.5;
//--- calculate the interval bounds
   x1=MathQuantileNormal(p1,mu,sigma,error_code1);
   x2=MathQuantileNormal(p2,mu,sigma,error_code2);
//--- check the error codes
   if(error_code1==ERR_OK && error_code2==ERR_OK)
     {
      //--- output the result 
      PrintFormat("2. For confidence interval = %.2f, find the range of random variable",probability);
      PrintFormat("  Answer: range is  %5.8f <= x <=%5.8f",x1,x2);
     }
 
   PrintFormat("3. Compute the first 4 calculated and theoretical moments of the distribution");
//--- Generate an array of random numbers, calculate the first 4 moments and compare with the theoretical values
   int data_count=1000000;  // set the number of values and prepare an array
   double data[];
   ArrayResize(data,data_count);
//--- generate random values and store them into the array
   for(int i=0; i<data_count; i++)
     {
      data[i]=MathRandomNormal(mu,sigma,error_code1);
     }
//--- set the index of the initial value and the amount of data for calculation
   int start=0;
   int count=data_count;
//--- calculate the first 4 moments of the generated values
   double mean=MathMean(data,start,count);
   double variance=MathVariance(data,start,count);
   double skewness=MathSkewness(data,start,count);
   double kurtosis=MathKurtosis(data,start,count);
//--- variables for the theoretical moments
   double normal_mean=0;
   double normal_variance=0;
   double normal_skewness=0;
   double normal_kurtosis=0;
//--- display the values of the calculated moments
   PrintFormat("            Mean           Variance          Skewness           Kurtosis");
   PrintFormat("Calculated  %.10f   %.10f      %.10f      %.10f",mean,variance,skewness,kurtosis);
//--- calculate the theoretical values of the moments and compare them with the obtained values
   if(MathMomentsNormal(mu,sigma,normal_mean,normal_variance,normal_skewness,normal_kurtosis,error_code1))
     {
      PrintFormat("Theoretical %.10f   %.10f      %.10f       %.10f",normal_mean,normal_variance,normal_skewness,normal_kurtosis);
      PrintFormat("Difference  %.10f   %.10f      %.10f       %.10f",mean-normal_mean,variance-normal_variance,skewness-normal_skewness,kurtosis-normal_kurtosis);
     }
  }

```
