# ConfusionMatrix

Compute confusion matrix. The method is applied to the vector of predicted values.

```
matrix vector::ConfusionMatrix(
   const vector&       vect_true      // vector of true values
   );
 
 
matrix vector::ConfusionMatrix(
   const vector&       vect_true,     // vector of true values
   uint                label          // label value
   );

```

Parameters

vect_true

[in] Vector of true values.

label

[in] Label value for calculating the confusion matrix.

Return Value

Confusion matrix. If a label value is not specified, a multi-class confusion matrix is returned, where each label is matched to each other label individually. If a label value is specified, a 2 x 2 matrix is returned, in which the specified label is considered positive, while all other labels are negative (ovr, one vs rest).

Note

Confusion matrix C is such that Cij is equal to the number of observations known to be in group i and predicted to be in group j. Thus in binary classification, the count of true negatives (TN) is C00, false negatives (FN) is C10, true positives (TP) is C11 and false positives (FP) is C01.

In other words, the matrix can be graphically represented as follows:

```
TN

FP

FN

TP

```

The sizes of the vector of true values and the vector of predicted values should be the same.

Example:

```
   vector y_true={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,8,4,2,7,6,8,4,2,3,6};
   vector y_pred={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,2,9,4,9,5,9,2,7,7,0};
   matrix confusion=y_pred.ConfusionMatrix(y_true);
   Print(confusion);
   confusion=y_pred.ConfusionMatrix(y_true,0);
   Print(confusion);
   confusion=y_pred.ConfusionMatrix(y_true,1);
   Print(confusion);
   confusion=y_pred.ConfusionMatrix(y_true,2);
   Print(confusion);
 
 
/*
  [[3,0,0,0,0,0,0,0,0,0]
   [0,3,0,0,0,0,0,0,0,0]
   [0,0,1,0,1,0,0,1,0,0]
   [0,0,0,1,0,0,0,1,0,0]
   [0,0,1,0,3,0,0,0,0,1]
   [0,0,0,0,0,2,0,0,0,0]
   [1,0,0,0,0,1,1,0,0,0]
   [0,0,0,0,0,0,0,2,0,1]
   [0,0,1,0,0,0,0,0,0,1]
   [0,0,0,0,0,0,0,0,0,4]]
  [[26,1]
   [0,3]]
  [[27,0]
   [0,3]]
  [[25,2]
   [2,1]]
*/

```
