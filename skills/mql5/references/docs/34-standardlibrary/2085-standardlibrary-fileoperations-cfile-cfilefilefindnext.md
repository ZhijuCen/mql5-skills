# FileFindNext

Continues file search started by the FileFindFirst() method.

```
bool  FileFindNext(
   int      search_handle,     // search handle
   string&  file_name          // reference
   )

```

Parameters

search_handle

[in]  Search handle returned by FileFindFirst() method.

file_name

[in]  The reference to the string the name of the found file is placed into if successful.

Return Value

true - successful, false - there are no files corresponding to the filter.
