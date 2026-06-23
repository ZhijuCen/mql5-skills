# GetTickCount64

The GetTickCount64() function returns the number of milliseconds that have elapsed since the system was launched.

```
ulong  GetTickCount64();

```

Return Value

A ulong type value.

Note

The counter is limited to the accuracy of the system timer, which usually returns a result with the 10-16 millisecond precision. Unlike [GetTickCount](/en/docs/common/gettickcount), which is of [uint](/en/docs/basis/types/integer/integertypes) type and the contents of which overflow every 49.7 days in the case of continued computer operation, GetTickCount64() can be used for the unlimited computer operation time and is not subject to overflow.

Example:

```
#define MAX_SIZE 40
 
//+------------------------------------------------------------------+
//| Script for measuring the time of calculating 40 Fibo numbers     |
//+------------------------------------------------------------------+
void OnStart()
  {
   long fib_array[MAX_SIZE];
 
//--- store the initial value
   ulong start=GetTickCount64();
//--- a loop, in which we calculate a given number of numbers from the Fibo series
   for(int i=0;i<MAX_SIZE;i++) 
      fib_array[i]=TestFibo(i);
//--- get the spent time in milliseconds
   ulong time=GetTickCount64()-start;
 
//--- display the error message in the Experts journal
   ArrayPrint(fib_array);
   PrintFormat("Calculating the first %d Fibonacci numbers took %I64u ms",MAX_SIZE,time);
  }
//+------------------------------------------------------------------+
//| Function for obtaining a Fibo number by its serial number        |
//+------------------------------------------------------------------+
long TestFibo(long n)
  {
//--- first member of the Fibo series
   if(n<2)
      return(1);
//--- all subsequent members are calculated using this equation
   return(TestFibo(n-2)+TestFibo(n-1));
  }

```

See also

[Date and Time](/en/docs/dateandtime), [EventSetMillisecondTimer](/en/docs/eventfunctions/eventsetmillisecondtimer), [GetTickCount](/en/docs/common/gettickcount), [GetMicrosecondCount](/en/docs/common/getmicrosecondcount)
