# Tracking event changes by country or currency

As mentioned in the section on [basic concepts of the calendar](/en/book/advanced/calendar/calendar_overview), the platform registers all event changes by some internal means. Each state is characterized by a change identifier (change_id). Among the MQL5 functions, there are two that allow you to find this identifier (at an arbitrary point in time) and then request calendar entries changed later. One of these functions is CalendarValueLast, which will be discussed in this section. The second one, CalendarValueLastByEvent, will be discussed in the next section.

int CalendarValueLast(ulong &change_id, MqlCalendarValue &values[],  

   const string country = NULL, const string currency = NULL)

The CalendarValueLast function is designed for two purposes: getting the last known calendar change identifier change_id and filling the values array with modified records since the previous modification given by the passed ID in the same change_id. In other words, the change_id parameter works as both input and output. That is why it is a reference and requires a variable to be specified.

If we input change_id equal to 0 into the function, then the function will fill the variable with the current identifier but will not fill the array.

Optionally, using parameters country and currency, you can set filtering records by country and currency.

The function returns the number of copied calendar items. Since the array is not populated in the first operation mode (change_id = 0), returning 0 is not an error. We can also get 0 if the calendar has not been modified since the specified change. Therefore, to check for an error, you should analyze _LastError.

So the usual way to use the function is to loop through the calendar for changes.

```
ulong change = 0;
MqlCalendarValue values[];
while(!IsStopped())
{
 // pass the last identifier known to us and get a new one if it appeared
   if(CalendarValueLast(change, values))
   {
 // analysis of added and changed records
      ArrayPrint(values);
      ... 
   }
   Sleep(1000);
}

```

This can be done in a loop, on a timer, or on other events.

Identifiers are constantly increasing, but they can go out of order, that is, jump over several values.

It is important to note that each calendar entry is always available in only one last state: the history of changes is not provided in MQL5. As a rule, this is not a problem, since the life cycle of each news is standard: adding to the database in advance for a sufficiently long time and supplementing with relevant data at the time of the event. However, in practice, various deviations can occur: editing the forecast, transferring time, or revising the values. It is impossible to find out exactly what time and what was changed in the record through the MQL5 API from the calendar history. Therefore, those trading systems that make decisions based on the momentary situation will require independent saving of the history of changes and its integration into an Expert Advisor for running in the tester.

Using the CalendarValueLast function, we can create a useful service, CalendarChangeSaver.mq5, which will check the calendar for changes at the specified intervals and, if any, save the change identifiers to the file along with the current server time. This will allow further use of the file information for more realistic testing of Expert Advisors on the history of the calendar. Of course, this will require organizing the export/import of the entire calendar database, which we will deal with over time.

Let's provide input variables for specifying the file name and the period between polls (in milliseconds).

```
input string Filename = "calendar.chn";
input int PeriodMsc = 1000;

```

At the beginning of the OnStart handler, we open the binary file for writing, or rather for appending (if it already exists). The format of an existing file is not checked here and thus you should add protection when embedding in a real application.

```
void OnStart()
{
   ulong change = 0, last = 0;
   int count = 0;
   int handle = FileOpen(Filename,
      FILE_WRITE | FILE_READ | FILE_SHARE_WRITE | FILE_SHARE_READ | FILE_BIN);
   if(handle == INVALID_HANDLE)
   {
      PrintFormat("Can't open file '%s' for writing", Filename);
      return;
   }
   
   const ulong p = FileSize(handle);
   if(p > 0)
   {
      PrintFormat("Resuming file %lld bytes", p);
      FileSeek(handle, 0, SEEK_END);
   }
   
   Print("Requesting start ID...");
   ...

```

Here we should make a small digression.

Each time the calendar is changed, at least a pair of integer 8-byte numbers must be written to the file: the current time (datetime) and news ID (ulong), but there can be more than one record changed at the same time. Therefore, in addition to the date, the number of changed records is packed into the first number. This takes into account that dates fit in 0x7FFFFFFFF and therefore the upper 3 bytes are left unused. It is in the two most significant bytes (at a left offset of 48 bits) that the number of identifiers that the service will write after the corresponding timestamp is placed. The PACK_DATETIME_COUNTER macro creates an "extended" date, and the other two, DATETIME and COUNTER, we will need later when the archive of changes is read (by another program).

```
#define PACK_DATETIME_COUNTER(D,C) (D | (((ulong)(C)) << 48))
#define DATETIME(A) ((datetime)((A) & 0x7FFFFFFFF))
#define COUNTER(A)  ((ushort)((A) >> 48)) 

```

Now let's go back to the main service code. In a loop that is activated every PeriodMsc milliseconds, we request changes using CalendarValueLast. If there are changes, we write the current server time and the array of received identifiers to a file.

```
   while(!IsStopped())
   {
      if(!TerminalInfoInteger(TERMINAL_CONNECTED))
      {
         Print("Waiting for connection...");
         Sleep(PeriodMsc);
         continue;
      }
      
      MqlCalendarValue values[];
      const int n = CalendarValueLast(change, values);
      if(n > 0)
      {
         string records = "[" + Description(values[0]);
         for(int i = 1; i < n; ++i)
         {
            records += "," + Description(values[i]);
         }
         records += "]";
         Print("New change ID: ", change, " ",
            TimeToString(TimeTradeServer(), TIME_DATE | TIME_SECONDS), "\n", records);
         FileWriteLong(handle, PACK_DATETIME_COUNTER(TimeTradeServer(), n));
         for(int i = 0; i < n; ++i)
         {
            FileWriteLong(handle, values[i].id);
         }
         FileFlush(handle);
         ++count;
      }
      else if(_LastError == 0)
      {
         if(!last && change)
         {
            Print("Start change ID obtained: ", change);
         }
      }
      
      last = change;
      Sleep(PeriodMsc);
   }
   PrintFormat("%d records added", count);
   FileClose(handle);
}

```

For a convenient presentation of information about each news event, we have written a helper function Description.

```
string Description(const MqlCalendarValue &value)
{
   MqlCalendarEvent event;
   MqlCalendarCountry country;
   CalendarEventById(value.event_id, event);
   CalendarCountryById(event.country_id, country);
   return StringFormat("%lld (%s/%s @ %s)",
      value.id, country.code, event.name, TimeToString(value.time));
}

```

Thus, the log will display not only the identifier but also the country code, title, and scheduled time of the news.

It is assumed that the service should work for quite a long time in order to collect information for a period sufficient for testing (days, weeks, months). Unfortunately, just like with the order book, the platform does not provide a ready-made history of the order book or calendar edits, so their collection is left entirely to the developer of MQL programs.

Let's see the service in action. In the next fragment of the log (for the time period of 2022.06.28, 15:30 - 16:00), some news events relate to the distant future (they contain the values of the prev_value field, which is also the actual_value field of the current event of the same name). However, something else is more important: the actual time of a news release can differ significantly, sometimes by several minutes, from the planned one.

```
Requesting start ID...
Start change ID obtained: 86358784
New change ID: 86359040 2022.06.28 15:30:42
[155955 (US/Wholesale Inventories m/m @ 2022.06.28 15:30)]
New change ID: 86359296 2022.06.28 15:30:45
[155956 (US/Wholesale Inventories m/m @ 2022.07.08 17:00)]
New change ID: 86359552 2022.06.28 15:30:48
[156117 (US/Goods Trade Balance @ 2022.06.28 15:30)]
New change ID: 86359808 2022.06.28 15:30:51
[156118 (US/Goods Trade Balance @ 2022.07.27 15:30)]
New change ID: 86360064 2022.06.28 15:30:54
[156231 (US/Retail Inventories m/m @ 2022.06.28 15:30)]
New change ID: 86360320 2022.06.28 15:30:57
[156232 (US/Retail Inventories m/m @ 2022.07.15 17:00)]
New change ID: 86360576 2022.06.28 15:31:00
[156255 (US/Retail Inventories excl. Autos m/m @ 2022.06.28 15:30)]
New change ID: 86360832 2022.06.28 15:31:03
[156256 (US/Retail Inventories excl. Autos m/m @ 2022.07.15 17:00)]
New change ID: 86361088 2022.06.28 15:31:07
[155956 (US/Wholesale Inventories m/m @ 2022.07.08 17:00)]
New change ID: 86361344 2022.06.28 15:31:10
[156118 (US/Goods Trade Balance @ 2022.07.27 15:30)]
New change ID: 86361600 2022.06.28 15:31:13
[156232 (US/Retail Inventories m/m @ 2022.07.15 17:00)]
New change ID: 86362368 2022.06.28 15:36:47
[158534 (US/Challenger Job Cuts y/y @ 2022.07.07 14:30)]
New change ID: 86362624 2022.06.28 15:51:23
...
New change ID: 86364160 2022.06.28 16:01:39
[154531 (US/HPI m/m @ 2022.06.28 16:00)]
New change ID: 86364416 2022.06.28 16:01:42
[154532 (US/HPI m/m @ 2022.07.26 16:00)]
New change ID: 86364672 2022.06.28 16:01:46
[154543 (US/HPI y/y @ 2022.06.28 16:00)]
New change ID: 86364928 2022.06.28 16:01:49
[154544 (US/HPI y/y @ 2022.07.26 16:00)]
New change ID: 86365184 2022.06.28 16:01:54
[154561 (US/HPI @ 2022.06.28 16:00)]
New change ID: 86365440 2022.06.28 16:01:58
[154571 (US/HPI @ 2022.07.26 16:00)]
New change ID: 86365696 2022.06.28 16:02:01
[154532 (US/HPI m/m @ 2022.07.26 16:00)]
New change ID: 86365952 2022.06.28 16:02:05
[154544 (US/HPI y/y @ 2022.07.26 16:00)]
New change ID: 86366208 2022.06.28 16:02:09
[154571 (US/HPI @ 2022.07.26 16:00)]

```

Of course, this is important not for all classes of trading strategies, but only for those that trade quickly in the market. For them, the created archive of calendar edits can provide more accurate testing of news Expert Advisors. We will discuss how you can "connect" the calendar to the tester in the future, but for now, we will show how to read the received file.

We will use the script CalendarChangeReader.mq5 to demonstrate the discussed functionality. In practice, the given source code should be placed in the Expert Advisor.

The input variables allow you to set the name of the file to be read and the start date of the scan. If the service continues to work (write the file), you need to copy the file under a different name or to another folder (in the example script, the file is renamed). If the Start parameter is blank, the reading of news changes will start from the beginning of the current day.

```
input string Filename = "calendar2.chn";
input datetime Start;

```

The ChangeState structure is described to store information about individual edits.

```
struct ChangeState
{
   datetime dt;
   ulong ids[];
   
   ChangeState(): dt(LONG_MAX) {}
   ChangeState(const datetime at, ulong &_ids[])
   {
      dt = at;
      ArraySwap(ids, _ids);
   }
   
   void operator=(const ChangeState &other)
   {
      dt = other.dt;
      ArrayCopy(ids, other.ids);
   }
};

```

It is used in the ChangeFileReader class, which does the bulk of the work of reading the file and providing the caller with the changes that are appropriate for a particular point in time.

The file handle is passed as a parameter to the constructor, as is the start time of the test. Reading a file and populating the ChangeState structure for one calendar edit is performed in the readState method.

```
class ChangeFileReader
{
   const int handle;
   ChangeState current;
   const ChangeState zero;
   
public:
   ChangeFileReader(const int h, const datetime start = 0): handle(h)
   {
      if(readState())
      {
         if(start)
         {
            ulong dummy[];
            check(start, dummy, true); // find the first edit after start 
         }
      }
   }
   
   bool readState()
   {
      if(FileIsEnding(handle)) return false;
      ResetLastError();
      const ulong v = FileReadLong(handle);
      current.dt = DATETIME(v);
      ArrayFree(current.ids);
      const int n = COUNTER(v);
      for(int i = 0; i < n; ++i)
      {
         PUSH(current.ids, FileReadLong(handle));
      }
      return _LastError == 0;
   }
   ...

```

Method check reads the file until the next edit appears in the future. In this case, all previous (by timestamps) edits since the previous method call are placed in the output array records.

```
   bool check(datetime now, ulong &records[], const bool fastforward = false)
   {
      if(current.dt > now) return false;
      
      ArrayFree(records);
      
      if(!fastforward)
      {
         ArrayCopy(records, current.ids);
         current = zero;
      }
      
      while(readState() && current.dt <= now)
      {
         if(!fastforward) ArrayInsert(records, current.ids, ArraySize(records));
      }
      
      return true;
   }
};

```

Here is how the class is used in OnStart.

```
void OnStart()
{
   const long day = 60 * 60 * 24;
   datetime now = Start ? Start : (datetime)(TimeCurrent() / day * day);
   
   int handle = FileOpen(Filename,
      FILE_READ | FILE_SHARE_WRITE | FILE_SHARE_READ | FILE_BIN);
   if(handle == INVALID_HANDLE)
   {
      PrintFormat("Can't open file '%s' for reading", Filename);
      return;
   }
   
   ChangeFileReader reader(handle, now);
   
   // reading step by step, time now artificially increased in this demo
   while(!FileIsEnding(handle))
   {
      // in a real application, a call to reader.check can be made on every tick
      ulong records[];
      if(reader.check(now, records))
      {
         Print(now);          // output time
         ArrayPrint(records); // array of IDs of changed news
      }
      now += 60; // add 1 minute at a time, can be per second
   }
   
   FileClose(handle);
}

```

Here are the results of the script for the same calendar changes that were saved by the service in the context of the previous log fragment.

```
2022.06.28 15:31:00
155955 155956 156117 156118 156231 156232 156255
2022.06.28 15:32:00
156256 155956 156118 156232
2022.06.28 15:37:00
158534
...
2022.06.28 16:02:00
154531 154532 154543 154544 154561 154571
2022.06.28 16:03:00
154532 154544 154571

```

The same identifiers are reproduced in virtual time with the same delay as online, although here you can see the rounding to 1 minute, which happened because we set an artificial step of this size in the loop. In theory, for reasons of efficiency, we can postpone checks until the time stored in the ChangeState current structure. The attached source code defines the getState method to get this time.
