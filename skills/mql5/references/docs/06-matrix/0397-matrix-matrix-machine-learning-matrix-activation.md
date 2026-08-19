# Activation

Compute activation function values and write them to the passed vector/matrix.

```
bool vector::Activation(
  vector&                   vect_out,      // vector to get values
  ENUM_ACTIVATION_FUNCTION  activation,    // activation function
   ...                                     // additional parameters
   );
 
 
bool matrix::Activation(
  matrix&                   matrix_out,    // matrix to get values
  ENUM_ACTIVATION_FUNCTION  activation     // activation function
   );
 
 
bool matrix::Activation(
  matrix&                   matrix_out,    // matrix to get values
  ENUM_ACTIVATION_FUNCTION  activation,    // activation function
  ENUM_MATRIX_AXIS          axis,          // axis
   ...                                     // additional parameters
   );

```

Parameters

vect_out/matrix_out

[out]  Vector or matrix to get the computed values of the activation function.

activation

[in]  Activation function from the [ENUM_ACTIVATION_FUNCTION](/en/docs/matrix/matrix_types/matrix_enumerations#enum_activation_function) enumeration.

axis

[in] [ENUM_MATRIX_AXIS](/en/docs/matrix/matrix_types/matrix_enumerations#enum_matrix_axis) enumeration value (AXIS_HORZ — horizontal axis, AXIS_VERT — vertical axis).

...

[in]  Additional parameters required for some activation functions. If no parameters are specified, default values are used.

Return Value

Returns true if successful, otherwise - false.

Additional Parameters

Some activation functions accept additional parameters. If no parameters are specified, default values are used

```
   AF_ELU  (Exponential Linear Unit)  
     double alpha=1.0
   
   Activation function: if(x>=0) f(x) = x
                      else f(x) = alpha * (exp(x)-1)
   
   
   AF_LINEAR   
     double alpha=1.0
     double beta=0.0
   
   Activation function: f(x) = alpha*x + beta
   
   
   AF_LRELU   (Leaky REctified Linear Unit)   
     double alpha=0.3
   
   Activation function: if(x>=0) f(x)=x
                      else f(x) = alpha*x
   
                        
   AF_RELU  (REctified Linear Unit)   
     double alpha=0.0
     double max_value=0.0
     double treshold=0.0
   
   Activation function: if(alpha==0) f(x) = max(x,0)
                      else if(x>max_value) f(x) = x
                      else f(x) = alpha*(x - treshold)
   
   
   AF_SWISH   
     double beta=1.0
   
   Activation function: f(x) = x / (1+exp(-x*beta))
   
   
   AF_TRELU   (Thresholded REctified Linear Unit)   
     double theta=1.0
   
   Activation function: if(x>theta) f(x) = x
                      else f(x) = 0
   
   
   AF_PRELU   (Parametric REctified Linear Unit)   
     double alpha[] - learned array of coeefficients
   
   Activation function: if(x[i]>=0) f(x)[i] = x[i]
                      else f(x)[i] = alpha[i] * x[i]

```

Note

In artificial neural networks, the activation function of a neuron determines the output signal, which is defined by an input signal or a set of input signals. The selection of the activation function has a big impact on the neural network performance. Different model parts (layers) can use different activation functions.

Examples of using additional parameters:

```
   vector x={0.1, 0.4, 0.9, 2.0, -5.0, 0.0, -0.1};
   vector y;
 
   x.Activation(y,AF_ELU);
   Print(y);
   x.Activation(y,AF_ELU,2.0);
   Print(y);
 
   Print("");
   x.Activation(y,AF_LINEAR);
   Print(y);
   x.Activation(y,AF_LINEAR,2.0);
   Print(y);
   x.Activation(y,AF_LINEAR,2.0,5.0);
   Print(y);
 
   Print("");
   x.Activation(y,AF_LRELU);
   Print(y);
   x.Activation(y,AF_LRELU,1.0);
   Print(y);
   x.Activation(y,AF_LRELU,0.1);
   Print(y);
  
   Print("");
   x.Activation(y,AF_RELU);
   Print(y);
   x.Activation(y,AF_RELU,2.0,0.5);
   Print(y);
   x.Activation(y,AF_RELU,2.0,0.5,1.0);
   Print(y);
 
   Print("");
   x.Activation(y,AF_SWISH);
   Print(y);
   x.Activation(y,AF_SWISH,2.0);
   Print(y);
 
   Print("");
   x.Activation(y,AF_TRELU);
   Print(y);
   x.Activation(y,AF_TRELU,0.3);
   Print(y);
 
   Print("");
   vector a=vector::Full(x.Size(),2.0);
   x.Activation(y,AF_PRELU,a);
   Print(y);
 
/*  Results
   [0.1,0.4,0.9,2,-0.993262053000915,0,-0.095162581964040]
   [0.1,0.4,0.9,2,-1.986524106001829,0,-0.190325163928081]
   
   [0.1,0.4,0.9,2,-5,0,-0.1]
   [0.2,0.8,1.8,4,-10,0,-0.2]
   [5.2,5.8,6.8,9,-5,5,4.8]
   
   [0.1,0.4,0.9,2,-1.5,0,-0.03]
   [0.1,0.4,0.9,2,-5,0,-0.1]
   [0.1,0.4,0.9,2,-0.5,0,-0.01]
   
   [0.1,0.4,0.9,2,0,0,0]
   [0.2,0.8,0.9,2,-10,0,-0.2]
   [-1.8,-1.2,0.9,2,-12,-2,-2.2]
   
   [0.052497918747894,0.239475064044981,0.6398545523625035,1.761594155955765,-0.03346425462142428,0,-0.047502081252106]
   [0.054983399731247,0.275989792451045,0.7723340415895611,1.964027580075817,-0.00022698934351217,0,-0.045016600268752]
   
   [0,0,0,2,0,0,0]
   [0,0.4,0.9,2,0,0,0]
   
   [0.1,0.4,0.9,2,-10,0,-0.2]
*/  

```
