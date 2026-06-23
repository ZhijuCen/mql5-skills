# Loss

Compute the value of the loss function.

```
double vector::Loss(
  const vector&       vect_true,     // vector of true values
  ENUM_LOSS_FUNCTION  loss,          // loss function
   ...                               // additional parameter
   );
 
 
double matrix::Loss(
  const matrix&       matrix_true,   // matrix of true values
  ENUM_LOSS_FUNCTION  loss,          // loss function
   );
 
 
double matrix::Loss(
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

double value.

How the 'delta' parameter is used in the Hubert loss function (LOSS_HUBER)

```
   double delta = 1.0;
   double error = fabs(y - x);
   if(error<delta)
      loss = 0.5 * error^2;
   else
      loss = 0.5 * delta^2 + delta * (error - delta);

```

Note

A neural network aims at finding the algorithms that minimize the error on the training sample, for which the loss function is used.

The value of the loss function indicates by how much the value predicted by the model deviates from the real one.

Different loss functions are used depending on the problem. For example, Mean Squared Error ([MSE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for regression problems, and Binary Cross-Entropy ([BCE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for binary classification purposes.

Example of calling the Hubert loss function:

```
   vector y_true = {0.0, 1.0, 0.0, 0.0};
   vector y_pred = {0.6, 0.4, 0.4, 0.6};
   double loss=y_pred.Loss(y_true,LOSS_HUBER);
   Print(loss);
   double loss2=y_pred.Loss(y_true,LOSS_HUBER,0.5);
   Print(loss2);
 
/* Result
   0.155
   0.15125
*/

```
