# DebugBreak

It is a program breakpoint in debugging.

```
void  DebugBreak();

```

Return Value

No return value.

Note

Execution of an MQL5 program is interrupted only if a program is started in a debugging mode. The function can be used for viewing values of variables and/or for further step-by-step execution.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- compile the file using F5
//--- in debugging mode, if i == j, stop at the DebugBreak() string  
   for(int i=0,j=20; i<20; i++,j--)
     {
      if(i==j)
         DebugBreak();
     }
  }

```
