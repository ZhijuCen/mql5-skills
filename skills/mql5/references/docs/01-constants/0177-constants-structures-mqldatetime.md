# MqlDateTime

The date type structure contains eight fields of the [int](/en/docs/basis/types/integer/integertypes) type:

```
struct MqlDateTime
  {
   int year;           // Year
   int mon;            // Month
   int day;            // Day
   int hour;           // Hour
   int min;            // Minutes
   int sec;            // Seconds
   int day_of_week;    // Day of week (0-Sunday, 1-Monday, ... ,6-Saturday)
   int day_of_year;    // Day number of the year (January 1st is assigned the number value of zero)
  };

```

Note

The day number of the year day_of_year for the leap year, since March, will differ from a number of the corresponding day for a non-leap year.

Example:

```
void OnStart()
  {
//---
   datetime date1=D'2008.03.01';
   datetime date2=D'2009.03.01';
 
   MqlDateTime str1,str2;
   TimeToStruct(date1,str1);
   TimeToStruct(date2,str2);
   printf("%02d.%02d.%4d, day of year = %d",str1.day,str1.mon,
          str1.year,str1.day_of_year);
   printf("%02d.%02d.%4d, day of year = %d",str2.day,str2.mon,
          str2.year,str2.day_of_year);
  }
/*  Result:
   01.03.2008, day of year = 60
   01.03.2009, day of year = 59
*/

```

See also

[TimeToStruct](/en/docs/dateandtime/timetostruct), [Structures and Classes](/en/docs/basis/types/classes)
