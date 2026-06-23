# GlobalVariableTemp

The function attempts to create a temporary global variable. If the variable doesn't exist, the system creates a new temporary global variable.

```
bool  GlobalVariableTemp(
   string  name      // Global variable name
   );

```

Parameters

name

[in]  The name of a temporary global variable.

Return Value

If successful, the function returns true, otherwise - false. To get details about the [error](/en/docs/constants/errorswarnings/errorcodes), you should call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Temporary global variables exist only while the client terminal is running; after the terminal shutdown they are automatically deleted. Note that during the execution of [GlobalVariablesFlush()](/en/docs/globals/globalvariablesflush) temporary global variables are not written to a disk.

After a temporary global variable has been created, it can be accessed and modified the same as [global variable of the client terminal](/en/docs/globals).

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableTemp"
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   double value=0;   // we will receive the values of the global variable here
   
//--- if there is no temporary global variable of the client terminal yet, then:
//--- 1. either the program has not yet been launched,
//--- 2. or there was a reboot of the terminal with the program running
   if(!GlobalVariableCheck(GV_NAME))
     {
      //--- create a new temporary global variable for the client terminal
      if(!GlobalVariableTemp(GV_NAME))
        {
         Print("GlobalVariableTemp() failed. Error ", GetLastError());
         return;
        }
      //--- set the current date and time in the global variable
      if(!GlobalVariableSet(GV_NAME,(double)TimeCurrent()))
        {
         Print("GlobalVariableSet() failed. Error ", GetLastError());
         return;
        }
 
      //--- get the value of the temporary global variable and display in the journal the time of the first program launch or terminal restart
      if(!GlobalVariableGet(GV_NAME,value))
        {
         Print("GlobalVariableGet() failed. Error ", GetLastError());
         return;
        }
      Print("First start or starting the program after rebooting the terminal at ", TimeToString((datetime)value,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
     }
   
//--- if the temporary global variable of the client terminal has already been created, then this is a program restart
   else
     {
      //--- set the current date and time in the global variable
      if(!GlobalVariableSet(GV_NAME,(double)TimeCurrent()))
        {
         Print("GlobalVariableSet() failed. Error ", GetLastError());
         return;
        }
 
      //--- get the value of the temporary global variable and print the program restart time in the journal
      if(!GlobalVariableGet(GV_NAME,value))
        {
         Print("GlobalVariableGet() failed. Error ", GetLastError());
         return;
        }
      Print("Restarting the program at ", TimeToString((datetime)value, TIME_DATE|TIME_MINUTES|TIME_SECONDS));
     }
 
   /*
  result during the first launch, or after restarting the terminal:
   First start or starting the program after rebooting the terminal at 2024.11.29 15:03:18
   
  the result of several consecutive program restarts:
   Restarting the program at 2024.11.29 15:03:25
   Restarting the program at 2024.11.29 15:03:33
   Restarting the program at 2024.11.29 15:03:45
   */
  }

```
