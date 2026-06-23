# Force write cache to disk

File writing and reading in MQL5 are cached. This means that a certain buffer in memory is maintained for the data, due to which the efficiency of work is increased. So, the data transferred using function calls during writing gets into the output buffer, and only after it is full, the physical writing to the disk takes place. When reading, on the contrary, more data is read from the disk into the buffer than the program requested using functions (if it is not the end of the file), and subsequent read operations (which are very likely) are faster.

Caching is a standard technology used in most applications and at the level of the operating system itself. However, besides its pros, caching has its cons as well.

In particular, if files are used as a means of data exchange between programs, delayed writing can significantly slow down communication and make it less predictable, since the buffer size can be quite large, and the frequency of its "dumping" to disk can be adjusted according to some algorithms.

For example, in MetaTrader 5 there is a whole category of MQL programs for copying trading signals from one instance of the terminal to another. They tend to use files to transfer information, and it's very important to them that caching doesn't slow things down. For this case, MQL5 provides the FileFlush function.

void FileFlush(int handle)

The function performs a forced flush to a disk of all data remaining in the I/O file buffer for the file with the handle descriptor.

If you do not use this function, then part of the data "sent" from the program may, in the worst case, get to the disk only when the file is closed.

This feature provides greater guarantees for the safety of valuable data in case of unforeseen events (such as an operating system or program hang). However, on the other hand, frequent FileFlush calls during mass recording are not recommended, as they can adversely affect performance.

If the file is opened in the mixed mode, simultaneously for writing and reading, the FileFlush function must be called between reads and writes to the file.

As an example, consider the script FileFlush.mq5, in which we implement two modes that simulate the operation of the deal copier. We will need to run two instances of the script on different charts, with one of them becoming the data sender and the other one becoming the recipient.

The script has two input parameters: EnableFlashing allows you to compare the actions of programs using the FileFlush function and without it, and UseCommonFolder indicates the need to create a file that acts as a means of data transfer, to choose from: in the folder of the current instance of the terminal or in a shared folder (in the latter case, you can test data transfer between different terminals).

```
#property script_show_inputs
input bool EnableFlashing = false;
input bool UseCommonFolder = false;

```

Recall that in order for a dialog with input variables to appear when the script is launched, you must additionally set the script_show_inputs property.

The name of the transit file is specified in the dataport variable. Option UseCommonFolder controls the FILE_COMMON flag added to the set of mode switches for opened files in the File Open function.

```
const string dataport = "MQL5Book/dataport";
const int flag = UseCommonFolder ? FILE_COMMON : 0;

```

The main OnStart function actually consists of two parts: settings for the opened file and a loop that periodically sends or receives data.

We will need to run two instances of the script, and each will have its own file descriptor pointing to the same file on disk but opened in different modes.

```
void OnStart()
{
   bool modeWriter = true; // by default the script should write data
   int count = 0;          // number of writes/reads made
   // create a new or reset the old file in read mode, as a "sender"
   int handle = PRTF(FileOpen(dataport, 
      FILE_BIN | FILE_WRITE | FILE_SHARE_READ | flag));
   // if writing is not possible, most likely another instance of the script is already writing to the file,
   // so we try to open it for reading
   if(handle == INVALID_HANDLE)
   {
      // if it is possible to open the file for reading, we will continue to work as a "receiver"
      handle = PRTF(FileOpen(dataport, 
         FILE_BIN | FILE_READ | FILE_SHARE_WRITE | FILE_SHARE_READ | flag));
      if(handle == INVALID_HANDLE)
      {
         Print("Can't open file"); // something is wrong
         return;
      }
      modeWriter = false; // switch model/role
   }

```

In the beginning, we are trying to open the file in FILE_WRITE mode, without sharing write permission (FILE_SHARE_WRITE), so the first instance of the running script will capture the file and prevent the second one from working in write mode. The second instance will get an error and INVALID_HANDLE after the first call to FileOpen and will try to open the file in the read mode (FILE_READ) with the second FileOpen call using the FILE_SHARE_WRITE parallel write flag. Ideally, this should work. Then, the modeWriter variable will be set to false to indicate the actual role of the script.

The main operating loop has the following structure:

```
   while(!IsStopped())
   {
      if(modeWriter)
      {
         // ...write test data
      }
      else
      {
         // ...read test data
      }
      Sleep(5000);
   }

```

The loop is executed until the user deletes the script from the chart manually: this will be signaled by the [IsStopped](/en/book/common/environment/env_stop) function. Inside the loop, the action is triggered every 5 seconds by calling the [Sleep](/en/book/common/timing/timing_sleep) function, which "freezes" the program for the specified number of milliseconds (5000 in this case). This is done to make it easier to analyze ongoing changes and to avoid too frequent state logs. In a real program without detailed logs, you can send data every 100 milliseconds or even more often.

The transmitted data will include the current time (one datetime value, 8 bytes). In the first branch of the instruction if(modeWriter), where the file is written, we call FileWriteLong with the last count (obtained from the function [TimeLocal](/en/book/common/timing/timing_local_server)), increase the operation counter by 1 (count++) and output the current state to the log.

```
         long temp = TimeLocal(); // get the current local time datetime
         FileWriteLong(handle, temp); // append it to the file (every 5 seconds)
         count++;
         if(EnableFlashing)
         {
            FileFlush(handle);
         }
         Print(StringFormat("Written[%d]: %I64d", count, temp));

```

It is important to note that calling the FileFlush function after each entry is done only if the input parameter EnableFlashing is set to true.

In the second branch of the if operator, in which we read the data, we first reset the internal error flag by calling ResetLastError. This is necessary because we are going to read the data from the file as long as there is any data. Once there is no more data to read, the program will get a specific error code 5015 (ERR_FILE_READERROR).

Since the built-in MQL5 timers, including the Sleep function, have limited accuracy (approximately 10 ms), we cannot exclude the situation where two consecutive writes occurred between two consecutive attempts to read a file. For example, one reading occurred at 10:00:00'200, and the second at 10:00:05'210 (in the notation "hours:minutes:seconds'milliseconds"). In this case, two recordings occurred in parallel: one at 10:00:00'205, and the second at 10:00:05'205, and both fell into the above period. Such a situation is unlikely but possible. Even with absolutely precise time intervals, the MQL5 runtime system may be forced to choose between two running scripts (which one to invoke earlier than the other) if the total number of programs is large and there are not enough processor cores for all of them.

MQL5 provides [high-precision timers](/en/book/applications/timer/timer_event_set_millisecond) (up to microseconds), but this is not critical for the current task.

The nested loop is needed for one more reason. Immediately after the script is launched as a "receiver" of data, it must process all the records from the file that have accumulated since the launch of the "sender" (it is unlikely that both scripts can be launched simultaneously). Probably someone would prefer a different algorithm: skip all the "old" records and keep track of only the new ones. This can be done, but the "lossless" option is implemented here.

```
         ResetLastError();
         while(true)// loop as long as there is data and no problems
         {
            bool reportedEndBeforeRead = FileIsEnding(handle);
            ulong reportedTellBeforeRead = FileTell(handle);
  
            temp = FileReadLong(handle);
            // if there is no more data, we will get an error 5015 (ERR_FILE_READERROR)
            if(_LastError)break; // exit the loop on any error
  
            // here the data is received without errors
            count++;
            Print(StringFormat("Read[%d]: %I64d\t"
               "(size=%I64d, before=%I64d(%s), after=%I64d)", 
               count, temp, 
               FileSize(handle), reportedTellBeforeRead, 
               (string)reportedEndBeforeRead, FileTell(handle)));
         }

```

Please note the following point. The metadata about the file opened for reading, such as its size, returned by the FileSize function (see [Getting file properties](/en/book/common/files/files_properties)) does not change after the file is opened. If another program later adds something to the file we opened for reading, its "detectable" length will not be updated even if we call FileFlash for the read descriptor. It would be possible to close and reopen the file (before each read, but this is not efficient): then the new length would appear for the new descriptor. But we will do without it, with the help of another trick.

The trick is to keep reading data using read functions (in our case FileReadLong) for as long as they return data without errors. It is important not to use other functions that operate on metadata. In particular, due to the fact that the read-only end-of-file remains constant, checking with the FileIsEnding function (see [Position control within a file](/en/book/common/files/files_cursor)) will give true at the old position, despite the possible replenishment of the file from another process. Moreover, an attempt to move the internal file pointer to the end (FileSeek(handle, 0, SEEK_END); for the FileSeek function see the same [section](/en/book/common/files/files_cursor)) will not jump to the actual end of the data, but to the outdated position where the end was located at the time of opening.

The function tells us the real position inside the file FileTell (see the same [section](/en/book/common/files/files_cursor)). As information is added to the file from another instance of the script and read in this loop, the pointer will move further and further to the right, exceeding, however strange it is, FileSize. For a visual demonstration of how the pointer moves beyond the file size, let's save its values before and after calling FileReadLong, and then output the values along with the size to the log.

Once reading with FileReadLong generates any error, the inner loop will break. Regular loop exit implies error 5015 (ERR_FILE_READERROR). In particular, it occurs when there is no data available for reading at the current position in the file.

The last successfully read data is output to the log, and it is easy to compare it with what the sender script output there.

Let's run a new script twice. To distinguish between its copies, we'll do it on the charts of different instruments.

When running both scripts, it is important to observe the same value of the UseCommonFolder parameter. Let's leave it in our tests equal to false since we will be doing everything in one terminal. Data transfer between different terminals with UseCommonFolder set to true is suggested for independent testing.

First, let's run the first instance on the EURUSD,H1 chart, leaving all the default settings, including EnableFlashing=false. Then, we will run the second instance on the XAUUSD,H1 chart (also with default settings). The log will be as follows (your time will be different):

```
(EURUSD,H1) *
(EURUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(EURUSD,H1) Written[1]: 1629652995
(XAUUSD,H1) *
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=-1 / CANNOT_OPEN_FILE(5004)
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_READ|FILE_SHARE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(EURUSD,H1) Written[2]: 1629653000
(EURUSD,H1) Written[3]: 1629653005
(EURUSD,H1) Written[4]: 1629653010
(EURUSD,H1) Written[5]: 1629653015

```

The sender successfully opened the file for writing and started sending data every 5 seconds, according to the lines with the word "Written" and to the increasing values. Less than 5 seconds after the sender was started, the receiver was also started. It gave an error message because it could not open the file for writing. But then it successfully opened the file for reading. However, there are no records indicating that it was able to find the transmitted data in the file. The data remained "hanging" in the sender's cache.

Let's stop both scripts and run them again in the same sequence: first, we run the sender on EURUSD, and then the receiver on XAUUSD. But this time we will specify EnableFlashing=true for the sender.

Here's what happens in the log:

```
(EURUSD,H1) *
(EURUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(EURUSD,H1) Written[1]: 1629653638
(XAUUSD,H1) *
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=-1 / CANNOT_OPEN_FILE(5004)
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_READ|FILE_SHARE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(XAUUSD,H1) Read[1]: 1629653638 (size=8, before=0(false), after=8)
(EURUSD,H1) Written[2]: 1629653643
(XAUUSD,H1) Read[2]: 1629653643 (size=8, before=8(true), after=16)
(EURUSD,H1) Written[3]: 1629653648
(XAUUSD,H1) Read[3]: 1629653648 (size=8, before=16(true), after=24)
(EURUSD,H1) Written[4]: 1629653653
(XAUUSD,H1) Read[4]: 1629653653 (size=8, before=24(true), after=32)
(EURUSD,H1) Written[5]: 1629653658

```

The same file is again successfully opened in different modes in both scripts, but this time the written values are regularly read by the receiver.

It is interesting to note that before each next data reading, except for the first one, the FileIsEnding function returns true (displayed in the same string as the received data, in parentheses after the "before" string). Thus, there is a sign that we are at the end of the file, but then FileReadLong successfully reads a value supposedly outside of the file limit and shifts the position to the right. For example, the entry "size=8, before=8(true), after=16" means that the file size is reported to the MQL program as 8, the current pointer before the call to FileReadLong is also equal to 8 and the end-of-file sign is enabled. After a successful call to FileReadLong, the pointer is moved to 16. However, on the next and all other iterations, we see "size=8" again, and the pointer gradually moves further and further out of the file.

Since the write in the sender and the read in the receiver occur once every 5 seconds, depending on their loop offset phases, we can observe the effect of a different delay between the two operations, up to almost 5 seconds in the worst case. However, this does not mean that cache flushing is so slow. In fact, it is almost an instant process. To ensure a more rapid change detection, you can reduce the sleep period in loops (please note that this test, if the delay is too short, will quickly fill the log — unlike a real program, new data is always generated here as this is the sender's current time to the nearest second).

Incidentally, you can run multiple recipients, as opposed to the sender which must be only one. The log below shows the operation of a sender on EURUSD and of two recipients on the XAUUSD and USDRUB charts.

```
(EURUSD,H1) *
(EURUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(EURUSD,H1) Written[1]: 1629671658
(XAUUSD,H1) *
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=-1 / CANNOT_OPEN_FILE(5004)
(XAUUSD,H1) FileOpen(dataport,FILE_BIN|FILE_READ|FILE_SHARE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(XAUUSD,H1) Read[1]: 1629671658 (size=8, before=0(false), after=8)
(EURUSD,H1) Written[2]: 1629671663
(USDRUB,H1) *
(USDRUB,H1) FileOpen(dataport,FILE_BIN|FILE_WRITE|FILE_SHARE_READ|flag)=-1 / CANNOT_OPEN_FILE(5004)
(USDRUB,H1) FileOpen(dataport,FILE_BIN|FILE_READ|FILE_SHARE_WRITE|FILE_SHARE_READ|flag)=1 / ok
(USDRUB,H1) Read[1]: 1629671658 (size=16, before=0(false), after=8)
(USDRUB,H1) Read[2]: 1629671663 (size=16, before=8(false), after=16)
(XAUUSD,H1) Read[2]: 1629671663 (size=8, before=8(true), after=16)
(EURUSD,H1) Written[3]: 1629671668
(USDRUB,H1) Read[3]: 1629671668 (size=16, before=16(true), after=24)
(XAUUSD,H1) Read[3]: 1629671668 (size=8, before=16(true), after=24)
(EURUSD,H1) Written[4]: 1629671673
(USDRUB,H1) Read[4]: 1629671673 (size=16, before=24(true), after=32)
(XAUUSD,H1) Read[4]: 1629671673 (size=8, before=24(true), after=32)
(EURUSD,H1) Written[5]: 1629671678

```

By the time the third script on USDRUB was launched, there were already 2 records of 8 bytes in the file, so the inner loop immediately performed 2 iterations from FileReadLong, and the file size "seems" to be equal to 16.
