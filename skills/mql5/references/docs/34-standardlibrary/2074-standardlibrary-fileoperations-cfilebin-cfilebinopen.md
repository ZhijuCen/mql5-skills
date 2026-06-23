# Open

Opens the specified binary file and, if successful, assigns it to the class instance.

```
int  Open(
   const string  file_name,     // file name
   int           flags          // flags
   )

```

Parameters

file_name

[in]  File name of the file to open.

flags

[in]  File open flags (the FILE_BIN flag is set forcibly).

Return Value

Handle of the opened file.
