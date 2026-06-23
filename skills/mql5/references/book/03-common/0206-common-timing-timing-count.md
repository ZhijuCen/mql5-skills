# Time interval counters

To detect a time interval up to a second, it is enough to take the difference between two datetime values obtained using TimeLocal. However, sometimes we need even higher accuracy. For this purpose, MQL5 allows you to get system millisecond (GetTickCount, GetTickCount64) or microsecond (GetMicrosecondCount) counters.

uint GetTickCount()

ulong GetTickCount64()

The functions return the number of milliseconds that have passed since the operating system was loaded. The timing accuracy is limited by the standard system timer (~10-15 milliseconds). For a more accurate measurement of intervals, use the GetMicrosecondCount function.

In case of the GetTickCount function, the return type uint predetermines the period of time after which the counter will overflow: approximately 49.7 days. In other words, the countdown will start again from 0 if the computer has not been turned off for such a long time.

In contrast, the GetTickCount64 function returns ulong values, and this counter will not overflow in the foreseeable future (584'942'417 years).

ulong GetMicrosecondCount()

The function returns the number of microseconds that have passed since the start of the MQL program.

Examples of using the counter functions and Sleep are summarized in the script TimeCount.mq5.

```
void OnStart()
{
   const uint startMs = GetTickCount();
   const ulong startMcs =  GetMicrosecondCount();
   
   // loop for 5 seconds
   while(PRTF(GetTickCount()) < startMs + 5000)
   {
      PRTF(GetMicrosecondCount());
      Sleep(1000);
   }
   
   PRTF(GetTickCount() - startMs);
   PRTF(GetMicrosecondCount() - startMcs);
}

```

Here's what the log output of the script might look like.

```
GetTickCount()=12912811 / ok
GetMicrosecondCount()=278 / ok
GetTickCount()=12913903 / ok
GetMicrosecondCount()=1089845 / ok
GetTickCount()=12914995 / ok
GetMicrosecondCount()=2182216 / ok
GetTickCount()=12916087 / ok
GetMicrosecondCount()=3273823 / ok
GetTickCount()=12917179 / ok
GetMicrosecondCount()=4365889 / ok
GetTickCount()=12918271 / ok
GetTickCount()-startMs=5460 / ok
GetMicrosecondCount()-startMcs=5458271 / ok

```
