# GlobalVariablesTotal

Returns the total number of global variables of the client terminal.

```
int  GlobalVariablesTotal();

```

Return Value

Number of global variables.

Note

Global variables exist in the client terminal during 4 weeks since their last use, then they are automatically deleted. Call of a global variable is not only setting a new value, but also reading the value of the global variable.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get and log the total number of global variables of the client terminal
   int total=GlobalVariablesTotal();
   Print("Total number of global variables of the client terminal: ", total);
   /*
  result:
   Total number of global variables of the client terminal: 20
   */
  }

```
