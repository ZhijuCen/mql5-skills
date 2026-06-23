# Mathematical operations with matrices and vectors

Mathematical operations, including addition, subtraction, multiplication and division, can be performed on matrices and vectors element-wise.

Mathematical functions were originally designed to perform relevant operations on scalar values. Most of the functions can be applied to [matrices and vectors](/en/docs/basis/types/matrix_vector). These include MathAbs, MathArccos, MathArcsin, MathArctan, MathCeil, MathCos, MathExp, MathFloor, MathLog, MathLog10, MathMod, MathPow, MathRound, MathSin, MathSqrt, MathTan, MathExpm1, MathLog1p, MathArccosh, MathArcsinh, MathArctanh, MathCosh, MathSinh, and MathTanh. Such operations imply element-wise processing of matrices and vectors. Example

```
//---
  matrix a= {{1, 4}, {9, 16}};
  Print("matrix a=\n",a);
  a=MathSqrt(a);
  Print("MatrSqrt(a)=\n",a);
  /*
   matrix a=
   [[1,4]
    [9,16]]
   MatrSqrt(a)=
   [[1,2]
    [3,4]]
  */

```

For [MathMod](/en/docs/math/mathmod) and [MathPow](/en/docs/math/mathpow), the second element can be either a scalar or a matrix/vector of the appropriate size.

The following example shows how to calculate the standard deviation by applying math functions to a vector.

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- use the initializing function to fill the vector
  vector r(10, ArrayRandom); // array of random numbers from 0 to 1
//--- calculate the mean value
  double avr=r.Mean();       // array mean value
  vector d=r-avr;            // calculate an array of deviations from the mean
  Print("avr(r)=", avr);
  Print("r=", r);
  Print("d=", d);
  vector s2=MathPow(d, 2);   // array of squared deviations
  double sum=s2.Sum();       // sum of squared deviations
//--- calculate the standard deviation in two different methods
  double std=MathSqrt(sum/r.Size());
  Print(" std(r)=", std);
  Print("r.Std()=", r.Std());   
 }
/*
  avr(r)=0.5300302133243813
  r=[0.8346201971495713,0.8031556138798182,0.6696676534318063,0.05386516922513505,0.5491195410016175,0.8224433118686484,...
  d=[0.30458998382519,0.2731254005554369,0.1396374401074251,-0.4761650440992462,0.01908932767723626,0.2924130985442671, ...
   std(r)=0.2838269732183663
  r.Std()=0.2838269732183663
*/
//+------------------------------------------------------------------+
//| Fills a vector with random values                                |
//+------------------------------------------------------------------+
void ArrayRandom(vector& v)
 {
  for(ulong i=0; i<v.Size(); i++)
    v[i]=double(MathRand())/32767.;
 }

```
