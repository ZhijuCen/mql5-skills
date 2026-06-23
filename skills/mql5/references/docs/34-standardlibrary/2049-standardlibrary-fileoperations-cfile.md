# CFile

CFile is a base class for CFileBin and CFileTxt classes.

### Description

CFile class provides the simplified access to MQL5 API file and folder functions for all of its descendants.

### Declaration

```
   class CFile: public CObject

```

### Title

```
   #include <Files\File.mqh>

```

```
Inheritance hierarchy
   CObject
       CFile
Direct descendants
CFileBin, CFilePipe, CFileTxt

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Handle | Gets file handle |
| Filename | Gets file name |
| Flags | Gets file flags |
| SetUnicode | Sets/clears the FILE_UNICODE flag |
| SetCommon | Sets/clears the FILE_COMMON flag |
| General methods for files |  |
| Open | Opens file |
| Close | Closes file |
| Delete | Deletes file |
| IsExist | Checks file for existence |
| Copy | Copies file |
| Move | Renames/moves file |
| Size | Gets file size |
| Tell | Gets current file position |
| Seek | Sets current file position |
| Flush | Flushes data on disk |
| IsEnding | Checks file for end |
| IsLineEnding | Checks line for end |
| General methods for folders |  |
| FolderCreate | Creates folder |
| FolderDelete | Deletes folder |
| FolderClean | Clears folder |
| Files and folders search methods |  |
| FileFindFirst | Begins file search |
| FileFindNext | Continues file search |
| FileFindClose | Closes search handle |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
