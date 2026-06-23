# Working with folders

It is difficult to imagine a file system without the ability to structure stored information through an arbitrary hierarchy of directories — containers for sets of logically related files. At the MQL5 level, this feature is also supported. If necessary, we can create, clean up and delete folders using the built-in functions FolderCreate, FolderClean, and FolderDelete.

Earlier, we have already seen one way to create a folder, and, perhaps, not even one, but the entire required hierarchy of subfolders at once. For this, when creating (opening) a file using [FileOpen](/en/book/common/files/files_open_close), or when copying it ([FileCopy](/en/book/common/files/files_copy_move), [FileMove](/en/book/common/files/files_copy_move)), you should specify not just a name, but precede it with the required path. For example,

```
   FileCopy("MQL5Book/unicode1.txt", 0, "ABC/DEF/code.txt", 0);

```

This statement will create the "ABC" folder in the sandbox, the "DEF" folder in it, and copy the file there under a new name (the source file must exist).

If you do not want to create a source file in advance, you can create a dummy file on the go:

```
   uchar dummy[];
   FileSave("ABC/DEF/empty", dummy);

```

Here we will get the same folder hierarchy as in the previous example but with a zero-size "empty" file.

With such approaches, the creation of folders becomes some sort of a by-product of working with files. However, sometimes it is required to operate with folders as independent entities and without side effects, in particular, just create an empty folder. This is offered by the FolderCreate function.

bool FolderCreate(const string folder, int flag = 0)

The function creates a folder named folder, which can include a path (several top-level folder names). In either case, a single folder or folder hierarchy is created in the sandbox defined by the flag parameter. By default when flag is 0, the local working folder MQL5/Files of terminal or tester agent (if the program is running in the tester) is used. If flag equals FILE_COMMON, the shared folder of all terminals is used.

The function returns true on success, or if the folder already exists. In case of an error, the result is false.

bool FolderClean(const string folder, int flag = 0)

The function deletes all files and folders of any nesting level (together with all content) in the specified folder directory. The flag parameter specifies the sandbox (local or global) in which the action takes place.

Use this feature with caution, as all files and subfolders (with their files) are permanently deleted.

bool FolderDelete(const string folder, int flag = 0)

The function deletes the specified folder (folder). Before calling the function, the folder must be empty, otherwise it cannot be deleted.

Techniques for working with these three functions are demonstrated in the script FileFolder.mq5. You can execute this script in the debug mode step by step (statement by statement) and watch in the file manager how folders and files appear and disappear. However, please note that before executing the next instruction, you should use the file manager to exit the created folders up to the "MQL5Book" level, because otherwise the folders may be occupied by the file manager, and this will disrupt the script.

We first create several subfolders as a by-product of writing an empty dummy file into them.

```
void OnStart()
{
   const string filename = "MQL5Book/ABC/DEF/dummy";
   uchar dummy[];
   PRTF(FileSave(filename, dummy)); // true

```

Next, we create another folder at the bottom nesting level with FolderCreate: This time the folder appears on its own, without the helper file.

```
   PRTF(FolderCreate("MQL5Book/ABC/GHI")); // true

```

If you try to delete the "DEF" folder, it will fail because it is not empty (there is a file there).

```
   PRTF(FolderDelete("MQL5Book/ABC/DEF")); // false / CANNOT_DELETE_DIRECTORY(5024)

```

In order to remove it, you must first clear it, and the easiest way to do this is with FolderClean. But we will try to simulate a common situation when some files in the folders being cleared can be locked by other MQL programs, external applications, or the terminal itself. Let's open the file for reading and call FolderClean.

```
   int handle = PRTF(FileOpen(filename, FILE_READ)); // 1
   PRTF(FolderClean("MQL5Book/ABC")); // false / CANNOT_CLEAN_DIRECTORY(5025)

```

The function returns false and exposes error code 5025 (CANNOT_CLEAN_DIRECTORY). After we close the file, cleaning and deleting the entire folder hierarchy succeeds.

```
   FileClose(handle);
   PRTF(FolderClean("MQL5Book/ABC")); // true
   PRTF(FolderDelete("MQL5Book/ABC")); // true
}

```

Potential locks are more likely when using a shared terminal directory, where the same file or folder can be "claimed" by different program instances. But even in a local sandbox, you should not forget about possible conflicts (for example, if a csv file is opened in Excel). Implement detailed diagnostics and error output for the code parts that work with folders, so that the user can notice and fix the problem.
