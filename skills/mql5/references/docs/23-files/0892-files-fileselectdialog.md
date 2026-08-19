# FileSelectDialog

Create a file or folder opening/creation dialog.

```
int  FileSelectDialog(
   string   caption,              // window header
   string   initial_dir,          // initial directory
   string   filter,               // extension filter
   uint     flags,                // combination of flags
   string&  filenames[],          // array with file names
   string   default_filename      // default file name
   );

```

Parameters

caption

[in]  Dialog window header.

initial_dir

[in]  Initial directory name relative to MQL5\Files, the contents of which is to be displayed in the dialog box. If the value is [NULL](/en/docs/basis/types/void), MQL5\Files is displayed in the dialog.

filter

[in]  Extension filter of the files to be displayed in the selection dialog window. Files of other formats are hidden.

flags

[in] [Combination of flags](/en/docs/constants/io_constants/fileflags) defining the dialog window mode. The flags are defined as follows:   

FSD_WRITE_FILE – file open dialog;  

FSD_SELECT_FOLDER – allow selection of folders only;  

FSD_ALLOW_MULTISELECT – allow selection of multiple files;  

FSD_FILE_MUST_EXIST – selected files should exist;  

FSD_COMMON_FOLDER – file is located in the common folder of all client terminals \Terminal\Common\Files.

filenames[]

[out]  Array of strings the names of selected files/folders are placed to.

default_filename

[in]  Default file/folder name. If specified, a name is automatically added to the open dialog and returned in the filenames[] array when testing.

Return Value

In case of a successful completion, the function returns the number of selected files whose names can be obtained in filenames[]. If a user closes the dialog without selecting a file, the function returns 0. In case of unsuccessful execution, a value less than 0 is returned. The error code can be obtained using [GetLastError()](/en/docs/check/getlasterror).

Note

For reasons of security, working with files is strictly controlled in MQL5 language. Files used in file operations by means of MQL5 language cannot be located outside the file sandbox (namely, outside the MQL5\Files directory).

The initial_dir name is searched in the client terminal's directory in MQL5\Files (or testing_agent_directory\MQL5\Files in case of testing). If FSD_COMMON_FOLDER is set among the flags, the search for the initial directory is performed in the common folder of all client terminals \Terminal\Common\Files.

The filter parameter indicates valid files and should be set in the "<description 1>|<extension 1>|<description 2>|<extension 2>..." format, for example, "Text files (*.txt)|*.txt|All files (*.*)|*.*". The first extension "Text files (*.txt)|*.txt" is selected as a default file type.

If filter=NULL, the mask of file selection in the dialog window is "All Files (*.*)|*.*|"

If the default_filename parameter is set, calling FileSelectDialog() returns 1, while the default_filename value itself is copied to the filenames[] array during the non-visualized testing.

The function cannot be used in custom indicators since calling FileSelectDialog() suspends the [thread of execution](/en/docs/runtime/running) for the whole time while waiting for the user's response. Since all indicators for each symbol are executed in a single thread, such suspension makes the operation of all charts on all timeframes for this symbol impossible.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the names of text files for downloading from the common folder of the client terminals
   string filenames[];
   if(FileSelectDialog("Select files to download", NULL, 
                       "Text files (*.txt)|*.txt|All files (*.*)|*.*", 
                       FSD_ALLOW_MULTISELECT|FSD_COMMON_FOLDER, filenames, "data.txt")>0)
     {
      //--- display the name of each selected file
      int total=ArraySize(filenames);
      for(int i=0; i<total; i++)
         Print(i, ": ", filenames[i]);
     }
   else
     {
     Print("Files not selected");
     }
//---
  }

```

See also

[FileOpen](/en/docs/files/fileopen), [FileIsExist](/en/docs/files/fileisexist), [FileDelete](/en/docs/files/filedelete), [FileMove](/en/docs/files/filemove), [FolderCreate](/en/docs/files/foldercreate), [FolderDelete](/en/docs/files/folderdelete), [FolderClean](/en/docs/files/folderclean), [Flags of opening files](/en/docs/constants/io_constants/fileflags)
