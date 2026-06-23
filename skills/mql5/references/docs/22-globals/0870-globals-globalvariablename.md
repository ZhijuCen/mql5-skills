# GlobalVariableName

Returns the name of a global variable by its ordinal number.

```
string  GlobalVariableName(
   int  index      // Global variable number in the list of global variables
   );

```

Parameters

index

[in]  Sequence number in the list of global variables. It should be greater than or equal to 0 and less than [GlobalVariablesTotal()](/en/docs/globals/globalvariablestotal).

Return Value

Global variable name by its ordinal number in the list of global variables. For more details about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).

Note

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableSet"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- first, let's create global variables
   for(int i=0; i<21; i++)
      GlobalVariableSet(GV_NAME+string(i),i);
//--- get the number of global variables of the client terminal and display their names in a loop
   int total=GlobalVariablesTotal();
   for(int i=total-1; i>=0; i--)
     {
      string name=GlobalVariableName(i);
      if(GetLastError()!=0)
        {
         PrintFormat("Error %d occurred while getting global variable name at index %d", GetLastError(), i);
         ResetLastError();
         continue;
        }
      PrintFormat("GlobalVariableName(%02d) = \"%s\"", i, name);
     }
//--- clean up
   GlobalVariablesDeleteAll(GV_NAME);
   /*
  result:
   GlobalVariableName(20) = "TestGlobalVariableSet9"
   GlobalVariableName(19) = "TestGlobalVariableSet8"
   GlobalVariableName(18) = "TestGlobalVariableSet7"
   GlobalVariableName(17) = "TestGlobalVariableSet6"
   GlobalVariableName(16) = "TestGlobalVariableSet5"
   GlobalVariableName(15) = "TestGlobalVariableSet4"
   GlobalVariableName(14) = "TestGlobalVariableSet3"
   GlobalVariableName(13) = "TestGlobalVariableSet20"
   GlobalVariableName(12) = "TestGlobalVariableSet2"
   GlobalVariableName(11) = "TestGlobalVariableSet19"
   GlobalVariableName(10) = "TestGlobalVariableSet18"
   GlobalVariableName(09) = "TestGlobalVariableSet17"
   GlobalVariableName(08) = "TestGlobalVariableSet16"
   GlobalVariableName(07) = "TestGlobalVariableSet15"
   GlobalVariableName(06) = "TestGlobalVariableSet14"
   GlobalVariableName(05) = "TestGlobalVariableSet13"
   GlobalVariableName(04) = "TestGlobalVariableSet12"
   GlobalVariableName(03) = "TestGlobalVariableSet11"
   GlobalVariableName(02) = "TestGlobalVariableSet10"
   GlobalVariableName(01) = "TestGlobalVariableSet1"
   GlobalVariableName(00) = "TestGlobalVariableSet0"
   */
  }

```
