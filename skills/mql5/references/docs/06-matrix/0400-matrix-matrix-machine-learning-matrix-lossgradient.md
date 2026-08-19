# LossGradient

Compute a vector or matrix of loss function gradients.

```
vector vector::LossGradient(
  const vector&       vect_true,     // vector of true values
  ENUM_LOSS_FUNCTION  loss,          // loss function type
   ...                               // additional parameter
   );
 
 
matrix matrix::LossGradient(
  const matrix&       matrix_true,   // matrix of true values
  ENUM_LOSS_FUNCTION  loss,          // loss function
   );
 
 
matrix matrix::LossGradient(
  const matrix&       matrix_true,   // matrix of true values
  ENUM_LOSS_FUNCTION  loss,          // loss function
  ENUM_MATRIX_AXIS    axis,          // axis
   ...                               // additional parameter
   );

```

Parameters

vect_true/matrix_true

[in] Vector or matrix of true values.

loss

[in]  Loss function from the [ENUM_LOSS_FUNCTION](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function) enumeration.

axis

[in] [ENUM_MATRIX_AXIS](/en/docs/matrix/matrix_types/matrix_enumerations#enum_matrix_axis) enumeration value (AXIS_HORZ — horizontal axis, AXIS_VERT — vertical axis).

...

[in]  Additional parameter 'delta' can only be used by the Hubert loss function (LOSS_HUBER)

Return Value

Vector or matrix of loss function gradient values. The gradient is the partial derivative with respect to dx (x is the predicted value) of the loss function at a given point.

Note

Gradients are used in neural networks to adjust the weight matrix weights during backpropagation, when training the model.

A neural network aims at finding the algorithms that minimize the error on the training sample, for which the loss function is used.

Different loss functions are used depending on the problem. For example, Mean Squared Error ([MSE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for regression problems, and Binary Cross-Entropy ([BCE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for binary classification purposes.

Example of calculating loss function gradients

```
   matrixf y_true={{ 1, 2, 3, 4 },
                   { 5, 6, 7, 8 },
                   { 9,10,11,12 }};
   matrixf y_pred={{ 1, 2, 3, 4 },
                   {11,10, 9, 8 },
                   { 5, 6, 7,12 }};
   matrixf loss_gradient =y_pred.LossGradient(y_true,LOSS_MAE);
   matrixf loss_gradienth=y_pred.LossGradient(y_true,LOSS_MAE,AXIS_HORZ);
   matrixf loss_gradientv=y_pred.LossGradient(y_true,LOSS_MAE,AXIS_VERT);
   Print("loss gradients\n",loss_gradient);
   Print("loss gradients on horizontal axis\n",loss_gradienth);
   Print("loss gradients on vertical axis\n",loss_gradientv);
 
/* Result
   loss gradients
   [[0,0,0,0]
    [0.083333336,0.083333336,0.083333336,0]
    [-0.083333336,-0.083333336,-0.083333336,0]]
   loss gradients on horizontal axis
   [[0,0,0,0]
    [0.33333334,0.33333334,0.33333334,0]
    [-0.33333334,-0.33333334,-0.33333334,0]]
   loss gradients on vertical axis
   [[0,0,0,0]
    [0.25,0.25,0.25,0]
    [-0.25,-0.25,-0.25,0]]
*/

```
