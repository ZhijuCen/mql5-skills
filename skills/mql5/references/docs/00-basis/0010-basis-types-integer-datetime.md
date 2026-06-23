# Datetime Type

The datetime type is intended for storing the date and time as the number of seconds elapsed since January 01, 1970. This type occupies 8 bytes of memory.

Constants of the date and time can be represented as a literal string, which consists of 6 parts showing the numerical value of the year, month, day (or day, month, year), hours, minutes and seconds. The constant is enclosed in single quotation marks and starts with the D character.

Values range from 1 January, 1970 to 31 December, 3000. Either date (year , month, day) or time (hours, minutes, seconds), or all together can be omitted.

With literal date specification, it is desirable that you specify year, month and day. Otherwise the compiler returns a [warning](/en/docs/constants/errorswarnings/warningscompile) about an incomplete entry.

Examples:

```
datetime NY=D'2015.01.01 00:00';     // Time of beginning of year 2015
datetime d1=D'1980.07.19 12:30:27';  // Year Month Day Hours Minutes Seconds
datetime d2=D'19.07.1980 12:30:27';  // Equal to D'1980.07.19 12:30:27';
datetime d3=D'19.07.1980 12';        // Equal to D'1980.07.19 12:00:00'
datetime d4=D'01.01.2004';           // Equal to D'01.01.2004 00:00:00'
datetime compilation_date=__DATE__;             // Compilation date
datetime compilation_date_time=__DATETIME__;    // Compilation date and time
datetime compilation_time=__DATETIME__-__DATE__;// Compilation time
//--- Examples of declarations after which compiler warnings will be returned
datetime warning1=D'12:30:27';       // Equal to D'[date of compilation] 12:30:27'
datetime warning2=D'';               // Equal to __DATETIME__

```

See also

[Structure of the Date Type](/en/docs/constants/structures/mqldatetime), [Date and Time](/en/docs/dateandtime), [TimeToString](/en/docs/convert/timetostring), [StringToTime](/en/docs/convert/stringtotime)
