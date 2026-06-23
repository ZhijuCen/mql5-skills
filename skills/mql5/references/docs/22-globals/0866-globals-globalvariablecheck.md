# GlobalVariableCheck

Checks the existence of a global variable with the specified name

```
bool  GlobalVariableCheck(
   string  name      // Global variable name
   );

```

Parameters

name

[in]  Global variable name.

Return Value

Returns true, if the global variable exists, otherwise returns false.

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableCheck"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the flag of the client terminal global variable named GV_NAME
   bool exist=GlobalVariableCheck(GV_NAME);
   PrintFormat("Terminal global variable named \"%s\" %s", GV_NAME, (exist ? "exists" : "does not exist"));
   
   /*
   result in the presence of a global variable:
   Terminal global variable named "TestGlobalVariableCheck" exists
   
   result in the absence of a global variable:
   Terminal global variable named "TestGlobalVariableCheck" does not exist
   */
  }

```

See also

[GlobalVariableTime()](/en/docs/globals/globalvariabletime)
