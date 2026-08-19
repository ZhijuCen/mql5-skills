# TimeGMTOffset

Returns the current difference between GMT time and the local computer time in seconds, taking into account switch to winter or summer time. Depends on the time settings of your computer.

```
int  TimeGMTOffset();

```

Return Value

The value of int type, representing the current difference between [GMT time](/en/docs/dateandtime/timegmt) and the local time of the computer [TimeLocal](/en/docs/dateandtime/timelocal) in seconds.

```
TimeGMTOffset() =  TimeGMT() - TimeLocal()

```

Example:

```
void OnStart()
  {
//--- get local time, GMT and the difference between GMT and local computer time in seconds 
   datetime time_local=TimeLocal();
   datetime time_gmt  =TimeGMT();
   int      offset    =TimeGMTOffset();
   
//--- show the obtained time and offset values in the log
   PrintFormat("Local Time: %s, GMT Time: %s, Seconds Offset: %+d", (string)time_local, (string)time_gmt, offset);
   /*
   result:
   Local Time: 2024.04.18 19:35:52, GMT Time: 2024.04.18 12:35:52, Seconds Offset: -25200
   */
  }

```
