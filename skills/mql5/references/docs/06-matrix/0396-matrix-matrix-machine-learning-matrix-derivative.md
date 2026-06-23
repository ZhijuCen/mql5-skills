# Derivative

Compute activation function derivative values and write them to the passed vector/matrix

```
bool vector::Derivative(
  vector&                   vect_out,      // vector to get values
  ENUM_ACTIVATION_FUNCTION  activation,    // activation function
   ...                                     // additional parameters
   );
 
 
bool matrix::Derivative(
  matrix&                   matrix_out,    // matrix to get values
  ENUM_ACTIVATION_FUNCTION  activation,    // activation function
   );
 
 
bool matrix::Derivative(
  matrix&                   matrix_out,    // matrix to get values
  ENUM_ACTIVATION_FUNCTION  activation,    // activation function
  ENUM_MATRIX_AXIS          axis,          // axis
   ...                                     // additional parameters
   );

```

Parameters

vect_out/matrix_out

[out]  Vector or matrix to get the computed values of the derivative of the activation function.

activation

[in]  Activation function from the [ENUM_ACTIVATION_FUNCTION](/en/docs/matrix/matrix_types/matrix_enumerations#enum_activation_function) enumeration.

axis

[in] [ENUM_MATRIX_AXIS](/en/docs/matrix/matrix_types/matrix_enumerations#enum_matrix_axis) enumeration value (AXIS_HORZ — horizontal axis, AXIS_VERT — vertical axis).

...

[in]  Additional parameters are the same as that of the activation functions. Only some activation functions accept additional parameters. If no parameters are specified, default values are used.

Return Value

Returns true if successful, otherwise - false.

Note

Function derivatives enable an efficient update of model parameters based on the error received in learning during the error backpropagation.
