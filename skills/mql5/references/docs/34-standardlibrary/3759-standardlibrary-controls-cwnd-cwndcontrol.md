# Control

Gets the control from the container by index.

```
CWnd*  Control(
   const int  ind      // index
   )  const

```

Parameters

ind

[in]  Control index.

Return Value

A pointer to the control.

Note

The base class method does not have the container, it provides the access to container for its heirs and always returns NULL.
