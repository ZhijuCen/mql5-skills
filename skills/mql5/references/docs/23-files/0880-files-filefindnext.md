# FileFindNext

The function continues the search started by [FileFindFirst()](/en/docs/files/filefindfirst).

```
bool  FileFindNext(
   long      search_handle,         // Search handle
   string&   returned_filename      // Name of the file or subdirectory found
   );

```

Parameters

search_handle

[in]  Search handle, retrieved by [FileFindFirst()](/en/docs/files/filefindfirst).

returned_filename

[out] The name of the next file or subdirectory found. Only the file name is returned (including the extension), the directories and subdirectories are not included no matter if they are specified or not in the search filter.

Return Value

If successful returns true, otherwise false.

Example:

```
//--- display the window of input parameters when launching the script
#property script_show_inputs
//--- filter
input string InpFilter="*";
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string file_name;
   int    i=1;
//--- receive search handle in local folder's root
   long search_handle=FileFindFirst(InpFilter,file_name);
//--- check if FileFindFirst() function executed successfully
   if(search_handle!=INVALID_HANDLE)
     {
      //--- check if the passed strings are file or directory names in the loop
      do
        {
         ResetLastError();
         //--- if this is a file, the function will return true, if it is a directory, the function will generate error ERR_FILE_IS_DIRECTORY
         FileIsExist(file_name);
         PrintFormat("%d : %s name = %s",i,GetLastError()==ERR_FILE_IS_DIRECTORY ? "Directory" : "File",file_name);
         i++;
        }
      while(FileFindNext(search_handle,file_name));
      //--- close search handle
      FileFindClose(search_handle);
     }
   else
      Print("Files not found!");
  }

```

See also

[FileFindFirst](/en/docs/files/filefindfirst), [FileFindClose](/en/docs/files/filefindclose)
