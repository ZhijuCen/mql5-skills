# HistoryNameWidth (Get method)

Returns the maximum allowed length for displaying a curve name.

```
int  HistoryNameWidth()

```

Return Value

Maximum length in pixels.

Note

If the curve name exceeds the maximum allowed length, it is truncated and dots are added to its end.

# HistoryNameWidth (Set method)

Sets the maximum allowed length for displaying a curve name.

```
void  HistoryNameWidth(
   const int  width      // maximum length
   )

```

Parameters

width

[in]  Maximum length in pixels.

Note

If the curve name exceeds the maximum allowed length, it is truncated and dots are added to its end.
