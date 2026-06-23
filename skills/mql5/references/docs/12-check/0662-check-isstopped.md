# IsStopped

Checks the forced shutdown of an mql5 program.

```
bool  IsStopped();

```

Return Value

Returns true, if the [_StopFlag](/en/docs/predefined/_stopflag) system variable contains a value other than 0. A nonzero value is written into _StopFlag, if a mql5 program has been commanded to complete its operation. In this case, you must immediately terminate the program, otherwise the program will be completed forcibly from the outside after 3 seconds.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- in an endless loop with a stop check
   while(!IsStopped())
     {
      //--- display the local PC time on the chart
      Comment("Time Local: ", TimeToString(TimeLocal(), TIME_DATE|TIME_MINUTES|TIME_SECONDS));
      Sleep(16);
     }
   Print("The StopFlag is set. The program will be stopped.");
 
//--- clean up
   Comment("");
  }

```
