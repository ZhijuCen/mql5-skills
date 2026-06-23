# StructToTime

Converts a structure variable [MqlDateTime](/en/docs/constants/structures/mqldatetime) into a value of [datetime](/en/docs/basis/types/integer/datetime) type and returns the resulting value.

```
datetime  StructToTime(
   MqlDateTime&  dt_struct      // structure of the date and time
   );

```

Parameters

dt_struct

[in] Variable of structure type MqlDateTime.

Return Value

The value of datetime type containing the number of seconds since 01.01.1970.

Example:

```
#property script_show_inputs
 
input int   InpYear  =  0;    // Year
input int   InpMonth =  0;    // Month
input int   InpDay   =  0;    // Day
input int   InpHour  =  0;    // Hour
input int   InpMin   =  0;    // Minutes
input int   InpSec   =  0;    // Seconds
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- adjust the entered values and write them to variables
   int year =  (InpYear<1970 ? 1970 : InpYear); // If the year entered is less than 1970, then 1970 is used
   int month=  (InpMonth<1 ?  1  :  InpMonth > 12  ?  12 :  InpMonth);
   int day  =  (InpDay  <1 ?  1  :  InpDay   > 31  ?  31 :  InpDay);
   int hour =  (InpHour <0 ?  0  :  InpHour  > 23  ?  23 :  InpHour);
   int min  =  (InpMin  <0 ?  0  :  InpMin   > 59  ?  59 :  InpMin);
   int sec  =  (InpSec  <0 ?  0  :  InpSec   > 59  ?  59 :  InpSec);
 
//--- display the entered values in the log
   PrintFormat("Entered date and time: %04u.%02u.%02u %02u:%02u:%02u", InpYear, InpMonth, InpDay, InpHour, InpMin, InpSec);
   
//--- display the adjusted entered values in the log
   PrintFormat("Corrected date and time: %04u.%02u.%02u %02u:%02u:%02u", year, month, day, hour, min, sec);
   
//--- write the input values to the corresponding structure fields
   MqlDateTime time_struct={};
   time_struct.year= year;
   time_struct.mon = month;
   time_struct.day = day;
   time_struct.hour= hour;
   time_struct.min = min;
   time_struct.sec = sec;
   
//--- convert the date and time from the structure into a variable of datetime type and
   datetime time = StructToTime(time_struct);
   
//--- display the result of conversion from an MqlDateTime structure type variable to a datetime type value
   Print("Converted date and time: ",TimeToString(time,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
   /*
   results if zero default values are entered:
   Entered date and time: 0000.00.00 00:00:00
   Corrected date and time: 1970.01.01 00:00:00
   Converted date and time: 1970.01.01 00:00:00
   
   results if the wrong day of the current year's February is entered:
   Entered date and time: 2024.02.31 00:00:00
   Corrected date and time: 2024.02.31 00:00:00
   Converted date and time: 2024.03.02 00:00:00
   */
  }

```
