# Class for working with OpenCL programs

The COpenCL class is a wrapper to facilitate working with the [OpenCL functions](/en/docs/opencl). In some cases, use of the GPU allows to substantially increase the speed of computations.

Examples of class use for calculations based on float and double values can be found in the corresponding subdirectories of the MQL5\Scripts\Examples\OpenCL\ folder. The source codes of the OpenCL programs are located in MQL5\Scripts\Examples\OpenCL\Double\Kernels and MQL5\Scripts\Examples\OpenCL\Float\Kernels subdirectories.

- MatrixMult.mq5 - example of matrix multiplication using global and local memory
- BitonicSort.mq5 - example of parallel sorting of array elements in GPU
- FFT.mq5 - example of fast Fourier transform calculation
- Wavelet.mq5 - example of wavelet transform of data using the Morlet wavelet.

It is recommended to write the source code for OpenCL in separate CL files, which can later be included in the MQL5 program using the [resource variables](/en/docs/runtime/resources#resourcevariables).

### Declaration

```
   class COpenCL

```

### Title

```
   #include <OpenCL\OpenCL.mqh>

```

### Class methods

| Name | Description |
| --- | --- |
| BufferCreate | Creates an OpenCL buffer at the specified index |
| BufferFree | Deletes buffer at the specified index |
| BufferFromArray | Creates a buffer at the specified index from an array of values |
| BufferRead | Reads an OpenCL buffer at the specified index into an array |
| BufferWrite | Writes an array of values into buffer at the specified index |
| Execute | Executes the OpenCL kernel with the specified index |
| GetContext | Returns handle of the OpenCL context |
| GetKernel | Returns handle of the kernel object at the specified index |
| GetKernelName | Returns name of the kernel object at the specified index |
| GetProgram | Returns handle of the OpenCL program |
| Initialize | Initializes the OpenCL program |
| KernelCreate | Creates an entry point into the OpenCL program at the specified index |
| KernelFree | Removes an OpenCL start function at the specified index |
| SetArgument | Sets a parameter for the OpenCL function at the specified index |
| SetArgumentBuffer | Sets an OpenCL buffer as a parameter of the OpenCL function at the specified index |
| SetArgumentLocalMemory | Sets a parameter in local memory for the OpenCL function at the specified index |
| SetBuffersCount | Sets the number of buffers |
| SetKernelsCount | Sets the number of kernel objects |
| Shutdown | Unloads the OpenCL program |
| SupportDouble | Checks if floating point data types are supported on the device |
