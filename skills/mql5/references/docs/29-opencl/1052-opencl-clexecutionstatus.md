# CLExecutionStatus

Returns the OpenCL program execution status.

```
int  CLExecutionStatus(
   int   kernel            // handle to a kernel of an OpenCL program
   );

```

Parameters

kernel

[in]  Handle to a kernel of the OpenCL program.

Return Value

Returns the OpenCL program status. The value can be one of the following:

- CL_COMPLETE=0 – program complete,
- CL_RUNNING=1 – running,
- CL_SUBMITTED=2 – submitted for execution,
- CL_QUEUED=3 – queued,
- -1 (minus one) – error occurred when executing CLExecutionStatus().
