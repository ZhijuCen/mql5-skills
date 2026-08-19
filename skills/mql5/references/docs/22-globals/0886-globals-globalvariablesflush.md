# GlobalVariablesFlush

Forcibly saves contents of all global variables to a disk.

```
void  GlobalVariablesFlush();

```

Return Value

No return value.

Note

The terminal writes all the global variables when the work is over, but data can be lost at a sudden computer operation failure. This function allows independently controlling the process of saving global variables in case of contingency.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableFlush"
#define   GV_VALUE   1.23456
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create a global variable for the client terminal
   if(!GlobalVariableSet(GV_NAME, GV_VALUE))
     {
      Print("GlobalVariableSet() failed. Error ", GetLastError());
      return;
     }
   //--- work in the program with the created global variables of the client terminal
   //--- ...
   //--- at the required moment of the program operation, depending on the logic of the independent
   //--- process of saving global variables in case of emergency,
   //--- forcefully write the contents of all global variables to the disk
   GlobalVariablesFlush();
  }

```
