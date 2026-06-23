# FileIsExist

Checks the existence of a file.

```
bool  FileIsExist(
   const string  file_name,       // File name
   int           common_flag=0    // Search area
   );

```

Parameters

file_name

[in]  The name of the file being checked

common_flag=0

[in]  [Flag](/en/docs/constants/io_constants/fileflags) determining the location of the file. If common_flag = FILE_COMMON, then the file is located in a shared folder for all client terminals \Terminal\Common\Files. Otherwise, the file is located in a local folder.

Return Value

Returns true, if the specified file exists.

Note

Checked file can turn out to be a subdirectory. In this case, FileIsExist() function will return false, while error 5018 will be logged in _LastError variable - "This is a directory, not a file" (see example for [FileFindFirst](/en/docs/files/filefindfirst) function).

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

If common_flag = FILE_COMMON, then the function looks for the file in a shared folder for all client terminals \Terminal\Common\Files, otherwise the function looks for a file in a local folder (MQL5\Files or MQL5\Tester\Files in the case of testing).

Example:

```
//--- show the window of input parameters when launching the script
#property script_show_inputs
//--- date for old files
input datetime InpFilesDate=D'2013.01.01 00:00';
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string   file_name;      // variable for storing file names
   string   filter="*.txt"; // filter for searching the files
   datetime create_date;    // file creation date
   string   files[];        // list of file names
   int      def_size=25;    // array size by default
   int      size=0;         // number of files
//--- allocate memory for the array
   ArrayResize(files,def_size);
//--- receive the search handle in the local folder's root
   long search_handle=FileFindFirst(filter,file_name);
//--- check if FileFindFirst() executed successfully
   if(search_handle!=INVALID_HANDLE)
     {
      //--- searching files in the loop
      do
        {
         files[size]=file_name;
         //--- increase the array size
         size++;
         if(size==def_size)
           {
            def_size+=25;
            ArrayResize(files,def_size);
           }
         //--- reset the error value
         ResetLastError();
         //--- receive the file creation date
         create_date=(datetime)FileGetInteger(file_name,FILE_CREATE_DATE,false);
         //--- check if the file is old
         if(create_date<InpFilesDate)
           {
            PrintFormat("%s file deleted!",file_name);
            //--- delete the old file
            FileDelete(file_name);
           }
        }
      while(FileFindNext(search_handle,file_name));
      //--- close the search handle
      FileFindClose(search_handle);
     }
   else
     {
      Print("Files not found!");
      return;
     }
//--- check what files have remained
   PrintFormat("Results:");
   for(int i=0;i<size;i++)
     {
      if(FileIsExist(files[i]))
         PrintFormat("%s file exists!",files[i]);
      else
         PrintFormat("%s file deleted!",files[i]);
     }
  }

```

See also

[FileFindFirst](/en/docs/files/filefindfirst)
