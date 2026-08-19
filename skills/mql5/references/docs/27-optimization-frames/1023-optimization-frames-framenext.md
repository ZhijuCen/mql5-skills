# FrameNext

Reads a frame and moves the pointer to the next one. There are two variants of the function.

1. Calling to receive one numeric value

```
bool  FrameNext(
   ulong&   pass,      // The number of a pass in the optimization, during which the frame has been added
   string&  name,      // Public name/label
   long&    id,        // Public ID
   double&  value      // Value
   );

```

2. Calling to receive all the data of a frame

```
bool  FrameNext(
   ulong&   pass,      // The number of a pass in the optimization, during which the frame has been added
   string&  name,      // Public name/label
   long&    id,        // Public ID
   double&  value,     // Value
   void&    data[]     // Array of any type
   );

```

Parameters

pass

[out]  The number of a pass during optimization in the strategy tester.

name

[out]  The name of the identifier.

id

[out]  The value of the identifier.

value

[out]  A single numeric value.

data

[out]  An array of any type.

Return Value

Returns true if successful, otherwise false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

In the second version of the call, you must correctly handle the received data in the data[] array.
