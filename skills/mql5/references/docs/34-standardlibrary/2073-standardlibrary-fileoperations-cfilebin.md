# CFileBin

CFileBin is a class for simplified access to binary files.

### Description

CFileBin class provides access to binary files.

### Declaration

```
   class CFileBin: public CFile

```

### Title

```
   #include <Files\FileBin.mqh>

```

```
Inheritance hierarchy
   CObject
       CFile
           CFileBin

```

### Class Methods by Groups

| Open methods |  |
| --- | --- |
| Open | Opens a binary file |
| Write methods |  |
| WriteChar | Writes char or uchar type variable |
| WriteShort | Writes short or ushort type variable |
| WriteInteger | Writes int or uint type variable |
| WriteLong | Writes long or ulong type variable |
| WriteFloat | Writes float type variable |
| WriteDouble | Writes double type variable |
| WriteString | Writes string type variable |
| WriteCharArray | Writes an array of char or uchar type variables |
| WriteShortArray | Writes an array of short or ushort type variables |
| WriteIntegerArray | Writes an array of int or uint type variables |
| WriteLongArray | Writes an array of long or ulong type variables |
| WriteFloatArray | Writes an array of float variables |
| WriteDoubleArray | Writes an array of double type variables |
| WriteObject | Writes data of the CObject class inheritor instance |
| Read methods |  |
| ReadChar | Reads char or uchar type variable |
| ReadShort | Reads short or ushort type variable |
| ReadInteger | Reads int or uint type variable |
| ReadLong | Reads long or ulong type variable |
| ReadFloat | Reads float type variable |
| ReadDouble | Reads double type variable |
| ReadString | Reads string type variable |
| ReadCharArray | Reads an array of char or uchar type variables |
| ReadShortArray | Reads an array of short or ushort type variables |
| ReadIntegerArray | Reads an array of int or uint type variables |
| ReadLongArray | Reads an array of long or ulong type variables |
| ReadFloatArray | Reads an array of float type variables |
| ReadDoubleArray | Reads an array of double type variables |
| ReadObject | Reads data of the CObject class inheritor instance |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CFile 
 Handle ,  FileName ,  Flags ,  SetUnicode ,  SetCommon ,  Open ,  Close ,  Delete ,  Size ,  Tell ,  Seek ,  Flush ,  IsEnding ,  IsLineEnding ,  Delete ,  IsExist ,  Copy ,  Move ,  FolderCreate ,  FolderDelete ,  FolderClean ,  FileFindFirst ,  FileFindNext ,  FileFindClose |
