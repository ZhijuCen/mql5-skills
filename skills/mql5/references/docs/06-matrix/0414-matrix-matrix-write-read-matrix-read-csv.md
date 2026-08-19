ReadCSV

The method reads a matrix or a vector from a file written by the [WriteCSV](/en/docs/matrix/matrix_write_read/matrix_write_csv) method.

```
long matrix::ReadCSV(
   int                file_handle,     // file handle opened for reading
   ulong              flags=0          // flags
   );
 
long vector::ReadCSV(
   int                file_handle,     // file handle opened for reading
   ulong              flags=0          // flags
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

flags

[in]  Can be a combination of MATRIX_CSV_SKIP_HEADER and MATRIX_CSV_RESIZE values.

Return Value

Returns the number of bytes read from the file. Or -1 in case of error.

Note

Reading is performed from the current file position. The file must be opened as CSV for reading (FILE_CSV|FILE_READ flags). If the MATRIX_CSV_RESIZE flag is not set, the matrix or vector must have a nonzero size.

If the MATRIX_CSV_RESIZE flag is set, the matrix or vector can be of any size. The size is set according to the number of rows and columns in the read data.

Real-type data can be read into a complex-type matrix or vector. In this case, the imaginary parts of complex numbers are set to 0.

Complex-type data can be read into a real-type matrix or vector. In this case, all imaginary parts are discarded.

If the MATRIX_CSV_SKIP_HEADER flag is set, the first line from the current file position is skipped.
