# Open

Opens the specified text file and, if successful, assigns it to the class instance.

```
int  Open(
   const string  file_name,     // file name
   int           flags          // flags
   )

```

Parameters

file_name

[in]  File name to open.

flags

[in]  File open flags (FILE_TXT flag is forcibly set).

Return Value

Opened file handle.
