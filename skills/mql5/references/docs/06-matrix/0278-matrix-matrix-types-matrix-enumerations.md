# Enumeration for matrix and vector operations

This section describes the enumerations that are used in various matrix and vector methods.

ENUM_AVERAGE_MODE

Smoothing type enumeration.

| ID | Description |
| --- | --- |
| AVERAGE_NONE | No averaging. Results are provided for each label separately |
| AVERAGE_BINARY | Label 1 result for binary classification |
| AVERAGE_MICRO | Average error matrix result (confusion matrix) |
| AVERAGE_MACRO | Average result from the results of the error matrices of each label |
| AVERAGE_WEIGHTED | Weighted average result |

ENUM_VECTOR_NORM

Enumeration of vector norms for vector::[Norm](/en/docs/matrix/matrix_characteristics/matrix_norm).

| ID | Description |
| --- | --- |
| VECTOR_NORM_INF | Inf norm |
| VECTOR_NORM_MINUS_INF | Minus Inf norm |
| VECTOR_NORM_P | Norm P |

ENUM_MATRIX_NORM

Enumeration of matrix norms for matrix::[Norm](/en/docs/matrix/matrix_characteristics/matrix_norm) and for obtaining the matrix::[Cond](/en/docs/matrix/matrix_characteristics/matrix_cond) matrix condition number.

| ID | Description |
| --- | --- |
| MATRIX_NORM_FROBENIUS | Frobenius norm |
| MATRIX_NORM_SPECTRAL | Spectral norm |
| MATRIX_NORM_NUCLEAR | Nuclear norm |
| MATRIX_NORM_INF | Inf norm |
| MATRIX_NORM_P1 | P1 norm |
| MATRIX_NORM_P2 | P2 norm |
| MATRIX_NORM_MINUS_INF | Minus Inf norm |
| MATRIX_NORM_MINUS_P1 | Minus P1 norm |
| MATRIX_NORM_MINUS_P2 | Minus P2 norm |

ENUM_VECTOR_CONVOLVE

Enumeration for convolution vector::[Convolve](/en/docs/matrix/matrix_products/matrix_convolve) and cross-correlation vector::[Correlate](/en/docs/matrix/matrix_products/matrix_correlate).

| ID | Description |
| --- | --- |
| VECTOR_CONVOLVE_FULL | Convolve full |
| VECTOR_CONVOLVE_SAME | Convolve same |
| VECTOR_CONVOLVE_VALID | Convolve valid |

ENUM_REGRESSION_METRIC

Enumeration of regression metrics for vector::[RegressionMetric](/en/docs/matrix/matrix_machine_learning/matrix_regressionmetrics).

| ID | Description |
| --- | --- |
| REGRESSION_MAE | Mean Absolute Error |
| REGRESSION_MSE | Mean Squared Error |
| REGRESSION_RMSE | Root Mean Squared Error |
| REGRESSION_R2 | R-Squared |
| REGRESSION_MAPE | Mean Absolute Percentage Error |
| REGRESSION_MSPE | Mean Squared Percentage Error |
| REGRESSION_RMSLE | Root Mean Squared Logarithmic Error |
| REGRESSION_SMAPE | Symmetric Mean Absolute Percentage Error |
| REGRESSION_MAXE | Maximal Absolute Error |
| REGRESSION_MEDE | Median Absolute Error |
| REGRESSION_MPD | Mean Poisson Deviance |
| REGRESSION_MGD | Mean Gamma Deviance |
| REGRESSION_EXPV | Explained Variance |

ENUM_CLASSIFICATION_METRIC

Enumeration of metrics for classification problems.

| ID | Description |
| --- | --- |
| CLASSIFICATION_ACCURACY | Model quality in terms of prediction accuracy for all classes |
| CLASSIFICATION_AVERAGE_PRECISION | Average model accuracy |
| CLASSIFICATION_BALANCED_ACCURACY | Balanced prediction accuracy |
| CLASSIFICATION_F1 | F1 score. Harmonic mean between the model precision and recall |
| CLASSIFICATION_JACCARD | Jaccard score |
| CLASSIFICATION_PRECISION | Model accuracy in predicting true positives for the target class |
| CLASSIFICATION_RECALL | Model completeness |
| CLASSIFICATION_ROC_AUC | Area under the error curve |
| CLASSIFICATION_TOP_K_ACCURACY | Frequency of the correct label appearing at the top of k predicted labels |

ENUM_LOSS_FUNCTION

Enumeration for loss function calculations vector::[Loss](/en/docs/matrix/matrix_machine_learning/matrix_loss).

| ID | Description |
| --- | --- |
| LOSS_MSE | Root mean square error |
| LOSS_MAE | Mean Absolute Error |
| LOSS_CCE | Categorical Crossentropy |
| LOSS_BCE | Binary Crossentropy |
| LOSS_MAPE | Mean Absolute Percentage Error |
| LOSS_MSLE | Mean Squared Logarithmic Error |
| LOSS_KLD | Kullback-Leibler Divergence |
| LOSS_COSINE | Cosine similarity/proximity |
| LOSS_POISSON | Poisson |
| LOSS_HINGE | Hinge |
| LOSS_SQ_HINGE | Squared Hinge |
| LOSS_CAT_HINGE | Categorical Hinge |
| LOSS_LOG_COSH | Logarithm of the Hyperbolic Cosine |
| LOSS_HUBER | Huber |

ENUM_ACTIVATION_FUNCTION

Enumeration for the activation function vector::[Activation](/en/docs/matrix/matrix_machine_learning/matrix_activation) and for the activation function derivative vector::[Derivative](/en/docs/matrix/matrix_machine_learning/matrix_derivative).

| ID | Description |
| --- | --- |
| AF_ELU | Exponential Linear Unit |
| AF_EXP | Exponential |
| AF_GELU | Gaussian Error Linear Unit |
| AF_HARD_SIGMOID | Hard Sigmoid |
| AF_LINEAR | Linear |
| AF_LRELU | Leaky Rectified Linear Unit |
| AF_RELU | REctified Linear Unit |
| AF_SELU | Scaled Exponential Linear Unit |
| AF_SIGMOID | Sigmoid |
| AF_SOFTMAX | Softmax |
| AF_SOFTPLUS | Softplus |
| AF_SOFTSIGN | Softsign |
| AF_SWISH | Swish |
| AF_TANH | The hyperbolic tangent function |
| AF_TRELU | Thresholded Rectified Linear Unit |

ENUM_SORT_MODE

Enumeration of sort types for the [Sort](/en/docs/matrix/matrix_manipulations/matrix_sort) function.

| ID | Description |
| --- | --- |
| SORT_ASCENDING | Sort ascending |
| SORT_DESCENDING | Sort descending |

ENUM_MATRIX_AXIS

Enumeration for specifying the axis in all [statistical functions](/en/docs/matrix/matrix_statistics) for matrices.

| ID | Description |
| --- | --- |
| AXIS_NONE | The axis is not specified. Calculation is performed over all matrix elements, as if it were a vector (see the  Flat  method). |
| AXIS_HORZ | Horizontal axis |
| AXIS_VERT | Vertical axis |
