# Move

Renames/moves file.

```
bool  Move(
   const string  src_name,      // file name
   int           src_flag,      // flag
   const string  dst_name,      // file name
   int           dst_flags      // flags
   )

```

Parameters

src_name

[in]  Source file name.

src_flag

[in]  Source file flags (only FILE_COMMON is used).

dst_name

[in]  File name of the destination file.

dst_flags

[in]  Flags of the destination file (only FILE_REWRITE and FILE_COMMON are used).

Return Value

true - successful, false - failed to move/rename the file.
