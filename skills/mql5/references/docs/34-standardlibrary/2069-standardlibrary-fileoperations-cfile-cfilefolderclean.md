# FolderClean

Cleans specified folder.

```
bool  FolderClean(
   const string  folder_name      // folder name
   )

```

Parameters

folder_name

[in]  Name of the folder to clean. It contains path to the folder relative to the folder defined by FILE_COMMON flag.

Return Value

true - successful, and false - cannot change the folder.

Note

The working folder is dependent on the flag previously set/reset by SetCommon() method.
