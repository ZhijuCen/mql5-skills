# ClassificationScore

Compute the classification metric to evaluate the quality of the predicted data compared to the true data.

Unlike other methods in the Machine Learning section, this one applies to the vector of true values rather than the vector of predicted values.

```
vector vector::ClassificationScore(
   const matrix&              pred_scores,   // matrix containing probability distribution for each class 
   ENUM_CLASSIFICATION_METRIC metric         // metric type
   ENUM_AVERAGE_MODE          mode           // averaging mode
   );
 
 
vector vector::ClassificationScore(
   const matrix&              pred_scores,   // matrix containing probability distribution for each class 
   ENUM_CLASSIFICATION_METRIC metric         // metric type
   int                        param          // additional parameter
   );

```

Parameters

pred_scores

[in] A matrix containing a set of horizontal vectors with probabilities for each class. The number of matrix rows should correspond to the size of the vector of true values.

metric

[in] Metric type from the [ENUM_CLASSIFICATION_METRIC](/en/docs/matrix/matrix_types/matrix_enumerations#enum_classification_metric) enumeration. The CLASSIFICATION_TOP_K_ACCURACY, CLASSIFICATION_AVERAGE_PRECISION and CLASSIFICATION_ROC_AUC values are used.

mode

[in]  Averaging mode from the [ENUM_AVERAGE_MODE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_average_mode) enumeration. Used for the CLASSIFICATION_AVERAGE_PRECISION and CLASSIFICATION_ROC_AUC metrics.

param

[in]  In case of the CLASSIFICATION_TOP_K_ACCURACY metric, the integer K value should be specified instead of the averaging mode.

Return Value

A vector containing the calculated metric. In the case of the AVERAGE_NONE averaging mode, the vector contains metric values for each class without averaging. (For example, in case of the binary classification, this would be two metrics for 'false' and 'true' respectively).

Note about averaging modes

AVERAGE_BINARY is only meaningful for binary classification.

AVERAGE_MICRO — calculate metrics globally by considering each element of the label indicator matrix as a label. The label indicator matrix refers to a matrix with a set of probabilities for each label.

AVERAGE_MACRO — calculate metrics for each label and find their unweighted mean. This does not take label imbalance into account.

AVERAGE_WEIGHTED — calculate metrics for each label and find their average weighted by support (the number of true instances for each label).

Note

In case of binary classification, we can input not only an n x 2 matrix, where the first column contains probabilities for a negative label, and the second column contains probabilities for a positive label, but also a matrix consisting of one column with positive probabilities. This is because binary classification models can return either two probabilities or one probability for a positive label.

Example:

```
   vector y_true={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,8,4,2,7,6,8,4,2,3,6};
   //vector y_pred={7,2,1,0,4,1,4,9,5,9,0,6,9,0,1,5,9,7,3,4,2,9,4,9,5,9,2,7,7,0};
 
//--- label scores          0         1         2         3         4         5         6         7         8         9    true pred
   matrix y_scores={{0.000109, 0.000186, 0.000449, 0.000052, 0.000002, 0.000022, 0.000005, 0.998059, 0.000010, 0.001104},  // 7    7
                    {0.000091, 0.081956, 0.916816, 0.001106, 0.000006, 0.000002, 0.000001, 0.000000, 0.000021, 0.000000},  // 2    2
                    {0.000108, 0.972863, 0.003600, 0.000021, 0.010479, 0.000015, 0.000131, 0.010385, 0.002339, 0.000060},  // 1    1
                    {0.925425, 0.000080, 0.002913, 0.000057, 0.000274, 0.000638, 0.063529, 0.000316, 0.000095, 0.006673},  // 0    0
                    {0.000060, 0.000126, 0.000006, 0.000000, 0.993513, 0.000000, 0.000003, 0.000222, 0.000001, 0.006069},  // 4    4
                    {0.000016, 0.982124, 0.000045, 0.000002, 0.008445, 0.000001, 0.000005, 0.009230, 0.000120, 0.000013},  // 1    1
                    {0.000000, 0.000040, 0.000001, 0.000000, 0.989395, 0.000167, 0.000004, 0.000070, 0.000177, 0.010146},  // 4    4
                    {0.000795, 0.002938, 0.023447, 0.007418, 0.021838, 0.002476, 0.000260, 0.047551, 0.000082, 0.893194},  // 9    9
                    {0.000091, 0.000226, 0.000038, 0.000007, 0.000048, 0.854910, 0.068644, 0.000080, 0.001097, 0.074860},  // 5    5
                    {0.000000, 0.000000, 0.000000, 0.000000, 0.003004, 0.000000, 0.000000, 0.000035, 0.000000, 0.996960},  // 9    9
                    {0.998856, 0.000009, 0.000976, 0.000002, 0.000000, 0.000013, 0.000131, 0.000006, 0.000000, 0.000007},  // 0    0
                    {0.000178, 0.000446, 0.000326, 0.000033, 0.000193, 0.000071, 0.998403, 0.000015, 0.000328, 0.000007},  // 6    6
                    {0.000005, 0.000016, 0.000153, 0.000045, 0.004110, 0.000012, 0.000015, 0.000031, 0.000076, 0.995537},  // 9    9
                    {0.994188, 0.000003, 0.002584, 0.000005, 0.000005, 0.000100, 0.000739, 0.001473, 0.000038, 0.000864},  // 0    0
                    {0.000173, 0.990569, 0.000792, 0.000040, 0.001798, 0.000035, 0.000114, 0.004750, 0.001716, 0.000013},  // 1    1
                    {0.000000, 0.000537, 0.000008, 0.005080, 0.000046, 0.992910, 0.000012, 0.000671, 0.000390, 0.000347},  // 5    5
                    {0.000127, 0.000003, 0.000003, 0.000000, 0.001583, 0.000000, 0.000002, 0.000555, 0.000016, 0.997712},  // 9    9
                    {0.000001, 0.000012, 0.000072, 0.000020, 0.000000, 0.000000, 0.000000, 0.999868, 0.000000, 0.000026},  // 7    7
                    {0.000020, 0.000105, 0.001139, 0.901343, 0.002132, 0.083873, 0.000124, 0.000097, 0.010981, 0.000186},  // 3    3
                    {0.000002, 0.000048, 0.000019, 0.000000, 0.999347, 0.000002, 0.000040, 0.000051, 0.000000, 0.000489},  // 4    4
                    {0.000059, 0.001344, 0.612502, 0.002749, 0.000229, 0.000678, 0.000038, 0.001844, 0.379727, 0.000831},  // 8    2
                    {0.000586, 0.000740, 0.001625, 0.000007, 0.269341, 0.000076, 0.016417, 0.000199, 0.000107, 0.710902},  // 4    9
                    {0.009547, 0.018055, 0.283795, 0.071079, 0.426074, 0.082335, 0.036379, 0.021188, 0.003924, 0.047623},  // 2    4
                    {0.002506, 0.002545, 0.001148, 0.005659, 0.020416, 0.000112, 0.006092, 0.272536, 0.003148, 0.685839},  // 7    9
                    {0.001263, 0.001769, 0.000293, 0.000011, 0.000302, 0.881768, 0.112019, 0.000125, 0.002327, 0.000123},  // 6    5
                    {0.002904, 0.002909, 0.013421, 0.001461, 0.007519, 0.001251, 0.000555, 0.106219, 0.107125, 0.756637},  // 8    9
                    {0.000055, 0.001080, 0.893158, 0.000000, 0.104492, 0.000159, 0.001042, 0.000013, 0.000000, 0.000000},  // 4    2
                    {0.000344, 0.002693, 0.071184, 0.000262, 0.000001, 0.000003, 0.000032, 0.924362, 0.000714, 0.000404},  // 2    7
                    {0.001404, 0.009375, 0.002638, 0.229189, 0.000064, 0.000896, 0.007516, 0.743557, 0.004462, 0.000897},  // 3    7
                    {0.491140, 0.000125, 0.000024, 0.000302, 0.000038, 0.034947, 0.473161, 0.000170, 0.000028, 0.000066}}; // 6    0
 
   vector top_k=y_true.ClassificationScore(y_scores,CLASSIFICATION_TOP_K_ACCURACY,1);
   Print("top 1 accuracy score = ",top_k);
   top_k=y_true.ClassificationScore(y_scores,CLASSIFICATION_TOP_K_ACCURACY,2);
   Print("top 2 accuracy score = ",top_k);
   vector y_true2={0, 1, 2, 2};
   matrix y_score2={{0.5, 0.2, 0.2},  // 0 is in top 2
                    {0.3, 0.4, 0.2},  // 1 is in top 2
                    {0.2, 0.4, 0.3},  // 2 is in top 2
                    {0.7, 0.2, 0.1}}; // 2 isn't in top 2
   top_k=y_true2.ClassificationScore(y_score2,CLASSIFICATION_TOP_K_ACCURACY,2);
   Print("top k = ",top_k);
   Print("");
 
   vector ap_micro=y_true.ClassificationScore(y_scores,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_MICRO);
   Print("average precision score micro = ",ap_micro);
   vector ap_macro=y_true.ClassificationScore(y_scores,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_MACRO);
   Print("average precision score macro = ",ap_macro);
   vector ap_weighted=y_true.ClassificationScore(y_scores,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_WEIGHTED);
   Print("average precision score weighted = ",ap_weighted);
   vector ap_none=y_true.ClassificationScore(y_scores,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_NONE);
   Print("average precision score none = ",ap_none);
   Print("");
 
   vector area_micro=y_true.ClassificationScore(y_scores,CLASSIFICATION_ROC_AUC,AVERAGE_MICRO);
   Print("roc auc score micro = ",area_micro);
   vector area_macro=y_true.ClassificationScore(y_scores,CLASSIFICATION_ROC_AUC,AVERAGE_MACRO);
   Print("roc auc score macro = ",area_macro);
   vector area_weighted=y_true.ClassificationScore(y_scores,CLASSIFICATION_ROC_AUC,AVERAGE_WEIGHTED);
   Print("roc auc score weighted = ",area_weighted);
   vector area_none=y_true.ClassificationScore(y_scores,CLASSIFICATION_ROC_AUC,AVERAGE_NONE);
   Print("roc auc score none = ",area_none);
   Print("");
 
//--- binary classification
   vector y_pred_bin={0,1,0,1,1,0,0,0,1};
   vector y_true_bin={1,0,0,0,1,0,1,1,1};
   vector y_score_true={0.3,0.7,0.1,0.6,0.9,0.0,0.4,0.2,0.8};
   matrix y_score1_bin(y_score_true.Size(),1);
   y_score1_bin.Col(y_score_true,0);
   matrix y_scores_bin={{0.7, 0.3},
                        {0.3, 0.7},
                        {0.9, 0.1},
                        {0.4, 0.6},
                        {0.1, 0.9},
                        {1.0, 0.0},
                        {0.6, 0.4},
                        {0.8, 0.2},
                        {0.2, 0.8}};
 
   vector ap=y_true_bin.ClassificationScore(y_scores_bin,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_BINARY);
   Print("average precision score binary = ",ap);
   vector ap2=y_true_bin.ClassificationScore(y_score1_bin,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_BINARY);
   Print("average precision score binary = ",ap2);
   vector ap3=y_true_bin.ClassificationScore(y_scores_bin,CLASSIFICATION_AVERAGE_PRECISION,AVERAGE_NONE);
   Print("average precision score none = ",ap3);
   Print("");
 
   vector area=y_true_bin.ClassificationScore(y_scores_bin,CLASSIFICATION_ROC_AUC,AVERAGE_BINARY);
   Print("roc auc score binary = ",area);
   vector area2=y_true_bin.ClassificationScore(y_score1_bin,CLASSIFICATION_ROC_AUC,AVERAGE_BINARY);
   Print("roc auc score binary = ",area2);
   vector area3=y_true_bin.ClassificationScore(y_scores_bin,CLASSIFICATION_ROC_AUC,AVERAGE_NONE);
   Print("roc auc score none = ",area3);
 
 
/*
  top 1 accuracy score = [0.6666666666666666]
  top 2 accuracy score = [1]
  top k = [0.75]
  
  average precision score micro = [0.8513333333333333]
  average precision score macro = [0.9326666666666666]
  average precision score weighted = [0.9333333333333333]
  average precision score none = [1,1,0.7,1,0.9266666666666666,0.8333333333333333,1,0.8666666666666667,1,1]
  
  roc auc score micro = [0.9839506172839506]
  roc auc score macro = [0.9892068783068803]
  roc auc score weighted = [0.9887354497354497]
  roc auc score none = [1,1,0.9506172839506173,1,0.984,0.9821428571428571,1,0.9753086419753086,1,1]
  
  average precision score binary = [0.7961904761904761]
  average precision score binary = [0.7961904761904761]
  average precision score none = [0.7678571428571428,0.7961904761904761]
  
  roc auc score binary = [0.7]
  roc auc score binary = [0.7]
  roc auc score none = [0.7,0.7]
*/

```
