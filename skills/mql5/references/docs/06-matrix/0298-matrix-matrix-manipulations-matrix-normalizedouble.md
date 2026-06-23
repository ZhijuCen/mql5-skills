# NormalizeDouble

Round matrix/vector elements to a specified accuracy. For complex numbers, the real and imaginary parts are normalized separately. Returns matrix/vector with normalized elements.

```
vector vector::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
vectorf vectorf::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
vectorc vectorc::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
vectorcf vectorcf::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
matrix matrix::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
matrixf matrixf::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
matrixc matrixc::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );
 
matrixcf matrixcf::NormalizeDouble(
  int            digits      // number of digits after decimal point
   );

```

Parameters

digits

[in]  Accuracy format, number of digits after point (0-11).

Return Value

Matrix/vector with normalized values.

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
//--- round to 5 decimal places
   matrixf aain=aai.NormalizeDouble(5);
//--- accurate identity matrix
   Print("identity matrix\n",aain);
 
/*
[[0.99999976,0,0,-2.3841858e-07,0]
 [-4.1723251e-07,1,1.8626451e-09,-5.9604645e-08,2.3841858e-07]
 [-1.0728836e-06,-1.1920929e-07,0.99999994,-8.3446503e-07,4.7683716e-07]
 [-2.9802322e-07,5.9604645e-08,-3.9115548e-08,0.99999958,0]
 [-5.9604645e-08,-5.9604645e-08,4.2840838e-08,-6.5565109e-07,1.0000002]]
identity matrix
[[1,0,0,0,0]
 [0,1,0,0,0]
 [0,0,1,0,0]
 [0,0,0,1,0]
 [0,0,0,0,1]]
*/

```
