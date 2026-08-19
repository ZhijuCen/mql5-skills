ReadBin

The method reads a matrix or a vector from a file written by the [WriteBin](/en/docs/matrix/matrix_write_read/matrix_write_bin) method.

```
long matrix::ReadBin(
   int                file_handle      // file handle opened for reading
   );
 
long vector::ReadBin(
   int                file_handle      // file handle opened for reading
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

Return Value

Returns the number of bytes read from the file. Or -1 in case of error.

Note

Reading is performed from the current file position. The file must be opened as binary for reading (FILE_BIN|FILE_READ flags). The matrix or vector must have a nonzero size. Reading is performed according to the matrix (vector) size and type.
