# Getting file properties

In the process of working with files, in addition to directly writing and reading data, it often becomes necessary to analyze their properties. One of the main properties, the file size, can be obtained using the FileSize function. But there are a few more characteristics which can be requested using FileGetInteger.

Please note that the FileSize function requires an open file handle. FileGetInteger has some properties, including the size, that can be recognized by the file name, and you do not need to open it first.

ulong FileSize(int handle)

The function returns the size of an open file by its descriptor. In case of an error, the result is equal to 0, which is a valid size for the normal execution of the function, so you should always analyze potential errors using _LastError (or [GetLastError](/en/book/common/environment/env_last_error)).

The file size can also be obtained by moving the pointer to the end of the file FileSeek(handle, 0, SEEK_END) and calling FileTell(handle). These two functions are described in the previous section.

long FileGetInteger(int handle, ENUM_FILE_PROPERTY_INTEGER property)

long FileGetInteger(const string filename, ENUM_FILE_PROPERTY_INTEGER property, bool common = false)

The function has two options: to work through an open file descriptor, and by the file name (including a closed one).

The function returns one of the file properties specified in the property parameter. The list of valid properties is different for each of the options (see below). Even though the value type is long, depending on the requested property, it can contain not only an integer number but also datetime or bool: perform the required typecast explicitly.

When requesting a property by the file name, you can additionally use the common parameter to specify in which folder the file should be searched: the current terminal folder MQL5/Files (false, default) or the common folder Users/<user_name>...MetaQuotes/Terminal/Common/Files (true). If the MQL program is running in the tester, the working directory is located inside the test agent folder (Tester/<agent>/MQL5/Files), see the introduction of the chapter [Working with files](/en/book/common/files).

The following table lists all the members of ENUM_FILE_PROPERTY_INTEGER.

| Property | Description |
| --- | --- |
| FILE_EXISTS  * | Check for existence (similar to FileIsExist) |
| FILE_CREATE_DATE  * | Creation date |
| FILE_MODIFY_DATE  * | Last modified date |
| FILE_ACCESS_DATE  * | Last access date |
| FILE_SIZE  * | File size in bytes (similar to FileSize) |
| FILE_POSITION | Pointer position in the file (similar to FileTell) |
| FILE_END | Position at the end of the file (similar to FileIsEnding) |
| FILE_LINE_END | Position at the end of a string (similar to FileIsLineEnding) |
| FILE_IS_COMMON | File opened in terminals shared folder (FILE_COMMON) |
| FILE_IS_TEXT | File opened as text (FILE_TXT) |
| FILE_IS_BINARY | File opened as binary (FILE_BIN) |
| FILE_IS_CSV | File opened as CSV (FILE_CSV) |
| FILE_IS_ANSI | File opened as ANSI (FILE_ANSI) |
| FILE_IS_READABLE | File opened for reading (FILE_READ) |
| FILE_IS_WRITABLE | File opened for writing (FILE_WRITE) |

Properties allowed for use by filename are marked with an asterisk. If you try to get other properties, the second version of the function will return an error 4003 (INVALID_PARAMETER).

Some properties can change while working with an open file: FILE_MODIFY_DATE, FILE_ACCESS_DATE, FILE_SIZE, FILE_POSITION, FILE_END, FILE_LINE_END (for text files only).

In case of an error, the result of the call is -1.

The second version of the function allows you to check if the specified name is the name of a file or directory. If a directory is specified when getting properties by name, the function will set a special internal error code 5018 (ERR_MQL_FILE_IS_DIRECTORY), while the returned value will be correct.

We will test the functions of this section using the script FileProperties.mq5. It will work on a file with a predefined name.

```
const string fileprop = "MQL5Book/fileprop";

```

At the beginning of OnStart, let's try to request the size by a wrong descriptor (it was not received through the File Open call). After FileSize, the _LastError variable check is required, and FileGetInteger immediately returns a special value, an error indicator (-1).

```
void OnStart()
{
   int handle = 0;
   ulong size = FileSize(handle);
   if(_LastError)
   {
      Print("FileSize error=", E2S(_LastError) + "(" + (string)_LastError + ")");
      // We will get: FileSize 0, error=WRONG_FILEHANDLE(5008)
   }
   
   PRTF(FileGetInteger(handle, FILE_SIZE)); // -1 / WRONG_FILEHANDLE(5008)

```

Next, we create a new file or open an existing file and reset it, and then write the test text.

```
   handle = PRTF(FileOpen(fileprop, FILE_TXT | FILE_WRITE | FILE_ANSI)); // 1
   PRTF(FileWriteString(handle, "Test Text\n")); // 11

```

We selectively request some of the properties.

```
   PRTF(FileGetInteger(fileprop, FILE_SIZE)); // 0, not written to the disk yet
   PRTF(FileGetInteger(handle, FILE_SIZE)); // 11
   PRTF(FileSize(handle)); // 11
   PRTF(FileGetInteger(handle, FILE_MODIFY_DATE)); //1629730884, number of seconds since 1970
   PRTF(FileGetInteger(handle, FILE_IS_TEXT)); // 1, bool true
   PRTF(FileGetInteger(handle, FILE_IS_BINARY)); // 0, bool false

```

Information about the length of the file by its descriptor takes into account the current caching buffer, and by the file name, the actual length will become available only after the file is closed, or if you call the FileFlush function (see section [Force write cache to disk](/en/book/common/files/files_flush)).

The function returns dates and times as the number of seconds of the standard epoch since January 1, 1970, which corresponds to the datetime type and can be brought to it.

The request for file open flags (its mode) is successful for the function version with a descriptor, in particular, we received a response that the file is text and not binary. However, the next similar request for a filename will fail because the property is only supported when a valid handle is passed. This happens even though the name points to the same file that we have opened.

```
   PRTF(FileGetInteger(fileprop, FILE_IS_TEXT)); // -1 / INVALID_PARAMETER(4003)

```

Let's wait for one second, close the file, and check the modification date again (this time by name, since the descriptor is no longer valid).

```
   Sleep(1000);
   FileClose(handle);
   PRTF(FileGetInteger(fileprop, FILE_MODIFY_DATE)); // 1629730885 / ok

```

Here you can clearly see that the time has increased by 1.

Finally, make sure that properties are available for directories (folders).

```
   PRTF((datetime)FileGetInteger("MQL5Book", FILE_CREATE_DATE));
   // We will get: 2021.08.09 22:38:00 / FILE_IS_DIRECTORY(5018)

```

Since all examples of the book are located in the "MQL5Book" folder, it must already exist. However, your actual creation time will be different. The FILE_IS_DIRECTORY error code in this case is displayed for us by the PRTF macro. In the working program, the function call should be made without a macro, and then the code should be read in _LastError.
