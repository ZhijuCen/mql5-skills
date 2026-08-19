# File Functions

This is a group of functions for working with files.

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means cannot be outside the file sandbox.

There are two directories (with subdirectories) in which working files can be located:

- terminal_data_folder\MQL5\FILES\ (in the terminal menu select to view "File" - "Open the data directory");
- the common folder for all the terminals installed on a computer - usually located in the directory C:\Documents and Settings\All Users\Application Data\MetaQuotes\Terminal\Common\Files.

There is a program method to obtain names of these catalogs using the [TerminalInfoString()](/en/docs/check/terminalinfostring) function, using the [ENUM_TERMINAL_INFO_STRING](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_string) enumeration:

```
//--- Folder that stores the terminal data
   string terminal_data_path=TerminalInfoString(TERMINAL_DATA_PATH);
//--- Common folder for all client terminals
   string common_data_path=TerminalInfoString(TERMINAL_COMMONDATA_PATH);

```

Work with files from other directories is prohibited.

If the file is opened for writing using [FileOpen()](/en/docs/files/fileopen), all subfolders specified in the path will be created if there are no such ones.

File functions allow working with so-called "named pipes". To do this, simply call [FileOpen()](/en/docs/files/fileopen) function with appropriate parameters.

| Function | Action |
| --- | --- |
| FileSelectDialog | Create a file or folder opening/creation dialog |
| FileFindFirst | Starts the search of files in a directory in accordance with the specified filter |
| FileFindNext | Continues the search started by the FileFindFirst() function |
| FileFindClose | Closes search handle |
| FileOpen | Opens a file with a specified name and flag |
| FileDelete | Deletes a specified file |
| FileFlush | Writes to a disk all data remaining in the input/output file buffer |
| FileGetInteger | Gets an integer property of a file |
| FileIsEnding | Defines the end of a file in the process of reading |
| FileIsLineEnding | Defines the end of a line in a text file in the process of reading |
| FileClose | Closes a previously opened file |
| FileIsExist | Checks the existence of a file |
| FileCopy | Copies the original file from a local or shared folder to another file |
| FileMove | Moves or renames a file |
| FileReadArray | Reads arrays of any type except for string from the file of the BIN type |
| FileReadBool | Reads from the file of the CSV type a string from the current position till a delimiter (or till the end of a text line) and converts the read string to a value of bool type |
| FileReadDatetime | Reads from the file of the CSV type a string of one of the formats: "YYYY.MM.DD HH:MM:SS", "YYYY.MM.DD" or "HH:MM:SS" - and converts it into a datetime value |
| FileReadDouble | Reads a double value from the current position of the file pointer |
| FileReadFloat | Reads a float value from the current position of the file pointer |
| FileReadInteger | Reads int, short or char value from the current position of the file pointer |
| FileReadLong | Reads a long type value from the current position of the file pointer |
| FileReadNumber | Reads from the file of the CSV type a string from the current position till a delimiter (or til the end of a text line) and converts the read string into double value |
| FileReadString | Reads a string from the current position of a file pointer from a file |
| FileReadStruct | Reads the contents from a binary file  into a structure passed as a parameter, from the current position of the file pointer |
| FileSeek | Moves the position of the file pointer by a specified number of bytes relative to the specified position |
| FileSize | Returns the size of a corresponding open file |
| FileTell | Returns the current position of the file pointer of a corresponding open file |
| FileWrite | Writes data to a file of CSV or TXT type |
| FileWriteArray | Writes arrays of any type except for string into a file of BIN type |
| FileWriteDouble | Writes value of the double type from the current position of a file pointer into a binary file |
| FileWriteFloat | Writes value of the float type from the current position of a file pointer into a binary file |
| FileWriteInteger | Writes value of the int type from the current position of a file pointer into a binary file |
| FileWriteLong | Writes value of the long type from the current position of a file pointer into a binary file |
| FileWriteString | Writes the value of a string parameter into a BIN or TXT file starting from the current position of the file pointer |
| FileWriteStruct | Writes the contents of a structure passed as a parameter into a binary file, starting from the current position of the file pointer |
| FileLoad | Reads all data of a specified binary file into a passed array of numeric types or simple structures |
| FileSave | Writes to a binary file all elements of an array passed as a parameter |
| FolderCreate | Creates a folder in the Files directory |
| FolderDelete | Removes a selected directory. If the folder is not empty, then it can't be removed |
| FolderClean | Deletes all files in the specified folder |
