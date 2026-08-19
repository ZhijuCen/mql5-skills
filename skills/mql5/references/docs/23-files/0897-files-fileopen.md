# FileOpen

The function opens the file with the specified name and flag.

```
int  FileOpen(
   string  file_name,           // File name
   int     open_flags,          // Combination of flags
   short   delimiter='\t',      // Delimiter
   uint    codepage=CP_ACP      // Code page
   );

```

Parameters

file_name

[in]  The name of the file can contain subfolders. If the file is opened for writing, these subfolders will be created if there are no such ones.

open_flags

[in] [ combination of flags](/en/docs/constants/io_constants/fileflags) determining the operation mode for the file. The flags are defined as follows:  

FILE_READ file is opened for reading  

FILE_WRITE file is opened for writing  

FILE_BIN binary read-write mode (no conversion from a string and to a string)  

FILE_CSV file of csv type (all recorded items are converted to the strings of unicode or ansi type, and are separated by a delimiter)  

FILE_TXT a simple text file (the same as csv, but the delimiter is not taken into account)  

FILE_ANSI lines of ANSI type (single-byte symbols)   

FILE_UNICODE lines of UNICODE type (double-byte characters)  

FILE_SHARE_READ shared reading from several programs  

FILE_SHARE_WRITE shared writing from several programs  

FILE_COMMON location of the file in a shared folder for all client terminals \Terminal\Common\Files

delimiter='\t'

[in]  value to be used as a separator in txt or csv-file. If the csv-file delimiter is not specified, it defaults to a tab. If the txt-file delimiter is not specified, then no separator is used. If the separator is clearly set to 0, then no separator is used.

codepage=CP_ACP

[in]  The value of the code page. For the most-used [code pages](/en/docs/constants/io_constants/codepageusage) provide appropriate constants.

Return Value

If a file has been opened successfully, the function returns the file handle, which is then used to access the file data. In case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants).

Note

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

Make sure to set the FILE_ANSI flag if the file should be read in a specific encoding (the codepage parameter with [a code page](/en/docs/constants/io_constants/codepageusage) value is specified). If there is no specified FILE_ANSI flag, the text file is read in Unicode without any conversion.

The file is opened in the folder of the client terminal in the subfolder MQL5\files (or testing_agent_directory\MQL5\files in case of testing). If FILE_COMMON is specified among flags, the file is opened in a shared folder for all MetaTrader 5 client terminals.

"Named pipes" can be opened according to the following rules:

- Pipe name is a string, which should have the following look: "\\servername\pipe\pipename", where servername - server name in the network, while pipename is a pipe name. If the pipes are used on the same computer, the server name can be omitted but a point should be inserted instead of it: "\\.\pipe\pipename". A client trying to connect the pipe should know its name.
- [FileFlush()](/en/docs/files/fileflush) and [FileSeek()](/en/docs/files/fileseek) should be called to the beginning of a file between sequential operations of reading from the pipe and writing to it.

A special symbol '\' is used in shown strings. Therefore, '\' should be doubled when writing a name in MQL5 application. It means that the above example should have the following look in the code: "\\\\servername\\pipe\\pipename".

More information about working with named pipes can be found in the article "[Communicating With MetaTrader 5 Using Named Pipes Without Using DLLs](https://www.mql5.com/en/articles/503)".

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- incorrect file opening method
   string terminal_data_path=TerminalInfoString(TERMINAL_DATA_PATH);
   string filename=terminal_data_path+"\\MQL5\\Files\\"+"fractals.csv";
   int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV);
   if(filehandle<0)
     {
      Print("Failed to open the file by the absolute path ");
      Print("Error code ",GetLastError());
     }
 
//--- correct way of working in the "file sandbox"
   ResetLastError();
   filehandle=FileOpen("fractals.csv",FILE_WRITE|FILE_CSV);
   if(filehandle!=INVALID_HANDLE)
     {
      FileWrite(filehandle,TimeCurrent(),Symbol(), EnumToString(_Period));
      FileClose(filehandle);
      Print("FileOpen OK");
     }
   else Print("Operation FileOpen failed, error ",GetLastError());
//--- another example with the creation of an enclosed directory in MQL5\Files\
   string subfolder="Research";
   filehandle=FileOpen(subfolder+"\\fractals.txt",FILE_WRITE|FILE_CSV);
      if(filehandle!=INVALID_HANDLE)
     {
      FileWrite(filehandle,TimeCurrent(),Symbol(), EnumToString(_Period));
      FileClose(filehandle);
      Print("The file must be created in the folder "+terminal_data_path+"\\"+subfolder);
     }
   else Print("File open failed, error ",GetLastError());
  }

```

See also

[Use of a Codepage](/en/docs/constants/io_constants/codepageusage), [FileFindFirst](/en/docs/files/filefindfirst), [FolderCreate](/en/docs/files/foldercreate), [File opening flags](/en/docs/constants/io_constants/fileflags)
