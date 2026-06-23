# FileCopy

The function copies the original file from a local or shared folder to another file.

```
bool  FileCopy(
   const string  src_file_name,     // Name of a source file
   int           common_flag,       // Location
   const string  dst_file_name,     // Name of the destination file
   int           mode_flags         // Access mode
   );

```

Parameters

src_file_name

[in]  File name to copy.

common_flag

[in]  [Flag](/en/docs/constants/io_constants/fileflags) determining the location of the file. If common_flag = FILE_COMMON, then the file is located in a shared folder for all client terminals \Terminal\Common\Files. Otherwise, the file is located in a local folder (for example, common_flag=0).

dst_file_name

[in]  Result file name.

mode_flags

[in]  [Access flags](/en/docs/constants/io_constants/fileflags). The parameter can contain only 2 flags: FILE_REWRITE and/or FILE_COMMON - other flags are ignored. If the file already exists, and the FILE_REWRITE flag hasn't been specified, then the file will not be rewritten, and the function will return false.

Return Value

In case of failure the function returns false.

Note

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

If the new file already exists, the copy will be made depending on the availability of the FILE_REWRITE flag in the mode_flags parameter.

Example:

```
//--- display the window of input parameters when launching the script
#property script_show_inputs
//--- input parameters
input string InpSrc="source.txt";       // source
input string InpDst="destination.txt";  // copy
input int    InpEncodingType=FILE_ANSI; // ANSI=32 or UNICODE=64
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- display the source contents (it must exist)
   if(!FileDisplay(InpSrc))
      return;
//--- check if the copy file already exists (may not be created)
   if(!FileDisplay(InpDst))
     {
      //--- the copy file does not exist, copying without FILE_REWRITE flag (correct copying)
      if(FileCopy(InpSrc,0,InpDst,0))
         Print("File is copied!");
      else
         Print("File is not copied!");
     }
   else
     {
      //--- the copy file already exists, try to copy without FILE_REWRITE flag (incorrect copying)
      if(FileCopy(InpSrc,0,InpDst,0))
         Print("File is copied!");
      else
         Print("File is not copied!");
      //--- InpDst file's contents remains the same
      FileDisplay(InpDst);
      //--- copy once more with FILE_REWRITE flag (correct copying if the file exists)
      if(FileCopy(InpSrc,0,InpDst,FILE_REWRITE))
         Print("File is copied!");
      else
         Print("File is not copied!");
     }
//--- receive InpSrc file copy
   FileDisplay(InpDst);
  }
//+------------------------------------------------------------------+
//| Read the file contents                                           |
//+------------------------------------------------------------------+
bool FileDisplay(const string file_name)
  {
//--- reset the error value
   ResetLastError();
//--- open the file
   int file_handle=FileOpen(file_name,FILE_READ|FILE_TXT|InpEncodingType);
   if(file_handle!=INVALID_HANDLE)
     {
      //--- display the file contents in the loop
      Print("+---------------------+");
      PrintFormat("File name = %s",file_name);
      while(!FileIsEnding(file_handle))
         Print(FileReadString(file_handle));
      Print("+---------------------+");
      //--- close the file
      FileClose(file_handle);
      return(true);
     }
//--- failed to open the file
   PrintFormat("%s is not opened, error = %d",file_name,GetLastError());
   return(false);
  }

```
