# WindowIsVisible

Gets visibility flag of the specified chart subwindow.

```
bool  WindowIsVisible(
   int  num      // subwindow
   ) const

```

Parameters

num

[in]  Subwindow number (0 means main window).

Return Value

Returns visibility flag of the specified chart subwindow assigned to the chart instance.  If there is no chart assigned, it returns false.
