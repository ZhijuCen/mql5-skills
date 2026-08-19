# FileFindFirst

Begins file search using the specified filter.

```
int  FileFindFirst(
   const string  filter,        // search filter
   string&       file_name      // reference
   )

```

Parameters

filter

[in]  Search filter.

file_name

[out]  The reference to the string the name of the first found file is placed into in case of success.

Return Value

The handle that can be used for further file search using FileFindNext, or INVALID_HANDLE if there are no files corresponding to the filter.

Note

The working folder is dependent on the flag previously set/reset by SetCommon() method.
