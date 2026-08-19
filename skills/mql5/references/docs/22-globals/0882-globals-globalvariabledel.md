# GlobalVariableDel

Deletes a global variable from the client terminal.

```
bool  GlobalVariableDel(
   string  name      // Global variable name
   );

```

Parameters

name

[in]  Global variable name.

Return Value

If successful, the function returns true, otherwise it returns false. To obtain an information about the [error](/en/docs/constants/errorswarnings/errorcodes) it is necessary to call the function [GetLastError()](/en/docs/check/getlasterror).

Note

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableDel"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- check for the presence of the client terminal global variable named GV_NAME
   if(!GlobalVariableCheck(GV_NAME))
     {
      PrintFormat("Terminal global variable named \"%s\" does not exist", GV_NAME);
      return;
     }
     
//--- delete the client terminal global variable named GV_NAME
   if(!GlobalVariableDel(GV_NAME))
     {
      Print("GlobalVariableDel() failed. Error ",GetLastError());
      return;
     }
     
//--- check the success of deleting the client terminal global variable named GV_NAME
   if(!GlobalVariableCheck(GV_NAME))
     {
      PrintFormat("The terminal global variable named \"%s\" was successfully deleted", GV_NAME);
     }
     
   /*
   result in case of the absence of the client terminal global variable with the name GV_NAME
   Terminal global variable named "TestGlobalVariableDel" does not exist
   
   result in case of the presence of the client terminal global variable with the name GV_NAME
   The terminal global variable named "TestGlobalVariableDel" was successfully deleted
   */
  }

```
