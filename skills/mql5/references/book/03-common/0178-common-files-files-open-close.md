# Opening and closing files

To write and read data from a file, most MQL5 functions require that the file be opened first. For this purpose, there is the FileOpen function. After performing the required operations, the open file should be closed using the FileClose function. The fact is that an open file may, depending on the applied options, be blocked for access from other programs. In addition, file operations are buffered in memory (cache) for performance reasons, and without closing the file, new data may not be physically uploaded to it for some time. This is especially critical if the data being written is waiting for an external program (for example, when integrating an MQL program with other systems). We learn about an alternative way to flush the buffer to disk from the description of the [FileFlush](/en/book/common/files/files_flush) function.

A special integer referred to as the descriptor is associated with an open file in an MQL program. It is returned by the FileOpen function. All operations related to accessing or modifying the internal contents of a file require this identifier to be specified in the corresponding API functions. Those functions that operate on the entire file (copy, delete, move, check for existence) do not require a descriptor. You do not need to open the file to perform these steps.

int FileOpen(const string filename, int flags, const short delimiter = '\t', uint codepage = CP_ACP)

int FileOpen(const string filename, int flags, const string delimiter, uint codepage = CP_ACP)

The function opens a file with the specified name, in the mode specified by the flags parameter. The filename parameter may contain subfolders before the actual file name. In this case, if the file is opened for writing and the required folder hierarchy does not yet exist, it will be created.

The flags parameter must contain a combination of constants describing the required mode of working with the file. The combination is performed using the operations of [bitwise OR](/en/book/basis/expressions/operators_bitwise). Below is a table of available constants.

| Identifier | Value | Description |
| --- | --- | --- |
| FILE_READ | 1 | The file is opened for reading |
| FILE_WRITE | 2 | The file is opened for writing |
| FILE_BIN | 4 | Binary read-write mode, no data conversion from string to string |
| FILE_CSV | 8 | File of CSV type; the data being written is converted to text of the appropriate type (Unicode or ANSI, see below), and when reading, the reverse conversion is performed from the text to the required type (specified in the reading function); one CSV record is a single line of text, delimited by newline characters (usually CRLF); inside the CSV record, the elements are separated by a delimiter character (parameter  delimiter ); |
| FILE_TXT | 16 | Plain text file, similar to CSV mode, but a delimiter character is not used (the value of the parameter  delimiter  is ignored) |
| FILE_ANSI | 32 | ANSI type strings (single-byte characters) |
| FILE_UNICODE | 64 | Unicode type strings (double-byte characters) |
| FILE_SHARE_READ | 128 | Shared read access from several programs |
| FILE_SHARE_WRITE | 256 | Shared writing access by multiple programs |
| FILE_REWRITE | 512 | Permission to overwrite a file (if it already exists) in functions  FileCopy  and  FileMove |
| FILE_COMMON | 4096 | File location in the shared folder of all client terminals /Terminal/Common/Files (the flag is used when opening files (FileOpen), copying files (FileCopy, FileMove) and checking the existence of files ( FileIsExist )) |

When opening a file, one of the FILE_WRITE, FILE_READ flags or their combination must be specified.

The FILE_SHARE_READ and FILE_SHARE_WRITE flags do not replace or cancel the need to specify the FILE_READ and FILE_WRITE flags.

The MQL program execution environment always buffers files for reading, which is equivalent to implicitly adding the FILE_READ flag. Because of this, FILE_SHARE_READ should always be used to work properly with shared files (even if another process is known to have a write-only file open).

If none of the FILE_CSV, FILE_BIN, FILE_TXT flags is specified, FILE_CSV is assumed as the highest priority. If more than one of these three flags is specified, the highest priority passed is applied (they are listed above in descending order of priority).

For text files, the default mode is FILE_UNICODE.

The delimiter parameter affecting only CSV, could be of type ushort or string. In the second case, if the length of the string is greater than 1, only its first character will be used.

The codepage parameter only affects files opened in text mode (FILE_TXT or FILE_CSV), and only if FILE_ANSI mode is selected for strings. If the strings are stored in Unicode (FILE_UNICODE), the code page is not important.

If successful, the function returns a file descriptor, a positive integer. It is unique only within a particular MQL program; it makes no sense to share it with other programs. For further work with the file, the descriptor is passed to calls to other functions.

On error, the result is INVALID_HANDLE (-1). The essence of the error should be clarified from the code returned by the [GetLastError](/en/book/common/environment/env_last_error) function.

All operating mode settings made at the time the file is opened remain unchanged for as long as the file is open. If it becomes necessary to change the mode, the file should be closed and reopened with the new parameters.

For each open file, the MQL program execution environment maintains an internal pointer, i.e. the current position within the file. Immediately after opening the file, the pointer is set to the beginning (position 0). In the process of writing or reading, the position is shifted appropriately, according to the amount of data transmitted or received from various file functions. It is also possible to directly influence the position (move back or forward). All these opportunities will be discussed in the following sections.

FILE_READ and FILE_WRITE in various combinations allow you to achieve several scenarios:

- FILE_READ — open a file only if it exists; otherwise, the function returns an error and no new file is created.
- FILE_WRITE — creating a new file if it does not already exist, or opening an existing file, and its contents are cleared and the size is reset to zero.
- FILE_READ|FILE_WRITE — open an existing file with all its contents or create a new file if it does not already exist.

As you can see, some scenarios are inaccessible only due to flags. In particular, you cannot open a file for writing only if it already exists. This can be achieved using additional functions, for example, [FileIsExist](/en/book/common/files/files_exist_delete). Also, it will not be possible to "automatically" reset a file opened for a combination of reading and writing: in this case, MQL5 always leaves the contents.

To append data to a file, one must not only open the file in FILE_READ|FILE_WRITE mode, but also move the current position within the file to its end by calling [FileSeek](/en/book/common/files/files_cursor).

The correct description of the shared access to the file is a prerequisite for successful execution of File Open. This aspect is managed as follows.

- If neither of the FILE_SHARE_READ and FILE_SHARE_WRITE flags is specified, then the current program gets exclusive access to the file if it opens it first. If the same file has already been opened by someone before (by another program,or by the same program), the function call will fail.
- When the FILE_SHARE_READ flag is set, the program allows subsequent requests to open the same file for reading. If at the time of the function call the file is already open for reading by another or the same program, and this flag is not set, the function will fail.
- When the FILE_SHARE_WRITE flag is set, the program allows subsequent requests to open the same file for writing. If at the time of the function call the file is already open for writing by another or the same program, and this flag is not set, the function will fail.

Access sharing is checked not only in relation to other MQL programs or processes external to MetaTrader 5, but also in relation to the same MQL program if it reopens the file.

Thus, the least conflicting mode implies that both flags are specified, but it still does not guarantee that the file will be opened if someone has already been issued a descriptor to it with no sharing. However, more stringent rules should be followed depending on the planned reads or writes.

For example, when opening a file for reading, it makes sense to leave the opportunity for others to read it. Additionally, you can probably allow others to write to it, if it is a file that is being replenished (for example, a journal). However, when opening a file for writing, it is hardly worth leaving write access to others: this would lead to unpredictable data overlay.

void FileClose(int handle)

The function closes a previously opened file by its handle.

After the file is closed, its handle in the program becomes invalid: an attempt to call any file function on it will result in an error. However, you can use the same variable to store a different handle if you reopen the same or a different file.

When the program terminates, open files are forcibly closed, and the write buffer, if it is not empty, is written to disk. However, it is recommended to close files explicitly.

Closing a file when you're finished working with it is an important rule to follow. This is due not only to the caching of the information being written, which may remain in RAM for some time and not saved to disk (as already mentioned above), if the file is not closed. In addition, an open file consumes some internal resource of the operating system, and we are not talking about disk space. The number of simultaneously open files is limited (maybe several hundred or thousands depending on Windows settings). If many programs keep a large number of files open, this limit may be reached and attempts to open new files will fail.

In this regard, it is desirable to protect yourself from the possible loss of descriptors using a wrapper class that would open a file and receive a descriptor when creating an object, and the descriptor would be released and the file closed automatically in the destructor.

We will create a wrapper class after testing the pure FileOpen and FileClose functions.

But before diving into file specifics, let's prepare a new version of the macro to illustrate an output of our functions to the call log. The new version was required because, until now, macros like PRT and PRTS (used in previous sections) "absorbed" function return values during printing. For example, we wrote:

```
PRT(FileLoad(filename, read));

```

Here the result of the FileLoad call is sent to the log, but it is not possible to get it in the calling string of code. To tell the truth, we did not need it. But now the FileOpen function will return a file descriptor, and should be stored in a variable for further manipulation of the file.

There are two problems with the old macros. First, they are based on the function Print, which consumes the passed data (sending it to the log) but does not itself return anything. Second, any value for a variable with a result can only be obtained from an expression, and a Print call cannot be made a part of an expression due to the fact that it has the type void.

To solve these problems, we need a print helper function that returns a printable value. And we will pack its call into a new PRTF macro:

```
#include <MQL5Book/MqlError.mqh>
  
#define PRTF(A) ResultPrint(#A, (A))
  
template<typename T>
T ResultPrint(const string s, const T retval = 0)
{
   const string err = E2S(_LastError) + "(" + (string)_LastError + ")";
   Print(s, "=", retval, " / ", (_LastError == 0 ? "ok" : err));
 ResetLastError();// clear the error flag for the next call
   return retval;
}

```

Using the '#' magic string conversion operator, we get a detailed descriptor of the code fragment (expression A) that is passed as the first argument to ResultPrint. The expression itself (the macro argument) is evaluated (if there is a function, it is called), and its result is passed as the second argument to ResultPrint. Next, the usual Print function comes into play, and finally, the same result is returned to the calling code.

In order not to look into the Help for decoding error codes, an E2S macro was prepared that uses the MQL_ERROR enumeration with all MQL5 errors. It can be found in the header file MQL5/Include/MQL5Book/MqlError.mqh. The new macro and the ResultPrint function are defined in the PRTF.mqh file, next to the test scripts.

In the FileOpenClose.mq5 script, let's try to open different files, and, in particular, the same file will open several times in parallel. This is usually avoided in real programs. A single handle to a particular file in a program instance is sufficient for most tasks.

One of the files, MQL5Book/rawdata, must already exist since it was created by a script from the section [Writing and reading files in simplified mode](/en/book/common/files/files_save_load). Another file will be created during the test.

We will choose the file type FILE_BIN. working with FILE_TXT or FILE_CSV would be similar at this stage.

Let's reserve an array for file descriptors so that at the end of the script we close all files at once.

First, let's open MQL5Book/rawdata in reading mode without access sharing. Assuming that the file is not in use by any third party application, we can expect the handle to be successfully received.

```
void OnStart()
{
   int ha[4] = {}; // array for test file handles 
   
   // this file must exist after running FileSaveLoad.mq5
   const string rawdata = "MQL5Book/rawdata";
   ha[0] = PRTF(FileOpen(rawdata, FILE_BIN | FILE_READ)); // 1 / ok

```

If we try to open the same file again, we will encounter an error because neither the first nor the second call allows sharing.

```
 ha[1] = PRTF(FileOpen(rawdata, FILE_BIN | FILE_READ)); // -1 / CANNOT_OPEN_FILE(5004)

```

Let's close the first handle, open the file again, but with shared read permissions, and make sure that reopening now works (although it also needs to allow shared reading):

```
   FileClose(ha[0]);
   ha[0] = PRTF(FileOpen(rawdata, FILE_BIN | FILE_READ | FILE_SHARE_READ)); // 1 / ok
   ha[1] = PRTF(FileOpen(rawdata, FILE_BIN | FILE_READ | FILE_SHARE_READ)); // 2 / ok

```

Opening a file for writing (FILE_WRITE) will not work, because the two previous calls of FileOpen only allow FILE_SHARE_READ.

```
   ha[2] = PRTF(FileOpen(rawdata, FILE_BIN | FILE_READ | FILE_WRITE | FILE_SHARE_READ));
   // -1 / CANNOT_OPEN_FILE(5004)

```

Now let's try to create a new file MQL5Book/newdata. If you open it as read-only, the file will not be created.

```
   const string newdata = "MQL5Book/newdata";
   ha[3] = PRTF(FileOpen(newdata, FILE_BIN | FILE_READ));
   // -1 / CANNOT_OPEN_FILE(5004)

```

To create a file, you must specify the FILE_WRITE mode (the presence of FILE_READ is not critical here, but it makes the call more universal: as we remember, in this combination, the instruction guarantees that either the old file will be opened, if it exists, or a new one will be created).

```
   ha[3] = PRTF(FileOpen(newdata, FILE_BIN | FILE_READ | FILE_WRITE)); // 3 / ok

```

Let's try to write something to a new file using the function [FileSave](/en/book/common/files/files_save_load) known to us. It acts as an "external player", since it works with the file bypassing our descriptor, in much the same way as it could be done by another MQL program or a third-party application.

```
   long x[1] = {0x123456789ABCDEF0};
   PRTF(FileSave(newdata, x)); // false

```

This call fails because the handle was opened without sharing permissions. Close and reopen the file with maximum "permissions".

```
   FileClose(ha[3]);
   ha[3] = PRTF(FileOpen(newdata, 
      FILE_BIN | FILE_READ | FILE_WRITE | FILE_SHARE_READ | FILE_SHARE_WRITE)); // 3 / ok

```

This time FileSave works as expected.

```
   PRTF(FileSave(newdata, x)); // true

```

You can look in the folder MQL5/Files/MQL5Book/ and find there the newdata file, 8 bytes long.

Note that after we close the file, its descriptor is returned to the free descriptor pool, and the next time a file (maybe another file) is opened, the same number comes into play again.

For a neat shutdown, we will explicitly close all open files.

```
   for(int i = 0; i < ArraySize(ha); ++i)
   {
      if(ha[i] != INVALID_HANDLE)
      {
        FileClose(ha[i]);
      }
   }
}

```
