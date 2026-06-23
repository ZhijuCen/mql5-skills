# Sleep

The function suspends execution of the current Expert Advisor or script within a specified interval.

```
void  Sleep(
   int  milliseconds      // interval
   );

```

Parameters

milliseconds

[in]  Delay interval in milliseconds.

Return Value

No return value.

Note

The Sleep() function can't be called for custom indicators, because indicators are executed in the interface thread and must not slow down it. The function has the built-in check of EA halt flag every 0.1 seconds.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- display a countdown from 10 to 1 in the comments on the chart
   for(int i=10; i>0 && !IsStopped(); i--)
     {
      Comment(StringFormat("Wait %u seconds",i));
      Sleep(1000);
     }
//--- write a text in the "arriving" comment that describes the purpose of the script
   string text="This was a test showing how the Sleep() function works";
   string mess="";
   for(int i=0; i<(int)text.Length(); i++)
     {
      mess+=ShortToString(text.GetChar(i));
      Sleep(100);
      Comment(mess);
     }
//--- say goodbye...
   Sleep(1000);
   for(int i=0; i<6; i++)
     {
      mess=(i % 2 == 0 ? "" : "  Bye!");
      Comment(mess);
      Sleep(300);
     }
//--- delete the text on the chart
   Comment("");
  }

```
