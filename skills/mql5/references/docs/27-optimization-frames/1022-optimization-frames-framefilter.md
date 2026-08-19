# FrameFilter

Sets the frame reading filter and moves the pointer to the beginning.

```
bool  FrameFilter(
   const string  name,         // Public name/label
   long          id            // Public ID
   );

```

Return Value

Returns true if successful, otherwise false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

If an empty string is passed as the first parameter, the filter will work only with a numeric parameter, i.e. only frames with the specified id will be viewed. If the value of the second parameter is [ULONG_MAX](/en/docs/constants/namedconstants/typeconstants), only a text filter works.

Call of FrameFilter("", ULONG_MAX) is equivalent to calling [FrameFirst()](/en/docs/optimization_frames/framefirst), i.e. equal to not using any filter.
