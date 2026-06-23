# Random

Static function. Create and return a new matrix or vector filled with random values. Random values are generated uniformly within the specified range.

```
static vector vector::Random(
  const ulong   size,       // vector length
  const double  min=0.0,    // minimum value
  const double  max=1.0     // maximum value
   );
 
static matrix matrix::Random(
  const ulong   rows,       // number of rows
  const ulong   cols        // number of columns
  const float   min=0.0,    // minimum value
  const float   max=1.0     // maximum value
   );
 

```

The function fills an existing matrix or vector with random values. Random values are generated uniformly within the specified range.

```
void  vector::Random(
  const double  min=0.0,    // minimum value
  const double  max=1.0     // maximum value
   );
 
void  matrix::Random(
  const float  min=0.0,     // minimum value
  const float  max=1.0      // maximum value
   );

```

Parameters

rows

[in]  Number of rows.

cols

[in]  Number of columns.

size

[in]  Vector length.

min=0.0

[in] The minimum value in the generated sample of random numbers.

max=1.0

[in]  The maximum value in the generated sample of random numbers.

Return Value

Return a new matrix of given rows and columns filled with random values.

Example

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   vector v1= vector::Random(6,0,4);
   Print("vector v1 \n", v1);  
   /*
   vector v1 
   [3.340834286841758,0.9073984578501895,3.15598511117417,0.7106475841045956,2.294010032502471,0.2469535936245121]
   */
      
   vector v2(4);
   v2.Random(-3,3);
   Print("vector v2 \n", v2);      
   /*
   vector v2 
   [-2.642032080246609,1.008521607147651,1.340623848219547,-2.789016363161853]
   */
 
   matrix m1 = matrix::Random(5, 5, -1, 3);
   Print("matrix m1 \n", m1);
   /*
   matrix m1 
   [[1.468433369525809,1.199383023707052,0.6154667729547869,2.830012157519816,-0.06995551732134897]
    [2.638591175814763,2.966658948912904,2.001837257994767,-0.08570802469870731,0.8260628995080626]
    [0.982665140643405,0.5825661973987162,-0.6615881071569371,0.4069533109215444,-0.1612716566681097]
    [-0.5791836119208447,-0.9332020478167575,2.801898707589577,-0.09887318478405316,-0.3206291206461911]
    [-0.1069569017521471,-0.04576879345014895,0.6320100840255642,-0.3805729270401813,0.7021634554728315]]
   */
 
   matrix m2(3, 3);
   m2.Random(-2, 2);
   Print("matrix m2 \n", m2);
   /*
   matrix m2 
   [[-1.928191291151613,-1.222873445419332,-1.965333905062949]
    [-1.077723600686929,1.053317863273741,-0.1786824246353196]
    [-1.965241401448204,1.620956906029246,-1.696386492740453]]
   */   
  }

```
