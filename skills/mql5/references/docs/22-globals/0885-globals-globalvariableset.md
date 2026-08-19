# GlobalVariableSet

Sets a new value for a global variable. If the variable does not exist, the system creates a new global variable.

```
datetime  GlobalVariableSet(
   string  name,      // Global variable name
   double  value      // Value to set
   );

```

Parameters

name

[in]  Global variable name.

value

[in]  The new numerical value.

Return Value

If successful, the function returns the last modification time, otherwise 0. For more details about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).

Note

A global variable name should not exceed 63 characters. Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableSet"
#define   GV_VALUE   1.23456
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the new GV_VALUE value to the global variable of the client terminal named GV_NAME
//--- if the variable does not exist yet, it will be created
   if(GlobalVariableSet(GV_NAME, GV_VALUE)==0)
     {
      Print("GlobalVariableSet() failed. Error ", GetLastError());
      return;
     }
//--- check the result and print it in the journal
   double value=0;
   if(GlobalVariableGet(GV_NAME, value))
     {
      PrintFormat("The global variable of the client terminal named \"%s\" is set to %.5f", GV_NAME, value);
     }
   /*
  result:
   The global variable of the client terminal named "TestGlobalVariableSet" is set to 1.23456
   */
  }

```
