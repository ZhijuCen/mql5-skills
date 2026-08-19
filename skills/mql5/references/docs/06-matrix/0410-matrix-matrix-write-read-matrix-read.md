Read

The method reads a matrix or a vector from a file written by the [Write](/en/docs/matrix/matrix_write_read/matrix_write) method.

```
long matrix::Read(
   int                file_handle      // file handle opened for reading
   );
 
long vector::Read(
   int                file_handle      // file handle opened for reading
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

Return Value

Returns the number of bytes read from the file. Or -1 in case of error.

Note

Reading is performed from the current file position. The file must be opened as binary for reading (FILE_BIN|FILE_READ flags). First, the [MqlMatrixInfo](/en/docs/matrix/matrix_classification/matrix_info#mqlmatrixinfo) structure is read, followed by the matrix contents according to the information in the read structure. Before reading data, the matrix size is adjusted according to info.rows and info.cols. The stored data type (info.data_type) may differ from the type of the matrix for which the method is called. In this case, the data is converted.
