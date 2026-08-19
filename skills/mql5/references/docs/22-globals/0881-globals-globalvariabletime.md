# GlobalVariableTime

Returns the time when the global variable was last accessed.

```
datetime  GlobalVariableTime(
   string  name      // name
   );

```

Parameters

name

[in]  Name of the global variable.

Return Value

The function returns time of last accessing the specified global variable. Addressing a variable for its value, for example using the [GlobalVariableGet()](/en/docs/globals/globalvariableget) and [GlobalVariableCheck()](/en/docs/globals/globalvariablecheck) functions, also modifies the time of last access. In order to obtain [error](/en/docs/constants/errorswarnings/errorcodes) details, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Global variables exist in the client terminal during 4 weeks since they were called last. After that they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableTime"
#define   GV_TOTAL   5
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- delete the global variables of the client terminal with the GV_NAME prefix created for the test
   GlobalVariablesDeleteAll(GV_NAME);
   
//--- create client terminal global variables in the amount of GV_TOTAL
//--- with the GV_NAME prefix and the 5-second pause between the creation of each one
   for(int i=0; i<GV_TOTAL; i++)
     {
      string name=GV_NAME+"_"+(string)i;
      ulong value=GetMicrosecondCount();
      ResetLastError();
      datetime time=GlobalVariableSet(name, (double)value);
      if(time==0)
        {
         Print("GlobalVariableSet() failed. Error ", GetLastError());
         continue;
        }
      Sleep(5000);
      PrintFormat("GlobalVariableSet(%s, %.0f). Create time: %s", name, value, TimeToString(time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
     }
     
//--- wait a couple of seconds and print in the journal the time of creation of terminal global variables with the GV_NAME prefix
   Sleep(2000);
   Print(""); 
   GlobalVariableTimePrint("Creation time");
   
//--- wait a couple more seconds and print in the journal the time of the last access to the terminal global variables with the GV_NAME prefix
//--- we can see that the time of the last access to each variable is equal to the time of its creation
   Sleep(2000);
   Print(""); 
   GlobalVariableTimePrint("Last access time");
 
//--- now request the value of each of the created variables
   Print(""); 
   int total=GlobalVariablesTotal();
   for(int i=0; i<total; i++)
     {
      string name=GlobalVariableName(i);
      if(GetLastError()!=0)
        {
         PrintFormat("Error %d occurred while getting global variable name at index %d", GetLastError(), i);
         ResetLastError();
         continue;
        }
      if(StringFind(name, GV_NAME)==WRONG_VALUE)
         continue;
         
      double value=GlobalVariableGet(name);
      if(GetLastError()!=0)
        {
         PrintFormat("Error %d occurred while getting global variable value at index %d", GetLastError(), i);
         ResetLastError();
         continue;
        }
      PrintFormat("Value of global variable named \"%s\": %.0f", name, value);
     }
   
//--- wait a couple more seconds and print in the journal the time of the last access to the terminal global variables with the GV_NAME prefix
//--- we can see that the time of the last access to each variable is equal to the time of requesting its value
   Sleep(2000);
   Print(""); 
   GlobalVariableTimePrint("After getting value, the last access time");
 
//--- delete all the global variables of the client terminal with the GV_NAME prefix created for the test
   GlobalVariablesDeleteAll(GV_NAME);
   /*
   result:
   GlobalVariableSet(TestGlobalVariableTime_0, 3987). Create time: 2024.11.28 22:00:39
   GlobalVariableSet(TestGlobalVariableTime_1, 5012302). Create time: 2024.11.28 22:00:44
   GlobalVariableSet(TestGlobalVariableTime_2, 10034365). Create time: 2024.11.28 22:00:49
   GlobalVariableSet(TestGlobalVariableTime_3, 15045008). Create time: 2024.11.28 22:00:54
   GlobalVariableSet(TestGlobalVariableTime_4, 20060340). Create time: 2024.11.28 22:00:59
   
   Creation time of global variable named "TestGlobalVariableTime_0": 2024.11.28 22:00:39
   Creation time of global variable named "TestGlobalVariableTime_1": 2024.11.28 22:00:44
   Creation time of global variable named "TestGlobalVariableTime_2": 2024.11.28 22:00:49
   Creation time of global variable named "TestGlobalVariableTime_3": 2024.11.28 22:00:54
   Creation time of global variable named "TestGlobalVariableTime_4": 2024.11.28 22:00:59
   
   Last access time of global variable named "TestGlobalVariableTime_0": 2024.11.28 22:00:39
   Last access time of global variable named "TestGlobalVariableTime_1": 2024.11.28 22:00:44
   Last access time of global variable named "TestGlobalVariableTime_2": 2024.11.28 22:00:49
   Last access time of global variable named "TestGlobalVariableTime_3": 2024.11.28 22:00:54
   Last access time of global variable named "TestGlobalVariableTime_4": 2024.11.28 22:00:59
   
   Value of global variable named "TestGlobalVariableTime_0": 3987
   Value of global variable named "TestGlobalVariableTime_1": 5012302
   Value of global variable named "TestGlobalVariableTime_2": 10034365
   Value of global variable named "TestGlobalVariableTime_3": 15045008
   Value of global variable named "TestGlobalVariableTime_4": 20060340
   
   After getting value, the last access time of global variable named "TestGlobalVariableTime_0": 2024.11.28 22:01:08
   After getting value, the last access time of global variable named "TestGlobalVariableTime_1": 2024.11.28 22:01:08
   After getting value, the last access time of global variable named "TestGlobalVariableTime_2": 2024.11.28 22:01:08
   After getting value, the last access time of global variable named "TestGlobalVariableTime_3": 2024.11.28 22:01:08
   After getting value, the last access time of global variable named "TestGlobalVariableTime_4": 2024.11.28 22:01:08
   */
  }
//+------------------------------------------------------------------+
//| Prints to journal the time when the client terminal's            |
//| global variable was last accessed                                |
//+------------------------------------------------------------------+
void GlobalVariableTimePrint(const string reason)
  {
   int total=GlobalVariablesTotal();
   for(int i=0;i<total;i++)
     {
      string name=GlobalVariableName(i);
      if(GetLastError()!=0)
        {
         PrintFormat("Error %d occurred while getting global variable name at index %d", GetLastError(), i);
         ResetLastError();
         continue;
        }
      datetime time=GlobalVariableTime(name);
      if(GetLastError()!=0)
        {
         PrintFormat("Error %d occurred while getting global variable time at index %d", GetLastError(), i);
         ResetLastError();
         continue;
        }
      PrintFormat("%s of global variable named \"%s\": %s", reason, name, TimeToString(time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
     }
  }

```

See also

[GlobalVariableCheck()](/en/docs/globals/globalvariablecheck)
