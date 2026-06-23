# FolderCreate

Creates new folder.

```
bool  FolderCreate(
   const string  folder_name      // folder name
   )

```

Parameters

folder_name

[in]  Name of the folder to create. It contains path to the folder relative to the folder defined by FILE_COMMON flag.

Return Value

true - successful, false - cannot create the folder.

Note

The working folder is dependent on the flag that was previously set/reset using the SetCommon() method.
