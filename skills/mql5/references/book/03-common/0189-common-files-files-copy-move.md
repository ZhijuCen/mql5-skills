# Copying and moving files

The main operations on files at the file system level are copying and moving. For these purposes, MQL5 implements two functions with identical prototypes.

bool FileCopy(const string source, int flag, const string destination, int mode)

The function copies the source file to the destination file. Both mentioned parameters can contain only file names, or names together with prefixing paths (folder hierarchies) in MQL5 sandboxes. The flag and mode parameters determine, in which working folder the source file is searched and which working folder is the target: 0 means it is a folder of the local current instance of the terminal (or the tester agent, if the program is running in the tester), and the value FILE_COMMON means the common folder for all terminals.

In addition, in the mode parameter, you can optionally specify the FILE_REWRITE constant (if you need to combine FILE_REWRITE and FILE_COMMON, this is done using the bitwise operator OR (|)). In the absence of FILE_REWRITE, copying over an existing file is prohibited. In other words, if the file with the path and name specified in the destination parameter already exists, you must confirm your intention to overwrite it by setting FILE_REWRITE. If this is not done, the function call will fail.

The function returns true upon successful completion or false in case of an error.

Copying may fail if the source or destination file is occupied (opened) by another process.

When copying files, their metadata (creation time, access rights, alternative data streams) is usually saved. If you need to perform "pure" copying of only the data of the file itself, you can use successive calls FileLoad and FileSave, see [Writing and reading files in simplified mode](/en/book/common/files/files_save_load).

bool FileMove(const string source, int flag, const string destination, int mode)

The function moves or renames a file. The source path and name are specified in the source parameter and the target path and name are specified in destination.

The list of parameters and their operating principles are the same as for the FileCopy function. Roughly speaking, FileMove does the same work as FileCopy, but it additionally deletes the original file after a successful copy.

Let's learn how to work with functions in practice using the script FileCopy.mq5. It has two variables with the file names. Both files do not exist when the script is run.

```
const string source = "MQL5Book/source";
const string destination = "MQL5Book/destination";

```

In OnStart, we perform a sequence of actions according to a simple scenario. First, we try to copy the source file from the local working directory to the destination file of the general directory. As expected, we get false, and the error code in _LastError will be 5019 (FILE_NOT_EXIST).

```
void OnStart()
{
   PRTF(FileCopy(source, 0, destination, FILE_COMMON)); // false / FILE_NOT_EXIST(5019)
   ...

```

Therefore, we will create a source file in the usual way, write some data and flush it onto the disk.

```
   int handle = PRTF(FileOpen(source, FILE_TXT | FILE_WRITE)); // 1
   PRTF(FileWriteString(handle, "Test Text\n")); // 22
   FileFlush(handle);

```

Since the file was left open and the FILE_SHARE_READ permission was not specified when opening, access to it in other ways (bypassing the handle) is still blocked. Hence, the next copy attempt will fail again.

```
   PRTF(FileCopy(source, 0, destination, FILE_COMMON)); // false / CANNOT_OPEN_FILE(5004)

```

Let's close the file and try again. But first, let's output the properties of the resulting file to the log: when it was created and modified. Both properties will contain the current timestamp of your computer.

```
   FileClose(handle);
   PRTF(FileGetInteger(source, FILE_CREATE_DATE)); // 1629757115, example
   PRTF(FileGetInteger(source, FILE_MODIFY_DATE)); // 1629757115, example

```

Let's wait for 3 seconds before calling FileCopy. This will allow you to see the difference in the properties of the original file and its copy. This pause has nothing to do with the previous lock on the file: we could copy immediately after we closed the file, or even while writing it if the FILE_SHARE_READ option was enabled.

```
   Sleep(3000);

```

Let's copy the file. This time the operation succeeds. Let's see the copy properties.

```
   PRTF(FileCopy(source, 0, destination, FILE_COMMON)); // true
   PRTF(FileGetInteger(destination, FILE_CREATE_DATE, true)); // 1629757118, +3 seconds
   PRTF(FileGetInteger(destination, FILE_MODIFY_DATE, true)); // 1629757115, example

```

Each file has its own creation time (for a copy it is 3 seconds later than for the original), but the modification time is the same (the copy has inherited the properties of the original).

Now let's try to move the copy back to the local folder. It cannot be done without the FILE_REWRITE option because there is no permission to overwrite the original file.

```
   PRTF(FileMove(destination, FILE_COMMON, source, 0)); // false / FILE_CANNOT_REWRITE(5020)

```

By changing the value of the parameter, we will achieve a successful file transfer.

```
   PRTF(FileMove(destination, FILE_COMMON, source, FILE_REWRITE)); // true

```

Finally, the original file is also deleted to leave a clean environment for new experiments with this script.

```
   ...
   FileDelete(source);
}

```
