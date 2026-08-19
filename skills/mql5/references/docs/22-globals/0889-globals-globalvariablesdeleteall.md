# GlobalVariablesDeleteAll

Deletes global variables of the client terminal.

```
int  GlobalVariablesDeleteAll(
   string     prefix_name=NULL,     // All global variables with names beginning with the prefix
   datetime   limit_data=0          // All global variables that were changed before this date
   );

```

Parameters

prefix_name=NULL

[in] Name prefix global variables to remove. If you specify a prefix NULL or empty string, then all variables that meet the data criterion will be deleted.

limit_data=0

[in] Date to select global variables by the time of their last modification. The function removes global variables, which were changed before this date. If the parameter is zero, then all variables that meet the first criterion (prefix) are deleted.

Return Value

The number of deleted variables.

Note

If both options are equal to zero (prefix_name = NULL and limit_data = 0), then function deletes all global variables of the terminal. If both parameters are specified, then it deletes global variables corresponding to both parameters.

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#property script_show_inputs
 
#property description   "The script deletes global variables of the client terminal."
#property description   "Limit date: Variables before the specified date are deleted."
#property description   "If is zero, then variables that match the Name prefix criterion are deleted."
#property description   "Name prefix: Prefix of the variable name. If not specified, then variables are deleted based on the Limit date criterion."
#property description   "If all input parameters are zero, then all global variables are deleted."
#property description   "If both parameters are specified, then global variables corresponding to each of the specified parameters are deleted."
 
//--- input variables
input datetime InpLimitDate=  0;       // Limit date
input string   InpPrefix   =  NULL;    // Name prefix
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the total number of global variables of the client terminal,
//--- delete variables in accordance with the deletion criteria selected in the script settings and
//--- print the deletion result in the log
   int total=GlobalVariablesTotal();
   int deleted=GlobalVariablesDeleteAll(InpPrefix, InpLimitDate);
   PrintFormat("Of %d global variables, %d have been removed. %d remain", total, deleted, total-deleted);
   /*
  result:
   Of 21 global variables, 21 have been removed. 0 remain
   */
  }

```
