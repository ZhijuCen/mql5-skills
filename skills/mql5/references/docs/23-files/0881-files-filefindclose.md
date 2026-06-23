# FileFindClose

The function closes the search handle.

```
void  FileFindClose(
   long  search_handle      //  Search handle
   );

```

Parameters

search_handle

[in]  Search handle, retrieved by [FileFindFirst()](/en/docs/files/filefindfirst).

Return Value

No value returned.

Note

Function must be called to free up system resources.

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
         //--- if this is a file, the function will return true, if it is a directory, the function will generate error 5018
         FileIsExist(file_name);
         PrintFormat("%d : %s name = %s",i,GetLastError()==5018 ? "Directory" : "File",file_name);
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

[FileFindFirst](/en/docs/files/filefindfirst), [FileFindNext](/en/docs/files/filefindnext)
