# Managing position in a file

As we already know, the system associates a certain pointer with each open file: it determines the place in the file (offset from its beginning) where data will be written or read from the next time any I/O function is called. After the function is executed, the pointer is shifted by the size of the written or read data.

In some cases, you want to change the position of the pointer without I/O operations. In particular, when we need to append data to the end of a file, we open it in "mixed" mode FILE_READ | FILE_WRITE, and then we must somehow end up at the end of the file (otherwise we will start overwriting the data from the beginning). We could call the read functions while there is something to read (thus shifting the pointer), but this is not efficient. It is better to use the special function FileSeek. And the FileTell function allows getting the actual value of the pointer (position in the file).

In this section, we'll explore these and a couple of other functions related to the current position in a file. Some of them work the same way for files in text and binary mode, while others are different.

bool FileSeek(int handle, long offset, ENUM_FILE_POSITION origin)

The function moves the file pointer by the offset number of bytes using origin as a reference which is one of the predefined positions described in the ENUM_FILE_POSITION enumeration. The offset can be either positive (moving to the end of the file and beyond) or negative (moving to the beginning). ENUM_FILE_POSITION has the following members:

- SEEK_SET for the file beginning
- SEEK_CUR for the current position
- SEEK_END for the file end

If the calculation of the new position relative to the anchor point gave a negative value (i.e., an offset to the left of the beginning of the file is requested), then the file pointer will be set to the beginning of the file.

If you set the position beyond the end of the file (the value is greater than the file size), then the subsequent writing to the file will be made not from the end of the file, but from the set position. In this case, undefined values will be written between the previous end of the file and the given position (see below).

The function returns true on success and false in case of an error.

ulong FileTell(int handle)

For a file opened with the handle descriptor, the function returns the current position of the internal pointer (an offset relative to the beginning of the file). In case of an error, ULONG_MAX ((ulong)-1) will be returned. The error code is available in the _LastError variable, or through the [GetLastError](/en/book/common/environment/env_last_error) function.

bool FileIsEnding(int handle)

The function returns an indication of whether the pointer is at the end of the handle file. If so, the result is true.

bool FileIsLineEnding(int handle)

For a text file with the handle descriptor, the function returns a sign of whether the file pointer is at the end of the line (immediately after the newline characters '\n' or '\r\n'). In other words, the return value true means that the current position is at the beginning of the next line (or at the end of the file). For binary files, the result is always false.

The test script for the aforementioned functions is called FileCursor.mq5. It works with three files: two binary and one text.

```
const string fileraw = "MQL5Book/cursor.raw";
const string filetxt = "MQL5Book/cursor.csv";
const string file100 = "MQL5Book/k100.raw";

```

To simplify logging of the current position, along with the end-of-file (End-Of-File, EOF) and end-of-line (End-Of-Line, EOL) signs, we have created a helper function FileState.

```
string FileState(int handle)
{
   return StringFormat("P:%I64d, F:%s, L:%s", 
      FileTell(handle),
      (string)FileIsEnding(handle),
      (string)FileIsLineEnding(handle));
}

```

The scenario for testing the functions on a binary file includes the following steps.

Create a new or open an existing fileraw file ("MQL5Book/cursor.raw") in read/write mode. Immediately after opening, and then after each operation, we output the current state of the file by calling FileState.

```
void OnStart()
{
   int handle;
   Print("\n * Phase I. Binary file");
   handle = PRTF(FileOpen(fileraw, FILE_BIN | FILE_WRITE | FILE_READ));
   Print(FileState(handle));
   ...

```

Move the pointer to the end of the file, which will allow us to append data to this file every time the script is executed (and not overwrite it from the beginning). The most obvious way to refer to the file end: null offset relative to origin=SEEK_END.

```
   PRTF(FileSeek(handle, 0, SEEK_END));
   Print(FileState(handle));

```

If the file is no longer empty (not new), we can read existing data at its arbitrary position (relative or absolute). In particular, if the origin parameter of the FileSeek function is equal to SEEK_CUR, that means that with a negative offset the current position will move the corresponding number of bytes back (to the left), and with positive it will move forward (to the right).

In this example, we are trying to step back by the size of one value of type int. A little later we will see that in this place there should be a field day_of_year (last field) of the structure [MqlDateTime](/en/book/common/conversions/conversions_datetime), because we write it to a file in subsequent instructions, and this data is available from the file on the next run. The read value is logged for comparison with what was previously saved.

```
   if(PRTF(FileSeek(handle, -1 * sizeof(int), SEEK_CUR)))
   {
      Print(FileState(handle));
      PRTF(FileReadInteger(handle));
   }

```

In a new empty file, the FileSeek call will end with error 4003 (INVALID_PARAMETER), and the if statement block will not be executed.

Next, the file is filled with data. First, the current local time of the computer (8 bytes of datetime) is written with FileWriteLong.

```
   datetime now = TimeLocal();
   PRTF(FileWriteLong(handle, now));
   Print(FileState(handle));

```

Then we try to step back from the current location by 4 bytes (-4) and read long.

```
   PRTF(FileSeek(handle, -4, SEEK_CUR));
   long x = PRTF(FileReadLong(handle));
   Print(FileState(handle));

```

This attempt will end with error 5015 (FILE_READERROR), because we were at the end of the file and after shifting 4 bytes to the left, we cannot read 8 bytes from the right (size long). However, as we will see from the log, as a result of this unsuccessful attempt, the pointer will still move back to the end of the file.

If you step back by 8 bytes (-8), the subsequent reading of the long value will be successful, and both time values, including the original and one received from the file, must match.

```
   PRTF(FileSeek(handle, -8, SEEK_CUR));
   Print(FileState(handle));
   x = PRTF(FileReadLong(handle));
   PRTF((now == x));

```

Finally, write the MqlDateTime structure filled with the same time to the file. The position in the file will increase by 32 (the size of the structure in bytes).

```
   MqlDateTime mdt;
   TimeToStruct(now, mdt);
   StructPrint(mdt); // display the date/time in the log visually
   PRTF(FileWriteStruct(handle, mdt)); // 32 = sizeof(MqlDateTime)
   Print(FileState(handle));
   FileClose(handle);

```

After the first run of the script for the scenario with the file fileraw (MQL5Book/cursor.raw) we get something like the following (the time will be different):

```
first run 
 * Phase I. Binary file
FileOpen(fileraw,FILE_BIN|FILE_WRITE|FILE_READ)=1 / ok
P:0, F:true, L:false
FileSeek(handle,0,SEEK_END)=true / ok
P:0, F:true, L:false
FileSeek(handle,-1*sizeof(int),SEEK_CUR)=false / INVALID_PARAMETER(4003)
FileWriteLong(handle,now)=8 / ok
P:8, F:true, L:false
FileSeek(handle,-4,SEEK_CUR)=true / ok
FileReadLong(handle)=0 / FILE_READERROR(5015)
P:8, F:true, L:false
FileSeek(handle,-8,SEEK_CUR)=true / ok
P:0, F:false, L:false
FileReadLong(handle)=1629683392 / ok
(now==x)=true / ok
  2021     8    23      1    49    52             1           234
FileWriteStruct(handle,mdt)=32 / ok
P:40, F:true, L:false

```

According to the status, the file size is initially zero because the position is "P:0" after the shift to the end of the file ("F:true"). After each recording (using FileWriteLong and FileWriteStruct) the position P is increased by the size of the written data.

After the second run of the script, you can notice some changes in the log:

```
second run
 * Phase I. Binary file
FileOpen(fileraw,FILE_BIN|FILE_WRITE|FILE_READ)=1 / ok
P:0, F:false, L:false
FileSeek(handle,0,SEEK_END)=true / ok
P:40, F:true, L:false
FileSeek(handle,-1*sizeof(int),SEEK_CUR)=true / ok
P:36, F:false, L:false
FileReadInteger(handle)=234 / ok
FileWriteLong(handle,now)=8 / ok
P:48, F:true, L:false
FileSeek(handle,-4,SEEK_CUR)=true / ok
FileReadLong(handle)=0 / FILE_READERROR(5015)
P:48, F:true, L:false
FileSeek(handle,-8,SEEK_CUR)=true / ok
P:40, F:false, L:false
FileReadLong(handle)=1629683397 / ok
(now==x)=true / ok
  2021     8    23      1    49    57             1           234
FileWriteStruct(handle,mdt)=32 / ok
P:80, F:true, L:false

```

First, the size of the file after opening is 40 (according to the position "P:40" after the shift to the end of the file). Each time the script is run, the file will grow by 40 bytes.

Second, since the file is not empty, it is possible to navigate through it and read the "old" data. In particular, after retreating to -1*sizeof(int) from the current position (which is also the end of the file), we successfully read the value 234 which is the last field of the structure MqlDateTime (it is the number of the day in a year and it will most likely be different for you).

The second test scenario works with the text csv file filetxt (MQL5Book/cursor.csv). We will also open it in the combined read and write mode, but will not move the pointer to the end of the file. Because of this, every run of the script will overwrite the data, starting from the beginning of the file. To make it easy to spot the differences, the numbers in the first column of the CSV are randomly generated. In the second column, the same strings are always substituted from the template in the StringFormat function.

```
   Print(" * Phase II. Text file");
   srand(GetTickCount());
   // create a new file or open an existing file for writing/overwriting
   // from the very beginning and subsequent reading; inside CSV data (Unicode)
   handle = PRTF(FileOpen(filetxt, FILE_CSV | FILE_WRITE | FILE_READ, ','));
   // three rows of data (number,string pair in each), separated by '\n'
   // note that the last element does not end with a newline '\n'
   // this is optional, but allowed
   string content = StringFormat(
      "%02d,abc\n%02d,def\n%02d,ghi", 
      rand() % 100, rand() % 100, rand() % 100);
   // '\n' will be replaced with '\r\n' automatically, thanks to FileWriteString
   PRTF(FileWriteString(handle, content));

```

Here is an example of generated data:

```
34,abc
20,def
02,ghi

```

Then we return to the beginning of the file and read it in a loop with FileReadString, constantly logging the status.

```
   PRTF(FileSeek(handle, 0, SEEK_SET));
   Print(FileState(handle));
   // count the lines in the file using the FileIsLineEnding feature
   int lineCount = 0;
   while(!FileIsEnding(handle))
   {
      PRTF(FileReadString(handle));
      Print(FileState(handle));
      // FileIsLineEnding also equals true when FileIsEnding equals true,
      // even if there is no trailing '\n' character
      if(FileIsLineEnding(handle)) lineCount++;
   }
   FileClose(handle);
   PRTF(lineCount);

```

Below are the logs for the file filetxt after the first and second run of the script. First one first:

```
first run
 * Phase II. Text file
FileOpen(filetxt,FILE_CSV|FILE_WRITE|FILE_READ,',')=1 / ok
FileWriteString(handle,content)=44 / ok
FileSeek(handle,0,SEEK_SET)=true / ok
P:0, F:false, L:false
FileReadString(handle)=08 / ok
P:8, F:false, L:false
FileReadString(handle)=abc / ok
P:18, F:false, L:true
FileReadString(handle)=37 / ok
P:24, F:false, L:false
FileReadString(handle)=def / ok
P:34, F:false, L:true
FileReadString(handle)=96 / ok
P:40, F:false, L:false
FileReadString(handle)=ghi / ok
P:46, F:true, L:true
lineCount=3 / ok

```

And here is the second one:

```
second run
 * Phase II. Text file
FileOpen(filetxt,FILE_CSV|FILE_WRITE|FILE_READ,',')=1 / ok
FileWriteString(handle,content)=44 / ok
FileSeek(handle,0,SEEK_SET)=true / ok
P:0, F:false, L:false
FileReadString(handle)=34 / ok
P:8, F:false, L:false
FileReadString(handle)=abc / ok
P:18, F:false, L:true
FileReadString(handle)=20 / ok
P:24, F:false, L:false
FileReadString(handle)=def / ok
P:34, F:false, L:true
FileReadString(handle)=02 / ok
P:40, F:false, L:false
FileReadString(handle)=ghi / ok
P:46, F:true, L:true
lineCount=3 / ok

```

As you can see, the file does not change in size, but different numbers are written at the same offsets. Because this CSV file has two columns, after every second value we read, we see an EOL flag ("L:true") cocked.

The number of detected lines is 3, despite the fact that there are only 2 newline characters in the file: the last (third) line ends with the file.

Finally, the last test scenario uses the file file100 (MQL5Book/k100.raw) to move the pointer past the end of the file (to the mark of 1000000 bytes), and thereby increase its size (reserves disk space for potential future write operations).

```
   Print(" * Phase III. Allocate large file");
   handle = PRTF(FileOpen(file100, FILE_BIN | FILE_WRITE));
   PRTF(FileSeek(handle, 1000000, SEEK_END));
   // to change the size, you need to write at least something
   PRTF(FileWriteInteger(handle, 0xFF, 1));
   PRTF(FileTell(handle));
   FileClose(handle);

```

The log output for this script does not change from run to run, however, the random data that ends up in the space allocated for the file may differ (its contents are not shown here: use an external binary viewer).

```
 * Phase III. Allocate large file
FileOpen(file100,FILE_BIN|FILE_WRITE)=1 / ok
FileSeek(handle,1000000,SEEK_END)=true / ok
FileWriteInteger(handle,0xFF,1)=1 / ok
FileTell(handle)=1000001 / ok

```
