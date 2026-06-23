# Init

Initialize a matrix or a vector.

```
void matrix::Init(
  const ulong  rows,            // number of rows
  const ulong  cols,            // number of columns
  func_name    init_func=NULL,  // init function placed in some scope or static method of class
   ...         parameters
   );
 
void vector::Init(
  const ulong  size,            // vector size
  func_name    init_func=NULL,  // init function placed in some scope or static method of class
   ...         parameters
   );
 

```

Parameters

rows

[in]  Number of rows.

cols

[in]  Number of columns.

func_name

[in] Initializing function.

...

[in] Parameters of the initializing function.

Return Value

No return value.

Example

```
template<typename T>
void MatrixArange(matrix<T> &mat,T value=0.0,T step=1.0)
  {
   for(ulong i=0; i<mat.Rows(); i++)
     {
      for(ulong j=0; j<mat.Cols(); j++,value+=step)
         mat[i][j]=value;
     }
  }
template<typename T>
void VectorArange(vector<T> &vec,T value=0.0,T step=1.0)
  {
   for(ulong i=0; i<vec.Size(); i++,value+=step)
      vec[i]=value;
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
  int size_m=3, size_k=4;
  matrix  m(size_m,size_k,MatrixArange,-2.,0.1); // first an uninitialized matrix sized size_m x size_k is created,
  Print("matrix m \n",m);                        // then function MatrixArange with the parameters listed at initialization is called
  matrixf m_float(5,5,MatrixArange,-2.f,0.1f);   // after a matrix of float type is created, the MatrixArange function is called
  Print("matrix m_float \n",m_float);
  vector  v(size_k,VectorArange,-10.0);          // after a vector is created, VectorArange with one parameter is called; its second parameter is the default
  Print("vector v \n",v);  
  /*
   matrix m 
   [[-2,-1.9,-1.8,-1.7]
    [-1.6,-1.5,-1.399999999999999,-1.299999999999999]
    [-1.199999999999999,-1.099999999999999,-0.9999999999999992,-0.8999999999999992]]
   matrix m_float 
   [[-2,-1.9,-1.8,-1.6999999,-1.5999999]
    [-1.4999999,-1.3999999,-1.2999998,-1.1999998,-1.0999998]
    [-0.99999976,-0.89999974,-0.79999971,-0.69999969,-0.59999967]
    [-0.49999967,-0.39999968,-0.29999968,-0.19999969,-0.099999689]
    [3.1292439e-07,0.10000031,0.20000032,0.30000031,0.4000003]]
   vector v 
   [-10,-9,-8,-7]
  */ 
  }

```
