WriteBin

The method writes a matrix or a vector to a file according to its size and type.

```
long matrix::WriteBin(
   int                file_handle      // file handle opened to write
   );
 
long vector::WriteBin(
   int                file_handle      // file handle opened to write
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

Return Value

Returns the number of bytes written to the file. Or -1 in case of error.

Note

Writing is performed from the current file position. The file must be opened as binary for writing (FILE_BIN|FILE_WRITE flags). The matrix or vector must have a nonzero size.
