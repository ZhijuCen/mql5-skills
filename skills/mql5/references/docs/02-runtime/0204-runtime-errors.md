# Runtime Errors

The executing subsystem of the client terminal has an opportunity to save the [error code](/en/docs/constants/errorswarnings/errorcodes) in case it occurs during a MQL5 program run. There is a predefined variable [_LastError](/en/docs/predefined/_lasterror) for each executable MQL5 program.

Before starting the [OnInit](/en/docs/event_handlers/oninit) function, the _LastError variable is reset. In case an erroneous situation occurs during calculations or in the process of internal function calls, the _LastError variable accepts a corresponding error code. The value stored in this variable can be obtained using the [GetLastError()](/en/docs/check/getlasterror) function.

There are several critical errors in case of which a program is terminated immediately:

- division by zero
- going beyond array boundary
- using an incorrect [object pointer](/en/docs/basis/types/object_pointers)
