# Checking the MQL program status and reason for termination

We have already encountered the IsStopped function in different examples across the book. It must be called from time to time in cases where the MQL program performs lengthy calculations. This allows you to check if the user initiated the closing of the program (i.e. if they tried to remove it from the chart).

bool IsStopped() ≡ bool _StopFlag

The function returns true if the program was interrupted by the user (for example, by pressing the Delete button in the dialog opened by the Expert List command in the context menu).

The program is given 3 seconds to properly pause calculations, save intermediate results if necessary, and complete its work. If this does not happen, the program will be removed from the chart forcibly.

Instead of the IsStopped function, you can check the value of the built-in _StopFlag variable.

The test script EnvStop.mq5 emulates lengthy calculations in a loop: search for prime numbers. Conditions for exiting the while loop are written using the IsStopped function. Therefore, when the user deletes the script, the loop is interrupted in the usual way and the log displays the statistics of found prime numbers log (the script could also save the numbers to a file).

```
bool isPrime(int n)
{
   if(n < 1) return false;
   if(n <= 3) return true;
   if(n % 2 == 0) return false;
   const int p = (int)sqrt(n);
   int i = 3;
   for( ; i <= p; i += 2)
   {
      if(n % i == 0) return false;
   }
   
   return true;
}
   
void OnStart()
{
   int count = 0;
   int candidate = 1;
   
   while(!IsStopped()) // try to replace it with while(true)
   {
      // emulate long calculations
      if(isPrime(candidate))
      {
         Comment("Count:", ++count, ", Prime:", candidate);
      }
      ++candidate;
      Sleep(10);
   }
   Comment("");
   Print("Total found:", count);
}

```

If we replace the loop condition with true (infinite loop), the script will stop responding to the user's request to stop and will be unloaded from the chart forcibly. As a result, we will see the "Abnormal termination" error in the log, and the comment in the upper left corner of the window remains uncleaned. Thus, all instructions that in this example symbolize saving data and clearing busy resources (and this could be, for example, deleting your own graphic objects from the window) are ignored.

After a stop request has been sent to the program (and the value _StopFlag equals true), the reason for the termination can be found using the UninitializeReason function.

Unfortunately, this feature is only available for Expert Advisors and indicators.

int UninitializeReason() ≡ int _UninitReason

The function returns one of the predefined codes describing the reasons for deinitialization.

| Constant | Value | Description |
| --- | --- | --- |
| REASON_PROGRAM | 0 | ExpertRemove   function only available in Expert Advisors and scripts was called |
| REASON_REMOVE | 1 | Program removed from the chart |
| REASON_RECOMPILE | 2 | Program recompiled |
| REASON_CHARTCHANGE | 3 | Chart symbol or period changed |
| REASON_CHARTCLOSE | 4 | Chart closed |
| REASON_PARAMETERS | 5 | Program input parameters changed |
| REASON_ACCOUNT | 6 | Another account is connected or a reconnection to the trading server occurred |
| REASON_TEMPLATE | 7 | Another chart template applied |
| REASON_INITFAILED | 8 | OnInit  event handler returned an error flag |
| REASON_CLOSE | 9 | Terminal closed |

Instead of a function, you can access the built-in global variable _UninitReason.

The deinitialization reason code is also passed as a parameter to the [OnDeinit](/en/book/applications/runtime/runtime_oninit_ondeinit) event handler function.

Later, when studying [Program start and stop features](/en/book/applications/runtime/runtime_lifecycle), we will see an indicator (Indicators/MQL5Book/p5/LifeCycle.mq5) and an Expert Advisor (Experts/MQL5Book/p5/LifeCycle.mq5) that log the reasons for deinitialization and allow you to explore the behavior of programs depending on user actions.
