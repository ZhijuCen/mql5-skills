# Handling runtime errors

Any program written correctly enough to compile without errors is still not immune to runtime errors. They can occur both due to an oversight of the developer and due to unforeseen circumstances that have arisen in the software environment (such as Internet connection loss, running out of memory, etc.). But no less likely is the situation when the error occurs due to incorrect application of the program. In all these cases, the program must be able to analyze the essence of the problem and process it adequately.

Each MQL5 statement is a potential source of runtime errors. If such an error occurs, the terminal saves a descriptive code to the special _LastError variable. Make sure to analyze the code immediately after each statement, since potential errors in subsequent statements can overwrite this value.

Please note that there are a number of critical errors that will immediately abort program execution when they occur:

- Zero divide
- Index out of range
- Incorrect object pointer

For a complete list of error codes and what they mean, see the [documentation](https://www.mql5.com/en/docs/constants/errorswarnings/errorcodes).

In the [Opening and closing files](/en/book/common/files/files_open_close) section, we've already addressed the problem of diagnosing errors as part of writing a useful PRTF macro. There, in particular, we have seen an auxiliary header file MQL5/Include/MQL5Book/MqlError.mqh, in which the MQL_ERROR enumeration allow easy conversion of the numeric error code into a name using EnumToString.

```
enum MQL_ERROR
{
   SUCCESS = 0, 
   INTERNAL_ERROR = 4001, 
   WRONG_INTERNAL_PARAMETER = 4002, 
   INVALID_PARAMETER = 4003, 
   NOT_ENOUGH_MEMORY = 4004, 
   ...
   // start of area for errors defined by the programmer (see next section)
   USER_ERROR_FIRST = 65536, 
};
#define E2S(X) EnumToString((MQL_ERROR)(X))

```

Here, as the X parameter of the E2S macro, we should have the _LastError variable or its equivalent GetLastError function.

int GetLastError() ≡ int _LastError

The function returns the code of the last error that occurred in the MQL program statements. Initially, while there are no errors, the value is 0. The difference between reading _LastError and calling the GetLastError function is purely syntactic (choose the appropriate option in accordance with the preferred style).

It should be borne in mind that regular error-free execution of statements does not reset the error code. Calling GetLastError also does not do it.

Thus, if there is a sequence of actions, in which only one will set an error flag, this flag will be returned by the function for subsequent (successful) actions. For example,

```
// _LastError = 0 by default
action1; // ok, _LastError doe not change
action2; // error, _LastError = X
action3; // ok, _LastError does not change, i.e. is still equal to X
action4; // another error, _LastError = Y
action5; // ok, _LastError does not change, that is, it is still equal to Y
action6; // ok, _LastError does not change, that is, it is still equal to Y

```

This behavior would make it difficult to localize the problem area. To avoid this, there is a separate ResetLastError function that resets the _LastError variable to 0.

void ResetLastError()

The function sets the value of the built-in _LastError variable to zero.

It is recommended to call the function before any action that can lead to an error and after which you are going to analyze errors using GetLastError.

A good example of using both functions is the already mentioned PRTF macro (PRTF.mqh file). Its code is shown below:

```
#include <MQL5Book/MqlError.mqh>
   
#define PRTF(A) ResultPrint(#A, (A))
   
template<typename T>
T ResultPrint(const string s, const T retval = NULL)
{
   const int snapshot = _LastError; // recording _LastError at input
   const string err = E2S(snapshot) + "(" + (string)snapshot + ")";
   Print(s, "=", retval, " / ", (snapshot == 0 ? "ok" : err));
   ResetLastError(); // clear the error flag for the next calls
   return retval;
}

```

The purpose of the macro and of the ResultPrint function wrapped into it is to log the passed value, which is the current error code, and to immediately clear the error code. Thus, successive application of PRTF on a number of statements always ensures that the error (or success indication) printed to the log corresponds to the last statement with which the value of the retval parameter was obtained.

We need to save _LastError in the intermediate local variable snapshot because _LastError can change its value almost anywhere in the evaluation of an expression if any operation fails. In this particular example, the E2S macro uses the EnumToString function which may raise its own error code if a value that is not in the enumeration is passed as an argument. Then, in the subsequent parts of the same expression, when forming a string, we will see not the initial error but the raised one.

There may be several places in any statement where _LastError suddenly changes. In this regard, it is desirable to record the error code immediately after the desired action.
