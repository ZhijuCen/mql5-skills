# GlobalVariableGet

Returns the value of an existing global variable of the client terminal. There are 2 variants of the function.

1. Immediately returns the value of the global variable.

```
double  GlobalVariableGet(
   string  name      // Global variable name
   );

```

2. Returns true or false depending on the success of the function run.  If successful, the global variable of the client terminal is placed in a variable passed by reference in the second parameter.

```
bool  GlobalVariableGet(
   string  name,              // Global variable name
   double& double_var         // This variable will contain the value of the global variable
   );

```

Parameters

name

[in]  Global variable name.

double_var

[out]  Target variable of the double type, which accepts the value stored in a the global variable of the client terminal.

Return Value

The value of the existing global variable or 0 in case of an [error](/en/docs/constants/errorswarnings/errorcodes). For more details about the error, call [GetLastError()](/en/docs/check/getlasterror).

Note

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   GV_NAME    "TestGlobalVariableGet"
#define   GV_VALUE   1.23
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the value to the global variable of the client terminal named GV_NAME
   if(!GlobalVariableSetValue(GV_NAME, GV_VALUE))
      return;
     
//--- get the real value of the client terminal global variable with the name GV_NAME
//--- since when using the first form of calling GlobalVariableGet, zero is an error signal,
//--- it is necessary to analyze the last error code while reading the result
   double dvalue=GlobalVariableGet(GV_NAME);
   if(dvalue==0 && GetLastError()!=0)
     {
      Print("GlobalVariableGet() failed. Error ", GetLastError());
      return;
     }
//--- show the obtained result
   PrintFormat("The first form of the GlobalVariableGet() function call returned the value %.2f", dvalue);
   
//--- set the zero value to the global variable of the client terminal named GV_NAME
   if(!GlobalVariableSetValue(GV_NAME, 0))
      return;
     
//--- using the first form of the call we get the Boolean value of the client terminal global variable with the name GV_NAME
   bool bvalue=GlobalVariableGet(GV_NAME);
   if(!bvalue && GetLastError()!=0)
     {
      Print("GlobalVariableGet() failed. Error ", GetLastError());
      return;
     }
//--- show the obtained result
   PrintFormat("The first form of the GlobalVariableGet() function call returned the value %.2f with type bool as %s", bvalue, (string)bvalue);
     
//--- set the non-zero value to the global variable of the client terminal named GV_NAME
   if(!GlobalVariableSetValue(GV_NAME, GV_VALUE*100.0))
      return;
   
//--- read the Boolean value of the client terminal global variable named GV_NAME again
   bvalue=GlobalVariableGet(GV_NAME);
   if(!bvalue && GetLastError()!=0)
     {
      Print("GlobalVariableGet() failed. Error ", GetLastError());
      return;
     }
//--- show the obtained result
   PrintFormat("The first form of the GlobalVariableGet() function call returned the value %.2f with type bool as %s", bvalue, (string)bvalue);
     
//--- get the real value of the client terminal global variable with the name GV_NAME using the second form of the GlobalVariableGet call
   if(!GlobalVariableGet(GV_NAME, dvalue))
     {
      Print("GlobalVariableGet() failed. Error ", GetLastError());
      return;
     }
//--- convert the resulting real value into an integer of long type and show the result
   long lvalue=(long)dvalue;
   PrintFormat("The second form of the GlobalVariableGet() function call returned the value %.2f with type long as %I64d", dvalue, lvalue);
   
//--- delete the client terminal global variable named GV_NAME after use
   if(!GlobalVariableDel(GV_NAME))
     {
      Print("GlobalVariableDel() failed. Error ",GetLastError());
     }
   
   /*
  result:
   The first form of the GlobalVariableGet() function call returned the value 1.23
   The first form of the GlobalVariableGet() function call returned the value 0.00 with type bool as false
   The first form of the GlobalVariableGet() function call returned the value 1.00 with type bool as true
   The second form of the GlobalVariableGet() function call returned the value 123.00 with type long as 123
   */
  }
//+------------------------------------------------------------------+
//| Set the value to the terminal global variable;                   |
//| If there is no variable, create it                               |
//+------------------------------------------------------------------+
bool GlobalVariableSetValue(const string gv_name, const double value)
  {
   if(GlobalVariableSet(gv_name, value)==0)
     {
      Print("GlobalVariableSet() failed. Error ",GetLastError());
      return(false);
     }
   return(true);
  }

```
