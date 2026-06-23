# Deleting a file and checking if it exists

Checking if a file exists and deleting it are critical actions related to the file system, i.e., to the external environment in which files "live". So far, we've looked at functions that manipulate the internal contents of files. Starting with this section, the focus will shift towards functions that manage files as indivisible units.

bool FileIsExist(const string filename, int flag = 0)

The function checks if a file with the name filename exists and returns true if it does. The search directory is selected using the flag parameter: if it is 0 (the default value), the file is searched in the directory of the current terminal instance (MQL5/Files); if flag equals FILE_COMMON, the common directory of all terminals Users/<user>...MetaQuotes/Terminal/Common/Files is checked. If the MQL program is running in the tester, the working directory is located inside the tester agent folder (Tester/<agent>/MQL5/Files), see an introductory part of the chapter [Working with files](/en/book/common/files).

The specified name may belong not to a file but to a directory. In this case, the FileIsExist function will return false and a pseudo-error 5018 (FILE_IS_DIRECTORY) will be logged into the _LastError variable.

bool FileDelete(const string filename, int flag = 0)

The function deletes the file with the specified name filename. The flag parameter specifies the location of the file. With the default value, deletion is performed in the working directory of the current terminal instance (MQL5/Files) or tester agent (Tester/<agent>/MQL5/Files) if the program is running in the tester. If flag equals FILE_COMMON, the file must be located in the common folder of all terminals (/Terminal/Common/Files).

The function returns a sign of success (true) or error (false).

This function does not allow deleting directories. For this purpose, use the FolderDelete function (see [Working with folders](/en/book/common/files/files_folders)).

To see how the described functions work, we will use the script FileExist.mq5. We will do several manipulations with a temporary file.

```
const string filetemp = "MQL5Book/temp";
void OnStart()
{
   PRTF(FileIsExist(filetemp)); // false / FILE_NOT_EXIST(5019)
   PRTF(FileDelete(filetemp));  // false / FILE_NOT_EXIST(5019)
   
   int handle = PRTF(FileOpen(filetemp, FILE_TXT | FILE_WRITE | FILE_ANSI)); // 1
   
   PRTF(FileIsExist(filetemp)); // true
   PRTF(FileDelete(filetemp));  // false / CANNOT_DELETE_FILE(5006)
   
   FileClose(handle);
   
   PRTF(FileIsExist(filetemp)); // true
   PRTF(FileDelete(filetemp));  // true
   PRTF(FileIsExist(filetemp)); // false / FILE_NOT_EXIST(5019)
   
   PRTF(FileIsExist("MQL5Book")); // false / FILE_IS_DIRECTORY(5018)
   PRTF(FileDelete("MQL5Book"));  // false / FILE_IS_DIRECTORY(5018)
}

```

The file does not initially exist, so both functions FileIsExist and FileDelet return false, and the error code is 5019 (FILE_NOT_EXIST).

We then create a file, and the FileIsExist function reports its presence. However, it cannot be deleted because it is open and busy with our process (error code 5006, CANNOT_DELETE_FILE).

Once the file is closed, it can be deleted.

At the end of the script, the "MQL5Book" directory is checked and an attempt is made to delete it. FileIsExist returns false because it's not a file, however the error code 5018 (FILE_IS_DIRECTORY) specifies that it's a directory.
