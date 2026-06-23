# FileDelete

Deletes the specified file in a local folder of the client terminal.

```
bool  FileDelete(
   const string  file_name,     // File name to delete 
   int           common_flag=0  // Location of the file to delete
   );

```

Parameters

file_name

[in]  File name.

common_flag=0

[in]  [Flag](/en/docs/constants/io_constants/fileflags) determining the file location. If common_flag = FILE_COMMON, then the file is located in a shared folder for all client terminals \Terminal\Common\Files. Otherwise, the file is located in a local folder.

Return Value

In case of failure the function returns false.

Note

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

Deletes the specified file from a local folder of the client terminal (MQL5\Files or MQL5\Tester\Files in case of testing). If common_flag = FILE_COMMON, then the function removes the file from the shared folder for all client terminals \Terminal\Common\Files.

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
