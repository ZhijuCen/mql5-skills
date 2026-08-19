Write

The method analyzes the matrix contents, determines its structural type (symmetric, Hermitian, triangular, banded, and so on), and writes the contents of the matrix to the open file in accordance with the selected storage method.

```
long matrix::Write(
   int                file_handle,     // file handle opened to write
   ENUM_BLAS_STORAGE  storage_method   // how to write
   );
 
long vector::Write(
   int                file_handle,     // file handle opened to write
   ENUM_BLAS_STORAGE  storage_method   // how to write
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

storage_method

[in]  [ENUM_BLAS_STORAGE](/en/docs/matrix/matrix_write_read/matrix_write#enum_blas_storage) enumeration value which determines the method for writing.

Return Value

Returns the number of bytes written to the file. Or -1 in case of error.

Note

Writing is performed from the current file position. The file must be opened as binary for writing (FILE_BIN|FILE_WRITE flags). First, the [MqlMatrixInfo](/en/docs/matrix/matrix_classification/matrix_info#mqlmatrixinfo) structure is written, followed by the matrix contents according to the selected storage method. The matrix must have a nonzero size.

If the BLASSTORAGE_GENERAL method is selected, the matrix is stored as is.

If the BLASSTORAGE_COMPACT method is selected, the matrix is stored as compactly as possible. For example, if the matrix is identified as general band (GB), the size (kl+ku+1)*cols is calculated. If this size is smaller than rows*cols, the matrix is written as general band; otherwise, it is written as general (GE). If a general matrix (GE) contains a significant number of zeros (info.nnz < info.rows*info.cols), it can be stored as sparse in the coordinate "sparse COO" format. The stored data size is calculated as info.nnz*sizeof(row_index) + info.nnz*sizeof(col_index) + nnz*sizeof(type). If this size is smaller than the size required to store a general matrix, the matrix is stored as sparse, while the matrix class info.matrix_class is set to BLASTYPE_CO and the corresponding 'CO' signature is set.

If the BLASSTORAGE_BAND method is selected and kl>=0 and ku>=0, the matrix is written as band: general band (GB), symmetric band (SB), Hermitian band (HB), or triangular band (TB).

When writing a vector, storage_method can be BLASSTORAGE_GENERAL or BLASSTORAGE_COMPACT. For compact vector storage, the size is calculated using the formula info.nnz*sizeof(index) + info.nnz*sizeof(type). If the sparse COO storage size is smaller than size * sizeof(type), the vector is stored as sparse.

ENUM_BLAS_STORAGE

Enumeration defining the matrix storage method.

| ID | Description |
| --- | --- |
| BLASSTORAGE_GENERAL | Store as is |
| BLASSTORAGE_COMPACT | Compact store |
| BLASSTORAGE_BAND | Band store |
