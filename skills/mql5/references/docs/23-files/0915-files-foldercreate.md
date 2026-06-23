# FolderCreate

Creates a directory in the Files folder (depending on the common_flag value)

```
bool  FolderCreate(
   string  folder_name,       // line with the created folder name
   int     common_flag=0      // action area
   );

```

Parameters

folder_name

[in]  Name of the directory to be created. Contains the relative path to the folder.

common_flag=0

[in]  [Flag](/en/docs/constants/io_constants/fileflags) defining the directory location. If common_flag=FILE_COMMON, the directory is located in the common folder of all client terminals \Terminal\Common\Files. Otherwise, the directory is in the local folder (MQL5\Files or MQL5\Tester\Files when testing).

Return Value

Returns true if successful, otherwise false.

Note

For reasons of security, working with files is strictly controlled in MQL5 language. Files used in file operations by means of MQL5 language cannot be located outside the file sandbox.

Example:

```
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- description
#property description "The script shows FolderCreate() application sample."
#property description "The external parameter defines the directory for creating folders."
#property description "The folder structure is created after executing the script"
 
//--- display window of the input parameters during the script's launch
#property script_show_inputs
//--- the input parameter defines the folder, in which the script works
input bool     common_folder=false; // common folder for all terminals
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- folder to be created in MQL5\Files
   string root_folder="Folder_A";
   if(CreateFolder(root_folder,common_folder))
     {
      //--- create the Child_Folder_B1 sub-folder in it
      string folder_B1="Child_Folder_B1";
      string path=root_folder+"\\"+folder_B1;          // create the folder name considering the structure
      if(CreateFolder(path,common_folder))
        {
         //--- create 3 more sub-directories in this folder
         string folder_C11="Child_Folder_C11";
         string child_path=root_folder+"\\"+folder_C11;// create the folder name considering the structure
         CreateFolder(child_path,common_folder);
         //--- second sub-directory
         string folder_C12="Child_Folder_C12";
         child_path=root_folder+"\\"+folder_C12;
         CreateFolder(child_path,common_folder);
 
         //--- third sub-directory
         string folder_C13="Child_Folder_C13";
         child_path=root_folder+"\\"+folder_C13;
         CreateFolder(child_path,common_folder);
        }
     }
//---
  }
//+------------------------------------------------------------------+
//| Try creating a folder and display a message about that           |
//+------------------------------------------------------------------+
bool CreateFolder(string folder_path,bool common_flag)
  {
   int flag=common_flag?FILE_COMMON:0;
   string working_folder;
//--- define the full path depending on the common_flag parameter
   if(common_flag)
      working_folder=TerminalInfoString(TERMINAL_COMMONDATA_PATH)+"\\MQL5\\Files";
   else
      working_folder=TerminalInfoString(TERMINAL_DATA_PATH)+"\\MQL5\\Files";
//--- debugging message  
   PrintFormat("folder_path=%s",folder_path);
//--- attempt to create a folder relative to the MQL5\Files path
   if(FolderCreate(folder_path,flag))
     {
      //--- display the full path for the created folder
      PrintFormat("Created the folder %s",working_folder+"\\"+folder_path);
      //--- reset the error code
      ResetLastError();
      //--- successful execution
      return true;
     }
   else
      PrintFormat("Failed to create the folder %s. Error code %d",working_folder+folder_path,GetLastError());
//--- execution failed
   return false;
  }

```

See also

[FileOpen()](/en/docs/files/fileopen), [FolderClean()](/en/docs/files/folderclean), [FileCopy()](/en/docs/files/filecopy)
