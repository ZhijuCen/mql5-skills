# ConfusionMatrixMultilabel

Compute confusion matrix for each label. The method is applied to the vector of predicted values.

```
uint vector::ConfusionMatrixMultiLabel(
   const vector&       vect_true,     // vector of true values
   matrix&             confusions[]   // array of calculated confusion matrices 
   );
 

```

Parameters

vect_true

[in] Vector of true values.

confusions

[out] An array of 2 x 2 matrices with computed confusion matrices for each label.

Return Value

Size of the array of calculated confusion matrices. In case of failure, it returns 0

Note

The result array can be dynamic or static. If the array is static, then it must be no less in size than the number of classes.

The sizes of the vector of true values and the vector of predicted values should be the same.

Example:

```
   vector y_true={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,8,4,2,7,6,8,4,2,3,6};
   vector y_pred={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,2,9,4,9,5,9,2,7,7,0};
   matrix label_confusions[12];
 
   uint   res=y_pred.ConfusionMatrixMultiLabel(y_true,label_confusions);
   Print("res=",res,"  size=",label_confusions.Size());
   for(uint i=0; i<res; i++)
      Print(label_confusions[i]);
 
 
/*
  res=10  size=12
  [[26,1]
   [0,3]]
  [[27,0]
   [0,3]]
  [[25,2]
   [2,1]]
  [[28,0]
   [1,1]]
  [[24,1]
   [2,3]]
  [[27,1]
   [0,2]]
  [[27,0]
   [2,1]]
  [[25,2]
   [1,2]]
  [[28,0]
   [2,0]]
  [[23,3]
   [0,4]]
*/

```
