# StartIndex

Gets the index of starting bar to analyze.

```
virtual int  StartIndex()

```

Return Value

The index of starting bar to analyze.

Note

The method returns 0 if the flag to analyze current bar is set to true (analysis from the current bar). If the flag is not set, it returns 1 (analysis from the last completed bar).
