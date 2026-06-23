# int _StopFlag

The _StopFlag variable contains the mql5 program stop flag equal to 0 during normal operation. When the client terminal tries to stop the program, the variable is set to a value other than zero.

To check the state of the _StopFlag you may also use the [IsStopped()](/en/docs/check/isstopped) function.
