WriteCSV

The method writes a matrix or a vector to a file according to its size and type.

```
long matrix::WriteCSV(
   int                file_handle,     // file handle opened to write
   ulong              flags=0,         // flags
   string             format_string="" // format string to output number
   );
 
long vector::WriteCSV(
   int                file_handle,     // file handle opened to write
   ulong              flags=0,         // flags
   string             format_string="" // format string to output number
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

flags

[in]  Can be set to MATRIX_CSV_USE_FORMATSTRING. In this case, a format string must be specified for output numbers.

format_string

[in]  String for formatting numbers.

Return Value

Returns the number of bytes written to the file. Or -1 in case of error.

Note

Writing is performed from the current file position. The file must be opened as CSV for writing (FILE_CSV|FILE_WRITE flags). The matrix or vector must have a nonzero size.

By default, numbers are output in the "%.17G" format. For example, if a matrix or vector stores normalized prices, it makes sense to use the "%.5f" format string.

The real and imaginary parts of complex numbers are formatted separately.
