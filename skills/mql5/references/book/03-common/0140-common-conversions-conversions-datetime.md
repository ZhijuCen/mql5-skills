# Date and Time

Values of type datetime intended for storing [date and/or time](/en/book/basis/builtin_types/datetime) usually undergo several types of conversion:

- into lines and back to display data to the user and to read data from external sources
- into special structures MqlDateTime (see below) to work with individual date and time components
- to the number of seconds elapsed since 01/01/1970, which corresponds to the internal representation of datetime and is equivalent to the integer type long

For the last item, use datetime to (long) casting, or vice versa, long To (datetime), but note that the supported date range is from January 1, 1970 (value 0) to December 31, 3000 (32535215999 seconds).

For the first two options, the MQL5 API provides the following functions.

string TimeToString(datetime value, int mode = TIME_DATE | TIME_MINUTES)

Function TimeToString converts a value of type datetime to a string with date and time components, according to the mode parameter in which you can set an arbitrary combination of flags:

- TIME_DATE — date in the format "YYYY.MM.DD"
- TIME_MINUTES — time in the format "hh:mm", i.e., with hours and minutes
- TIME_SECONDS — time in "hh:mm:ss" format, i.e. with hours, minutes and seconds

To output the date and time data in full, you can set mode equal to TIME_DATE | TIME_SECONDS (the TIME_DATE | TIME_MINUTES | TIME_SECONDS option will also work, but is redundant). This is equivalent to casting a value of type datetime to (string).

Usage examples are provided in the ConversionTime.mq5 file.

```
#define PRT(A) Print(#A, "=", (A))
 
void OnStart()
{
   datetime time = D'2021.01.21 23:00:15';
   PRT((string)time);
   PRT(TimeToString(time));
   PRT(TimeToString(time, TIME_DATE | TIME_MINUTES | TIME_SECONDS));
   PRT(TimeToString(time, TIME_MINUTES | TIME_SECONDS));
   PRT(TimeToString(time, TIME_DATE | TIME_SECONDS));
   PRT(TimeToString(time, TIME_DATE));
   PRT(TimeToString(time, TIME_MINUTES));
   PRT(TimeToString(time, TIME_SECONDS));
}

```

The script will print the following log:

```
(string)time=2021.01.21 23:00:15
TimeToString(time)=2021.01.21 23:00
TimeToString(time,TIME_DATE|TIME_MINUTES|TIME_SECONDS)=2021.01.21 23:00:15
TimeToString(time,TIME_MINUTES|TIME_SECONDS)=23:00:15
TimeToString(time,TIME_DATE|TIME_SECONDS)=2021.01.21 23:00:15
TimeToString(time,TIME_DATE)=2021.01.21
TimeToString(time,TIME_MINUTES)=23:00
TimeToString(time,TIME_SECONDS)=23:00:15

```

datetime StringToTime(string value)

The function StringToTime converts a string containing a date and/or time to a value of type datetime. The string can contain only the date, only the time, or the date and time together.

The following formats are recognized for dates:

- "YYYY.MM.DD"
- "YYYYMMDD"
- "YYYY/MM/DD"
- "YYYY-MM-DD"
- "DD.MM.YYYY"
- "DD/MM/YYYY"
- "DD-MM-YYYY"

The following formats are supported for time:

- "hh:mm"
- "hh:mm:ss"
- "hhmmss"

There must be at least one space between the date and time.

If only time is present in the string, the current date will be substituted in the result. If only the date is present in the string, the time will be set to 00:00:00.

If the supported syntax in the string is broken, the result is the current date.

The function usage examples are given in the script ConversionTime.mq5.

```
void OnStart()
{
   string timeonly = "21:01";   // time only
   PRT(timeonly);
   PRT((datetime)timeonly);
   PRT(StringToTime(timeonly));
   
   string date = "2000-10-10";  // date only
   PRT((datetime)date);
   PRT(StringToTime(date));
   PRT((long)(datetime)date);
   long seconds = 60;
   PRT((datetime)seconds); // 1 minute from the beginning of 1970
   
   string ddmmyy = "15/01/2012 01:02:03"; // date and time, and the date in
   PRT(StringToTime(ddmmyy));             // in "forward" order, still ok
   
   string wrong = "January 2-nd";
   PRT(StringToTime(wrong));
}

```

In the log, we will see something like the following (####.##.## is the current date the script was launched):

```
timeonly=21:01
(datetime)timeonly=####.##.## 21:01:00
StringToTime(timeonly)=####.##.## 21:01:00
(datetime)date=2000.10.10 00:00:00
StringToTime(date)=2000.10.10 00:00:00
(long)(datetime)date=971136000
(datetime)seconds=1970.01.01 00:01:00
StringToTime(ddmmyy)=2012.01.15 01:02:03
(datetime)wrong=####.##.## 00:00:00

```

In addition to StringToTime, you can use the cast operator (datetime) to convert strings to dates and times. However, the advantage of the function is that when an incorrect source string is detected, the function sets an internal variable with an error code _LastError (which is also available via the function [GetLastError](/en/book/common/environment/env_last_error)). Depending on which part of the string contains uninterpreted data, the error code could be ERR_WRONG_STRING_DATE (5031), ERR_WRONG_STRING_TIME (5032) or another option from the list related to getting the date and time from the string.

bool TimeToStruct(datetime value, MqlDateTime &struct)

To parse date and time components separately, the MQL5 API provides the TimeToStruct function which converts a value of type datetime into the MqlDateTime structure:

```
struct MqlDateTime
{ 
   int year;           // year
   int mon;            // month
   int day;            // day
   int hour;           // hour
   int min;            // minutes
   int sec;            // seconds
   int day_of_week;    // day of the week
   int day_of_year;    // the number of the day in a year (January 1 has number 0)
};

```

The days of the week are numbered in the American manner: 0 for Sunday, 1 for Monday, and so on up to 6 for Saturday. They can be identified using the built-in ENUM_DAY_OF_WEEK enumeration.

The function returns true if successful and false on error, in particular, if an incorrect date is passed.

Let's check the performance of the function using the ConversionTimeStruct.mq5 script. To do this, let's create the time array of type datetime with test values. We will call TimeToStruct for each of them in a loop.

The results will be added to an array of structures MqlDateTime mdt[]. We will first initialize it with zeros, but since the built-in function [ArrayInitialize](/en/book/common/arrays/arrays_init_fill) does not know how to handle structures, we will have to write an overload for it (in the future we will learn an easier way to fill an array with zeros: in the section [Zeroing objects and arrays](/en/book/common/arrays/zero_memory) the function ZeroMemory will be introduced).

```
int ArrayInitialize(MqlDateTime &mdt[], MqlDateTime &init)
{
   const int n = ArraySize(mdt);
   for(int i = 0; i < n; ++i)
   {
      mdt[i] = init;
   }
   return n;
}

```

After the process, we will output the array of structures to the log using the built-in function [ArrayPrint](/en/book/common/arrays/arrays_print). This is the easiest way to provide nice data formatting (it can be used even if there is only one structure: just put it in an array of size 1).

```
void OnStart()
{
   // fill the array with tests
   datetime time[] =
   {
      D'2021.01.28 23:00:15', // valid datetime value
      D'3000.12.31 23:59:59', // the largest supported date and time
      LONG_MAX // invalid date: will cause an error ERR_INVALID_DATETIME (4010)
   };
   
   // calculate the size of the array at compile time
   const int n = sizeof(time) / sizeof(datetime);
   
   MqlDateTime null = {}; // example with zeros
   MqlDateTime mdt[];
   
   // allocating memory for an array of structures with results
   ArrayResize(mdt, n);
   
   // call our ArrayInitialize overload 
   ArrayInitialize(mdt, null);
   
   // run tests
   for(int i = 0; i < n; ++i)
   {
      PRT(time[i]); // displaying initial data
   
      if(!TimeToStruct(time[i], mdt[i])) // if an error occurs, output its code
      {
         Print("error: ", _LastError);
         mdt[i].year = _LastError;
      }
   }
   
   // output the results to the log
   ArrayPrint(mdt);
   ...
}

```

As a result, we get the following strings in the log:

```
time[i]=2021.01.28 23:00:15
time[i]=3000.12.31 23:59:59
time[i]=wrong datetime
wrong datetime -> 4010
    [year] [mon] [day] [hour] [min] [sec] [day_of_week] [day_of_year]
[0]   2021     1    28     23     0    15             4            27
[1]   3000    12    31     23    59    59             3           364
[2]   4010     0     0      0     0     0             0             0

```

You can make sure that all fields have received the appropriate values. For incorrect initial dates, we store the error code in the year field (in this case, there is only one such error: 4010, ERR_INVALID_DATETIME).

Recall that for the maximum date value in MQL5, the DATETIME_MAX constant is introduced, equal to the integer value 0x793406fff, which corresponds to 23:59:59 December 31, 3000.

The most common problem that is solved using the function TimeToStruct, is getting the value of a particular date/time component. Therefore, it makes sense to prepare an auxiliary header file (MQL5Book/DateTime.mqh) with a ready implementation option. The file has the datetime class.

```
class DateTime
{
private:
   MqlDateTime mdtstruct;
   datetime origin;
   
   DateTime() : origin(0)
   {
      TimeToStruct(0, mdtstruct);
   }
   
   void convert(const datetime &dt)
   {
      if(origin != dt)
      {
         origin = dt;
         TimeToStruct(dt, mdtstruct);
      }
   }
   
public:
   static DateTime *assign(const datetime dt)
   {
      _DateTime.convert(dt);
      return &_DateTime;
   }
   ENUM_DAY_OF_WEEK timeDayOfWeek() const
   {
      return (ENUM_DAY_OF_WEEK)mdtstruct.day_of_week;
   }
   int timeDayOfYear() const
   {
      return mdtstruct.day_of_year;
   }
   int timeYear() const
   {
      return mdtstruct.year;
   }
   int timeMonth() const
   {
      return mdtstruct.mon;
   }
   int timeDay() const
   {
      return mdtstruct.day;
   }
   int timeHour() const
   {
      return mdtstruct.hour;
   }
   int timeMinute() const
   {
      return mdtstruct.min;
   }
   int timeSeconds() const
   {
      return mdtstruct.sec;
   }
   
   static DateTime _DateTime;
};
   
static DateTime DateTime::_DateTime;

```

The class comes with several macros that make it easier to call its methods.

```
#define TimeDayOfWeek(T) DateTime::assign(T).timeDayOfWeek()
#define TimeDayOfYear(T) DateTime::assign(T).timeDayOfYear()
#define TimeYear(T) DateTime::assign(T).timeYear()
#define TimeMonth(T) DateTime::assign(T).timeMonth()
#define TimeDay(T) DateTime::assign(T).timeDay()
#define TimeHour(T) DateTime::assign(T).timeHour()
#define TimeMinute(T) DateTime::assign(T).timeMinute()
#define TimeSeconds(T) DateTime::assign(T).timeSeconds()
   
#define _TimeDayOfWeek DateTime::_DateTime.timeDayOfWeek
#define _TimeDayOfYear DateTime::_DateTime.timeDayOfYear
#define _TimeYear DateTime::_DateTime.timeYear
#define _TimeMonth DateTime::_DateTime.timeMonth
#define _TimeDay DateTime::_DateTime.timeDay
#define _TimeHour DateTime::_DateTime.timeHour
#define _TimeMinute DateTime::_DateTime.timeMinute
#define _TimeSeconds DateTime::_DateTime.timeSeconds

```

The class has the mdtstruct field of the MqlDateTime structure type. This field is used in all internal conversions. Structure fields are read using getter methods: a corresponding method is allocated for each field.

One static instance is defined inside the class: _DateTime (one object is enough, because all MQL programs are single-threaded). The constructor is private, so trying to create other datetime objects will fail.

Using macros, we can conveniently receive separate components from datetime, for example, the year (TimeYear(T)), month (TimeMonth(T)), number (TimeDay(T)), or day of the week (TimeDayOfWeek(T)).

If from one value of datetime it is necessary to receive several fields, then it is better to use similar macros in all calls except the first one without a parameter and starting with the underscore symbol: they read the desired field from the structure without re-setting the date/time and calling the TimeToStruct function. For example:

```
   // use the DateTime class from MQL5Book/DateTime.mqh:
   // first get the day of the week for the specified datetime value
   PRT(EnumToString(TimeDayOfWeek(time[0])));
   // then read year, month and day for the same value
   PRT(_TimeYear());
   PRT(_TimeMonth());
   PRT(_TimeDay());

```

The following strings should appear in the log.

```
EnumToString(DateTime::_DateTime.assign(time[0]).__TimeDayOfWeek())=THURSDAY
DateTime::_DateTime.__TimeYear()=2021
DateTime::_DateTime.__TimeMonth()=1
DateTime::_DateTime.__TimeDay()=28

```

The built-in function EnumToString converts an element of any enumeration into a string. It will be described in a [separate section](/en/book/common/conversions/conversions_enums).

datetime StructToTime(MqlDateTime &struct)

The StructToTime function performs a conversion from the MqlDateTime structure (see above the description of the TimeToStruct function) containing date and time components, into a value of type datetime. The fields day_of_week  and day_of_year are not used.

If the state of the remaining fields is invalid (corresponding to a non-existent or unsupported date), the function may return either a corrected value, or WRONG_VALUE (-1 in the representation of type long), depending on the problem. Therefore, you should check for an error based on the state of the global variable [_LastError](/en/book/common/environment/env_last_error). A successful conversion is completed with code 0. Before converting, you should reset a possible failed state in _LastError (preserved as an artifact of the execution of some previous instructions) using the [ResetLastError](/en/book/common/environment/env_last_error) function.

The StructToTime function test is also provided in the script ConversionTimeStruct.mq5. The array of structures parts is converted to datetime in the loop.

```
   MqlDateTime parts[] =
   {
      {0, 0, 0, 0, 0, 0, 0, 0},
      {100, 0, 0, 0, 0, 0, 0, 0},
      {2021, 2, 30, 0, 0, 0, 0, 0},
      {2021, 13, -5, 0, 0, 0, 0, 0},
      {2021, 50, 100, 0, 0, 0, 0, 0},
      {2021, 10, 20, 15, 30, 155, 0, 0},
      {2021, 10, 20, 15, 30, 55, 0, 0},
   };
   ArrayPrint(parts);
   Print("");
   
   // convert all elements in the loop
   for(int i = 0; i < sizeof(parts) / sizeof(MqlDateTime); ++i)
   {
      ResetLastError();
      datetime result = StructToTime(parts[i]);
      Print("[", i, "] ", (long)result, " ", result, " ", _LastError);
   }

```

For each element, the resulting value and an error code are displayed.

```
       [year] [mon] [day] [hour] [min] [sec] [day_of_week] [day_of_year]
   [0]      0     0     0      0     0     0             0             0
   [1]    100     0     0      0     0     0             0             0
   [2]   2021     2    30      0     0     0             0             0
   [3]   2021    13    -5      0     0     0             0             0
   [4]   2021    50   100      0     0     0             0             0
   [5]   2021    10    20     15    30   155             0             0
   [6]   2021    10    20     15    30    55             0             0
   
   [0] -1 wrong datetime 4010
   [1] 946684800 2000.01.01 00:00:00 4010
   [2] 1614643200 2021.03.02 00:00:00 0
   [3] 1638316800 2021.12.01 00:00:00 4010
   [4] 1640908800 2021.12.31 00:00:00 4010
   [5] 1634743859 2021.10.20 15:30:59 4010
   [6] 1634743855 2021.10.20 15:30:55 0

```

Note that the function corrects some values without raising the error flag. So, in element number 2, we passed the date, February 30, 2021, into the function, which was converted to March 2, 2021, and _LastError = 0.
