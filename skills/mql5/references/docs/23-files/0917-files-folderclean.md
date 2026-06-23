# FolderClean

The function deletes all files in a specified folder.

```
bool  FolderClean(
   string  folder_name,       // String with the name of the deleted folder
   int     common_flag=0      // Scope
   );

```

Parameters

folder_name

[in] The name of the directory where you want to delete all files. Contains the full path to the folder.

common_flag=0

[in]  [Flag](/en/docs/constants/io_constants/fileflags) determining the location of the directory. If common_flag = FILE_COMMON, then the directory is in the shared folder for all client terminals \Terminal\Common\Files. Otherwise, the directory is in a local folder(MQL5\Files or MQL5\Tester\Files in case of testing).

Return Value

Returns true if successful, otherwise false.

Note

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

This function should be used with caution, since all the files and all subdirectories are deleted irretrievably.

Example:

```
//+------------------------------------------------------------------+
//|                                             Demo_FolderClean.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- Description
#property description "The script shows a sample use of FolderClean()."
#property description "First, files are created in the specified folder using the FileOpen() function."
#property description "Then, before the files are deleted, a warning is shown using MessageBox()."
 
//--- Show the dialog of input parameters when starting the script
#property script_show_inputs
//--- Input parameters
input string   foldername="demo_folder";  // Create a folder in MQL5/Files/
input int      files=5;                   // The number of files to create and delete
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string name="testfile";
//--- First open or create files in the terminal data folder
   for(int N=0;N<files;N++)
     {
      //--- The name of the file in the form of 'demo_folder\testfileN.txt'
      string filemane=StringFormat("%s\\%s%d.txt",foldername,name,N);
      //--- Open a file with the flag for writing, in this case the 'demo_folder' will be created automatically
      int handle=FileOpen(filemane,FILE_WRITE);
      //--- Find out if the FileOpen() function was successful
      if(handle==INVALID_HANDLE)
        {
         PrintFormat("Failed to create file %s. Error code",filemane,GetLastError());
         ResetLastError();
        }
      else
        {
         PrintFormat("File %s has been successfully opened",filemane);
         //--- The opened file is not needed any more, so close it
         FileClose(handle);
        }
     }
 
//--- Check the number of files in the folder 
   int k=FilesInFolder(foldername+"\\*.*",0);
   PrintFormat("Totally the folder %s contains %d files",foldername,k);
 
//--- Show a dialog to ask the user
   int choice=MessageBox(StringFormat("You are going to delete %d files from folder %s. Do you want to continue?",foldername,k),
                         "Deleting files from the folder",
                         MB_YESNO|MB_ICONQUESTION); //  Two buttons - "Yes" and "No"
   ResetLastError();
 
//--- Run an action depending on the selected variant
   if(choice==IDYES)
     {
      //--- Start to delete files
      PrintFormat("Trying to delete all files from folder %s",foldername);
      if(FolderClean(foldername,0))
         PrintFormat("Files have been successfully deleted, %d files left in folder %s",
                     foldername,
                     FilesInFolder(foldername+"\\*.*",0));
      else
         PrintFormat("Failed to delete files from folder %s. Error code %d",foldername,GetLastError());
     }
   else
      PrintFormat("Deletion canceled");
//---
  }
//+------------------------------------------------------------------+
//| Returns the number of files in the specified folder              |
//+------------------------------------------------------------------+
int FilesInFolder(string path,int flag)
  {
   int count=0;
   long handle;
   string filename;
//---
   handle=FileFindFirst(path,filename,flag);
//--- If at least one file found, search for more files
   if(handle!=INVALID_HANDLE)
     {
      //--- Show the name of the file
      PrintFormat("File %s found",filename);
      //--- Increase the counter of found files/folders
      count++;
      //--- Start search in all files/folders 
      while(FileFindNext(handle,filename))
        {
         PrintFormat("File %s found",filename);
         count++;
        }
      //--- Do not forget to close the search handle upon completion
      FileFindClose(handle);
     }
   else // Failed to get the handle
     {
      PrintFormat("Files search in folder %s failed",path);
     }
//--- Return the result
   return count;
  }

```

See also

[FileFindFirst](/en/docs/files/filefindfirst), [FileFindNext](/en/docs/files/filefindnext), [FileFindClose](/en/docs/files/filefindclose)
