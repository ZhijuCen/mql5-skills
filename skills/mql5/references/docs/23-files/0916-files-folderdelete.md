# FolderDelete

The function removes the specified directory. If the folder is not empty, then it can't be removed.

```
bool  FolderDelete(
   string  folder_name,       // String with the name of the folder to delete
   int     common_flag=0      // Scope
   );

```

Parameters

folder_name

[in] The name of the directory you want to delete. Contains the full path to the folder.

common_flag=0

[in]  [Flag](/en/docs/constants/io_constants/fileflags) determining the location of the directory. If common_flag=FILE_COMMON, then the directory is in the shared folder for all client terminals \Terminal\Common\Files. Otherwise, the directory is in a local folder (MQL5\Files or MQL5\Tester\Files in the case of testing).

Return Value

Returns true if successful, otherwise false.

Note

For security reasons, work with files is strictly controlled in the MQL5 language. Files with which file operations are conducted using MQL5 means, cannot be outside the file sandbox.

If the directory contains at least one file and/or subdirectory, then this directory can't be deleted, it must be cleared first. [FolderClean()](/en/docs/files/folderclean) is used to clear a folder of all its files or subfolders.

Example:

```
//+------------------------------------------------------------------+
//|                                            Demo_FolderDelete.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- Description
#property description "The script shows a sample use of FolderDelete()."
#property description "First two folders are created; one of them is empty, the second one contains a file."
#property description "When trying to delete a non-empty folder, an error is returned and a warning is shown."
 
//--- Show the dialog of input parameters when starting the script
#property script_show_inputs
//--- Input parameters
input string   firstFolder="empty";    // An empty folder
input string   secondFolder="nonempty";// The folder, in which one file will be created
string filename="delete_me.txt";       // The name of the file that will be created in folder secondFolder
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Write the file handle here
   int handle;
//--- Find out in what folder we are working
   string working_folder=TerminalInfoString(TERMINAL_DATA_PATH)+"\\MQL5\\Files";
//--- A debug message   
   PrintFormat("working_folder=%s",working_folder);
//--- Trying to create an empty folder relative to path MQL5\Files
   if(FolderCreate(firstFolder,0)) // 0 means that we are working in the local folder of the terminal
     {
      //--- Enter the full path to the created folder
      PrintFormat("Folder %s has been created",working_folder+"\\"+firstFolder);
      //--- Reset the error code
      ResetLastError();
     }
   else
      PrintFormat("Failed to create folder %s. Error code %d",working_folder+"\\"+firstFolder, GetLastError());
 
//--- Now create a non-empty folder using the FileOpen() function
   string filepath=secondFolder+"\\"+filename;  // Form path to file that we want to open to write in a nonexistent folder
   handle=FileOpen(filepath,FILE_WRITE|FILE_TXT); // Flag FILE_WRITE in this case is obligatory, see Help for FileOpen
   if(handle!=INVALID_HANDLE)
      PrintFormat("File %s has been opened for reading",working_folder+"\\"+filepath);
   else
      PrintFormat("Failed to create file %s in folder %s. Error code=",filename,secondFolder, GetLastError());
 
   Comment(StringFormat("Prepare to delete folders %s and %s", firstFolder, secondFolder));
//--- A small pause of 5 seconds to read a message in the chart
   Sleep(5000); // Sleep() cannot be used in indicators!
 
//--- Show a dialog and ask the user
   int choice=MessageBox(StringFormat("Do you want to delete folders %s and %s?", firstFolder, secondFolder),
                         "Deleting folders",
                         MB_YESNO|MB_ICONQUESTION); //  Two buttons - "Yes" and "No"
 
//--- Run an action depending on the selected variant
   if(choice==IDYES)
     {
      //--- Delete the comment form the chart
      Comment("");
      //--- Add a message into the "Experts" journal
      PrintFormat("Trying to delete folders %s and %s",firstFolder, secondFolder);
      ResetLastError();
      //--- Delete the empty folder
      if(FolderDelete(firstFolder))
         //--- The following message should appear since the folder is empty
         PrintFormat("Folder %s has been successfully deleted",firstFolder);
      else
         PrintFormat("Failed to delete folder %s. Error code=%d", firstFolder, GetLastError());
 
      ResetLastError();
      //--- Delete the folder that contains a file 
      if(FolderDelete(secondFolder))
         PrintFormat("Folder %s has been successfully deleted", secondFolder);
      else
         //--- The following message should appear since the folder contains a file
         PrintFormat("Failed to delete folder %s. Error code=%d", secondFolder, GetLastError());
     }
   else
      Print("Deletion canceled");
//---
  }

```

See also

[FileOpen()](/en/docs/files/fileopen), [FolderClean()](/en/docs/files/folderclean), [FileMove()](/en/docs/files/filemove)
