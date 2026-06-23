# Copy

Copies a file.

```
bool  Copy(
   const string  src_name,      // file name
   int           src_flag,      // flag
   const string  dst_name,      // file name
   int           dst_flags      // flags
   )

```

Parameters

src_name

[in]  Name of a source file.

src_flag

[in]  Flags of a source file (only FILE_COMMON is used).

dst_name

[in]  File name of the destination file.

dst_flags

[in]  Flags of the destination file (only FILE_REWRITE and FILE_COMMON are used).

Return Value

true - successful, false - cannot copy the file.
