# ReplaceToZero

Replace small values in a matrix/vector with the zero value and return the number of elements replaced.

```
ulong vector::ReplaceToZero(
  const double   abs_tol      // absolute tolerance value
   );
 
ulong vectorf::ReplaceToZero(
  const float    abs_tol      // absolute tolerance value
   );
 
ulong vectorc::ReplaceToZero(
  const double   abs_tol      // absolute tolerance value
   );
 
ulong vectorcf::ReplaceToZero(
  const float    abs_tol      // absolute tolerance value
   );
 
ulong matrix::ReplaceToZero(
  const double   abs_tol      // absolute tolerance value
   );
 
ulong matrixf::ReplaceToZero(
  const float    abs_tol      // absolute tolerance value
   );
 
ulong matrixc::ReplaceToZero(
  const double   abs_tol      // absolute tolerance value
   );
 
ulong matrixcf::ReplaceToZero(
  const float    abs_tol      // absolute tolerance value
   );

```

Parameters

abs_tol

[in]  Absolute tolerance value that compared to vector/matrix element. If absolute value of vector/matrix is less or equal to absolute tolerance value then element replaced to zero. In complex case module of complex value ( sqrt(value.real*value.real+value.imag*value.imag) ) compared to absolute tolerance value.

Return Value

The number of matrix/vector small elements that were replaced to zero.

Example

```
   matrixf a={{ 1, 1, 2, 3, 4},
              { 1, 2, 5, 6, 7},
              { 2, 5, 3, 9,10},
              { 3, 6, 9, 4, 5},
              { 4, 7,10, 5, 5}};
   matrixf ai=a.Inv();
//--- result matrix should be an identity matrix
   matrixf aai=a@ai;
   Print(aai);
//--- replace small values
   ulong replaced=aai.ReplaceToZero(1e-5);
   Print("replaced=",replaced);
//--- this looks more like an identity matrix
   Print(aai);
 
  /*
[[0.99999976,0,0,-2.3841858e-07,0]
 [-4.1723251e-07,1,1.8626451e-09,-5.9604645e-08,2.3841858e-07]
 [-1.0728836e-06,-1.1920929e-07,0.99999994,-8.3446503e-07,4.7683716e-07]
 [-2.9802322e-07,5.9604645e-08,-3.9115548e-08,0.99999958,0]
 [-5.9604645e-08,-5.9604645e-08,4.2840838e-08,-6.5565109e-07,1.0000002]]
replaced=20
[[0.99999976,0,0,0,0]
 [0,1,0,0,0]
 [0,0,0.99999994,0,0]
 [0,0,0,0.99999958,0]
 [0,0,0,0,1.0000002]]
  */

```
