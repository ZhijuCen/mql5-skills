# CLBufferWrite

Writes into the OpenCL buffer and returns the number of written elements.

```
uint  CLBufferWrite(
   int          buffer,                    // A handle to the OpenCL buffer
   const void&  data[],                    // An array of values
   uint         buffer_offset=0,           // An offset in the OpenCL buffer in bytes, 0 by default
   uint         data_offset=0,             // An offset in the array in elements, 0 by default
   uint         data_count=WHOLE_ARRAY     // The number of values from the array for writing, the whole array by default
   );

```

There are also versions for handling [matrices and vectors](/en/docs/matrix).

Writes the values from the matrix to the buffer and returns true if successful.

```
uint  CLBufferWrite(
   int           buffer,                    // a handle to the OpenCL buffer
   uint          buffer_offset,             // an offset in the OpenCL buffer in bytes
   matrix<T>     &mat                       // the values matrix for writing to the buffer
   );

```

Writes the values from the vector to the buffer and returns true if successful.

```
uint  CLBufferWrite(
   int           buffer,                    // a handle to the OpenCL buffer
   uint          buffer_offset,             // an offset in the OpenCL buffer in bytes
   vector<T>     &vec                       // the values vector for writing to the buffer
   );

```

Parameters

buffer

[in]  A handle of the OpenCL buffer.

data[]

[in]  An array of values that should be written in the OpenCL buffer. Passed by reference.

buffer_offset

[in]  An offset in the OpenCL buffer in bytes, from which writing begins. By default, writing start with the very beginning of the buffer.

data_offset

[in]  The index of the first array element, starting from which values from the array are written in the OpenCL buffer. By default, values from the very beginning of the array are taken.

data_count

[in]  The number of values that should be written. All the values of the array, by default.

mat

[out]  The matrix for reading data from the buffer can be any of the three types — matrix, matrixf or matrixc.

vec

[out]  The vector for reading data from the buffer can be of any of the three types — vector, vectorf or vectorc.

Return Value

The number of written elements. 0 is returned in case of an error. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

true if a matrix or a vector is handled successfully, otherwise false.

Note

For one-dimensional arrays, the number of the element, with which reading of data for writing into an OpenCL buffer begins, is calculated taking into account the [AS_SERIES](/en/docs/array/arraygetasseries) flags.

An array of two or more dimensions is presented as one-dimensional. In this case, data_offset is the number of elements that should be skipped in the presentation, not the number of elements in the first dimension.

Example of matrix multiplication using the [MatMul](/en/docs/matrix/matrix_products/matrix_matmul) method and parallel computing in OpenCL

```
#define M       3000      // the number of rows in the first matrix
#define K       2000      // the number of columns in the first matrix is equal to the number of rows in the second one 
#define N       3000      // the number of columns in the second matrix
 
//+------------------------------------------------------------------+
const string clSrc=
  "#define N     "+IntegerToString(N)+"                              \r\n"
  "#define K     "+IntegerToString(K)+"                              \r\n"
  "                                                                  \r\n"
  "__kernel void matricesMul( __global float *in1,                   \r\n"
  "                           __global float *in2,                   \r\n"
  "                           __global float *out  )                 \r\n"
  "{                                                                 \r\n"
  "  int m = get_global_id( 0 );                                     \r\n"
  "  int n = get_global_id( 1 );                                     \r\n"
  "  float sum = 0.0;                                                \r\n"
  "  for( int k = 0; k < K; k ++ )                                   \r\n"
  "     sum += in1[ m * K + k ] * in2[ k * N + n ];                  \r\n"
  "  out[ m * N + n ] = sum;                                         \r\n"
  "}                                                                 \r\n";
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- initialize the random number generator
  MathSrand((int)TimeCurrent());
//--- fill in the matrices of a given size with random values
  matrixf mat1(M, K, MatrixRandom) ;    // first matrix
  matrixf mat2(K, N, MatrixRandom);     // second matrix
 
//--- calculate the product of matrices using naive method
  uint start=GetTickCount();
  matrixf matrix_naive=matrixf::Zeros(M, N);// the result of multiplying two matrices is set here
  for(int m=0; m<M; m++)
    for(int k=0; k<K; k++)
      for(int n=0; n<N; n++)
        matrix_naive[m][n]+=mat1[m][k]*mat2[k][n];
  uint time_naive=GetTickCount()-start;   
     
//--- calculate the product of matrices via MatMull
  start=GetTickCount();
  matrixf matrix_matmul=mat1.MatMul(mat2);
  uint time_matmul=GetTickCount()-start;     
  
//--- calculate the product of matrices in OpenCL
  matrixf matrix_opencl=matrixf::Zeros(M, N);
  int cl_ctx;             // context handle
  if((cl_ctx=CLContextCreate(CL_USE_GPU_ONLY))==INVALID_HANDLE)
   {
    Print("OpenCL not found, leaving");
    return;
   }
  int cl_prg;             // program handle 
  int cl_krn;             // kernel handle
  int cl_mem_in1;         // first (input) buffer handle
  int cl_mem_in2;         // second (input) buffer handle
  int cl_mem_out;         // third (output) buffer handle
//--- create the program and the kernel
  cl_prg = CLProgramCreate(cl_ctx, clSrc);
  cl_krn = CLKernelCreate(cl_prg, "matricesMul");
//--- create all three buffers for three matrices
  cl_mem_in1=CLBufferCreate(cl_ctx, M*K*sizeof(float), CL_MEM_READ_WRITE);
  cl_mem_in2=CLBufferCreate(cl_ctx, K*N*sizeof(float), CL_MEM_READ_WRITE);
//--- third matrix - output
  cl_mem_out=CLBufferCreate(cl_ctx, M*N*sizeof(float), CL_MEM_READ_WRITE);
//--- set the kernel arguments
  CLSetKernelArgMem(cl_krn, 0, cl_mem_in1);
  CLSetKernelArgMem(cl_krn, 1, cl_mem_in2);
  CLSetKernelArgMem(cl_krn, 2, cl_mem_out);
//--- write matrices to the device buffers
  CLBufferWrite(cl_mem_in1, 0, mat1);
  CLBufferWrite(cl_mem_in2, 0, mat2);
  CLBufferWrite(cl_mem_out, 0, matrix_opencl);
//--- OpenCL code execution time start
  start=GetTickCount();
//--- set the parameters of the task working area and execute the OpenCL program
  uint  offs[2] = {0, 0};
  uint works[2] = {M, N};
  start=GetTickCount();  
  bool ex=CLExecute(cl_krn, 2, offs, works);
//--- calculate the result to the matrix
  if(CLBufferRead(cl_mem_out, 0, matrix_opencl))
    PrintFormat("[%d x %d] matrix read: ", matrix_opencl.Rows(), matrix_opencl.Cols());
   else
      Print("CLBufferRead(cl_mem_out, 0, matrix_opencl failed. Error ",GetLastError()); 
  uint time_opencl=GetTickCount()-start;   
  Print("Compare calculation time using each method");
  PrintFormat("Naive product time = %d ms",time_naive);
  PrintFormat("MatMul product time = %d ms",time_matmul);
  PrintFormat("OpenCl product time = %d ms",time_opencl);  
//--- release all OpenCL contexts
  CLFreeAll(cl_ctx, cl_prg, cl_krn, cl_mem_in1, cl_mem_in2, cl_mem_out);
 
//--- compare all obtained result matrices with each other
  Print("How many discrepancy errors are there between result matrices?");
  ulong errors=matrix_naive.Compare(matrix_matmul,(float)1e-12);
  Print("matrix_direct.Compare(matrix_matmul,1e-12)=",errors);
  errors=matrix_matmul.Compare(matrix_opencl,float(1e-12));
  Print("matrix_matmul.Compare(matrix_opencl,1e-12)=",errors);
/*
  Result:
   
   [3000 x 3000] matrix read: 
  Compare the time of calculation with each method
   Naive product time = 54750 ms
   MatMul product time = 4578 ms
   OpenCl product time = 922 ms
   How many discrepancy errors are there between result matrices?
   matrix_direct.Compare(matrix_matmul,1e-12)=0
   matrix_matmul.Compare(matrix_opencl,1e-12)=0
*/  
 }
//+------------------------------------------------------------------+
//| Fills the matrix with random values                              |
//+------------------------------------------------------------------+
void MatrixRandom(matrixf& m)
 {
  for(ulong r=0; r<m.Rows(); r++)
   {
    for(ulong c=0; c<m.Cols(); c++)
     {
      m[r][c]=(float)((MathRand()-16383.5)/32767.);
     }
   }
 }
//+------------------------------------------------------------------+
//| Release all OpenCL contexts                                      |
//+------------------------------------------------------------------+
void CLFreeAll(int cl_ctx, int cl_prg, int cl_krn,
               int cl_mem_in1, int cl_mem_in2, int cl_mem_out)
 {
//--- delete all contexts created by OpenCL in reverse order
  CLBufferFree(cl_mem_in1);
  CLBufferFree(cl_mem_in2);
  CLBufferFree(cl_mem_out);
  CLKernelFree(cl_krn);
  CLProgramFree(cl_prg);
  CLContextFree(cl_ctx);
 }

```
