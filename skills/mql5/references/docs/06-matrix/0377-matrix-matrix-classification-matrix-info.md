MatrixInfo

The method analyzes the matrix contents, determines its structural type (symmetric, Hermitian, triangular, banded, and so on), and fills the MqlMatrixInfo structure.

```
bool matrix::MatrixInfo(
  MqlMatrixInfo&  info      // matrix info
   );

```

Parameters

info

[out]  An object of the [MqlMatrixInfo](/en/docs/matrix/matrix_classification/matrix_info#mqlmatrixinfo) type where matrix information is placed.

Return Value

Returns true if the matrix is initialized and has a nonzero size. Otherwise, false is returned.

Note

The MqlMatrixInfo structure object contains more information than individual matrix classification methods can provide ([IsSymmetric](/en/docs/matrix/matrix_classification/matrix_issymmetric), [IsHermitian](/en/docs/matrix/matrix_classification/matrix_ishermitian), [IsUpperTriangular](/en/docs/matrix/matrix_classification/matrix_isuppertriangular), and so on).

MqlMatrixInfo Structure

```
struct MqlMatrixInfo
  {
    ushort            version,          // 5950
   char              signature[2],     // "GE", "SY", "HE", "TR", ...
   ENUM_BLAS_TYPE    matrix_class,     // BLASTYPE_GE, BLASTYPE_SY, BLASTYPE_HE etc must match signature
   ENUM_DATATYPE     data_type,        // TYPE_MATRIXD, TYPE_MATRIXF, TYPE_MATRIXCD, TYPE_MATRIXCF
    uint              flags,            // MATRIX_UPPER, MATRIX_LOWER, MATRIX_UNITDIAG, ...
    ulong             rows,             // rows of matrix
    ulong             cols,             // cols of matrix
    ulong             nnz,              // number of non-zeros
    long              lower_bandwidth,  // kl: number of potentially non-zero subdiagonals
    long              upper_bandwidth,  // ku: number of potentially non-zero superdiagonals
    ulong             data_size,        // size of following payload in bytes
  };

```

Information from the MqlMatrixInfo structure is used when [writing](/en/docs/matrix/matrix_write_read/matrix_write) a matrix to a file and when [reading](/en/docs/matrix/matrix_write_read/matrix_read) a matrix from a file. The data_size value is calculated depending on the recognized matrix class and contains the number of bytes required to store the matrix. For example, a general matrix (GE) occupies m * n * sizeof(type) bytes. A general band matrix (GB) occupies (kl+ku+1) * n * sizeof(type) bytes. A symmetric n x n matrix (SY) occupies n * (n+1)/2 * sizeof(type) bytes.

ENUM_BLAS_TYPE

An enumeration containing the type of the recognized matrix.

| ID | Description |
| --- | --- |
| BLASTYPE_GE | 'GE': general matrix |
| BLASTYPE_BD | 'BD': bidiagonal matrix |
| BLASTYPE_DI | 'DI': diagonal matrix |
| BLASTYPE_GB | 'GB': general band matrix |
| BLASTYPE_GT | 'GT': general tridiagonal matrix |
| BLASTYPE_HB | 'HB': Hermitian band matrix |
| BLASTYPE_HE | 'HE': Hermitian matrix |
| BLASTYPE_HT | 'HT': Hermitian tridiagonal matrix |
| BLASTYPE_HS | 'HS': Hessenberg matrix |
| BLASTYPE_SB | 'SB': symmetric band matrix |
| BLASTYPE_ST | 'ST': symmetric tridiagonal matrix |
| BLASTYPE_SY | 'SY': symmetric matrix |
| BLASTYPE_TB | 'TB': triangular band matrix |
| BLASTYPE_TR | 'TR': triangular matrix |
| BLASTYPE_TZ | 'TZ': trapezoidal matrix |
| BLASTYPE_VE | 'VE': vector - used when  writing  and  reading  a vector |
| BLASTYPE_CO | 'CO': sparse COO - used when  writing  and  reading  a matrix or vector if storing it as sparse is more efficient than storing it as 'GE' or 'VE' |

The BLASTYPE_VE and BLASTYPE_CO types are never returned by the MatrixInfo method. The names of the remaining enumeration items correspond to the abbreviations used in LAPACK to denote [various matrix classes](https://netlib.org/lapack/lug/node24.html). The HT type is an exception: Hermitian tridiagonal. HT is not present in standard LAPACK terminology and is introduced by analogy with ST (symmetric tridiagonal) to denote a Hermitian tridiagonal matrix, which also allows the corresponding matrix to be stored compactly.

MqlMatrixInfo::flags

Flags that refine the recognized matrix type.

| ID | Value | Description |
| --- | --- | --- |
| MATRIX_UPPER | 0x0001 | upper part above main diagonal |
| MATRIX_LOWER | 0x0002 | lower part below main diagonal |
| MATRIX_UNITDIAG | 0x0004 | main diagonal contains ones (1) only |
| MATRIX_DIAGSCALAR | 0x0008 | main diagonal contains the same values |
| MATRIX_QUASI_TRIANGULAR | 0x0010 | possible quasi-triangular matrix |
| MATRIX_TRIANGLE_RIGHT_ALIGNED | 0x0020 | upper triangular part aligned to right bound of wide matrix |
| MATRIX_TRIANGLE_BOTTOM_ALIGNED | 0x0040 | lower triangular part aligned to bottom bound of tall matrix |

The listed flags (except MATRIX_QUASI_TRIANGULAR) allow matrices to be stored more compactly.

Example

```
   ulong   n=10;
   matrix  matrix_a=matrix::Random(n,n);
   vectorc vector_ev;
   matrix  matrix_t,matrix_z;
   MqlMatrixInfo info;
   
   matrix_a.EigenSolverSchur(EIGSCHUR_V,vector_ev,matrix_t,matrix_z);
   matrix_t.MatrixInfo(info);
   PrintFormat("%d, %c%c, %s, %s, 0x%04x, rows=%I64u, cols=%I64u, nnz=%I64u, lower_bandwidth=%I64d, upper_bandwidth=%I64d, data_size=%I64u",
               info.version,info.signature[0],info.signature[1],EnumToString(info.matrix_class),EnumToString(info.data_type),
               info.flags,info.rows,info.cols,info.nnz,info.lower_bandwidth,info.upper_bandwidth,info.data_size);
   string flags="";
   if((info.flags&MATRIX_UPPER)==MATRIX_UPPER)
      flags+="  MATRIX_UPPER";
   if((info.flags&MATRIX_LOWER)==MATRIX_LOWER)
      flags+="  MATRIX_LOWER";
   if((info.flags&MATRIX_UNITDIAG)==MATRIX_UNITDIAG)
      flags+="  MATRIX_UNITDIAG";
   if((info.flags&MATRIX_DIAGSCALAR)==MATRIX_DIAGSCALAR)
      flags+="  MATRIX_DIAGSCALAR";
   if((info.flags&MATRIX_QUASI_TRIANGULAR)==MATRIX_QUASI_TRIANGULAR)
      flags+="  MATRIX_QUASI_TRIANGULAR";
   if((info.flags&MATRIX_TRIANGLE_RIGHT_ALIGNED)==MATRIX_TRIANGLE_RIGHT_ALIGNED)
      flags+="  MATRIX_TRIANGLE_RIGHT_ALIGNED";
   if((info.flags&MATRIX_TRIANGLE_BOTTOM_ALIGNED)==MATRIX_TRIANGLE_BOTTOM_ALIGNED)
      flags+="  MATRIX_TRIANGLE_BOTTOM_ALIGNED";
   Print("info.flags :",flags);
 
 
   /*
   5950, HS, BLASTYPE_HS, TYPE_MATRIX, 0x0011, rows=10, cols=10, nnz=57, lower_bandwidth=1, upper_bandwidth=-1, data_size=512
   info.flags :  MATRIX_UPPER  MATRIX_QUASI_TRIANGULAR
   */

```
