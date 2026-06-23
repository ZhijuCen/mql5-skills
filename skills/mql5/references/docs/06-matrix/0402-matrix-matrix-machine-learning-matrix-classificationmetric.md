# ClassificationMetric

Compute the classification metric to evaluate the quality of the predicted data compared to the true data. The method is applied to the vector of predicted values.

```
vector vector::ClassificationMetric(
   const vector&              vect_true,     // vector of true values
   ENUM_CLASSIFICATION_METRIC metric         // metric type
   );
 
 
vector vector::ClassificationMetric(
   const vector&              vect_true,     // vector of true values
   ENUM_CLASSIFICATION_METRIC metric         // metric type
   ENUM_AVERAGE_MODE          mode           // averaging mode
   );

```

Parameters

vect_true

[in] Vector of true values.

metric

[in] Metric type from the [ENUM_CLASSIFICATION_METRIC](/en/docs/matrix/matrix_types/matrix_enumerations#enum_classification_metric) enumeration. Values other than CLASSIFICATION_TOP_K_ACCURACY, CLASSIFICATION_AVERAGE_PRECISION and CLASSIFICATION_ROC_AUC (used in the ClassificationScore method) are applied.

mode

[in]  Averaging mode from the [ENUM_AVERAGE_MODE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_average_mode) enumeration. Used for the CLASSIFICATION_F1, CLASSIFICATION_JACCARD, CLASSIFICATION_PRECISION and CLASSIFICATION_RECALL metrics.

Return Value

A vector containing the calculated metric. In the case of the AVERAGE_NONE averaging mode, the vector contains metric values for each class without averaging. (For example, in case of the binary classification, this would be two metrics for 'false' and 'true' respectively).

Note about averaging modes

AVERAGE_BINARY is only meaningful for binary classification.

AVERAGE_MICRO — calculate metrics globally by counting the total true positives, false negatives and false positives.

AVERAGE_MACRO — calculate metrics for each label and find their unweighted mean. This does not take label imbalance into account.

AVERAGE_WEIGHTED — calculate metrics for each label and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

Note

In case of binary classification, we can input not only an n x 2 matrix, where the first column contains probabilities for a negative label, and the second column contains probabilities for a positive label, but also a matrix consisting of one column with positive probabilities. This is because binary classification models can return either two probabilities or one probability for a positive label.

Example:

```
   vector y_true={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,8,4,2,7,6,8,4,2,3,6};
   vector y_pred={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,2,9,4,9,5,9,2,7,7,0};
 
   vector accuracy=y_pred.ClassificationMetric(y_true,CLASSIFICATION_ACCURACY);
   Print("accuracy=",accuracy);
   vector balanced=y_pred.ClassificationMetric(y_true,CLASSIFICATION_BALANCED_ACCURACY);
   Print("balanced=",balanced);
   Print("");
 
   vector f1_micro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_F1,AVERAGE_MICRO);
   Print("f1_micro=",f1_micro);
   vector f1_macro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_F1,AVERAGE_MACRO);
   Print("f1_macro=",f1_macro);
   vector f1_weighted=y_pred.ClassificationMetric(y_true,CLASSIFICATION_F1,AVERAGE_WEIGHTED);
   Print("f1_weighted=",f1_weighted);
   vector f1_none=y_pred.ClassificationMetric(y_true,CLASSIFICATION_F1,AVERAGE_NONE);
   Print("f1_none=",f1_none);
   Print("");
 
   vector jaccard_micro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_JACCARD,AVERAGE_MICRO);
   Print("jaccard_micro=",jaccard_micro);
   vector jaccard_macro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_JACCARD,AVERAGE_MACRO);
   Print("jaccard_macro=",jaccard_macro);
   vector jaccard_weighted=y_pred.ClassificationMetric(y_true,CLASSIFICATION_JACCARD,AVERAGE_WEIGHTED);
   Print("jaccard_weighted=",jaccard_weighted);
   vector jaccard_none=y_pred.ClassificationMetric(y_true,CLASSIFICATION_JACCARD,AVERAGE_NONE);
   Print("jaccard_none=",jaccard_none);
   Print("");
 
   vector precision_micro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_PRECISION,AVERAGE_MICRO);
   Print("precision_micro=",precision_micro);
   vector precision_macro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_PRECISION,AVERAGE_MACRO);
   Print("precision_macro=",precision_macro);
   vector precision_weighted=y_pred.ClassificationMetric(y_true,CLASSIFICATION_PRECISION,AVERAGE_WEIGHTED);
   Print("precision_weighted=",precision_weighted);
   vector precision_none=y_pred.ClassificationMetric(y_true,CLASSIFICATION_PRECISION,AVERAGE_NONE);
   Print("precision_none=",precision_none);
   Print("");
 
   vector recall_micro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_RECALL,AVERAGE_MICRO);
   Print("recall_micro=",recall_micro);
   vector recall_macro=y_pred.ClassificationMetric(y_true,CLASSIFICATION_RECALL,AVERAGE_MACRO);
   Print("recall_macro=",recall_macro);
   vector recall_weighted=y_pred.ClassificationMetric(y_true,CLASSIFICATION_RECALL,AVERAGE_WEIGHTED);
   Print("recall_weighted=",recall_weighted);
   vector recall_none=y_pred.ClassificationMetric(y_true,CLASSIFICATION_RECALL,AVERAGE_NONE);
   Print("recall_none=",recall_none);
   Print("");
 
//--- binary classification
   vector y_pred_bin={0,1,0,1,1,0,0,0,1};
   vector y_true_bin={1,0,0,0,1,0,1,1,1};
 
   vector f1_bin=y_pred_bin.ClassificationMetric(y_true_bin,CLASSIFICATION_F1,AVERAGE_BINARY);
   Print("f1_bin=",f1_bin);
   vector jaccard_bin=y_pred_bin.ClassificationMetric(y_true_bin,CLASSIFICATION_JACCARD,AVERAGE_BINARY);
   Print("jaccard_bin=",jaccard_bin);
   vector precision_bin=y_pred_bin.ClassificationMetric(y_true_bin,CLASSIFICATION_PRECISION,AVERAGE_BINARY);
   Print("precision_bin=",precision_bin);
   vector recall_bin=y_pred_bin.ClassificationMetric(y_true_bin,CLASSIFICATION_RECALL,AVERAGE_BINARY);
   Print("recall_bin=",recall_bin);
 
 
/*
  accuracy=[0.6666666666666666]
  balanced=[0.6433333333333333]
  
  f1_micro=[0.6666666666666666]
  f1_macro=[0.6122510822510823]
  f1_weighted=[0.632049062049062]
  f1_none=[0.8571428571428571,1,0.3333333333333333,0.6666666666666666,0.6666666666666665,0.8,0.5,0.5714285714285715,0,0.7272727272727273]
  
  jaccard_micro=[0.5]
  jaccard_macro=[0.4921428571428572]
  jaccard_weighted=[0.5056349206349205]
  jaccard_none=[0.75,1,0.2,0.5,0.5,0.6666666666666666,0.3333333333333333,0.4,0,0.5714285714285714]
  
  precision_micro=[0.6666666666666666]
  precision_macro=[0.6571428571428571]
  precision_weighted=[0.6706349206349207]
  precision_none=[0.75,1,0.3333333333333333,1,0.75,0.6666666666666666,1,0.5,0,0.5714285714285714]
  
  recall_micro=[0.6666666666666666]
  recall_macro=[0.6433333333333333]
  recall_weighted=[0.6666666666666666]
  recall_none=[1,1,0.3333333333333333,0.5,0.6,1,0.3333333333333333,0.6666666666666666,0,1]
  
  f1_bin=[0.4444444444444445]
  jaccard_bin=[0.2857142857142857]
  precision_bin=[0.5]
  recall_bin=[0.4]
*/

```
