# Machine learning

These methods are used in machine learning.

The neural network activation function determines the output value of a neuron depending on the weighted sum of inputs. The selection of the activation function has a big impact on the neural network performance. Different model parts (layers) can use different activation functions.

In addition to all known activation functions, MQL5 also offers their derivatives. Function derivatives enable an efficient update of model parameters based on the error received in learning.

A neural network aims at finding an algorithm that minimizes the error in learning, for which the loss function is used. The value of the loss function indicates by how much the value predicted by the model deviates from the real one. Different loss functions are used depending on the problem. For example, Mean Squared Error ([MSE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for regression problems, and Binary Cross-Entropy ([BCE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_loss_function)) is used for binary classification purposes.

| Function | Action |
| --- | --- |
| Activation | Compute activation function values and write them to the passed vector/matrix |
| Derivative | Compute activation function derivative values and write them to the passed vector/matrix |
| Loss | Compute loss function values and write them to the passed vector/matrix |
| LossGradient | Compute a vector or matrix of loss function gradients |
| RegressionMetric | Compute the regression metric as the deviation error from the regression line constructed on the specified data array |
| ConfusionMatrix | Compute confusion matrix. The method is applied to the vector of predicted values |
| ConfusionMatrixMultilabel | Compute confusion matrix for each label. The method is applied to the vector of predicted values |
| ClassificationMetric | Compute the classification metric to evaluate the quality of the predicted data compared to the true data The method is applied to the vector of predicted values |
| ClassificationScore | Compute the classification metric to evaluate the quality of the predicted data compared to the true data |
| PrecisionRecall | Compute values to construct a precision-recall curve. Similarly to  ClassificationScore , this method is applied to the vector of true values |
| ReceiverOperatingCharacteristic | Compute values to construct the Receiver Operating Characteristic (ROC) curve. Similarly to  ClassificationScore , this method is applied to the vector of true values. |

Example

This example demonstrates the training of a model using matrix operations. The model is trained for the function (a + b + c)^2 / (a^2 + b^2 + c^2). We input the initial data matrix, in which a, b and c are contained in different columns. The function result is obtained at the model output.

```
matrix weights1, weights2, weights3;               // matrices of weights
matrix output1, output2, result;                   // matrices of neural layer outputs
input int layer1 = 200;                            // the size of the first hidden layer
input int layer2 = 200;                            // the size of the second hidden layer
input int Epochs = 20000;                          // the number of training epochs
input double lr = 3e-6;                            // learning rate
input ENUM_ACTIVATION_FUNCTION ac_func = AF_SWISH; // activation function
//+------------------------------------------------------------------+
//| Script start function                                            |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int train = 1000;    // training sample size
   int test = 10;       // test sample size
   matrix m_data, m_target;
//--- generate a training sample
   if(!CreateData(m_data, m_target, train))  
      return;
//--- train the model
   if(!Train(m_data, m_target, Epochs))      
      return;
//--- generate a test sample
   if(!CreateData(m_data, m_target, test))   
      return;
//--- test the model
   Test(m_data, m_target);                   
  }
//+------------------------------------------------------------------+
//| Sample generation method                                         |
//+------------------------------------------------------------------+
bool CreateData(matrix &data, matrix &target, const int count)
  {
//--- initialize the initial data and result matrices
   if(!data.Init(count, 3) || !target.Init(count, 1))
      return false;
//--- fill the initial data matrix with random values
   data.Random(-10, 10);                     
//--- calculate the target values for the training sample
   vector X1 = MathPow(data.Col(0) + data.Col(1) + data.Col(1), 2);
   vector X2 = MathPow(data.Col(0), 2) + MathPow(data.Col(1), 2) + MathPow(data.Col(2), 2);
   if(!target.Col(X1 / X2, 0))
      return false;
//--- return result
   return true;
  }
//+------------------------------------------------------------------+
//| Model training method                                            |
//+------------------------------------------------------------------+
bool Train(matrix &data, matrix &target, const int epochs = 10000)
  {
//--- create the model
   if(!CreateNet())
      return false;
//--- train the model
   for(int ep = 0; ep < epochs; ep++)
     {
      //--- feedforward pass
      if(!FeedForward(data))
         return false;
      PrintFormat("Epoch %d, loss %.5f", ep, result.Loss(target, LOSS_MSE));
      //--- backpropagation and update of weight matrix
      if(!Backprop(data, target))
         return false;
     }
//--- return result
   return true;
  }
//+------------------------------------------------------------------+
//| Model creation method                                            |
//+------------------------------------------------------------------+
bool CreateNet()
  {
//--- initialize weight matrices
   if(!weights1.Init(4, layer1) || !weights2.Init(layer1 + 1, layer2) || !weights3.Init(layer2 + 1, 1))
      return false;
//--- fill the weight matrices with random values
   weights1.Random(-0.1, 0.1);
   weights2.Random(-0.1, 0.1);
   weights3.Random(-0.1, 0.1);
//--- return result
   return true;
  }
//+------------------------------------------------------------------+
//| Feedforward method                                               |
//+------------------------------------------------------------------+
bool FeedForward(matrix &data)
  {
//--- check the initial data size
   if(data.Cols() != weights1.Rows() - 1)
      return false;
//--- calculate the first neural layer
   matrix temp = data;
   if(!temp.Resize(temp.Rows(), weights1.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights1.Rows() - 1))
      return false;
   output1 = temp.MatMul(weights1);
//--- calculate the activation function
   if(!output1.Activation(temp, ac_func))
      return false;
//--- calculate the second neural layer
   if(!temp.Resize(temp.Rows(), weights2.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights2.Rows() - 1))
      return false;
   output2 = temp.MatMul(weights2);
//--- calculate the activation function
   if(!output2.Activation(temp, ac_func))
      return false;
//--- calculate the third neural layer
   if(!temp.Resize(temp.Rows(), weights3.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights3.Rows() - 1))
      return false;
   result = temp.MatMul(weights3);
//--- return result
   return true;
  }
//+------------------------------------------------------------------+
//| Backpropagation method                                           |
//+------------------------------------------------------------------+
bool Backprop(matrix &data, matrix &target)
  {
//--- check the size of the matrix of target values
   if(target.Rows() != result.Rows() ||
      target.Cols() != result.Cols())
      return false;
//--- determine the deviation of calculated values from target
   matrix loss = (target - result) * 2;
//--- propagate the gradient to the previous layer
   matrix gradient = loss.MatMul(weights3.Transpose());
//--- update the wight matrix of the last layer
   matrix temp;
   if(!output2.Activation(temp, ac_func))
      return false;
   if(!temp.Resize(temp.Rows(), weights3.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights3.Rows() - 1))
      return false;
   weights3 = weights3 + temp.Transpose().MatMul(loss) * lr;
//--- adjust the error gradient by the derivative of the activation function
   if(!output2.Derivative(temp, ac_func))
      return false;
   if(!gradient.Resize(gradient.Rows(), gradient.Cols() - 1))
      return false;
   loss = gradient * temp;
//--- propagate the gradient to a lower layer
   gradient = loss.MatMul(weights2.Transpose());
//--- update the weight matrix of the second hidden layer
   if(!output1.Activation(temp, ac_func))
      return false;
   if(!temp.Resize(temp.Rows(), weights2.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights2.Rows() - 1))
      return false;
   weights2 = weights2 + temp.Transpose().MatMul(loss) * lr;
//--- adjust the error gradient by the derivative of the activation function
   if(!output1.Derivative(temp, ac_func))
      return false;
   if(!gradient.Resize(gradient.Rows(), gradient.Cols() - 1))
      return false;
   loss = gradient * temp;
//--- update the weight matrix of the first hidden layer
   temp = data;
   if(!temp.Resize(temp.Rows(), weights1.Rows()) ||
      !temp.Col(vector::Ones(temp.Rows()), weights1.Rows() - 1))
      return false;
   weights1 = weights1 + temp.Transpose().MatMul(loss) * lr;
//--- return result
   return true;
  }
//+------------------------------------------------------------------+
//| Model testing method                                             |
//+------------------------------------------------------------------+
bool Test(matrix &data, matrix &target)
  {
//--- feedfarward on test data
   if(!FeedForward(data))
      return false;
//--- log the model calculation results and true values
   PrintFormat("Test loss %.5f", result.Loss(target, LOSS_MSE));
   ulong total = data.Rows();
   for(ulong i = 0; i < total; i++)
      PrintFormat("(%.2f + %.2f + %.2f)^2 / (%.2f^2 + %.2f^2 + %.2f^2) =  Net %.2f, Target %.2f", data[i, 0], data[i, 1], data[i, 2],
                  data[i, 0], data[i, 1], data[i, 2], result[i, 0], target[i, 0]);
//--- return result
   return true;
  }
//+------------------------------------------------------------------+

```
